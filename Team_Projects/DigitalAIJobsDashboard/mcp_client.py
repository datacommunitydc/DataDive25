#!/usr/bin/env python3
"""
MCP Client for Streamlit App

This module provides a simplified interface to fetch data from various sources
using the MCP server. It can be used directly in the Streamlit dashboard.
"""

import json
import asyncio
import pandas as pd
from typing import Optional, Dict, Any
import requests

# Try importing World Bank helper
try:
    from worldbank_helper import try_world_bank_api_alternative
    WB_HELPER_AVAILABLE = True
except ImportError:
    WB_HELPER_AVAILABLE = False


class MCPDataFetcher:
    """Simplified MCP client for fetching data in Streamlit."""
    
    def __init__(self):
        """Initialize the data fetcher."""
        self.use_mcp = False
        self._check_mcp_available()
    
    def _check_mcp_available(self):
        """Check if MCP SDK is available."""
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
            self.use_mcp = True
            self.ClientSession = ClientSession
            self.StdioServerParameters = StdioServerParameters
            self.stdio_client = stdio_client
        except ImportError:
            self.use_mcp = False
    
    def _call_mcp_tool_sync(self, tool_name: str, arguments: dict) -> dict:
        """Call an MCP tool synchronously (for Streamlit)."""
        if not self.use_mcp:
            return {"error": "MCP SDK not installed. Install with: pip install mcp"}
        
        try:
            # Run async function in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._call_mcp_tool_async(tool_name, arguments))
            loop.close()
            return result
        except Exception as e:
            return {"error": str(e)}
    
    async def _call_mcp_tool_async(self, tool_name: str, arguments: dict) -> dict:
        """Call an MCP tool (async version)."""
        server_params = self.StdioServerParameters(
            command="python",
            args=["mcp_server/server.py"]
        )
        
        try:
            async with self.stdio_client(server_params) as (read, write):
                async with self.ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, arguments)
                    return json.loads(result.content[0].text)
        except Exception as e:
            return {"error": str(e)}
    
    def fetch_anthropic_data(self, release: str = "release_2025_09_15") -> Dict[str, Any]:
        """Fetch Anthropic EconomicIndex data."""
        if self.use_mcp:
            return self._call_mcp_tool_sync(
                "get_anthropic_economic_index",
                {"release": release}
            )
        else:
            # Fallback: try direct Hugging Face access
            try:
                from datasets import load_dataset
                dataset = load_dataset("Anthropic/EconomicIndex", release)
                df = dataset['train'].to_pandas()
                return {
                    "success": True,
                    "records": len(df),
                    "columns": list(df.columns),
                    "data": df.head(100).to_dict('records'),
                    "source": "direct_huggingface"
                }
            except ImportError:
                return {
                    "error": "datasets library not installed", 
                    "install": "pip install datasets",
                    "suggestion": "Install with: pip install datasets"
                }
            except (ValueError, Exception) as e:
                # Catch PyArrow compatibility issues and other errors
                error_msg = str(e)
                if "pyarrow" in error_msg.lower() or "binary incompatibility" in error_msg.lower():
                    return {
                        "error": "PyArrow version incompatibility detected",
                        "details": error_msg[:200],
                        "suggestion": "Try: pip install --force-reinstall datasets pyarrow",
                        "alternative": "Use CSV upload feature or download data manually from Hugging Face"
                    }
                return {
                    "error": str(e)[:200],
                    "suggestion": "Check your datasets and pyarrow versions"
                }
    
    def fetch_stanford_ai_index(self, metric_type: str = "all") -> Dict[str, Any]:
        """Fetch Stanford AI Index data."""
        if self.use_mcp:
            return self._call_mcp_tool_sync(
                "get_stanford_ai_index",
                {"metric_type": metric_type}
            )
        else:
            # Return key metrics directly
            return {
                "success": True,
                "source": "stanford_ai_index",
                "key_metrics": {
                    "investment": {
                        "us_2024": "$109.1 billion",
                        "china_2024": "$9.3 billion",
                        "uk_2024": "$4.5 billion"
                    },
                    "adoption": {
                        "organizations_using_ai_2024": "78%",
                        "organizations_using_ai_2023": "55%"
                    }
                },
                "url": "https://hai.stanford.edu/ai-index/2025-ai-index-report"
            }
    
    def fetch_world_bank_indicator(
        self, 
        indicator_code: str, 
        country_code: str = "all",
        start_year: int = 2015,
        end_year: int = 2024
    ) -> Dict[str, Any]:
        """Fetch World Bank indicator data."""
        # Direct API call (faster than MCP for simple requests)
        try:
            # Use correct World Bank API v2 format
            # For "all" countries, use "all" or "WLD" for world aggregate
            if country_code.lower() == "all":
                country_param = "all"
            else:
                country_param = country_code
            
            url = f"https://api.worldbank.org/v2/country/{country_param}/indicator/{indicator_code}"
            params = {
                "format": "json",
                "per_page": 20000,
                "date": f"{start_year}:{end_year}",
                "mrnev": 1  # Most recent non-empty value
            }
            
            # Add headers to avoid 401 errors
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; DigitalAIJobsDashboard/1.0)",
                "Accept": "application/json"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            
            # Handle 401 errors - try alternative method
            if response.status_code == 401:
                # Try alternative endpoint if helper is available
                if WB_HELPER_AVAILABLE:
                    alt_result = try_world_bank_api_alternative(indicator_code, country_code, start_year, end_year)
                    if "success" in alt_result and alt_result["success"]:
                        return alt_result
                
                return {
                    "error": "World Bank API access denied (401). This may be due to rate limiting or API changes.",
                    "indicator": indicator_code,
                    "status_code": 401,
                    "suggestion": "Try using the World Bank DataBank website directly: https://databank.worldbank.org/",
                    "alternative": "Some indicators may require authentication. Check World Bank API documentation.",
                    "workaround": "The dashboard includes sample World Bank data. You can also download CSV files from DataBank and import them."
                }
            
            response.raise_for_status()
            data = response.json()
            
            if len(data) < 2 or not data[1]:
                return {
                    "error": "No data available", 
                    "indicator": indicator_code,
                    "suggestion": f"Check if indicator code '{indicator_code}' is correct at https://data.worldbank.org/"
                }
            
            records = []
            for entry in data[1]:
                records.append({
                    "country_code": entry.get("country", {}).get("id", ""),
                    "country_name": entry.get("country", {}).get("value", ""),
                    "year": entry.get("date", ""),
                    "value": entry.get("value")
                })
            
            df = pd.DataFrame(records)
            df = df[df["value"].notna()]
            
            if df.empty:
                return {
                    "error": "No valid data found after filtering",
                    "indicator": indicator_code,
                    "records_fetched": len(records),
                    "suggestion": "Try a different year range or country"
                }
            
            return {
                "success": True,
                "indicator_code": indicator_code,
                "records": len(df),
                "data": df.to_dict('records'),
                "statistics": {
                    "mean": float(df["value"].mean()) if not df.empty else None,
                    "min": float(df["value"].min()) if not df.empty else None,
                    "max": float(df["value"].max()) if not df.empty else None
                }
            }
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return {
                    "error": "World Bank API authentication required or access denied",
                    "indicator": indicator_code,
                    "status_code": 401,
                    "suggestion": "World Bank API may require registration. Visit https://datahelpdesk.worldbank.org/ for API access."
                }
            return {"error": f"HTTP Error {e.response.status_code}: {str(e)}"}
        except Exception as e:
            return {"error": str(e), "indicator": indicator_code}
    
    def fetch_itu_ict_data(self, indicator: str = "internet", country_code: str = "all") -> Dict[str, Any]:
        """Fetch ITU ICT data."""
        indicator_codes = {
            "mobile": "IT.CEL.SETS.P2",
            "internet": "IT.NET.USER.ZS",
            "broadband": "IT.NET.BBND.P2"
        }
        
        if indicator not in indicator_codes:
            return {"error": f"Unknown indicator: {indicator}"}
        
        return self.fetch_world_bank_indicator(
            indicator_codes[indicator],
            country_code,
            2015,
            2024
        )
    
    def get_data_source_info(self, source_name: str) -> Dict[str, Any]:
        """Get information about a specific data source."""
        sources = {
            "anthropic": {
                "name": "Anthropic EconomicIndex",
                "status": "✅ Available",
                "description": "Economic indicators related to AI impacts",
                "fetch_function": "fetch_anthropic_data"
            },
            "stanford": {
                "name": "Stanford AI Index",
                "status": "✅ Available",
                "description": "AI investment, adoption, and performance metrics",
                "fetch_function": "fetch_stanford_ai_index"
            },
            "world_bank": {
                "name": "World Bank Indicators",
                "status": "✅ Available",
                "description": "Various economic and development indicators",
                "fetch_function": "fetch_world_bank_indicator"
            },
            "itu": {
                "name": "ITU ICT Data",
                "status": "✅ Available",
                "description": "ICT indicators (mobile, internet, broadband)",
                "fetch_function": "fetch_itu_ict_data"
            },
            "pwc": {
                "name": "PwC AI Jobs Barometer",
                "status": "⚠️ PDF Reports",
                "description": "AI job posting trends and skills demand",
                "url": "https://www.pwc.com/gx/en/services/ai/ai-jobs-barometer.html"
            },
            "yale": {
                "name": "Yale Budget Lab",
                "status": "⚠️ Research Publications",
                "description": "AI labor market impact research",
                "url": "https://budgetlab.yale.edu/research/evaluating-impact-ai-labor-market-current-state-affairs"
            },
            "mckinsey": {
                "name": "McKinsey Generative AI",
                "status": "⚠️ Research Reports",
                "description": "Economic potential of generative AI",
                "url": "https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier"
            }
        }
        
        return sources.get(source_name.lower(), {"error": "Unknown source"})


# Global instance for use in Streamlit
data_fetcher = MCPDataFetcher()

