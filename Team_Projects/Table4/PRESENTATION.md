---
marp: true
theme: default
paginate: true
backgroundColor: #fff
---

<!-- _class: lead -->
# Women in Public Sector Jobs
## Crowding Out or Crowding In?

**Team Table4**
World Bank Data Dive 2025 - Challenge 4

---

## The Research Question

**Does the public sector act as a:**
- 🧲 **Magnet** that drains female talent from the private sector?
- 🚀 **Catalyst** that normalizes female employment and spurs growth?

---

## The Context

Across developing countries, women disproportionately work in the public sector:

- ✅ More predictable wages
- ✅ Better work-family balance  
- ✅ Less discriminatory pay practices
- ✅ Stronger regulatory frameworks

**Result**: Women's public-sector employment shares >> Men's

---

## Two Competing Hypotheses

### H1: Crowding Out (Negative Effect)
- High public wages → Higher reservation wages
- Women "queue" for government jobs
- Private sector faces talent shortage
- **Prediction**: Public sector ↑ → Unemployment ↑

### H2: Crowding In (Positive Effect)
- Visible women in leadership → Norm shifts
- Reduced gender discrimination
- Spillover to private sector
- **Prediction**: Public sector ↑ → FLFP ↑

---

## Our Approach

### Data Sources
1. **World Bank Worldwide Bureaucracy Indicators (WWBI)**
   - Public sector employment share
2. **World Bank WDI - Female Labor Force Participation (FLFP)**
3. **World Bank WDI - Female Unemployment Rate**

### Merged Dataset
- **1,141 observations** across **137 countries**
- Cross-country correlation analysis

---

## Key Finding #1: Crowding Out Test

**Hypothesis**: Public sector ↑ → Unemployment ↑

**Result**: Correlation = **0.253** (Weak Positive)

### Interpretation
- ⚠️ Slight positive correlation exists
- But effect is **weak**, not dominant
- Public sector alone doesn't strongly predict unemployment

---

## Key Finding #2: Crowding In Test

**Hypothesis**: Public sector ↑ → FLFP ↑

**Result**: Correlation = **-0.118** (Weak Negative)

### Interpretation
- ❌ Contrary to hypothesis (negative, not positive)
- Effect is **very weak**
- No evidence of strong spillover effects

---

## Top 10 Countries by Public Sector Share

| Country | Public Sector | FLFP | Unemployment |
|---------|--------------|------|--------------|
| 🇲🇻 Maldives | 47.1% | 41.0% | 3.8% |
| 🇷🇺 Russia | 44.9% | 55.7% | 5.4% |
| 🇩🇯 Djibouti | 42.8% | 18.1% | 36.0% |
| 🇺🇦 Ukraine | 38.7% | 50.9% | 6.2% |
| 🇰🇿 Kazakhstan | 37.2% | 66.7% | 6.6% |

---

## The Surprising Insight

### Similar Public Sector, Different Outcomes

**Norway (32.8% public sector)**
- FLFP: 62.0%
- Unemployment: 4.1%

**Saudi Arabia (32.2% public sector)**
- FLFP: 19.8%
- Unemployment: 23.5%

**→ Context matters more than public sector share!**

---

## Main Conclusions

1. ❌ **Neither crowding out nor crowding in is strongly supported**
   - Both correlations are weak

2. 📊 **Public sector share is a weak predictor**
   - Explains little variation in outcomes

3. 🌍 **Country-specific factors dominate**
   - Culture, economic development, institutions
   - Labor market regulations

---

## Limitations & Future Work

### Limitations
- Cross-sectional analysis (snapshot in time)
- Cannot establish causality
- Missing control variables

### Recommendations
- **Time-series analysis**: Track within-country changes
- **Regional clustering**: Analyze similar economies together
- **Control variables**: GDP, education, regulations

---

## Technical Implementation

### Analysis Pipeline
```python
1. Data acquisition (WWBI, FLFP, Unemployment)
2. Data cleaning and merging
3. Correlation analysis
4. Visualization generation
5. Case study identification
```

### Reproducibility
- All code available on GitHub
- `comprehensive_analysis.py` - Full pipeline
- `README.md` - Reproduction instructions

---

<!-- _class: lead -->
## Key Takeaway

**The relationship between public sector employment and female labor outcomes is complex and context-dependent.**

Public sector policies alone won't solve gender employment gaps—
holistic approaches considering cultural, economic, and institutional factors are essential.

---

<!-- _class: lead -->
# Thank You!

**Team Table4**

GitHub: [nbajpai-code/DataDive25](https://github.com/nbajpai-code/DataDive25/tree/team/Table4)

Questions?
