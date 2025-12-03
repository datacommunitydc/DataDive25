# MCP Server Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
cd Team_Projects/DigitalAIJobsDashboard/mcp_server
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python -c "import mcp; print('MCP SDK installed successfully')"
```

If you get an import error, install the MCP SDK:
```bash
pip install mcp
```

### 3. Test the Server

```bash
# Run the example client
python mcp_server/client_example.py
```

## Project Structure

```
DigitalAIJobsDashboard/
├── mcp_server/
│   ├── server.py                    # Main MCP server
│   ├── client_example.py            # Example client usage
│   ├── integrate_with_dashboard.py  # Integration with dashboard
│   ├── requirements.txt              # Dependencies
│   ├── README.md                    # Documentation
│   └── SETUP.md                     # This file
├── app.py                           # Streamlit dashboard
├── load_data.py                     # Data loading script
└── ...
```

## Available Tools

The MCP server provides 8 tools:

1. **get_anthropic_economic_index** - Fetch from Hugging Face
2. **get_stanford_ai_index** - Get Stanford AI Index metrics  
3. **get_world_bank_indicator** - Fetch World Bank data
4. **get_itu_ict_data** - Get ITU ICT indicators
5. **get_pwc_ai_jobs_data** - Get PwC AI Jobs Barometer info
6. **get_yale_budget_lab_info** - Get Yale research info
7. **get_mckinsey_generative_ai_info** - Get McKinsey insights
8. **list_available_data_sources** - List all sources

## Usage Examples

### Using Python Client

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def fetch_data():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Fetch Anthropic data
            result = await session.call_tool(
                "get_anthropic_economic_index",
                {"release": "release_2025_09_15"}
            )
            
            data = json.loads(result.content[0].text)
            print(f"Records: {data['records']}")

asyncio.run(fetch_data())
```

### Integrating with Dashboard

```bash
# Run integration script
python mcp_server/integrate_with_dashboard.py
```

This will:
- Fetch data from various sources via MCP
- Integrate into the dashboard's DuckDB database
- Update existing tables with new data

## Troubleshooting

### Import Errors

If you see `ImportError: No module named 'mcp'`:
```bash
pip install mcp
```

### Dataset Loading Errors

For Anthropic EconomicIndex, ensure datasets library is installed:
```bash
pip install datasets
```

### World Bank API Errors

World Bank API may have rate limits. If you see 429 errors:
- Wait a few seconds between requests
- Use smaller date ranges
- Cache responses locally

## Next Steps

1. Test all tools using `client_example.py`
2. Integrate data using `integrate_with_dashboard.py`
3. Update dashboard to use MCP-fetched data
4. Add new data sources as needed

## Support

For issues or questions:
- Check `README.md` for detailed documentation
- Review `INTEGRATION_GUIDE.md` for integration steps
- Check `DATA_SOURCES.md` for source information

