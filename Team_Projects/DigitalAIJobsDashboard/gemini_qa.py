#!/usr/bin/env python3
"""
Google Gemini Q&A Integration for Data Sources

This module provides question-answering capabilities using Google Gemini API
to answer questions about data from various sources.
"""

import json
from typing import Dict, Any, Optional, List
import requests
from mcp_client import data_fetcher


class GeminiQA:
    """Question-answering system using Google Gemini API."""
    
    def __init__(self, api_key: str, model: str = None):
        """Initialize Gemini QA with API key and model."""
        self.api_key = api_key
        # Default to gemini-pro-latest which is more widely available
        self.model = model or "gemini-pro-latest"
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
    
    def list_available_models(self) -> Dict[str, Any]:
        """List available models from Gemini API."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}"
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text[:200]}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _call_gemini_api(self, prompt: str) -> Dict[str, Any]:
        """Call Google Gemini API."""
        url = f"{self.base_url}?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            # Better error handling
            if response.status_code == 404:
                # Try alternative model names (most common ones)
                alternative_models = [
                    "gemini-pro-latest",
                    "gemini-flash-latest",
                    "gemini-2.5-flash",
                    "gemini-2.5-pro",
                    "gemini-2.0-flash",
                    "gemini-pro",
                    "gemini-1.0-pro"
                ]
                
                # Remove current model from alternatives if it's already there
                if self.model in alternative_models:
                    alternative_models.remove(self.model)
                
                for model_name in alternative_models:
                    try:
                        alt_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
                        alt_response = requests.post(alt_url, json=payload, headers=headers, timeout=30)
                        if alt_response.status_code == 200:
                            # Update model name if successful
                            self.model = model_name
                            self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
                            return alt_response.json()
                    except:
                        continue
                
                # If all alternatives fail, try to list available models
                models_info = self.list_available_models()
                available_models = []
                if "models" in models_info:
                    for m in models_info["models"]:
                        if "generateContent" in m.get("supportedGenerationMethods", []):
                            available_models.append(m.get("name", "").split("/")[-1])
                
                error_detail = response.text[:500] if hasattr(response, 'text') else "No details"
                error_msg = f"Model '{self.model}' not found (404)."
                
                if available_models:
                    error_msg += f"\n\nAvailable models: {', '.join(available_models)}"
                else:
                    error_msg += "\n\nCould not retrieve available models. Please check your API key at https://aistudio.google.com/api-keys"
                
                return {"error": error_msg}
            
            if response.status_code == 400:
                error_detail = response.text[:500] if hasattr(response, 'text') else "Bad Request"
                return {
                    "error": f"Bad Request (400): {error_detail}. Please check your API key and request format."
                }
            
            if response.status_code == 403:
                return {
                    "error": "Access Forbidden (403). Your API key may be invalid or not have permission. Check https://aistudio.google.com/api-keys"
                }
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP {e.response.status_code}"
            if hasattr(e.response, 'text'):
                error_msg += f": {e.response.text[:200]}"
            return {"error": error_msg}
        except Exception as e:
            return {"error": str(e)}
    
    def answer_question(self, question: str, use_sources: List[str] = None) -> Dict[str, Any]:
        """
        Answer a question using available data sources.
        
        Args:
            question: User's question
            use_sources: List of sources to use (e.g., ['world_bank', 'stanford', 'anthropic'])
        
        Returns:
            Dict with answer, source used, and confidence
        """
        # Determine which sources to query based on question keywords
        if use_sources is None:
            use_sources = self._detect_sources_from_question(question)
        
        # Fetch relevant data from sources
        source_data = {}
        sources_used = []
        
        for source in use_sources:
            try:
                if source == "world_bank":
                    # Try to fetch World Bank data
                    # Extract indicator from question if possible
                    data = self._fetch_world_bank_context(question)
                    if data:
                        source_data["world_bank"] = data
                        sources_used.append("World Bank")
                
                elif source == "stanford":
                    if data_fetcher:
                        data = data_fetcher.fetch_stanford_ai_index("all")
                        if "error" not in data:
                            source_data["stanford"] = data
                            sources_used.append("Stanford AI Index")
                
                elif source == "anthropic":
                    if data_fetcher:
                        data = data_fetcher.fetch_anthropic_data("release_2025_09_15")
                        if "error" not in data:
                            source_data["anthropic"] = data
                            sources_used.append("Anthropic EconomicIndex")
                
                elif source == "itu":
                    if data_fetcher:
                        data = data_fetcher.fetch_itu_ict_data("internet", "all")
                        if "error" not in data:
                            source_data["itu"] = data
                            sources_used.append("ITU ICT Data")
            
            except Exception as e:
                # Continue with other sources if one fails
                continue
        
        # Build prompt for Gemini
        prompt = self._build_prompt(question, source_data)
        
        # Call Gemini API
        result = self._call_gemini_api(prompt)
        
        if "error" in result:
            return {
                "answer": f"Error calling Gemini API: {result['error']}",
                "sources": sources_used,
                "error": True
            }
        
        # Extract answer from Gemini response
        try:
            if "candidates" in result and len(result["candidates"]) > 0:
                answer_text = result["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "answer": answer_text,
                    "sources": sources_used,
                    "source_data_available": len(source_data) > 0,
                    "error": False
                }
            else:
                return {
                    "answer": "No answer generated from Gemini API.",
                    "sources": sources_used,
                    "error": True
                }
        except Exception as e:
            return {
                "answer": f"Error parsing Gemini response: {str(e)}",
                "sources": sources_used,
                "error": True
            }
    
    def _detect_sources_from_question(self, question: str) -> List[str]:
        """Detect which data sources might be relevant based on question keywords."""
        question_lower = question.lower()
        sources = []
        
        # Keywords for different sources
        world_bank_keywords = ["employment", "ict", "job", "labor", "workforce", "economic", "gdp", "world bank"]
        stanford_keywords = ["ai investment", "ai adoption", "stanford", "ai index", "artificial intelligence"]
        anthropic_keywords = ["anthropic", "economic index", "llm", "language model"]
        itu_keywords = ["internet", "mobile", "broadband", "ict", "telecommunications", "itu"]
        
        if any(kw in question_lower for kw in world_bank_keywords):
            sources.append("world_bank")
        
        if any(kw in question_lower for kw in stanford_keywords):
            sources.append("stanford")
        
        if any(kw in question_lower for kw in anthropic_keywords):
            sources.append("anthropic")
        
        if any(kw in question_lower for kw in itu_keywords):
            sources.append("itu")
        
        # Default to world_bank and stanford if no specific keywords found
        if not sources:
            sources = ["world_bank", "stanford"]
        
        return sources
    
    def _fetch_world_bank_context(self, question: str) -> Optional[Dict[str, Any]]:
        """Try to fetch relevant World Bank data based on question."""
        if not data_fetcher:
            return None
        
        question_lower = question.lower()
        
        # Map keywords to indicator codes
        indicator_mapping = {
            "ict employment": "SL.EMP.ICTI.ZS",
            "ict services": "SL.EMP.ICTI.ZS",
            "ict manufacturing": "SL.EMP.ICTM.ZS",
            "internet users": "IT.NET.USER.ZS",
            "mobile": "IT.CEL.SETS.P2"
        }
        
        for keyword, indicator in indicator_mapping.items():
            if keyword in question_lower:
                try:
                    data = data_fetcher.fetch_world_bank_indicator(indicator, "all", 2015, 2024)
                    if "error" not in data:
                        return data
                except:
                    pass
        
        return None
    
    def _build_prompt(self, question: str, source_data: Dict[str, Any]) -> str:
        """Build prompt for Gemini API."""
        prompt = f"""You are a helpful assistant answering questions about digital/AI jobs, employment trends, and economic indicators.

User Question: {question}

"""
        
        if source_data:
            prompt += "Available Data Sources:\n\n"
            
            if "world_bank" in source_data:
                wb_data = source_data["world_bank"]
                prompt += f"World Bank Data:\n"
                prompt += f"- Indicator: {wb_data.get('indicator_code', 'N/A')}\n"
                prompt += f"- Records: {wb_data.get('records', 0)}\n"
                if "statistics" in wb_data:
                    stats = wb_data["statistics"]
                    prompt += f"- Mean: {stats.get('mean', 'N/A')}\n"
                    prompt += f"- Min: {stats.get('min', 'N/A')}\n"
                    prompt += f"- Max: {stats.get('max', 'N/A')}\n"
                prompt += "\n"
            
            if "stanford" in source_data:
                stanford_data = source_data["stanford"]
                prompt += f"Stanford AI Index Data:\n"
                if "key_metrics" in stanford_data:
                    metrics = stanford_data["key_metrics"]
                    prompt += f"- Investment metrics: {json.dumps(metrics.get('investment', {}), indent=2)}\n"
                    prompt += f"- Adoption metrics: {json.dumps(metrics.get('adoption', {}), indent=2)}\n"
                prompt += "\n"
            
            if "anthropic" in source_data:
                anth_data = source_data["anthropic"]
                prompt += f"Anthropic EconomicIndex Data:\n"
                prompt += f"- Records: {anth_data.get('records', 0)}\n"
                prompt += f"- Columns: {', '.join(anth_data.get('columns', []))}\n"
                prompt += "\n"
            
            if "itu" in source_data:
                itu_data = source_data["itu"]
                prompt += f"ITU ICT Data:\n"
                prompt += f"- Records: {itu_data.get('records', 0)}\n"
                prompt += "\n"
        
        prompt += """
Instructions:
1. Answer the user's question based on the available data sources above
2. If specific data is available, cite numbers and statistics
3. If data is not available, provide general insights based on your knowledge
4. Be concise and informative
5. Mention which data sources you used in your answer

Answer:"""
        
        return prompt

