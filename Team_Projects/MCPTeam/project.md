# Digital/AI Jobs Demand & Supply Dashboard

## Overview

**Team MCPTeam** analyzed digital and AI job demand and supply trends using World Bank data and built an interactive analytical dashboard using Streamlit to visualize where digital/AI job demand and supply are rising or lagging across countries, industries, and skill types. The tool allows users to compare employment trends, identify demand-supply gaps, and track how digital job markets are evolving over time. It helps policymakers, researchers, and stakeholders understand the dynamics of the digital labor market and identify opportunities and challenges in the transition to a digital economy.

## Team Members

- Hussain Adeli
- Nick Wagner
- Maria Alejandra Zegarra


## Challenge Category

**Category V: Toward New Insights on Job Trends**

**Challenge 8**: Demand & supply in digital/AI jobs: understanding supply and demand trends? Build an interactive dashboard showing where digital/AI job demand and supply are rising or lagging across countries, industries, and skill types.

## Project Description

Team MCPTeam built an analytical application using Streamlit to visualize employment trends across different sectors and regions. The tool allows users to compare employment rates, job creation trends, and sector-specific employment data over time.

The world is undergoing a major employment transition: over 1.2 billion youth in developing countries will enter the labor force by 2030, many into economies where work remains largely informal, low-productivity, and vulnerable to disruption. Digitalization offers immense potential to create new and better jobs—expanding access, connectivity, and innovation—but it also poses risks, as technology can displace or transform existing forms of work.

Specifically looking at youth data, the dashboard helps track how youth education levels (15–24) will shift by 2035 across countries and scenarios, and what this implies for future skills, gender gaps, and regional winners & who may fall behind.

The application is designed to be user-friendly, with interactive visualizations that allow users to filter data by country, sector, and time period. It also includes a dashboard that provides key metrics and insights about employment trends.

Our interactive dashboard addresses this challenge by providing:

### Key Features

1. **Country-Level Analysis**
   - Demand and supply trends over time for digital/AI jobs
   - Demand-supply gap visualization
   - Comparison across multiple countries
   - Identification of rising vs. lagging countries

2. **Industry-Level Analysis**
   - Trends across different industries (IT, Financial Services, Healthcare, etc.)
   - Industry-specific demand-supply gaps
   - Identification of industries with the greatest digital job opportunities

3. **Skill Type Analysis**
   - Trends for different digital/AI skill types (AI/ML Engineering, Data Science, Software Development, etc.)
   - Skill-specific demand-supply gaps
   - Identification of skills in highest demand

4. **Rising vs. Lagging Analysis**
   - Comparison of recent trends (2020+) vs. historical data
   - Visual scatter plot showing demand and supply growth rates
   - Classification of countries as "Rising", "Moderate", or "Lagging"
   - Helps identify countries that need targeted interventions

### Technical Implementation

The dashboard is built using:

- **Streamlit**: Interactive web application framework
- **DuckDB**: High-performance analytical database for efficient data querying
- **Altair**: Declarative visualization library for interactive charts
- **Pandas**: Data manipulation and analysis
- **World Bank API**: Real-time data access from World Bank indicators

### Data Sources

The dashboard integrates data from multiple sources:

1. **World Bank Global Jobs Indicators Database**
   - Employment in ICT services (% of total employment)
   - Employment in ICT manufacturing (% of total employment)
   - ICT goods exports/imports

2. **World Bank Global Labor Database (GLD)**
   - Harmonized labor force survey data
   - Employment statistics across countries

3. **ITU ICT Data Hub**
   - Mobile cellular subscriptions
   - Internet users (% of population)
   - Fixed broadband subscriptions

4. **ILO Statistics**
   - International labor organization data
   - Employment and labor market indicators

5. **Data360 Indicators**
   - Digital connectivity metrics
   - Labor force participation data

### Dashboard Components

#### 1. Country Trends View
- Interactive time series charts showing demand and supply trends
- Gap analysis visualization
- Summary metrics for selected countries
- Detailed data tables

#### 2. Industry Trends View
- Industry-specific demand and supply trends
- Latest year comparison across industries
- Summary statistics by industry

#### 3. Skill Trends View
- Skill-specific demand and supply trends
- Identification of high-demand skills
- Gap analysis by skill type

#### 4. Rising vs. Lagging View
- Scatter plot visualization of growth rates
- Classification of countries by trend status
- Detailed analysis table with growth percentages

### Key Insights

The dashboard enables users to:

1. **Identify Opportunities**: Find countries, industries, and skills where digital job demand is growing rapidly
2. **Spot Vulnerabilities**: Identify areas where supply is lagging behind demand, indicating potential skill shortages
3. **Track Progress**: Monitor trends over time to see how digital job markets are evolving
4. **Compare Regions**: Compare digital job trends across different countries and regions
5. **Inform Policy**: Provide data-driven insights for policymakers to target interventions

### Usage Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Load Data**:
   ```bash
   python load_data.py
   ```
   This will:
   - Download data from World Bank API
   - Generate sample digital/AI jobs data
   - Create a DuckDB database with processed data
   - Generate aggregated views for efficient querying

3. **Run Dashboard**:
   ```bash
   streamlit run app.py
   ```

4. **Use the Dashboard**:
   - Select filters in the sidebar (year range, countries, industries, skills)
   - Choose an analysis view (Country, Industry, Skill, or Rising vs. Lagging)
   - Explore interactive visualizations
   - View detailed data tables

### Future Enhancements

Potential improvements for future iterations:

1. **Real-Time Data Integration**: Connect to live job posting APIs (LinkedIn, Indeed, etc.)
2. **Machine Learning Predictions**: Add forecasting models to predict future demand/supply trends
3. **Geographic Mapping**: Add choropleth maps showing trends by country
4. **Export Functionality**: Allow users to export charts and data
5. **Custom Reports**: Generate PDF reports with key findings
6. **API Integration**: Connect to additional data sources (Global Findex, etc.)
7. **User Authentication**: Support for multiple users and saved preferences

### Data Limitations

- Sample data is used for demonstration purposes. In production, this would be replaced with:
  - Real job posting data from APIs
  - Actual GLD harmonized microdata
  - Complete World Bank indicators
  - ILO and ITU datasets

### Links

- **Live Dashboard**: Run `streamlit run app.py` to launch locally
- **Data Sources**: See `load_data.py` for data loading implementation
- **Documentation**: This file (`project.md`)

### Acknowledgments

This project was developed for the World Bank Data Dive 2025, organized by:
- WBG Data Talent Board
- Office of the WBG Chief Statistician & Development Data Group
- WBG Data Technology Office
- Prosperity Vice Presidency's Jobs & Economic Growth Department
- Global Indicators Group (DEC)
- Digital Vice Presidency's Digital Foundations team
- And other contributing organizations

### References

- [World Bank Global Jobs Indicators Database](https://datacatalog.worldbank.org/search/dataset/0037526/Global-Jobs-Indicators-Database)
- [World Bank Open Data](https://data.worldbank.org/)
- [World Bank Global Labor Database](https://worldbank.github.io/gld/)
- [ILO Statistics](https://ilostat.ilo.org/topics/employment/)
- [ITU ICT Data Hub](https://datahub.itu.int/)
- [Global Findex](https://www.worldbank.org/en/publication/globalfindex)

