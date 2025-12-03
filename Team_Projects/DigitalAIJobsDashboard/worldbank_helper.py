#!/usr/bin/env python3
"""
World Bank Data Helper

Alternative methods to fetch World Bank data when API has access issues.
"""

import requests
import pandas as pd
from typing import Dict, Any, Optional


def fetch_world_bank_via_databank(indicator_code: str, country_code: str = "all") -> Dict[str, Any]:
    """
    Alternative method: Provide instructions for manual download from DataBank.
    
    Since the API may have access restrictions, this provides guidance on
    using World Bank DataBank website directly.
    """
    return {
        "method": "manual_download",
        "instructions": f"""
        To get data for indicator {indicator_code}:
        
        1. Visit: https://databank.worldbank.org/
        2. Search for indicator: {indicator_code}
        3. Select countries: {country_code}
        4. Download as CSV
        5. Import into dashboard
        
        Alternative: Use the sample data already loaded in the dashboard.
        """,
        "databank_url": "https://databank.worldbank.org/",
        "indicator_code": indicator_code
    }


def try_world_bank_api_alternative(indicator_code: str, country_code: str = "all", 
                                   start_year: int = 2015, end_year: int = 2024) -> Dict[str, Any]:
    """
    Try alternative World Bank API endpoints or methods.
    """
    # Try different API endpoint formats
    endpoints = [
        f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format=json&date={start_year}:{end_year}&per_page=20000",
        f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format=json&date={start_year}:{end_year}",
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": "https://data.worldbank.org/"
    }
    
    for url in endpoints:
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if len(data) >= 2 and data[1]:
                    records = []
                    for entry in data[1]:
                        records.append({
                            "country_code": entry.get("country", {}).get("id", ""),
                            "country_name": entry.get("country", {}).get("value", ""),
                            "year": entry.get("date", ""),
                            "value": entry.get("value")
                        })
                    
                    df = pd.DataFrame(records)
                    df = df[df["value"].notna()]
                    
                    if not df.empty:
                        return {
                            "success": True,
                            "indicator_code": indicator_code,
                            "records": len(df),
                            "data": df.to_dict('records'),
                            "method": "alternative_endpoint"
                        }
        except Exception:
            continue
    
    return {
        "error": "Unable to fetch data via API",
        "suggestion": "Use World Bank DataBank website for manual download",
        "databank_url": "https://databank.worldbank.org/"
    }

