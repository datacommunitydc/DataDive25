# Data Source Integration Guide

This guide provides instructions for integrating the new data sources into the Digital/AI Jobs Dashboard.

## New Data Sources

### 1. Anthropic EconomicIndex Dataset

**Installation:**
```bash
pip install datasets
```

**Integration Code:**
```python
from datasets import load_dataset
import pandas as pd

# Load the dataset
dataset = load_dataset("Anthropic/EconomicIndex", "release_2025_09_15")

# Convert to pandas DataFrame
df = dataset['train'].to_pandas()

# Process and integrate into DuckDB
# (Add to load_data.py)
```

**Data Structure:**
- Economic indicators related to AI adoption
- Time series data
- Country-level metrics

**Integration Steps:**
1. Add `datasets` to `requirements.txt`
2. Create function `load_anthropic_economic_index()` in `load_data.py`
3. Process and merge with existing `digital_jobs` table
4. Create new views for economic indicators

---

### 2. Stanford AI Index Report 2025

**Access Method:**
- Public data available via [AI Index Public Data Portal](https://hai.stanford.edu/ai-index/2025-ai-index-report)
- Download datasets or use API if available

**Key Data Points:**
- Private AI investment by country ($109.1B US, $9.3B China, $4.5B UK in 2024)
- AI adoption rates (78% of organizations using AI in 2024)
- Model development statistics
- Performance benchmarks

**Integration Steps:**
1. Download or access public data from Stanford HAI
2. Extract relevant metrics (investment, adoption, job impacts)
3. Create function `load_stanford_ai_index()` in `load_data.py`
4. Map to country codes and integrate with existing data

**Example Integration:**
```python
def load_stanford_ai_index():
    """Load Stanford AI Index data."""
    # Download or access data
    # Process investment data by country
    # Extract adoption and job impact metrics
    # Return DataFrame compatible with existing schema
    pass
```

---

### 3. PwC AI Jobs Barometer

**Access Method:**
- Download PDF reports from [PwC AI Jobs Barometer](https://www.pwc.com/gx/en/services/ai/ai-jobs-barometer.html)
- Extract data from tables and charts
- Use PDF parsing libraries or manual data extraction

**Key Data Points:**
- AI job posting trends by industry
- Skills demand analysis
- Regional job market variations
- Supply and demand dynamics

**Integration Steps:**
1. Download 2025 and 2024 reports
2. Extract structured data (consider using `pdfplumber` or `tabula-py`)
3. Create function `load_pwc_ai_jobs_barometer()` in `load_data.py`
4. Map to existing industry and skill taxonomies

**Example Integration:**
```python
import pdfplumber

def load_pwc_ai_jobs_barometer():
    """Extract data from PwC AI Jobs Barometer PDFs."""
    # Read PDF files
    # Extract tables and charts
    # Process into structured format
    # Return DataFrame
    pass
```

**Dependencies:**
```bash
pip install pdfplumber tabula-py
```

---

### 4. Yale Budget Lab - AI Labor Market Impact

**Access Method:**
- Access research publications
- Extract datasets from research papers
- Contact researchers for data access

**Key Data Points:**
- Labor market displacement metrics
- Job creation statistics
- Workforce transition data
- Economic impact assessments

**Integration Steps:**
1. Review research publications
2. Extract quantitative data
3. Create function `load_yale_budget_lab()` in `load_data.py`
4. Integrate with labor market indicators

---

### 5. McKinsey - Economic Potential of Generative AI

**Access Method:**
- Access research reports and articles
- Extract data from visualizations and tables
- Use web scraping for structured data (with permission)

**Key Data Points:**
- Economic value potential by industry
- Productivity gains metrics
- Workforce transformation data
- Skills requirements

**Integration Steps:**
1. Review McKinsey reports
2. Extract structured data
3. Create function `load_mckinsey_generative_ai()` in `load_data.py`
4. Map to industry and skill categories

---

## Integration Workflow

### Step 1: Update Requirements
Add new dependencies to `requirements.txt`:
```txt
datasets>=2.14.0
pdfplumber>=0.9.0
tabula-py>=2.5.0
```

### Step 2: Create Loader Functions
Add functions to `load_data.py`:
```python
def load_anthropic_economic_index():
    """Load Anthropic EconomicIndex dataset."""
    # Implementation
    pass

def load_stanford_ai_index():
    """Load Stanford AI Index data."""
    # Implementation
    pass

# ... etc
```

### Step 3: Update Database Schema
Add new tables to DuckDB:
```python
# In create_database() function
conn.execute("""
    CREATE TABLE anthropic_economic_index AS
    SELECT * FROM anthropic_df
""")

conn.execute("""
    CREATE TABLE stanford_ai_index AS
    SELECT * FROM stanford_df
""")
```

### Step 4: Create Aggregated Views
Create views that combine new data with existing data:
```python
conn.execute("""
    CREATE VIEW enhanced_country_trends AS
    SELECT 
        c.*,
        a.economic_index,
        s.ai_investment,
        s.ai_adoption_rate
    FROM country_trends c
    LEFT JOIN anthropic_economic_index a ON c.country_code = a.country_code
    LEFT JOIN stanford_ai_index s ON c.country_code = s.country_code
""")
```

### Step 5: Update Dashboard
Add new visualizations and metrics to `app.py`:
- New charts showing AI investment trends
- Economic index overlays
- Enhanced country comparisons

---

## Data Mapping

### Country Code Mapping
Ensure consistent country codes across all sources:
- World Bank: ISO 3-letter codes (USA, CHN, IND, etc.)
- Stanford AI Index: May use different codes - map to ISO
- PwC: May use country names - map to ISO codes
- Anthropic: Check dataset documentation for code format

### Industry Mapping
Map industry categories to existing taxonomy:
- Information Technology
- Financial Services
- Manufacturing
- Healthcare
- Education
- Retail
- Telecommunications
- Professional Services

### Skill Type Mapping
Map skill categories:
- AI/ML Engineering
- Data Science
- Software Development
- Cybersecurity
- Cloud Computing
- Digital Marketing
- Data Analytics
- IT Support

---

## Example: Integrating Anthropic EconomicIndex

```python
# In load_data.py

from datasets import load_dataset

def load_anthropic_economic_index():
    """Load Anthropic EconomicIndex dataset from Hugging Face."""
    print("Loading Anthropic EconomicIndex dataset...")
    
    try:
        # Load dataset
        dataset = load_dataset("Anthropic/EconomicIndex", "release_2025_09_15")
        
        # Convert to pandas
        df = dataset['train'].to_pandas()
        
        # Process and clean data
        # Map country codes if needed
        # Align with existing schema
        
        print(f"  Loaded {len(df)} records from Anthropic EconomicIndex")
        return df
        
    except Exception as e:
        print(f"  Error loading Anthropic EconomicIndex: {e}")
        return None

# In create_database() function:
anthropic_df = load_anthropic_economic_index()
if anthropic_df is not None:
    conn.execute("CREATE TABLE anthropic_economic_index AS SELECT * FROM anthropic_df")
```

---

## Data Quality Checks

Before integrating new sources:

1. **Data Validation:**
   - Check for missing values
   - Validate country codes
   - Verify date ranges
   - Check for duplicates

2. **Schema Alignment:**
   - Ensure consistent column names
   - Align data types
   - Map categorical variables

3. **Data Completeness:**
   - Check coverage by country
   - Verify time series continuity
   - Identify gaps

4. **Integration Testing:**
   - Test joins with existing tables
   - Verify aggregated views
   - Check dashboard performance

---

## Next Steps

1. **Priority 1:** Integrate Anthropic EconomicIndex (easiest - direct dataset access)
2. **Priority 2:** Extract and integrate Stanford AI Index public data
3. **Priority 3:** Process PwC AI Jobs Barometer reports
4. **Priority 4:** Integrate Yale and McKinsey research data

---

## Support

For questions about integration:
- Check source documentation
- Review dataset schemas
- Test with sample data first
- Validate against existing data

---

## Last Updated

January 2025

