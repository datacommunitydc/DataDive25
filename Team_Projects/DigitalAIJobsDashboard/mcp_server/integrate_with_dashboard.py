#!/usr/bin/env python3
"""
Integration script to use MCP server with the dashboard's load_data.py

This script shows how to fetch data using MCP and integrate it into the dashboard database.
"""

import asyncio
import json
import pandas as pd
import duckdb
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def fetch_data_via_mcp(tool_name: str, arguments: dict):
    """Fetch data using MCP server."""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return json.loads(result.content[0].text)


def integrate_anthropic_data(db_path: Path):
    """Integrate Anthropic EconomicIndex data into dashboard database."""
    print("Fetching Anthropic EconomicIndex data via MCP...")
    
    try:
        data = asyncio.run(fetch_data_via_mcp(
            "get_anthropic_economic_index",
            {"release": "release_2025_09_15"}
        ))
        
        if "error" in data:
            print(f"Error: {data['error']}")
            return
        
        # Convert sample data to DataFrame
        df = pd.DataFrame(data.get("sample_data", []))
        
        if df.empty:
            print("No data to integrate")
            return
        
        # Connect to database
        conn = duckdb.connect(str(db_path), read_only=False)
        
        # Create table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS anthropic_economic_index AS
            SELECT * FROM df
        """)
        
        print(f"✅ Integrated {len(df)} records from Anthropic EconomicIndex")
        conn.close()
        
    except Exception as e:
        print(f"Error integrating Anthropic data: {e}")


def integrate_world_bank_data(db_path: Path, indicator_code: str, country_code: str = "all"):
    """Integrate World Bank indicator data via MCP."""
    print(f"Fetching World Bank indicator {indicator_code} via MCP...")
    
    try:
        data = asyncio.run(fetch_data_via_mcp(
            "get_world_bank_indicator",
            {
                "indicator_code": indicator_code,
                "country_code": country_code,
                "start_year": 2015,
                "end_year": 2024
            }
        ))
        
        if "error" in data:
            print(f"Error: {data['error']}")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(data.get("sample_data", []))
        
        if df.empty:
            print("No data to integrate")
            return
        
        # Connect to database
        conn = duckdb.connect(str(db_path), read_only=False)
        
        # Create table
        table_name = f"wb_{indicator_code.lower().replace('.', '_')}"
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} AS
            SELECT * FROM df
        """)
        
        print(f"✅ Integrated {len(df)} records from World Bank indicator {indicator_code}")
        conn.close()
        
    except Exception as e:
        print(f"Error integrating World Bank data: {e}")


def main():
    """Main integration function."""
    # Path to dashboard database
    db_path = Path(__file__).parent.parent / "data" / "digital_jobs.duckdb"
    
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        print("Please run load_data.py first to create the database")
        return
    
    print("="*60)
    print("MCP Data Integration")
    print("="*60)
    
    # Integrate Anthropic data
    integrate_anthropic_data(db_path)
    
    print("\n" + "-"*60 + "\n")
    
    # Integrate World Bank ICT indicators
    indicators = [
        ("SL.EMP.ICTI.ZS", "ICT Services Employment"),
        ("SL.EMP.ICTM.ZS", "ICT Manufacturing Employment"),
        ("IT.NET.USER.ZS", "Internet Users")
    ]
    
    for code, name in indicators:
        integrate_world_bank_data(db_path, code)
        print()
    
    print("="*60)
    print("Integration complete!")
    print("="*60)


if __name__ == "__main__":
    main()

