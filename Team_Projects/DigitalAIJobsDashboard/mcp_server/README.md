# MCP Server for Digital/AI Jobs Data Sources

This MCP (Model Context Protocol) server provides tools to fetch data from various sources for the Digital/AI Jobs Dashboard.

## Installation

```bash
pip install -r requirements.txt
```

## Available Tools

### 1. `get_anthropic_economic_index`
Fetch Anthropic EconomicIndex dataset from Hugging Face.

**Parameters:**
- `release` (string, optional): Release version (default: "release_2025_09_15")

**Example:**
```python
{
  "release": "release_2025_09_15"
}
```

### 2. `get_stanford_ai_index`
Fetch data from Stanford AI Index Report 2025.

**Parameters:**
- `metric_type` (string): Type of metric - "investment", "adoption", "performance", or "all"

**Example:**
```python
{
  "metric_type": "investment"
}
```

### 3. `get_world_bank_indicator`
Fetch indicator data from World Bank API.

**Parameters:**
- `indicator_code` (string, required): World Bank indicator code
- `country_code` (string, optional): Country code or "all" (default: "all")
- `start_year` (integer, optional): Start year (default: 2000)
- `end_year` (integer, optional): End year (default: 2024)

**Example:**
```python
{
  "indicator_code": "SL.EMP.ICTI.ZS",
  "country_code": "USA",
  "start_year": 2015,
  "end_year": 2024
}
```

### 4. `get_pwc_ai_jobs_data`
Get information about PwC AI Jobs Barometer data sources.

**Parameters:**
- `year` (integer, optional): Report year (default: 2025)

### 5. `get_yale_budget_lab_info`
Get information about Yale Budget Lab AI labor market research.

### 6. `get_mckinsey_generative_ai_info`
Get information about McKinsey Generative AI economic potential research.

### 7. `get_itu_ict_data`
Fetch ICT data from ITU via World Bank API.

**Parameters:**
- `indicator` (string): "mobile", "internet", or "broadband"
- `country_code` (string, optional): Country code or "all"

### 8. `list_available_data_sources`
List all available data sources and their status.

## Running the Server

### Using MCP CLI

```bash
mcp run mcp_server/server.py
```

### Using Python directly

```bash
python mcp_server/server.py
```

## Integration with Dashboard

The MCP server can be integrated with the dashboard's `load_data.py` to fetch real-time data:

```python
# In load_data.py
import subprocess
import json

def fetch_via_mcp(tool_name, arguments):
    """Fetch data using MCP server."""
    # Implementation depends on MCP client setup
    pass
```

## Data Sources

1. **Anthropic EconomicIndex** - ✅ Direct API (Hugging Face)
2. **Stanford AI Index** - ⚠️ Public data portal
3. **World Bank** - ✅ Direct API
4. **ITU ICT** - ✅ Via World Bank API
5. **PwC AI Jobs Barometer** - ⚠️ PDF Reports
6. **Yale Budget Lab** - ⚠️ Research Publications
7. **McKinsey** - ⚠️ Research Reports

## Configuration

Create a `.env` file for API keys if needed:

```env
# Optional: Add API keys if required
WORLD_BANK_API_KEY=
HUGGINGFACE_TOKEN=
```

## License

MIT License - Same as main project

