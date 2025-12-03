#!/usr/bin/env python3
"""
MCP Server for Digital/AI Jobs Dashboard Data Sources

This MCP server provides tools to fetch data from various sources:
- Anthropic EconomicIndex (Hugging Face)
- Stanford AI Index Report 2025
- PwC AI Jobs Barometer
- Yale Budget Lab
- McKinsey Generative AI
- World Bank APIs
"""

import asyncio
import json
from typing import Any, Optional
from datetime import datetime
import pandas as pd
import requests
from pathlib import Path

try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
        LoggingLevel
    )
except ImportError:
    print("MCP SDK not installed. Install with: pip install mcp")
    raise


# Initialize MCP Server
server = Server("digital-ai-jobs-data-sources")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available data source tools."""
    return [
        Tool(
            name="get_anthropic_economic_index",
            description="Fetch Anthropic EconomicIndex dataset from Hugging Face. Returns economic indicators related to AI impacts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "release": {
                        "type": "string",
                        "description": "Release version (default: release_2025_09_15)",
                        "default": "release_2025_09_15"
                    }
                }
            }
        ),
        Tool(
            name="get_stanford_ai_index",
            description="Fetch data from Stanford AI Index Report 2025. Returns AI investment, adoption, and performance metrics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "metric_type": {
                        "type": "string",
                        "description": "Type of metric: 'investment', 'adoption', 'performance', 'all'",
                        "enum": ["investment", "adoption", "performance", "all"],
                        "default": "all"
                    }
                }
            }
        ),
        Tool(
            name="get_world_bank_indicator",
            description="Fetch indicator data from World Bank API.",
            inputSchema={
                "type": "object",
                "properties": {
                    "indicator_code": {
                        "type": "string",
                        "description": "World Bank indicator code (e.g., SL.EMP.ICTI.ZS)"
                    },
                    "country_code": {
                        "type": "string",
                        "description": "Country code (e.g., USA, CHN) or 'all' for all countries",
                        "default": "all"
                    },
                    "start_year": {
                        "type": "integer",
                        "description": "Start year",
                        "default": 2000
                    },
                    "end_year": {
                        "type": "integer",
                        "description": "End year",
                        "default": 2024
                    }
                },
                "required": ["indicator_code"]
            }
        ),
        Tool(
            name="get_pwc_ai_jobs_data",
            description="Get information about PwC AI Jobs Barometer data sources and how to access them.",
            inputSchema={
                "type": "object",
                "properties": {
                    "year": {
                        "type": "integer",
                        "description": "Report year (2024 or 2025)",
                        "default": 2025
                    }
                }
            }
        ),
        Tool(
            name="get_yale_budget_lab_info",
            description="Get information about Yale Budget Lab AI labor market research and data sources.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_mckinsey_generative_ai_info",
            description="Get information about McKinsey Generative AI economic potential research and data sources.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_itu_ict_data",
            description="Fetch ICT data from ITU via World Bank API.",
            inputSchema={
                "type": "object",
                "properties": {
                    "indicator": {
                        "type": "string",
                        "description": "ICT indicator: 'mobile', 'internet', 'broadband'",
                        "enum": ["mobile", "internet", "broadband"],
                        "default": "internet"
                    },
                    "country_code": {
                        "type": "string",
                        "description": "Country code or 'all'",
                        "default": "all"
                    }
                }
            }
        ),
        Tool(
            name="list_available_data_sources",
            description="List all available data sources and their status.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "get_anthropic_economic_index":
        return await get_anthropic_economic_index(arguments.get("release", "release_2025_09_15"))
    
    elif name == "get_stanford_ai_index":
        return await get_stanford_ai_index(arguments.get("metric_type", "all"))
    
    elif name == "get_world_bank_indicator":
        return await get_world_bank_indicator(
            arguments["indicator_code"],
            arguments.get("country_code", "all"),
            arguments.get("start_year", 2000),
            arguments.get("end_year", 2024)
        )
    
    elif name == "get_pwc_ai_jobs_data":
        return await get_pwc_ai_jobs_data(arguments.get("year", 2025))
    
    elif name == "get_yale_budget_lab_info":
        return await get_yale_budget_lab_info()
    
    elif name == "get_mckinsey_generative_ai_info":
        return await get_mckinsey_generative_ai_info()
    
    elif name == "get_itu_ict_data":
        return await get_itu_ict_data(
            arguments.get("indicator", "internet"),
            arguments.get("country_code", "all")
        )
    
    elif name == "list_available_data_sources":
        return await list_available_data_sources()
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def get_anthropic_economic_index(release: str) -> list[TextContent]:
    """Fetch Anthropic EconomicIndex from Hugging Face."""
    try:
        from datasets import load_dataset
        
        dataset = load_dataset("Anthropic/EconomicIndex", release)
        df = dataset['train'].to_pandas()
        
        summary = {
            "source": "Anthropic EconomicIndex",
            "release": release,
            "records": len(df),
            "columns": list(df.columns),
            "sample_data": df.head(10).to_dict('records'),
            "data_types": df.dtypes.to_dict(),
            "description": "Economic indicators related to AI impacts on labor markets and economy"
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(summary, indent=2, default=str)
        )]
    except ImportError:
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": "datasets library not installed",
                "install_command": "pip install datasets",
                "source": "https://huggingface.co/datasets/Anthropic/EconomicIndex"
            }, indent=2)
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2)
        )]


async def get_stanford_ai_index(metric_type: str) -> list[TextContent]:
    """Fetch Stanford AI Index data."""
    # Note: This would need to access Stanford's public data portal
    # For now, return information about how to access it
    
    info = {
        "source": "Stanford AI Index Report 2025",
        "url": "https://hai.stanford.edu/ai-index/2025-ai-index-report",
        "public_data_portal": "https://hai.stanford.edu/ai-index/2025-ai-index-report",
        "key_metrics": {
            "investment": {
                "us_2024": "$109.1 billion",
                "china_2024": "$9.3 billion",
                "uk_2024": "$4.5 billion"
            },
            "adoption": {
                "organizations_using_ai_2024": "78%",
                "organizations_using_ai_2023": "55%"
            },
            "performance": {
                "notable_models_us_2024": 40,
                "notable_models_china_2024": 15,
                "notable_models_europe_2024": 3
            }
        },
        "access_method": "Public data available via Stanford HAI website",
        "note": "Direct API access may require contacting Stanford HAI"
    }
    
    if metric_type != "all":
        info["filtered_metric"] = metric_type
        if metric_type in info["key_metrics"]:
            info["data"] = info["key_metrics"][metric_type]
    
    return [TextContent(
        type="text",
        text=json.dumps(info, indent=2)
    )]


async def get_world_bank_indicator(indicator_code: str, country_code: str, start_year: int, end_year: int) -> list[TextContent]:
    """Fetch World Bank indicator data."""
    try:
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"
        params = {
            "format": "json",
            "per_page": 20000,
            "date": f"{start_year}:{end_year}"
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if len(data) < 2 or not data[1]:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "No data available", "indicator": indicator_code}, indent=2)
            )]
        
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
        
        result = {
            "indicator_code": indicator_code,
            "country_code": country_code,
            "year_range": f"{start_year}-{end_year}",
            "records": len(df),
            "countries": df["country_name"].unique().tolist() if not df.empty else [],
            "years": sorted(df["year"].unique().tolist()) if not df.empty else [],
            "sample_data": df.head(20).to_dict('records'),
            "statistics": {
                "mean": float(df["value"].mean()) if not df.empty else None,
                "min": float(df["value"].min()) if not df.empty else None,
                "max": float(df["value"].max()) if not df.empty else None
            }
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, default=str)
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2)
        )]


async def get_pwc_ai_jobs_data(year: int) -> list[TextContent]:
    """Get PwC AI Jobs Barometer information."""
    info = {
        "source": "PwC AI Jobs Barometer",
        "url": "https://www.pwc.com/gx/en/services/ai/ai-jobs-barometer.html",
        "year": year,
        "description": "Comprehensive analysis of AI's impact on jobs, tracking job postings, skills demand, and labor market transformations",
        "data_types": [
            "AI job posting trends",
            "Skills demand analysis",
            "Industry-level job impacts",
            "Regional variations in AI job markets",
            "Supply and demand dynamics"
        ],
        "access_method": "Download PDF reports from PwC website",
        "reports_available": [
            "2025 AI Jobs Barometer (Full report and Executive summary)",
            "2024 AI Jobs Barometer (Historical comparison)"
        ],
        "note": "Data extraction from PDFs may require pdfplumber or tabula-py libraries",
        "integration_tip": "Use PDF parsing libraries to extract structured data from reports"
    }
    
    return [TextContent(
        type="text",
        text=json.dumps(info, indent=2)
    )]


async def get_yale_budget_lab_info() -> list[TextContent]:
    """Get Yale Budget Lab information."""
    info = {
        "source": "Yale Budget Lab - Evaluating Impact of AI on Labor Market",
        "url": "https://budgetlab.yale.edu/research/evaluating-impact-ai-labor-market-current-state-affairs",
        "description": "Research and analysis on the current state of AI's impact on labor markets",
        "data_types": [
            "Labor market impact assessments",
            "Job displacement analysis",
            "Workforce transition metrics",
            "Economic impact evaluations"
        ],
        "access_method": "Research publications and datasets",
        "license": "Academic research (check specific publication licenses)",
        "note": "Contact researchers for data access or extract from research publications"
    }
    
    return [TextContent(
        type="text",
        text=json.dumps(info, indent=2)
    )]


async def get_mckinsey_generative_ai_info() -> list[TextContent]:
    """Get McKinsey Generative AI information."""
    info = {
        "source": "McKinsey - The Economic Potential of Generative AI",
        "url": "https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier",
        "description": "Comprehensive analysis of generative AI's economic potential and productivity impacts",
        "key_insights": {
            "economic_value": "Generative AI could add trillions of dollars in value to global economy",
            "productivity_gains": "Significant productivity gains across knowledge work sectors",
            "workforce_implications": "Transformation of work activities and required skills"
        },
        "data_types": [
            "Economic value potential by industry",
            "Productivity gains metrics",
            "Workforce transformation data",
            "Skills requirements"
        ],
        "access_method": "Research reports and articles (publicly available insights)",
        "license": "McKinsey proprietary (publicly available insights)",
        "note": "Extract structured data from reports or contact McKinsey for datasets"
    }
    
    return [TextContent(
        type="text",
        text=json.dumps(info, indent=2)
    )]


async def get_itu_ict_data(indicator: str, country_code: str) -> list[TextContent]:
    """Fetch ITU ICT data via World Bank API."""
    indicator_codes = {
        "mobile": "IT.CEL.SETS.P2",
        "internet": "IT.NET.USER.ZS",
        "broadband": "IT.NET.BBND.P2"
    }
    
    if indicator not in indicator_codes:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown indicator: {indicator}"}, indent=2)
        )]
    
    return await get_world_bank_indicator(
        indicator_codes[indicator],
        country_code,
        2000,
        2024
    )


async def list_available_data_sources() -> list[TextContent]:
    """List all available data sources."""
    sources = {
        "available_sources": [
            {
                "name": "Anthropic EconomicIndex",
                "status": "✅ Available via Hugging Face",
                "tool": "get_anthropic_economic_index",
                "requires": "datasets library"
            },
            {
                "name": "Stanford AI Index Report 2025",
                "status": "⚠️ Public data portal",
                "tool": "get_stanford_ai_index",
                "note": "Key metrics available, full dataset via portal"
            },
            {
                "name": "World Bank Indicators",
                "status": "✅ Available via API",
                "tool": "get_world_bank_indicator",
                "indicators": [
                    "SL.EMP.ICTI.ZS (ICT Services Employment)",
                    "SL.EMP.ICTM.ZS (ICT Manufacturing Employment)",
                    "TX.VAL.ICTG.ZS.UN (ICT Exports)",
                    "TM.VAL.ICTG.ZS.UN (ICT Imports)"
                ]
            },
            {
                "name": "ITU ICT Data",
                "status": "✅ Available via World Bank API",
                "tool": "get_itu_ict_data",
                "indicators": ["mobile", "internet", "broadband"]
            },
            {
                "name": "PwC AI Jobs Barometer",
                "status": "⚠️ PDF Reports",
                "tool": "get_pwc_ai_jobs_data",
                "note": "Requires PDF extraction"
            },
            {
                "name": "Yale Budget Lab",
                "status": "⚠️ Research Publications",
                "tool": "get_yale_budget_lab_info",
                "note": "Contact researchers or extract from publications"
            },
            {
                "name": "McKinsey Generative AI",
                "status": "⚠️ Research Reports",
                "tool": "get_mckinsey_generative_ai_info",
                "note": "Extract from reports or contact for datasets"
            }
        ],
        "integration_status": {
            "direct_api": ["World Bank", "ITU (via WB)", "Anthropic (Hugging Face)"],
            "requires_extraction": ["PwC", "Yale", "McKinsey", "Stanford (full dataset)"]
        }
    }
    
    return [TextContent(
        type="text",
        text=json.dumps(sources, indent=2)
    )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="digital-ai-jobs-data-sources",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())

