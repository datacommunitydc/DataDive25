# Digital Workforce Navigator
Here is the dashboard link:
https://waterinag.github.io/DWN/

Here is the full code:
https://github.com/waterinag/DWN

# README: Data Sources, Indicators, and Methodology

## Overview
This document describes the data sources, indicator definitions, and methodology used to construct the **Supply** and **Demand** indicators for digital infrastructure and digital skills. It is intended to help users understand:

- What each metric represents  
- Where the data comes from  
- How composite indices were computed  
- Assumptions, limitations, and data processing steps  

---

# Indicators

Indicators are grouped into two main categories:

- **Supply** – skills and access  
- **Demand** – network interconnection  

Both categories were converted into composite scores using **Principal Component Analysis (PCA)**.

---

# Supply Indicators

### 1. **Percentage of graduates from STEM programs in tertiary education**
- **Definition:** Share of graduates at ISCED level 5–8 (tertiary education) whose degrees are in science, technology, engineering, and mathematics (STEM).
- **Purpose:** Proxy for the availability of advanced technical skills in the workforce and the pipeline of future talent.

---

### 2. **Percentage of graduates from ICT programs in tertiary education**
- **Definition:** Share of tertiary graduates whose degrees are in information and communication technologies (ICT), including computer science, information systems, and related fields.
- **Purpose:** Proxy for specialized digital skills relevant to software, networking, data, and digital services.

---

### 3. **Number of people with internet connection**
- **Definition:** Count of individuals with internet connectivity (fixed or mobile), measured as total users or active subscriptions.
- **Purpose:** Proxy for digital inclusion and the size of the population that can adopt and benefit from digital services.
- **Notes:**  
  - May be reported as total users, subscriptions, or penetration rates.  
  - Penetration rates were converted into counts where needed.

---

# Demand Indicators

### 1. **Number of connected data centers (PeeringDB)**
- **Definition:** Count of data centers with interconnection facilities and networks, as catalogued by PeeringDB.
- **Purpose:** Proxy for the density and maturity of interconnection infrastructure that supports low-latency, resilient digital services.
- **Source:** PeeringDB (community-maintained database).

---

### 2. **Number of IXPs (Packet Clearing House, PCH)**
- **Definition:** Count of active Internet Exchange Points (IXPs) recorded by PCH.
- **Purpose:** Proxy for the interconnection ecosystem and local traffic exchange capacity.
- **Source:** Packet Clearing House (PCH) IXP directory.

---

# Data Sources

### Tertiary Education Graduates (STEM/ICT)
- **Source type:** National statistical offices, ministries of education, or international education datasets.
- **Notes:**  
  - Standardized classifications such as ISCED were used where possible.  
  - When field mappings differ by country, assumptions were documented.

### Internet Connectivity (Individuals connected)
- **Source type:**  
  - National telecom regulators  
  - ICT household surveys  
  - International communications databases  
- **Notes:**  
  - Clarity on whether the measure reflects users, subscriptions, or households.  
  - Penetration rates multiplied by population to obtain counts.

### Interconnection Infrastructure
- **PeeringDB:** Data center counts & attributes  
- **Packet Clearing House (PCH):** IXP counts & attributes  

---

# Methodology: Principal Component Analysis (PCA)

PCA is applied separately for **Supply** and **Demand** indicators to compute composite indices.

## 1. Preparation
- Harmonize indicator reference years. When reporting years differ, use the nearest available year within a defined window.
- Transform indicators as needed (e.g., percentages to proportions, counts per capita if required).
- Standardize all variables using **z-scores**:  
  \[
  z = \frac{(value - mean)}{standard\ deviation}
  \]

## 2. PCA Computation
- Compute PCA on standardized indicators for each category (Supply / Demand).
- Extract the first principal component if it captures a sufficient share of variance and aligns with theoretical expectations.
- Use component loadings to calculate the composite index scores.

## 3. Interpretation
- **Higher Supply scores** → stronger human capital and digital inclusion.  
- **Higher Demand scores** → more mature interconnection ecosystems.  
- Scores are **relative**, not absolute.

---

# Data Processing & Quality Assurance

### Data Cleaning
- Deduplicate entries.  
- Validate country/geography identifiers.  
- Resolve inconsistencies in field definitions for STEM/ICT.

### Missing Data
- Apply documented imputation rules:
  - Nearest-year substitution  
  - Regional average  
  - Omission if data is missing beyond a threshold  
- Flag imputed values and maintain an audit trail.

### Outliers
- Inspect and validate extreme values.
- Cap to reasonable bounds if justified and documented.

### Versioning
- Track data source versions and extraction dates for reproducibility.

---

# Coverage and Timeframe

### Geographic Coverage
- List included countries/regions and any exclusions due to insufficient data.

### Temporal Coverage
- Specify the reference years used for each indicator.
- Record PCA computation date.

### Update Frequency
- **PeeringDB / PCH:** Periodically updated based on public listings.  
- **Education & Internet Connectivity:** Based on annual or multi-year official statistical releases.  

---

# Limitations

- **Indicator comparability:**  
  Differences in national education classifications may reduce comparability of STEM/ICT data.

- **Connectivity measurement:**  
  Distinctions between user counts and subscriptions require transparent assumptions.

- **Dynamic infrastructure:**  
  Data center and IXP listings change frequently; results reflect a snapshot in time.

- **PCA sensitivity:**  
  Composite scores depend on indicator selection and standardization; interpret as **relative**, not absolute benchmarks.
 

---

**Project Team**
- **Dr. Poolad Karimi**
- **Abdur Rahum Safi**
- **Billy**
- **Willi**
- **Ebad**
- **Aman**
