from pydantic_ai import Agent
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.models.openai import OpenAIChatModel


from typing import Literal
from pydantic import BaseModel, Field

import pandas as pd

# show all columns when displaying dataframes
pd.set_option('display.max_columns', None)

from markitdown import MarkItDown

import nest_asyncio

nest_asyncio.apply()

def get_legal_text(input) -> str:
    md = MarkItDown(enable_plugins=False) # Set to True to enable plugins
    law_in_markdown = md.convert(input)
    return law_in_markdown.markdown

def get_law_name(legal_text: str, ollama_model) -> str:
    class LawName(BaseModel):
        law_name: str = Field(..., description="The name of the law or legal document in english.")

    name_of_the_law_agent = Agent(model=ollama_model, 
                system_prompt=f"You are a legal expert. Given a legal document, extract the name of the law or legal document in english. Respond with only the name of the law or legal document.",
                output_type=LawName)

    law_name_result = name_of_the_law_agent.run_sync(legal_text[:1000])

    law_name = law_name_result.output.law_name
    return law_name
# law_name = get_law_name(legal_text)
# print(law_name)

questions = [
    "Does the law address or affect whether women can choose where to live in the same way as a men?",
    "Does the law address or affect child marriage?",
    # "Does the law address or affect sexual harassment?",
    # "Does the law address or affect domestic violence?",
    # "Does the law address or affect femicide?",
    # "Does the law address or affect whether women can travel internationally in the same way as a man?",
    # "Does the law address or affect whether women canntravel outside her home in the same way as a man?"
]

class LawSectionSexQuestion(BaseModel):
    question: str = Field(..., description="The question about the legal document.")
    answer: Literal['yes', 'no'] = Field(..., description="Answer with either 'yes' or 'no'.")
    reasoning: str = Field(..., description="The reasoning behind the answer.")
    specific_citation_and_quote: list[str] | None = Field(None, description="If the answer is yes, give the specific citation or citations in the law that supports the answer. You should give answers as a list of strings, even if there is only one citation.")

def reason_over_document(text: str, question: str, qa_agent: Agent, law_name: str):
    chunk_size = 20000
    overlap = 1000  # adjust overlap if you want larger/smaller overlap
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    first_answer = None
    collated_answers = []

    for i, chunk in enumerate(chunks, 1):
        qa_result = qa_agent.run_sync(f"Document (chunk {i}/{len(chunks)}): {chunk}\nLaw: {law_name}\nQuestion: {question}")
        out = qa_result.output
        print(f"Chunk {i}/{len(chunks)}\nQ: {out.question}\nA: {out.answer}\nReason: {out.reasoning}\nCitation: {out.specific_citation_and_quote}\n")
        if out.answer.lower() == 'yes':
            collated_answers.append(out)
        if i == 1:
            first_answer = out
        if i >= 2:  # limit to first 3 chunks for testing
            break
    return first_answer, collated_answers

def collate_all_answers(collated_answers: list[LawSectionSexQuestion], first_answer: LawSectionSexQuestion, law_name: str, ollama_model) -> LawSectionSexQuestion:
    if collated_answers and len(collated_answers) > 1:
        joined_reasons = f"# Law: {law_name}\n"+"\n".join([f"- Reasoning: {ans.reasoning}\n  Citation and quote: {ans.specific_citation_and_quote}" for ans in collated_answers])
        final_summary_agent = Agent(model=ollama_model,
                                system_prompt="You are a top legal expert in sexual equality. Given multiple answers to the same question from different sections of a legal document, collate the findings into a single coherent answer. Include the reasoning and citations.",
                                output_type=LawSectionSexQuestion)
        final_result = final_summary_agent.run_sync(f"Question: {question}\nHere are the findings from different sections of the law:\n{joined_reasons}\nPlease summarize into a single coherent answer.")
        final_result = final_result.output
    elif collated_answers and len(collated_answers) == 1:
        final_result = collated_answers[0]
    else:
        final_result = first_answer
    return final_result


def answer_question(legal_text: str, question: str, ollama_model, law_name: str) -> LawSectionSexQuestion:
    qa_agent = Agent(model=ollama_model,
                    system_prompt=f"You are the top legal expert in sexual equality. Given a portion of a legal document, answer the question with either 'yes' or 'no'. If yes, provide the specific citation in the law that supports your answer. Provide reasoning for your answer.",
                    output_type=LawSectionSexQuestion)
    
    first_answer, collated_answers = reason_over_document(legal_text, question, qa_agent, law_name)
    final_answer = collate_all_answers(collated_answers, first_answer, law_name, ollama_model)
    return final_answer


def qbyq_analysis(legal_text: str, ollama_model, law_name: str):
    analysis_results = []
    for question in questions:
        final_answer = answer_question(legal_text, question, ollama_model, law_name)
        print(f"Final Answer to '{question}':\nA: {final_answer.answer}\nReasoning: {final_answer.reasoning}\nCitations: {final_answer.specific_citation_and_quote}\n")
        analysis_results.append(final_answer)
    # break

def full_analysis(input: str):
    ollama_model = OpenAIChatModel(
        model_name='gpt-oss:20b',
        provider=OllamaProvider(base_url='http://localhost:11434/v1'),  
        settings={'temperature': 0.0}
    )

    legal_text = get_legal_text(input)
    law_name = get_law_name(legal_text, ollama_model)
    print(f"Analyzing Law: {law_name}\n")
    qbyq_analysis(legal_text, ollama_model, law_name)