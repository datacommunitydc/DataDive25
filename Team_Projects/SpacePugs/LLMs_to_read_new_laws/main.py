from fasthtml.common import *
from monsterui.all import *
from read_law import LawSectionSexQuestion, get_legal_text, get_law_name, answer_question, questions
import json
from pydantic_ai import Agent
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.models.openai import OpenAIChatModel

# Add Alpine.js for client-side interactivity
alpine_js = Script(src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js", defer=True)
app, rt = fast_app(hdrs=(Theme.blue.headers(highlightjs=True), alpine_js))

def InputGroup(placeholder=''):  
    # give input a name so it will be included in form-like submissions
    inp = Input(placeholder=placeholder, disabled=False, name='doc_url', id='doc_url')
    return DivHStacked(
        inp,
        Button('Get law', cls=ButtonT.primary, disabled=False, submit=False,
               # Use the route path directly so FastHTML resolves it correctly
               hx_get=show_text.to(),
               # include the input element by id so its value is submitted
               hx_include='#doc_url',
               # target must be a CSS selector when using HTMX (id selector)
               hx_target='#body_content',
               hx_swap='outerHTML',
               # hx_push_url='true'
               ))

@rt("/show_text", methods=['GET'])
def show_text(request, doc_url: str = ''):
    # FastHTML will bind query params to typed args (doc_url comes from hx_include)
    print("Request received headers:", dict(request.headers))
    print("Request query:", request.query_params)
    print("doc_url param:", doc_url)
    # Render initial container immediately so the page responds quickly.
    # Then trigger a follow-up HTMX request to fetch the (potentially slow) legal text.
    followup_url = fetch_text.to(doc_url=doc_url)
    return Div(
        H2("Analyzing Legal Document"),
        P(f'Received URL: {doc_url}'),
        # Placeholder area that will be populated by `fetch_text` when revealed
        Div("Loading text...", id="legal_text_container", 
            hx_get=followup_url, hx_target="#legal_text_container", hx_swap='outerHTML', hx_trigger='revealed'),
        id="body_content",
    )


@rt("/fetch_text", methods=['GET'])
def fetch_text(request, doc_url: str = ''):
    # This route performs the actual (possibly slow) text extraction and returns the result
    print("fetch_text called for:", doc_url)
    legal_text = ''
    try:
        legal_text = get_legal_text(doc_url) or ''
    except Exception as e:
        # print("Error getting legal text:", e)
        legal_text = f'Error fetching text: {e}'
    excerpt = (legal_text[:500] + '...') if len(legal_text) > 500 else legal_text
    # Prepare hx-vals JSON to POST the full legal_text to the law-name extractor
    hx_vals_payload = json.dumps({"legal_text": legal_text})
    return Div(
        P(excerpt),
        # This loader will POST the full legal_text to get_and_render_law_name and append its result
        Div('Reading...', id='law_name_loader', 
            hx_post=get_and_render_law_name.to(), 
            hx_vals=hx_vals_payload,
            hx_target='#legal_text_container', hx_swap='afterend', hx_trigger='revealed'),
        id="legal_text_container",
    )

@rt("/get_and_render_law_name", methods=['POST', 'GET'])
def get_and_render_law_name(request, legal_text: str = ''):
    print("get_and_render_law_name called; method=", request.method)
    # Try to obtain `legal_text` from multiple possible locations (form, json body, or bound param)
    if not legal_text:
        # HTMX hx-vals with JSON may appear as JSON body or form field depending on client.
        try:
            body_json = request.json() if hasattr(request, 'json') else None
        except Exception:
            body_json = None
        # body_json may be a dict with 'legal_text'
        if isinstance(body_json, dict) and 'legal_text' in body_json:
            legal_text = body_json.get('legal_text') or ''
        else:
            # try form / query params
            try:
                form = request.form() if hasattr(request, 'form') else None
            except Exception:
                form = None
            if form and 'legal_text' in form:
                legal_text = form.get('legal_text') or ''
            else:
                legal_text = request.query_params.get('legal_text', '')

    print("Extracting law name... (text length=", len(legal_text), ")")
    ollama_model = OpenAIChatModel(
        model_name='gpt-oss:20b',
        provider=OllamaProvider(base_url='http://localhost:11434/v1'),
        settings={'temperature': 0.0}
    )
    try:
        law_name = get_law_name(legal_text, ollama_model)
    except Exception as e:
        print("Error extracting law name:", e)
        law_name = f'Error: {e}'
    print("Extracted law name:", law_name)
    return Div(
        H3(f"Law Name: {law_name}"),
        H4(f"Answering question 1: {questions[0]}"),
        # Loader that will POST the legal_text and question (index 0) to answer_question_route and append the answer
        Div('', id='answer_loader',
            hx_post=answer_question_route.to(),
            hx_vals=json.dumps({"legal_text": legal_text, "qidx": 0}),
            hx_target='#law_name_container', hx_swap='afterend', hx_trigger='revealed'),
        id="law_name_container",
    )

@rt("/answer_question", methods=['POST', 'GET'])
def answer_question_route(request, legal_text: str = '', qidx: int | None = None):
    print("answer_question_route called; method=", request.method)
    # Extract legal_text and qidx from JSON/form/query if not provided
    if not legal_text:
        try:
            body_json = request.json() if hasattr(request, 'json') else None
        except Exception:
            body_json = None
        if isinstance(body_json, dict) and 'legal_text' in body_json:
            legal_text = body_json.get('legal_text') or ''
        else:
            try:
                form = request.form() if hasattr(request, 'form') else None
            except Exception:
                form = None
            if form and 'legal_text' in form:
                legal_text = form.get('legal_text') or ''
            else:
                legal_text = request.query_params.get('legal_text', '')

    if qidx is None:
        # try to extract qidx from body/json or query params
        try:
            body_json = request.json() if hasattr(request, 'json') else None
        except Exception:
            body_json = None
        if isinstance(body_json, dict) and 'qidx' in body_json:
            qidx = int(body_json.get('qidx'))
        else:
            qidx = int(request.query_params.get('qidx', 0))

    # clamp qidx
    qidx = int(qidx or 0)
    question = questions[qidx] if 0 <= qidx < len(questions) else ''

    print("Answering question... (text length=", len(legal_text), ", qidx=", qidx, ")")
    ollama_model = OpenAIChatModel(
        model_name='gpt-oss:20b',
        provider=OllamaProvider(base_url='http://localhost:11434/v1'),
        settings={'temperature': 0.0}
    )
    try:
        law_name = get_law_name(legal_text, ollama_model)
        final_answer = answer_question(legal_text, question, ollama_model, law_name)
    except Exception as e:
        print("Error answering question:", e)
        final_answer = type('E', (), {'answer': 'error', 'reasoning': str(e), 'specific_citation_and_quote': ''})()

    print("Final answer:", final_answer)

    # Build the answer block
    answer_block = Div(
        P("Answer: ", Strong(final_answer.answer)),
        P(f"Reasoning: {final_answer.reasoning}"),
        P(f"Citations: {final_answer.specific_citation_and_quote}" if final_answer.specific_citation_and_quote else ""),
        H4(f"Answering question {qidx+2}: {questions[qidx+1]}") if (qidx + 1) < len(questions) else "",
        id=f"answer_{qidx}",
    )

    # If there are more questions, include a loader to request the next answer and append it
    next_qidx = qidx + 1
    if next_qidx < len(questions):
        loader = Div('', id=f'answer_loader_{next_qidx}',
                     hx_post=answer_question_route.to(),
                     hx_vals=json.dumps({"legal_text": legal_text, "qidx": next_qidx}),
                     hx_target=f'#answer_{qidx}', hx_swap='afterend', hx_trigger='revealed')
        return Div(answer_block, loader)
    else:
        return answer_block

@rt("/reset", methods=['GET'])
def reset(request):
    return Div(InputGroup('Enter URL to legal document here...'), cls="max-w-2xl", id="body_content")

@rt("/")
def index():
    return Container(
        DivFullySpaced(
            Div(
                H1("Women, Business and the law"),
                P("How do laws shape women’s jobs and entrepreneurship?"),
                Button("Start Over", cls=ButtonT.secondary,
                       hx_get=reset.to(),
                       hx_target='#body_content',
                       hx_swap='outerHTML'),
                cls='uk-flex items-baseline gap-6'
            ),
            cls="uk-flex uk-flex-col uk-flex-center uk-flex-middle uk-gap-8 uk-min-h-screen"
        ),
        Div(InputGroup('Enter URL to legal document here...'), cls="max-w-2xl", id="body_content")
    )

serve()
