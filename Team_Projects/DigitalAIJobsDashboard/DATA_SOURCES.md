# Data Sources

This document lists all data sources used in the Digital/AI Jobs Demand & Supply Dashboard.

## Primary Data Sources

### 1. World Bank Global Jobs Indicators Database
**Source:** [World Bank Data Catalog](https://datacatalog.worldbank.org/search/dataset/0037526/Global-Jobs-Indicators-Database)

**Description:** Comprehensive database of job-related indicators across countries.

**Indicators Used:**
- Employment in ICT services (% of total employment) - Indicator Code: `SL.EMP.ICTI.ZS`
- Employment in ICT manufacturing (% of total employment) - Indicator Code: `SL.EMP.ICTM.ZS`

**Access Method:** World Bank API (`https://api.worldbank.org/v2`)

**License:** Public domain / Creative Commons Attribution 4.0

**Status:** ✅ Integrated (via API)

---

### 2. World Bank Global Labor Database (GLD)
**Source:** [World Bank GLD Repository](https://worldbank.github.io/gld/)

**Description:** Harmonized microdata from labor force surveys across multiple countries.

**Data Types:**
- Harmonized labor force survey data
- Employment statistics by country
- Demographic and labor market indicators

**Access Method:** 
- World Bank GLD Server (official use)
- Datalibweb (public access)
- Microdata Library
- GitHub repository

**License:** Varies by survey (Public, Official Use, or Restricted)

**Status:** ⚠️ Sample data used for demonstration (real data requires access permissions)

**Documentation:** [GLD Manual](https://worldbank.github.io/gld/Support/A%20-%20Guides%20and%20Documentation/GLD%20Manual%20Files/GLD%20content%2C%20storage%2C%20and%20access.html)

---

### 3. World Bank Open Data (Data360)
**Source:** [World Bank Open Data](https://data.worldbank.org/)

**Description:** Free and open access to global development data.

**Indicators Used:**
- ICT goods exports (% of total goods exports) - Indicator Code: `TX.VAL.ICTG.ZS.UN`
- ICT goods imports (% of total goods imports) - Indicator Code: `TM.VAL.ICTG.ZS.UN`
- Labor force participation rate, total (% of total population ages 15+)

**Access Method:** World Bank API

**License:** Public domain

**Status:** ✅ Integrated (via API)

**Platform:** [Data360](https://data360.worldbank.org/)

---

### 4. ITU ICT Data Hub
**Source:** [ITU ICT Data Hub](https://datahub.itu.int/)

**Description:** International Telecommunication Union's comprehensive database of ICT statistics.

**Indicators Used:**
- Mobile cellular subscriptions per 100 people - Indicator Code: `IT.CEL.SETS.P2`
- Internet users (% of population) - Indicator Code: `IT.NET.USER.ZS`
- Fixed broadband subscriptions per 100 people - Indicator Code: `IT.NET.BBND.P2`

**Access Method:** World Bank API (ITU indicators available through WB API)

**License:** Public domain

**Status:** ✅ Integrated (via World Bank API)

---

### 5. International Labor Organization (ILO)
**Source:** [ILO Statistics](https://ilostat.ilo.org/topics/employment/)

**Description:** International labor organization statistics on employment and labor markets.

**Data Types:**
- Employment statistics
- Labor market indicators
- Workforce demographics

**Access Method:** ILO API / Web portal

**License:** Public domain (with attribution)

**Status:** ⚠️ Referenced (not directly integrated in current version)

**Note:** ILO data can be integrated via their API or downloaded datasets.

---

### 6. Global Findex Digital Connectivity Tracker
**Source:** [World Bank Global Findex](https://www.worldbank.org/en/publication/globalfindex)

**Description:** Database on how adults in 160+ economies save, borrow, make payments, and manage risk, including digital financial services.

**Relevance:** Digital connectivity and financial inclusion metrics related to digital job opportunities.

**Access Method:** World Bank Global Findex database

**License:** Public domain

**Status:** ⚠️ Referenced (not directly integrated in current version)

---

### 7. Anthropic EconomicIndex Dataset
**Source:** [Hugging Face - Anthropic EconomicIndex](https://huggingface.co/datasets/Anthropic/EconomicIndex/tree/main/release_2025_09_15)

**Description:** Comprehensive dataset tracking economic indicators related to AI and technology impacts on labor markets and economic activity.

**Data Types:**
- Economic indicators related to AI adoption
- Labor market impacts
- Technology sector metrics
- Economic index measurements

**Access Method:** Hugging Face Datasets library / Direct download

**License:** MIT License

**Status:** ⚠️ Available for integration (requires Hugging Face datasets library)

**Documentation:** [Dataset Card](https://huggingface.co/datasets/Anthropic/EconomicIndex)

**Integration Note:** Can be loaded using:
```python
from datasets import load_dataset
dataset = load_dataset("Anthropic/EconomicIndex", "release_2025_09_15")
```

---

### 8. Stanford AI Index Report 2025
**Source:** [Stanford HAI - AI Index Report 2025](https://hai.stanford.edu/ai-index/2025-ai-index-report)

**Description:** Comprehensive annual report tracking AI progress, including research, technical performance, responsible AI, economy, science, policy, education, and public opinion.

**Key Metrics:**
- AI research and development trends
- Technical performance benchmarks
- Private AI investment data
- AI model development statistics
- Labor market impacts
- Public opinion on AI

**Access Method:**
- Public data access via [AI Index Public Data](https://hai.stanford.edu/ai-index/2025-ai-index-report)
- Report downloads (PDF)
- Data visualizations and datasets

**License:** Public domain / Open access

**Status:** ⚠️ Available for integration (data available via public data portal)

**Key Insights Relevant to Dashboard:**
- U.S. private AI investment: $109.1 billion (2024)
- 78% of organizations reported using AI in 2024
- AI boosts productivity and helps narrow skill gaps
- Performance gaps between top AI models shrinking

**Documentation:** [2025 AI Index Report](https://hai.stanford.edu/ai-index/2025-ai-index-report)

---

### 9. PwC AI Jobs Barometer
**Source:** [PwC AI Jobs Barometer](https://www.pwc.com/gx/en/services/ai/ai-jobs-barometer.html)

**Description:** Comprehensive analysis of AI's impact on jobs, tracking job postings, skills demand, and labor market transformations across industries and regions.

**Data Types:**
- AI job posting trends
- Skills demand analysis
- Industry-level job impacts
- Regional variations in AI job markets
- Supply and demand dynamics

**Access Method:**
- Annual reports (PDF downloads)
- 2025 AI Jobs Barometer report
- 2024 AI Jobs Barometer report (historical data)

**License:** PwC proprietary (publicly available reports)

**Status:** ⚠️ Available for integration (via report analysis and data extraction)

**Reports Available:**
- 2025 AI Jobs Barometer (Full report and Executive summary)
- 2024 AI Jobs Barometer (Historical comparison)

**Relevance:** Directly addresses Challenge 8 requirements for understanding digital/AI job demand and supply trends.

---

### 10. Yale Budget Lab - Evaluating Impact of AI on Labor Market
**Source:** [Yale Budget Lab Research](https://budgetlab.yale.edu/research/evaluating-impact-ai-labor-market-current-state-affairs)

**Description:** Research and analysis on the current state of AI's impact on labor markets, including displacement effects, job creation, and workforce transitions.

**Data Types:**
- Labor market impact assessments
- Job displacement analysis
- Workforce transition metrics
- Economic impact evaluations

**Access Method:** Research publications and datasets

**License:** Academic research (check specific publication licenses)

**Status:** ⚠️ Available for integration (via research publications)

**Relevance:** Provides academic perspective on AI labor market impacts, complementing industry and government data sources.

---

### 11. McKinsey - Economic Potential of Generative AI
**Source:** [McKinsey - The Economic Potential of Generative AI](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier)

**Description:** Comprehensive analysis of generative AI's economic potential, productivity impacts, and implications for the future of work across industries.

**Key Insights:**
- Economic value potential of generative AI
- Productivity gains by industry
- Workforce implications
- Skills transformation requirements
- Regional economic impacts

**Access Method:**
- Research reports and articles
- Data visualizations
- Industry-specific analyses

**License:** McKinsey proprietary (publicly available insights)

**Status:** ⚠️ Available for integration (via report analysis and insights extraction)

**Relevance:** Provides strategic insights on generative AI's economic impact, which directly relates to digital/AI job demand forecasting.

**Key Findings:**
- Generative AI could add trillions of dollars in value to global economy
- Significant productivity gains across knowledge work sectors
- Transformation of work activities and required skills

---

## Sample/Demonstration Data

### 12. Generated Sample Data
**Description:** Sample digital/AI jobs data created for demonstration purposes.

**Coverage:**
- 20 countries (USA, CHN, IND, BRA, MEX, IDN, TUR, THA, VNM, PHL, BGD, PAK, NGA, EGY, ZAF, KEN, GHA, ETH, TZA, UGA)
- 8 industries (Information Technology, Financial Services, Manufacturing, Healthcare, Education, Retail, Telecommunications, Professional Services)
- 8 skill types (AI/ML Engineering, Data Science, Software Development, Cybersecurity, Cloud Computing, Digital Marketing, Data Analytics, IT Support)
- Years: 2015-2024

**Purpose:** Demonstrates dashboard functionality when real data sources require authentication or are not yet integrated.

**Status:** ✅ Currently in use (to be replaced with real data sources)

**Note:** In production, this would be replaced with:
- Real job posting APIs (LinkedIn, Indeed, etc.)
- Actual GLD harmonized microdata
- Complete World Bank indicators
- ILO and ITU datasets

---

## Data Access Methods

### World Bank API
**Endpoint:** `https://api.worldbank.org/v2`
**Format:** JSON
**Rate Limits:** Standard API rate limits apply
**Documentation:** [World Bank API Documentation](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation)

### Direct Downloads
Some data sources may require:
- Direct download from data portals
- API authentication
- Registration for restricted datasets

---

## Data Processing

All data is processed and stored in a **DuckDB** database (`digital_jobs.duckdb`) for efficient querying and analysis.

**Database Structure:**
- `wb_indicators`: World Bank indicator data
- `digital_jobs`: Digital/AI jobs data (sample or real)
- `country_trends`: Aggregated country-level trends (view)
- `industry_trends`: Aggregated industry-level trends (view)
- `skill_trends`: Aggregated skill-level trends (view)
- `rising_lagging_countries`: Rising vs lagging analysis (view)

---

## Data Limitations

1. **API Access:** Some World Bank API endpoints may require authentication or have rate limits
2. **Sample Data:** Current implementation uses sample data for demonstration
3. **Coverage:** Not all countries may have complete data for all indicators
4. **Time Periods:** Data availability varies by country and indicator
5. **Real-time Updates:** Data may not be updated in real-time

---

## Future Data Integration

The following data sources are identified and available for integration:

### Priority Integration Sources:

1. **Anthropic EconomicIndex Dataset** (Hugging Face)
   - Ready for integration via Hugging Face datasets library
   - Provides economic indicators related to AI impacts
   - Status: ⚠️ Ready for integration

2. **Stanford AI Index Public Data**
   - Comprehensive AI metrics and trends
   - Investment and adoption data
   - Status: ⚠️ Available via public data portal

3. **PwC AI Jobs Barometer Data**
   - Direct job posting trends
   - Skills demand analysis
   - Status: ⚠️ Requires data extraction from reports

4. **Yale Budget Lab Research Data**
   - Academic research on AI labor impacts
   - Status: ⚠️ Requires data extraction from publications

5. **McKinsey Generative AI Insights**
   - Economic potential analysis
   - Productivity impact data
   - Status: ⚠️ Requires data extraction from reports

### Additional Potential Sources:

1. **Job Posting APIs:**
   - LinkedIn Jobs API
   - Indeed API
   - Glassdoor API
   - Other job board APIs

2. **AI/ML Job Specific Sources:**
   - AI job postings datasets
   - Tech job market reports
   - Skills demand surveys

3. **Satellite Data:**
   - Night-lights data (as mentioned in challenge description)
   - Economic activity indicators

4. **Additional World Bank Sources:**
   - Complete Global Jobs Indicators Database
   - Full GLD harmonized microdata
   - Additional development indicators

---

## Data Attribution

When using this dashboard or its data, please attribute:

- **World Bank:** "Data from The World Bank (https://data.worldbank.org)"
- **ITU:** "Data from International Telecommunication Union (https://datahub.itu.int/)"
- **ILO:** "Data from International Labour Organization (https://ilostat.ilo.org/)"
- **GLD:** "Data from World Bank Global Labor Database (https://worldbank.github.io/gld/)"
- **Anthropic:** "Data from Anthropic EconomicIndex Dataset (https://huggingface.co/datasets/Anthropic/EconomicIndex)"
- **Stanford HAI:** "Data from Stanford AI Index Report 2025 (https://hai.stanford.edu/ai-index/2025-ai-index-report)"
- **PwC:** "Data from PwC AI Jobs Barometer (https://www.pwc.com/gx/en/services/ai/ai-jobs-barometer.html)"
- **Yale Budget Lab:** "Research from Yale Budget Lab (https://budgetlab.yale.edu/research/evaluating-impact-ai-labor-market-current-state-affairs)"
- **McKinsey:** "Insights from McKinsey - Economic Potential of Generative AI (https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier)"

---

## Contact & Support

For questions about data sources:
- **World Bank Data:** data@worldbank.org
- **GLD:** See [GLD Contact](https://worldbank.github.io/gld/)
- **ITU:** Contact via [ITU Data Hub](https://datahub.itu.int/)
- **ILO:** Contact via [ILO Statistics](https://ilostat.ilo.org/)

---

## Last Updated

January 2025

---

## References

1. [World Bank Global Jobs Indicators Database](https://datacatalog.worldbank.org/search/dataset/0037526/Global-Jobs-Indicators-Database)
2. [World Bank Open Data](https://data.worldbank.org/)
3. [World Bank Global Labor Database](https://worldbank.github.io/gld/)
4. [ILO Statistics](https://ilostat.ilo.org/topics/employment/)
5. [ITU ICT Data Hub](https://datahub.itu.int/)
6. [Global Findex](https://www.worldbank.org/en/publication/globalfindex)
7. [World Bank API Documentation](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation)
8. [Anthropic EconomicIndex Dataset](https://huggingface.co/datasets/Anthropic/EconomicIndex/tree/main/release_2025_09_15)
9. [Stanford AI Index Report 2025](https://hai.stanford.edu/ai-index/2025-ai-index-report)
10. [PwC AI Jobs Barometer](https://www.pwc.com/gx/en/services/ai/ai-jobs-barometer.html)
11. [Yale Budget Lab - AI Labor Market Impact](https://budgetlab.yale.edu/research/evaluating-impact-ai-labor-market-current-state-affairs)
12. [McKinsey - Economic Potential of Generative AI](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier)

