#!/usr/bin/env python3
"""
Example MCP Client for Digital/AI Jobs Data Sources

This script demonstrates how to use the MCP server to fetch data from various sources.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Example usage of MCP server tools."""
    
    # Configure server
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # List available tools
            print("Available Tools:")
            tools = await session.list_tools()
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            
            print("\n" + "="*60 + "\n")
            
            # Example 1: Get Anthropic EconomicIndex
            print("1. Fetching Anthropic EconomicIndex...")
            try:
                result = await session.call_tool(
                    "get_anthropic_economic_index",
                    {"release": "release_2025_09_15"}
                )
                data = json.loads(result.content[0].text)
                print(f"   Records: {data.get('records', 'N/A')}")
                print(f"   Columns: {len(data.get('columns', []))}")
            except Exception as e:
                print(f"   Error: {e}")
            
            print("\n" + "-"*60 + "\n")
            
            # Example 2: Get Stanford AI Index data
            print("2. Fetching Stanford AI Index (Investment metrics)...")
            try:
                result = await session.call_tool(
                    "get_stanford_ai_index",
                    {"metric_type": "investment"}
                )
                data = json.loads(result.content[0].text)
                print(f"   US Investment 2024: {data.get('key_metrics', {}).get('investment', {}).get('us_2024', 'N/A')}")
            except Exception as e:
                print(f"   Error: {e}")
            
            print("\n" + "-"*60 + "\n")
            
            # Example 3: Get World Bank indicator
            print("3. Fetching World Bank ICT Services Employment data...")
            try:
                result = await session.call_tool(
                    "get_world_bank_indicator",
                    {
                        "indicator_code": "SL.EMP.ICTI.ZS",
                        "country_code": "USA",
                        "start_year": 2015,
                        "end_year": 2024
                    }
                )
                data = json.loads(result.content[0].text)
                print(f"   Records: {data.get('records', 'N/A')}")
                print(f"   Countries: {', '.join(data.get('countries', [])[:5])}")
            except Exception as e:
                print(f"   Error: {e}")
            
            print("\n" + "-"*60 + "\n")
            
            # Example 4: List all data sources
            print("4. Listing all available data sources...")
            try:
                result = await session.call_tool("list_available_data_sources", {})
                data = json.loads(result.content[0].text)
                print(f"   Total sources: {len(data.get('available_sources', []))}")
                for source in data.get('available_sources', []):
                    print(f"   - {source.get('name')}: {source.get('status')}")
            except Exception as e:
                print(f"   Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

