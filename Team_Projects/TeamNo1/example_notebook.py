# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # World Bank Labor Force Analysis
# 
# This notebook downloads World Bank labor force participation data and creates
# a simple visualization showing trends by region over time.
# 
# **What you'll learn:**
# - How to download data from the World Bank
# - How to use DuckDB for fast CSV loading and SQL analysis
# - How to create charts with Altair
# 
# **Required packages:**
# ```
# pip install requests duckdb pandas altair
# ```

# %% [markdown]
# ## Step 1: Setup and Imports

# %%
import requests
import duckdb
import altair as alt
from pathlib import Path

# %%
# Create a data folder to store our files
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

print(f"Data will be saved to: {DATA_DIR.absolute()}")

# %% [markdown]
# ## Step 2: Download the Data
# 
# We'll download two files from the World Bank:
# 1. **Indicator data** - The actual labor force participation rates
# 2. **Dictionary data** - Metadata about countries and regions

# %%
# URLs for World Bank data
INDICATOR_URL = "https://data360files.worldbank.org/data360-data/data/WB_WDI/WB_WDI_SL_TLF_CACT_ZS.csv"
DICTIONARY_URL = "https://data360files.worldbank.org/data360-data/data/WB_WDI/WB_WDI_SL_TLF_CACT_ZS_DATADICT.csv"

# Local file paths
INDICATOR_FILE = DATA_DIR / "labor_force_data.csv"
DICTIONARY_FILE = DATA_DIR / "data_dictionary.csv"

# %%
# Download indicator data (skip if already exists)
if not INDICATOR_FILE.exists():
    print("Downloading indicator data...")
    response = requests.get(INDICATOR_URL, timeout=60)
    response.raise_for_status()
    INDICATOR_FILE.write_bytes(response.content)
    print(f"Saved to {INDICATOR_FILE}")
else:
    print(f"Using cached file: {INDICATOR_FILE}")

# %%
# Download dictionary data (skip if already exists)
if not DICTIONARY_FILE.exists():
    print("Downloading dictionary data...")
    response = requests.get(DICTIONARY_URL, timeout=60)
    response.raise_for_status()
    DICTIONARY_FILE.write_bytes(response.content)
    print(f"Saved to {DICTIONARY_FILE}")
else:
    print(f"Using cached file: {DICTIONARY_FILE}")

# %% [markdown]
# ## Step 3: Load CSVs into DuckDB
# 
# DuckDB can read CSV files directly - no need to load into pandas first!
# This is faster and more memory efficient for large files.

# %%
# Create a DuckDB connection
DB_PATH = DATA_DIR / "worldbank.duckdb"
conn = duckdb.connect(str(DB_PATH))

print(f"Connected to DuckDB: {DB_PATH}")

# %%
# Load indicator CSV directly into DuckDB
conn.execute(f"""
    CREATE OR REPLACE TABLE indicator_raw AS
    SELECT * FROM read_csv_auto('{INDICATOR_FILE}', header=True)
""")

row_count = conn.execute("SELECT COUNT(*) FROM indicator_raw").fetchone()[0]
print(f"Loaded indicator_raw: {row_count:,} rows")

# %%
# Load dictionary CSV directly into DuckDB
conn.execute(f"""
    CREATE OR REPLACE TABLE dictionary AS
    SELECT DISTINCT * FROM read_csv_auto('{DICTIONARY_FILE}', header=True)
""")

row_count = conn.execute("SELECT COUNT(*) FROM dictionary").fetchone()[0]
print(f"Loaded dictionary: {row_count:,} rows")

# %% [markdown]
# ## Step 4: Explore the Data
# 
# Let's take a quick look at what we loaded using DuckDB queries.

# %%
# Preview indicator data (returns a pandas DataFrame)
conn.execute("SELECT * FROM indicator_raw LIMIT 5").df()

# %%
# Check indicator columns
conn.execute("DESCRIBE indicator_raw").df()

# %%
# Preview dictionary data
conn.execute("SELECT * FROM dictionary LIMIT 5").df()

# %%
# Check dictionary columns  
conn.execute("DESCRIBE dictionary").df()

# %% [markdown]
# ## Step 5: Clean and Transform the Data
# 
# Create a clean, analysis-ready table with proper data types and region info.

# %%
# Create a cleaned indicator table
conn.execute("""
    CREATE OR REPLACE TABLE indicator_clean AS
    SELECT
        REF_AREA AS country_code,
        REF_AREA_LABEL AS country_name,
        CAST(TIME_PERIOD AS INTEGER) AS year,
        CAST(OBS_VALUE AS DOUBLE) AS value,
        INDICATOR_LABEL AS indicator_name
    FROM indicator_raw
    WHERE OBS_VALUE IS NOT NULL
      AND TIME_PERIOD IS NOT NULL
""")

row_count = conn.execute("SELECT COUNT(*) FROM indicator_clean").fetchone()[0]
print(f"Cleaned data: {row_count:,} rows")

# %%
# Preview the cleaned data
conn.execute("SELECT * FROM indicator_clean LIMIT 5").df()

# %%
# Check what columns the dictionary table has
print("Dictionary table columns:")
print(conn.execute("DESCRIBE dictionary").df())

# %%
# The World Bank data dictionary file describes variables, not country metadata.
# We'll create a simple region mapping based on country codes.
# For a real project, you'd download a proper country-region mapping file.

# Create a region mapping table based on common World Bank region codes
conn.execute("""
    CREATE OR REPLACE TABLE region_mapping AS
    SELECT * FROM (VALUES
        -- East Asia & Pacific
        ('CHN', 'East Asia & Pacific'),
        ('JPN', 'East Asia & Pacific'),
        ('KOR', 'East Asia & Pacific'),
        ('AUS', 'East Asia & Pacific'),
        ('IDN', 'East Asia & Pacific'),
        ('THA', 'East Asia & Pacific'),
        ('VNM', 'East Asia & Pacific'),
        ('MYS', 'East Asia & Pacific'),
        ('PHL', 'East Asia & Pacific'),
        ('NZL', 'East Asia & Pacific'),
        -- Europe & Central Asia
        ('DEU', 'Europe & Central Asia'),
        ('FRA', 'Europe & Central Asia'),
        ('GBR', 'Europe & Central Asia'),
        ('ITA', 'Europe & Central Asia'),
        ('ESP', 'Europe & Central Asia'),
        ('POL', 'Europe & Central Asia'),
        ('NLD', 'Europe & Central Asia'),
        ('TUR', 'Europe & Central Asia'),
        ('RUS', 'Europe & Central Asia'),
        ('UKR', 'Europe & Central Asia'),
        -- Latin America & Caribbean
        ('BRA', 'Latin America & Caribbean'),
        ('MEX', 'Latin America & Caribbean'),
        ('ARG', 'Latin America & Caribbean'),
        ('COL', 'Latin America & Caribbean'),
        ('CHL', 'Latin America & Caribbean'),
        ('PER', 'Latin America & Caribbean'),
        ('VEN', 'Latin America & Caribbean'),
        -- Middle East & North Africa
        ('EGY', 'Middle East & North Africa'),
        ('SAU', 'Middle East & North Africa'),
        ('IRN', 'Middle East & North Africa'),
        ('IRQ', 'Middle East & North Africa'),
        ('MAR', 'Middle East & North Africa'),
        ('DZA', 'Middle East & North Africa'),
        -- North America
        ('USA', 'North America'),
        ('CAN', 'North America'),
        -- South Asia
        ('IND', 'South Asia'),
        ('PAK', 'South Asia'),
        ('BGD', 'South Asia'),
        ('LKA', 'South Asia'),
        ('NPL', 'South Asia'),
        -- Sub-Saharan Africa
        ('NGA', 'Sub-Saharan Africa'),
        ('ZAF', 'Sub-Saharan Africa'),
        ('KEN', 'Sub-Saharan Africa'),
        ('ETH', 'Sub-Saharan Africa'),
        ('GHA', 'Sub-Saharan Africa'),
        ('TZA', 'Sub-Saharan Africa')
    ) AS t(country_code, region)
""")

print("Created region_mapping table")

# %%
# Join with region mapping to add region information
conn.execute("""
    CREATE OR REPLACE TABLE indicator_with_region AS
    SELECT
        i.*,
        COALESCE(r.region, 'Other') AS region
    FROM indicator_clean i
    LEFT JOIN region_mapping r ON UPPER(i.country_code) = r.country_code
""")

print("Created table: indicator_with_region")

# %%
# Preview with regions
conn.execute("SELECT * FROM indicator_with_region LIMIT 10").df()

# %% [markdown]
# ## Step 6: Aggregate by Region
# 
# Calculate average labor force participation rate by region and year.

# %%
# Query regional averages and return as pandas DataFrame for charting
regional_df = conn.execute("""
    SELECT
        region,
        year,
        AVG(value) AS avg_participation_rate,
        COUNT(DISTINCT country_code) AS num_countries
    FROM indicator_with_region
    WHERE region != 'Unknown'
      AND region IS NOT NULL
      AND region != ''
    GROUP BY region, year
    HAVING COUNT(DISTINCT country_code) >= 3
    ORDER BY region, year
""").df()

print(f"Regional aggregates: {len(regional_df)} rows")
regional_df.head(10)

# %%
# What regions do we have?
regional_df['region'].unique()

# %% [markdown]
# ## Step 7: Create the Visualization
# 
# Create a line chart showing labor force participation trends by region.

# %%
# Configure Altair to handle large datasets
alt.data_transformers.disable_max_rows()

# %%
# Create the chart
chart = alt.Chart(regional_df).mark_line(point=True).encode(
    x=alt.X('year:Q', title='Year'),
    y=alt.Y('avg_participation_rate:Q', title='Average Participation Rate (%)'),
    color=alt.Color('region:N', title='Region'),
    tooltip=[
        alt.Tooltip('region:N', title='Region'),
        alt.Tooltip('year:Q', title='Year'),
        alt.Tooltip('avg_participation_rate:Q', title='Avg Rate', format='.1f'),
        alt.Tooltip('num_countries:Q', title='Countries')
    ]
).properties(
    width=700,
    height=400,
    title='Labor Force Participation Rate by Region Over Time'
)

chart

# %%
# Save the chart as an HTML file
CHART_FILE = DATA_DIR / "regional_labor_force_chart.html"
chart.save(str(CHART_FILE))
print(f"Chart saved to: {CHART_FILE}")

# %% [markdown]
# ## Step 8: Summary Statistics

# %%
# Get summary stats (DuckDB query → pandas DataFrame)
summary_df = conn.execute("""
    SELECT
        region,
        MIN(year) AS first_year,
        MAX(year) AS last_year,
        ROUND(AVG(value), 1) AS avg_rate,
        COUNT(*) AS data_points
    FROM indicator_with_region
    WHERE region != 'Unknown' AND region IS NOT NULL AND region != ''
    GROUP BY region
    ORDER BY avg_rate DESC
""").df()

print("Summary by Region:")
summary_df

# %%
# Close the database connection
conn.close()
print("Done! Database connection closed.")

# %% [markdown]
# ## Files Created
# 
# This notebook created the following files in the `data/` folder:
# - `labor_force_data.csv` - Raw indicator data
# - `data_dictionary.csv` - Metadata about countries
# - `worldbank.duckdb` - DuckDB database with cleaned tables
# - `regional_labor_force_chart.html` - Interactive chart
