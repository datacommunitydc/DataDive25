# MCP Integration in Streamlit Dashboard

## Overview

The MCP (Model Context Protocol) server has been integrated directly into the Streamlit dashboard, allowing you to fetch data from various sources without leaving the app.

## How to Use

### 1. Access the Data Fetching View

1. Open the Streamlit dashboard
2. In the sidebar, select **"📥 Fetch Data Sources"** from the Analysis View options
3. You'll see a new section for fetching data from external sources

### 2. Available Data Sources

#### Anthropic EconomicIndex
- **Source:** Hugging Face dataset
- **Usage:** Select "Anthropic EconomicIndex", enter release version, click "Fetch Data"
- **Returns:** Economic indicators related to AI impacts
- **Requires:** `pip install datasets` (if MCP not available)

#### Stanford AI Index
- **Source:** Stanford HAI AI Index Report 2025
- **Usage:** Select "Stanford AI Index", choose metric type, click "Fetch Data"
- **Returns:** AI investment, adoption, and performance metrics
- **Metrics Available:**
  - Investment (US: $109.1B, China: $9.3B, UK: $4.5B)
  - Adoption (78% of organizations using AI in 2024)
  - Performance metrics

#### World Bank Indicator
- **Source:** World Bank API
- **Usage:** Select "World Bank Indicator", enter indicator code, country, and year range
- **Common Indicators:**
  - `SL.EMP.ICTI.ZS` - ICT Services Employment
  - `SL.EMP.ICTM.ZS` - ICT Manufacturing Employment
  - `IT.NET.USER.ZS` - Internet Users
- **Returns:** Time series data with statistics

#### ITU ICT Data
- **Source:** ITU via World Bank API
- **Usage:** Select "ITU ICT Data", choose indicator (internet/mobile/broadband), enter country
- **Returns:** ICT penetration and usage data

#### View Source Information
- **Usage:** Select "View Source Information", choose a source
- **Returns:** Information about data sources, URLs, and access methods

## Features

### Automatic Fallback
- If MCP SDK is not installed, the app uses direct API access
- World Bank data uses direct API calls (faster)
- Anthropic data can use Hugging Face datasets library directly
- Stanford data shows key metrics even without MCP

### Data Display
- Fetched data is displayed in interactive tables
- Statistics are shown as metrics
- Data can be viewed, analyzed, and exported

### Error Handling
- Clear error messages if data fetch fails
- Installation instructions for missing dependencies
- Graceful degradation if services are unavailable

## Code Structure

### Files

1. **`mcp_client.py`** - Simplified MCP client wrapper
   - `MCPDataFetcher` class
   - Methods for each data source
   - Fallback mechanisms

2. **`app.py`** - Updated Streamlit app
   - New "Fetch Data Sources" view
   - UI components for data fetching
   - Integration with MCP client

### Usage in Code

```python
from mcp_client import data_fetcher

# Fetch Anthropic data
result = data_fetcher.fetch_anthropic_data("release_2025_09_15")

# Fetch Stanford AI Index
result = data_fetcher.fetch_stanford_ai_index("investment")

# Fetch World Bank indicator
result = data_fetcher.fetch_world_bank_indicator(
    "SL.EMP.ICTI.ZS", 
    "USA", 
    2015, 
    2024
)
```

## Installation

### Option 1: With MCP (Full Features)
```bash
pip install mcp
```

### Option 2: Without MCP (Fallback Mode)
```bash
# For Anthropic data
pip install datasets

# World Bank and ITU work without MCP (direct API)
```

## Example Workflow

1. **Start Dashboard:**
   ```bash
   streamlit run app.py
   ```

2. **Navigate to Fetch Data:**
   - Select "📥 Fetch Data Sources" from sidebar

3. **Fetch Data:**
   - Choose a data source
   - Configure parameters
   - Click "Fetch Data"

4. **View Results:**
   - Data appears in tables
   - Statistics shown as metrics
   - Can be analyzed further

5. **Integrate Data:**
   - Use fetched data for analysis
   - Compare with existing dashboard data
   - Export if needed

## Troubleshooting

### MCP Not Available
- The app will use direct API access
- World Bank data works without MCP
- Some features may be limited

### Import Errors
```bash
# Install missing dependencies
pip install mcp datasets requests pandas
```

### Data Fetch Failures
- Check internet connection
- Verify API endpoints are accessible
- Check error messages for specific issues

## Next Steps

1. **Test Data Fetching:** Try fetching from each source
2. **Integrate Data:** Use fetched data in dashboard analysis
3. **Extend Functionality:** Add more data sources as needed
4. **Save Data:** Optionally save fetched data to database

## Support

For issues:
- Check `mcp_server/README.md` for MCP server details
- Review `DATA_SOURCES.md` for source information
- See `INTEGRATION_GUIDE.md` for integration steps

