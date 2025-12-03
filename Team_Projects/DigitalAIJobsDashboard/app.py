#!/usr/bin/env python3
"""
Digital/AI Jobs Demand & Supply Dashboard

Interactive dashboard showing where digital/AI job demand and supply are
rising or lagging across countries, industries, and skill types.

Usage:
    streamlit run app.py

Prerequisites:
    Run load_data.py first to populate the DuckDB database.
"""

import streamlit as st
import duckdb
import altair as alt
import pandas as pd
from pathlib import Path
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# Import MCP client
try:
    from mcp_client import data_fetcher
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    data_fetcher = None

# Configuration
DATA_DIR = Path(__file__).parent / "data"
DB_PATH = DATA_DIR / "digital_jobs.duckdb"

# Page configuration
st.set_page_config(
    page_title="Digital/AI Jobs Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def check_database_exists():
    """Check if the database exists and has data."""
    if not DB_PATH.exists():
        return False
    try:
        conn = duckdb.connect(str(DB_PATH), read_only=True)
        count = conn.execute("SELECT COUNT(*) FROM digital_jobs").fetchone()[0]
        conn.close()
        return count > 0
    except Exception:
        return False


def get_country_trends(selected_countries=None, year_range=None):
    """Get country-level demand and supply trends."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    
    query = "SELECT * FROM country_trends WHERE 1=1"
    
    if selected_countries:
        countries_str = ", ".join([f"'{c}'" for c in selected_countries])
        query += f" AND country_code IN ({countries_str})"
    
    if year_range:
        query += f" AND year >= {year_range[0]} AND year <= {year_range[1]}"
    
    query += " ORDER BY country_code, year"
    
    df = conn.execute(query).df()
    conn.close()
    return df


def get_industry_trends(selected_industries=None, year_range=None, selected_countries=None):
    """Get industry-level demand and supply trends."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    
    # If countries are filtered, query from base table; otherwise use aggregated view
    if selected_countries:
        query = """
            SELECT 
                industry,
                year,
                AVG(demand_index) AS avg_demand,
                AVG(supply_index) AS avg_supply,
                AVG(gap) AS avg_gap,
                COUNT(DISTINCT country_code) AS num_countries
            FROM digital_jobs
            WHERE 1=1
        """
        
        if selected_countries:
            countries_str = ", ".join([f"'{c}'" for c in selected_countries])
            query += f" AND country_code IN ({countries_str})"
        
        if selected_industries:
            industries_str = ", ".join([f"'{i}'" for i in selected_industries])
            query += f" AND industry IN ({industries_str})"
        
        if year_range:
            query += f" AND year >= {year_range[0]} AND year <= {year_range[1]}"
        
        query += """
            GROUP BY industry, year
            ORDER BY industry, year
        """
    else:
        query = "SELECT * FROM industry_trends WHERE 1=1"
        
        if selected_industries:
            industries_str = ", ".join([f"'{i}'" for i in selected_industries])
            query += f" AND industry IN ({industries_str})"
        
        if year_range:
            query += f" AND year >= {year_range[0]} AND year <= {year_range[1]}"
        
        query += " ORDER BY industry, year"
    
    df = conn.execute(query).df()
    conn.close()
    return df


def get_skill_trends(selected_skills=None, year_range=None, selected_countries=None):
    """Get skill-level demand and supply trends."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    
    # If countries are filtered, query from base table; otherwise use aggregated view
    if selected_countries:
        query = """
            SELECT 
                skill_type,
                year,
                AVG(demand_index) AS avg_demand,
                AVG(supply_index) AS avg_supply,
                AVG(gap) AS avg_gap,
                COUNT(DISTINCT country_code) AS num_countries
            FROM digital_jobs
            WHERE 1=1
        """
        
        if selected_countries:
            countries_str = ", ".join([f"'{c}'" for c in selected_countries])
            query += f" AND country_code IN ({countries_str})"
        
        if selected_skills:
            skills_str = ", ".join([f"'{s}'" for s in selected_skills])
            query += f" AND skill_type IN ({skills_str})"
        
        if year_range:
            query += f" AND year >= {year_range[0]} AND year <= {year_range[1]}"
        
        query += """
            GROUP BY skill_type, year
            ORDER BY skill_type, year
        """
    else:
        query = "SELECT * FROM skill_trends WHERE 1=1"
        
        if selected_skills:
            skills_str = ", ".join([f"'{s}'" for s in selected_skills])
            query += f" AND skill_type IN ({skills_str})"
        
        if year_range:
            query += f" AND year >= {year_range[0]} AND year <= {year_range[1]}"
        
        query += " ORDER BY skill_type, year"
    
    df = conn.execute(query).df()
    conn.close()
    return df


def get_rising_lagging_analysis(selected_countries=None):
    """Get rising/lagging country analysis."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    
    query = "SELECT * FROM rising_lagging_countries WHERE 1=1"
    
    if selected_countries:
        countries_str = ", ".join([f"'{c}'" for c in selected_countries])
        query += f" AND country_code IN ({countries_str})"
    
    query += " ORDER BY demand_growth_pct DESC"
    
    df = conn.execute(query).df()
    conn.close()
    return df


def get_industry_trends_by_country(selected_industries=None, year_range=None, selected_countries=None):
    """Get industry-level trends broken down by country."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    
    query = """
        SELECT 
            country_code,
            country_name,
            industry,
            year,
            AVG(demand_index) AS avg_demand,
            AVG(supply_index) AS avg_supply,
            AVG(gap) AS avg_gap
        FROM digital_jobs
        WHERE 1=1
    """
    
    if selected_countries:
        countries_str = ", ".join([f"'{c}'" for c in selected_countries])
        query += f" AND country_code IN ({countries_str})"
    
    if selected_industries:
        industries_str = ", ".join([f"'{i}'" for i in selected_industries])
        query += f" AND industry IN ({industries_str})"
    
    if year_range:
        query += f" AND year >= {year_range[0]} AND year <= {year_range[1]}"
    
    query += """
        GROUP BY country_code, country_name, industry, year
        ORDER BY country_code, industry, year
    """
    
    df = conn.execute(query).df()
    conn.close()
    return df


def get_skill_trends_by_country(selected_skills=None, year_range=None, selected_countries=None):
    """Get skill-level trends broken down by country."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    
    query = """
        SELECT 
            country_code,
            country_name,
            skill_type,
            year,
            AVG(demand_index) AS avg_demand,
            AVG(supply_index) AS avg_supply,
            AVG(gap) AS avg_gap
        FROM digital_jobs
        WHERE 1=1
    """
    
    if selected_countries:
        countries_str = ", ".join([f"'{c}'" for c in selected_countries])
        query += f" AND country_code IN ({countries_str})"
    
    if selected_skills:
        skills_str = ", ".join([f"'{s}'" for s in selected_skills])
        query += f" AND skill_type IN ({skills_str})"
    
    if year_range:
        query += f" AND year >= {year_range[0]} AND year <= {year_range[1]}"
    
    query += """
        GROUP BY country_code, country_name, skill_type, year
        ORDER BY country_code, skill_type, year
    """
    
    df = conn.execute(query).df()
    conn.close()
    return df


def get_available_countries():
    """Get list of available countries."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    countries = conn.execute("""
        SELECT DISTINCT country_code, country_name 
        FROM digital_jobs 
        ORDER BY country_name
    """).fetchall()
    conn.close()
    return [(c[0], c[1]) for c in countries]


def get_available_industries():
    """Get list of available industries."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    industries = conn.execute("""
        SELECT DISTINCT industry 
        FROM digital_jobs 
        ORDER BY industry
    """).fetchall()
    conn.close()
    return [i[0] for i in industries]


def get_available_skills():
    """Get list of available skill types."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    skills = conn.execute("""
        SELECT DISTINCT skill_type 
        FROM digital_jobs 
        ORDER BY skill_type
    """).fetchall()
    conn.close()
    return [s[0] for s in skills]


def get_year_range():
    """Get the min and max years from the database."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    result = conn.execute("SELECT MIN(year), MAX(year) FROM digital_jobs").fetchone()
    conn.close()
    return int(result[0]), int(result[1])


def forecast_trends(df, x_col, color_col, forecast_years=5):
    """
    Forecast demand and supply trends for the next N years using linear regression.

    Args:
        df: DataFrame with historical data
        x_col: Column name for x-axis (typically 'year')
        color_col: Column name for grouping (typically 'country_name')
        forecast_years: Number of years to forecast

    Returns:
        DataFrame with forecast data
    """
    forecast_data = []
    max_year = df[x_col].max()

    for group_value in df[color_col].unique():
        group_df = df[df[color_col] == group_value].copy()
        group_df = group_df.sort_values(x_col)

        if len(group_df) < 2:
            continue

        # Prepare data for regression
        X = group_df[[x_col]].values
        y_demand = group_df['avg_demand'].values
        y_supply = group_df['avg_supply'].values

        # Fit linear regression models
        model_demand = LinearRegression()
        model_supply = LinearRegression()

        try:
            model_demand.fit(X, y_demand)
            model_supply.fit(X, y_supply)

            # Generate forecast years
            future_years = np.arange(max_year + 1, max_year + forecast_years + 1).reshape(-1, 1)

            # Predict
            pred_demand = model_demand.predict(future_years)
            pred_supply = model_supply.predict(future_years)

            # Create forecast dataframe
            for i, year in enumerate(future_years.flatten()):
                forecast_data.append({
                    x_col: int(year),
                    color_col: group_value,
                    'avg_demand': max(0, pred_demand[i]),  # Ensure non-negative
                    'avg_supply': max(0, pred_supply[i]),
                    'is_forecast': True
                })
        except:
            # Skip if regression fails
            continue

    return pd.DataFrame(forecast_data)


def create_demand_supply_chart(df, x_col, color_col, title, include_forecast=False):
    """Create a dual-axis chart showing demand and supply trends with optional forecast."""
    # Prepare historical data for Altair
    df_historical = df.copy()
    if 'is_forecast' not in df_historical.columns:
        df_historical['is_forecast'] = False

    # Add forecast if requested
    if include_forecast:
        try:
            forecast_df = forecast_trends(df, x_col, color_col, forecast_years=5)
            if not forecast_df.empty:
                # Combine historical and forecast
                df_combined = pd.concat([df_historical, forecast_df], ignore_index=True)
            else:
                df_combined = df_historical
        except:
            df_combined = df_historical
    else:
        df_combined = df_historical

    # Melt data for Altair
    df_melted = df_combined.melt(
        id_vars=[x_col, color_col, 'is_forecast'],
        value_vars=['avg_demand', 'avg_supply'],
        var_name='metric',
        value_name='value'
    )
    
    # Map metric names
    df_melted['metric'] = df_melted['metric'].map({
        'avg_demand': 'Demand',
        'avg_supply': 'Supply'
    })
    
    # Create data type indicator
    df_melted['data_type'] = df_melted['is_forecast'].map({
        True: 'Forecast',
        False: 'Historical'
    })

    # Separate historical and forecast data
    historical_data = df_melted[~df_melted['is_forecast']]
    forecast_data = df_melted[df_melted['is_forecast']]

    # Create base chart for historical data
    base = alt.Chart(historical_data).encode(
        x=alt.X(f'{x_col}:O', title=x_col.replace('_', ' ').title()),
        y=alt.Y('value:Q', title='Index Value', scale=alt.Scale(zero=False)),
        color=alt.Color('metric:N',
                       scale=alt.Scale(domain=['Demand', 'Supply'],
                                      range=['#1f77b4', '#ff7f0e']),
                       title='Metric'),
        strokeDash=alt.StrokeDash('metric:N',
                                 scale=alt.Scale(domain=['Demand', 'Supply'],
                                                range=[[0], [5, 5]])),
        tooltip=[
            alt.Tooltip(f'{x_col}:N', title=x_col.replace('_', ' ').title()),
            alt.Tooltip('metric:N', title='Metric'),
            alt.Tooltip('value:Q', title='Value', format='.1f'),
            alt.Tooltip('data_type:N', title='Type')
        ]
    )

    # Historical lines with points
    historical_chart = base.mark_line(point=True, strokeWidth=2)

    # Forecast lines (dashed, lighter)
    forecast_chart = None
    if not forecast_data.empty:
        forecast_base = alt.Chart(forecast_data).encode(
            x=alt.X(f'{x_col}:O', title=x_col.replace('_', ' ').title()),
            y=alt.Y('value:Q', title='Index Value', scale=alt.Scale(zero=False)),
            color=alt.Color('metric:N',
                           scale=alt.Scale(domain=['Demand', 'Supply'],
                                          range=['#1f77b4', '#ff7f0e']),
                           title='Metric'),
            strokeDash=alt.StrokeDash('metric:N',
                                     scale=alt.Scale(domain=['Demand', 'Supply'],
                                                    range=[[0], [5, 5]])),
            strokeOpacity=alt.value(0.5),
            tooltip=[
                alt.Tooltip(f'{x_col}:N', title=x_col.replace('_', ' ').title()),
                alt.Tooltip('metric:N', title='Metric'),
                alt.Tooltip('value:Q', title='Forecast', format='.1f'),
                alt.Tooltip('data_type:N', title='Type')
            ]
        )
        forecast_chart = forecast_base.mark_line(point=True, strokeWidth=2, strokeDash=[5, 5], opacity=0.6)

    # Combine charts
    if forecast_chart and not forecast_data.empty:
        # Add vertical line to separate historical from forecast
        max_historical_year = historical_data[x_col].max()
        separator_line = alt.Chart(pd.DataFrame({x_col: [max_historical_year + 0.5]})).mark_rule(
            strokeDash=[3, 3],
            strokeWidth=2,
            color='gray',
            opacity=0.5
        ).encode(
            x=alt.X(f'{x_col}:O')
        )

        chart = (historical_chart + forecast_chart + separator_line).properties(
            height=400,
            title=title + " (with 5-year forecast)"
        ).interactive()

        # Add legend note
        chart = chart.resolve_scale(
            strokeDash='independent'
        )
    else:
        chart = historical_chart.properties(
            height=400,
            title=title
        ).interactive()

    return chart


def create_gap_chart(df, x_col, color_col, title):
    """Create a chart showing the demand-supply gap."""
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f'{x_col}:O', title=x_col.replace('_', ' ').title()),
        y=alt.Y('avg_gap:Q', title='Demand-Supply Gap'),
        color=alt.Color('avg_gap:Q', 
                       scale=alt.Scale(scheme='redyellowgreen', 
                                      domainMid=0),
                       title='Gap'),
        tooltip=[
            alt.Tooltip(f'{x_col}:N', title=x_col.replace('_', ' ').title()),
            alt.Tooltip('avg_gap:Q', title='Gap', format='.1f')
        ]
    ).properties(
        height=400,
        title=title
    ).interactive()
    
    return chart


def create_rising_lagging_map(df):
    """Create visualization of rising vs lagging countries."""
    chart = alt.Chart(df).mark_circle(size=200).encode(
        x=alt.X('demand_growth_pct:Q', 
               title='Demand Growth (%)',
               scale=alt.Scale(domain=[-50, 150])),
        y=alt.Y('supply_growth_pct:Q', 
               title='Supply Growth (%)',
               scale=alt.Scale(domain=[-50, 150])),
        color=alt.Color('trend_status:N',
                       scale=alt.Scale(domain=['Rising', 'Moderate', 'Lagging'],
                                      range=['#2ecc71', '#f39c12', '#e74c3c']),
                       title='Status'),
        size=alt.Size('recent_demand:Q', title='Recent Demand'),
        tooltip=[
            alt.Tooltip('country_name:N', title='Country'),
            alt.Tooltip('demand_growth_pct:Q', title='Demand Growth %', format='.1f'),
            alt.Tooltip('supply_growth_pct:Q', title='Supply Growth %', format='.1f'),
            alt.Tooltip('trend_status:N', title='Status')
        ]
    ).properties(
        height=500,
        title='Rising vs Lagging Countries: Demand & Supply Growth'
    ).interactive()
    
    # Add quadrant lines
    hline = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(strokeDash=[5, 5]).encode(y='y:Q')
    vline = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(strokeDash=[5, 5]).encode(x='x:Q')
    
    return hline + vline + chart


def get_country_iso3_mapping():
    """Map country codes to ISO-3 codes for plotly maps."""
    return {
        "USA": "USA", "CHN": "CHN", "IND": "IND", "BRA": "BRA",
        "MEX": "MEX", "IDN": "IDN", "TUR": "TUR", "THA": "THA",
        "VNM": "VNM", "PHL": "PHL", "BGD": "BGD", "PAK": "PAK",
        "NGA": "NGA", "EGY": "EGY", "ZAF": "ZAF", "KEN": "KEN",
        "GHA": "GHA", "ETH": "ETH", "TZA": "TZA", "UGA": "UGA"
    }


def create_choropleth_map(df, value_col, title, color_scale="Viridis", reverse=False, selected_countries=None):
    """Create an enhanced choropleth map styled like Anthropic Economic Index."""
    # Map country codes to ISO-3
    iso_mapping = get_country_iso3_mapping()
    df = df.copy()
    df['iso_alpha'] = df['country_code'].map(iso_mapping)
    
    # Filter to only selected countries if provided
    if selected_countries:
        df = df[df['country_code'].isin(selected_countries)]
    
    # Remove rows without ISO mapping
    df = df[df['iso_alpha'].notna()]
    
    if df.empty:
        return None
    
    # Create enhanced color scales (more like Anthropic's style)
    if color_scale == "Gap":
        # Red-Yellow-Green diverging scale
        colorscale = [
            [0, '#d73027'],      # Red (negative gap)
            [0.25, '#f46d43'],   # Orange-red
            [0.5, '#fee08b'],    # Yellow (neutral)
            [0.75, '#abdda4'],   # Light green
            [1, '#3288bd']       # Blue (positive gap)
        ]
    elif reverse:
        colorscale = "Blues_r"
    else:
        # Modern blue-green scale similar to Anthropic
        colorscale = [
            [0, '#e8f4f8'],      # Very light blue
            [0.2, '#c6e5e8'],    # Light blue
            [0.4, '#9dd3d8'],    # Medium blue
            [0.6, '#6bb6c1'],    # Blue-green
            [0.8, '#3a9ab0'],    # Dark blue-green
            [1, '#1a7a8f']       # Dark blue
        ]
    
    # Calculate min/max for better color distribution
    min_val = df[value_col].min()
    max_val = df[value_col].max()
    
    # Create enhanced map
    fig = go.Figure()
    
    # Add choropleth trace with enhanced styling
    fig.add_trace(go.Choropleth(
        locations=df['iso_alpha'],
        z=df[value_col],
        text=df['country_name'],
        colorscale=colorscale,
        showscale=True,
        colorbar=dict(
            title=dict(
                text=value_col.replace('_', ' ').title(),
                font=dict(size=12, color='#333333')
            ),
            thickness=20,
            len=0.6,
            x=1.02,
            xanchor='left',
            yanchor='middle',
            tickfont=dict(size=10, color='#666666'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#e0e0e0',
            borderwidth=1
        ),
        hovertemplate='<b>%{text}</b><br>' +
                      f'{value_col.replace("_", " ").title()}: %{{z:,.1f}}<br>' +
                      '<extra></extra>',
        marker=dict(
            line=dict(
                width=0.5,
                color='rgba(255,255,255,0.8)'
            )
        ),
        zmin=min_val,
        zmax=max_val
    ))
    
    # Enhanced layout styling (inspired by Anthropic Economic Index)
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color='#1a1a1a', family='Arial, sans-serif'),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        height=600,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor='rgba(200,200,200,0.3)',
            showland=True,
            landcolor='rgba(250,250,250,1)',
            showocean=True,
            oceancolor='rgba(240,248,255,1)',
            showlakes=True,
            lakecolor='rgba(240,248,255,1)',
            projection_type='natural earth',
            projection=dict(
                scale=1.1
            ),
            bgcolor='rgba(255,255,255,0)',
            lonaxis=dict(showgrid=False),
            lataxis=dict(showgrid=False)
        ),
        margin=dict(l=0, r=0, t=80, b=0),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family='Arial, sans-serif', color='#333333')
    )
    
    return fig


def create_country_map_data(selected_countries=None, year_range=None, metric='avg_gap'):
    """Get country-level data for mapping."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    
    # Get latest year data or average across year range
    query = f"""
        SELECT 
            country_code,
            country_name,
            AVG({metric}) AS value
        FROM country_trends
        WHERE 1=1
    """
    
    if selected_countries:
        countries_str = ", ".join([f"'{c}'" for c in selected_countries])
        query += f" AND country_code IN ({countries_str})"
    
    if year_range:
        query += f" AND year >= {year_range[0]} AND year <= {year_range[1]}"
    
    query += """
        GROUP BY country_code, country_name
        ORDER BY value DESC
    """
    
    df = conn.execute(query).df()
    conn.close()
    
    if metric == 'avg_gap':
        df.rename(columns={'value': 'avg_gap'}, inplace=True)
    elif metric == 'avg_demand':
        df.rename(columns={'value': 'avg_demand'}, inplace=True)
    elif metric == 'avg_supply':
        df.rename(columns={'value': 'avg_supply'}, inplace=True)
    
    return df


def show_data_source_footer(sources=None, additional_info=""):
    """Display a footer indicating data sources for visualizations."""
    default_sources = [
        "World Bank Global Jobs Indicators Database",
        "World Bank Global Labor Database (GLD)",
        "ITU ICT Data Hub",
        "ILO Statistics",
        "Data360 Indicators"
    ]

    sources_to_show = sources if sources else default_sources

    footer_text = "**Data Sources:** " + " | ".join(sources_to_show)
    if additional_info:
        footer_text += f" | {additional_info}"

    st.caption(footer_text)


def main():
    """Main Streamlit app."""
    # Header
    st.title("🤖 Digital/AI Jobs: Demand & Supply Dashboard")
    st.markdown("""
    **Challenge 8**: Understanding supply and demand trends for digital/AI jobs across countries, 
    industries, and skill types. Identify where demand and supply are rising or lagging.
    """)
    
    # Check if database exists
    if not check_database_exists():
        st.error("⚠️ Database not found! Please run `python load_data.py` first to download and prepare the data.")
        st.code("python load_data.py", language="bash")
        return
    
    # Sidebar filters
    st.sidebar.header("🔧 Filters")
    
    # Get available options
    countries = get_available_countries()
    industries = get_available_industries()
    skills = get_available_skills()
    min_year, max_year = get_year_range()
    
    # Country filter (global - applies to all views)
    selected_country_codes = st.sidebar.multiselect(
        "Select Countries",
        options=[c[0] for c in countries],
        default=[c[0] for c in countries],  # Default to all countries
        format_func=lambda x: next((c[1] for c in countries if c[0] == x), x),
        help="Filter data by selected countries (applies to all views)"
    )
    
    # Year range filter
    year_range = st.sidebar.slider(
        "Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        help="Filter data by year range"
    )
    
    # Clear filters button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Clear All Filters", use_container_width=True, type="secondary"):
        st.session_state.clear()
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Analysis view selector
    view_options = ["Country Trends", "Industry Trends", "Skill Trends", "Rising vs Lagging"]
    if MCP_AVAILABLE:
        view_options.append("MCP Server")

    view = st.sidebar.radio(
        "Analysis View",
        view_options,
        help="Select the type of analysis to display"
    )
    
    # Main content area
    # Show warning if no countries selected
    if not selected_country_codes:
        st.warning("⚠️ Please select at least one country from the sidebar filters to view data.")
    
    if view == "Country Trends":
        st.header("📊 Country-Level Trends")
        
        if selected_country_codes:
            country_df = get_country_trends(selected_country_codes, year_range)
            
            if not country_df.empty:
                # Demand vs Supply chart
                col1, col2 = st.columns(2)
                
                with col1:
                    # Toggle for forecast
                    show_forecast = st.checkbox("📈 Show 5-Year Forecast", value=True, key="country_forecast")

                    chart = create_demand_supply_chart(
                        country_df,
                        'year',
                        'country_name',
                        'Demand vs Supply Trends by Country',
                        include_forecast=show_forecast
                    )
                    st.altair_chart(chart, use_container_width=True)
                    if show_forecast:
                        st.caption("💡 Forecast based on linear trend projection from historical data")
                    show_data_source_footer()
                
                with col2:
                    gap_chart = create_gap_chart(
                        country_df.groupby(['country_name', 'year'])['avg_gap'].mean().reset_index(),
                        'year',
                        'country_name',
                        'Demand-Supply Gap Over Time'
                    )
                    st.altair_chart(gap_chart, use_container_width=True)
                    show_data_source_footer()
                
                # Summary metrics
                st.subheader("📈 Summary Metrics")
                recent_data = country_df[country_df['year'] >= year_range[1] - 2]
                if not recent_data.empty:
                    cols = st.columns(min(len(selected_country_codes), 5))
                    for i, country_code in enumerate(selected_country_codes[:5]):
                        country_data = recent_data[recent_data['country_code'] == country_code]
                        if not country_data.empty:
                            with cols[i % len(cols)]:
                                country_name = country_data.iloc[0]['country_name']
                                avg_demand = country_data['avg_demand'].mean()
                                avg_supply = country_data['avg_supply'].mean()
                                gap = avg_demand - avg_supply
                                
                                st.metric(
                                    label=country_name,
                                    value=f"{gap:.1f}",
                                    delta=f"D: {avg_demand:.1f}, S: {avg_supply:.1f}",
                                    help=f"Gap = Demand - Supply"
                                )
                
                # Map visualizations
                st.subheader("🗺️ Geographic Distribution")
                st.caption(f"Showing data for {len(selected_country_codes)} selected countries ({year_range[0]}-{year_range[1]})")
                
                # Get latest year data for mapping
                latest_year = country_df['year'].max()
                map_data = create_country_map_data(selected_country_codes, year_range, 'avg_gap')
                
                if not map_data.empty:
                    # Map metric selector
                    map_metric = st.radio(
                        "Map Metric",
                        ["Demand-Supply Gap", "Demand", "Supply"],
                        horizontal=True,
                        key="map_metric"
                    )
                    
                    if map_metric == "Demand-Supply Gap":
                        map_df = create_country_map_data(selected_country_codes, year_range, 'avg_gap')
                        value_col = 'avg_gap'
                        title = f'Digital/AI Jobs: Demand-Supply Gap by Country ({year_range[0]}-{year_range[1]})'
                        color_scale = "Gap"
                    elif map_metric == "Demand":
                        map_df = create_country_map_data(selected_country_codes, year_range, 'avg_demand')
                        value_col = 'avg_demand'
                        title = f'Digital/AI Jobs: Demand Index by Country ({year_range[0]}-{year_range[1]})'
                        color_scale = "Viridis"
                    else:  # Supply
                        map_df = create_country_map_data(selected_country_codes, year_range, 'avg_supply')
                        value_col = 'avg_supply'
                        title = f'Digital/AI Jobs: Supply Index by Country ({year_range[0]}-{year_range[1]})'
                        color_scale = "Viridis"
                    
                    if not map_df.empty:
                        fig = create_choropleth_map(map_df, value_col, title, color_scale, selected_countries=selected_country_codes)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                            show_data_source_footer()
                
                # Data table
                with st.expander("📋 View Detailed Data"):
                    st.dataframe(
                        country_df[['country_name', 'year', 'avg_demand', 'avg_supply', 'avg_gap']].rename(columns={
                            'country_name': 'Country',
                            'year': 'Year',
                            'avg_demand': 'Avg Demand',
                            'avg_supply': 'Avg Supply',
                            'avg_gap': 'Gap'
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
            else:
                st.warning("No data available for selected filters.")
    
    elif view == "Industry Trends":
        st.header("🏭 Industry-Level Trends")
        if selected_country_codes:
            country_names = [next((c[1] for c in countries if c[0] == code), code) for code in selected_country_codes]
            st.caption(f"📌 Showing data for {len(selected_country_codes)} selected countries: {', '.join(country_names[:5])}{'...' if len(country_names) > 5 else ''} ({year_range[0]}-{year_range[1]})")
        
        # Industry filter
        selected_industries = st.multiselect(
            "Select Industries",
            options=industries,
            default=industries[:4]
        )
        
        if selected_industries:
            industry_df = get_industry_trends(selected_industries, year_range, selected_country_codes)
            industry_by_country_df = get_industry_trends_by_country(selected_industries, year_range, selected_country_codes)
            
            if not industry_df.empty:
                # Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    chart = create_demand_supply_chart(
                        industry_df,
                        'year',
                        'industry',
                        'Demand vs Supply by Industry (Aggregated)'
                    )
                    st.altair_chart(chart, use_container_width=True)
                    show_data_source_footer()

                with col2:
                    # Latest year comparison
                    latest_year = industry_df['year'].max()
                    latest_data = industry_df[industry_df['year'] == latest_year]
                    
                    bar_chart = alt.Chart(latest_data).mark_bar().encode(
                        x=alt.X('industry:N', title='Industry'),
                        y=alt.Y('avg_gap:Q', title='Gap'),
                        color=alt.Color('avg_gap:Q', 
                                       scale=alt.Scale(scheme='redyellowgreen', domainMid=0)),
                        tooltip=['industry:N', 'avg_gap:Q']
                    ).properties(
                        height=400,
                        title=f'Demand-Supply Gap by Industry ({int(latest_year)})'
                    )
                    st.altair_chart(bar_chart, use_container_width=True)
                    show_data_source_footer()

                # Country breakdown by industry
                if not industry_by_country_df.empty:
                    st.subheader("📊 Industry Trends by Selected Countries")
                    
                    # Latest year data by country and industry
                    latest_year = industry_by_country_df['year'].max()
                    latest_by_country = industry_by_country_df[industry_by_country_df['year'] == latest_year]
                    
                    # Create a heatmap or grouped bar chart showing countries vs industries
                    heatmap_data = latest_by_country.pivot_table(
                        index='country_name',
                        columns='industry',
                        values='avg_gap',
                        aggfunc='mean'
                    )
                    
                    # Create grouped bar chart
                    grouped_chart = alt.Chart(latest_by_country).mark_bar().encode(
                        x=alt.X('country_name:N', title='Country', sort='-y'),
                        y=alt.Y('avg_gap:Q', title='Demand-Supply Gap'),
                        color=alt.Color('industry:N', title='Industry'),
                        tooltip=['country_name:N', 'industry:N', 'avg_gap:Q']
                    ).properties(
                        height=400,
                        title=f'Gap by Country and Industry ({int(latest_year)})'
                    )
                    st.altair_chart(grouped_chart, use_container_width=True)
                    show_data_source_footer()

                    # Show country breakdown table
                    with st.expander("📋 View Country-Industry Breakdown"):
                        display_df = latest_by_country[['country_name', 'industry', 'avg_demand', 'avg_supply', 'avg_gap']].rename(columns={
                            'country_name': 'Country',
                            'industry': 'Industry',
                            'avg_demand': 'Avg Demand',
                            'avg_supply': 'Avg Supply',
                            'avg_gap': 'Gap'
                        })
                        st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # Summary table
                with st.expander("📋 View Industry Summary (Aggregated)"):
                    summary = industry_df.groupby('industry').agg({
                        'avg_demand': 'mean',
                        'avg_supply': 'mean',
                        'avg_gap': 'mean'
                    }).reset_index()
                    summary.columns = ['Industry', 'Avg Demand', 'Avg Supply', 'Avg Gap']
                    st.dataframe(summary, use_container_width=True, hide_index=True)
    
    elif view == "Skill Trends":
        st.header("🎯 Skill Type Trends")
        if selected_country_codes:
            country_names = [next((c[1] for c in countries if c[0] == code), code) for code in selected_country_codes]
            st.caption(f"📌 Showing data for {len(selected_country_codes)} selected countries: {', '.join(country_names[:5])}{'...' if len(country_names) > 5 else ''} ({year_range[0]}-{year_range[1]})")
        
        # Skill filter
        selected_skills = st.multiselect(
            "Select Skill Types",
            options=skills,
            default=skills[:4]
        )
        
        if selected_skills:
            skill_df = get_skill_trends(selected_skills, year_range, selected_country_codes)
            skill_by_country_df = get_skill_trends_by_country(selected_skills, year_range, selected_country_codes)
            
            if not skill_df.empty:
                # Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    chart = create_demand_supply_chart(
                        skill_df,
                        'year',
                        'skill_type',
                        'Demand vs Supply by Skill Type (Aggregated)'
                    )
                    st.altair_chart(chart, use_container_width=True)
                    show_data_source_footer()

                with col2:
                    # Latest year comparison
                    latest_year = skill_df['year'].max()
                    latest_data = skill_df[skill_df['year'] == latest_year]

                    bar_chart = alt.Chart(latest_data).mark_bar().encode(
                        x=alt.X('skill_type:N', title='Skill Type'),
                        y=alt.Y('avg_gap:Q', title='Gap'),
                        color=alt.Color('avg_gap:Q',
                                       scale=alt.Scale(scheme='redyellowgreen', domainMid=0)),
                        tooltip=['skill_type:N', 'avg_gap:Q']
                    ).properties(
                        height=400,
                        title=f'Demand-Supply Gap by Skill ({int(latest_year)})'
                    )
                    st.altair_chart(bar_chart, use_container_width=True)
                    show_data_source_footer()

                # Country breakdown by skill
                if not skill_by_country_df.empty:
                    st.subheader("📊 Skill Trends by Selected Countries")
                    
                    # Latest year data by country and skill
                    latest_year = skill_by_country_df['year'].max()
                    latest_by_country = skill_by_country_df[skill_by_country_df['year'] == latest_year]
                    
                    # Create grouped bar chart showing countries vs skills
                    grouped_chart = alt.Chart(latest_by_country).mark_bar().encode(
                        x=alt.X('country_name:N', title='Country', sort='-y'),
                        y=alt.Y('avg_gap:Q', title='Demand-Supply Gap'),
                        color=alt.Color('skill_type:N', title='Skill Type'),
                        tooltip=['country_name:N', 'skill_type:N', 'avg_gap:Q']
                    ).properties(
                        height=400,
                        title=f'Gap by Country and Skill Type ({int(latest_year)})'
                    )
                    st.altair_chart(grouped_chart, use_container_width=True)
                    show_data_source_footer()

                    # Show country breakdown table
                    with st.expander("📋 View Country-Skill Breakdown"):
                        display_df = latest_by_country[['country_name', 'skill_type', 'avg_demand', 'avg_supply', 'avg_gap']].rename(columns={
                            'country_name': 'Country',
                            'skill_type': 'Skill Type',
                            'avg_demand': 'Avg Demand',
                            'avg_supply': 'Avg Supply',
                            'avg_gap': 'Gap'
                        })
                        st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # Summary table
                with st.expander("📋 View Skill Summary (Aggregated)"):
                    summary = skill_df.groupby('skill_type').agg({
                        'avg_demand': 'mean',
                        'avg_supply': 'mean',
                        'avg_gap': 'mean'
                    }).reset_index()
                    summary.columns = ['Skill Type', 'Avg Demand', 'Avg Supply', 'Avg Gap']
                    st.dataframe(summary, use_container_width=True, hide_index=True)
    
    elif view == "Rising vs Lagging":
        st.header("📈 Rising vs Lagging Analysis")
        if selected_country_codes:
            country_names = [next((c[1] for c in countries if c[0] == code), code) for code in selected_country_codes]
            st.caption(f"📌 Showing analysis for {len(selected_country_codes)} selected countries: {', '.join(country_names[:5])}{'...' if len(country_names) > 5 else ''}")
        st.markdown("""
        This analysis compares recent trends (2020+) with historical data (pre-2020) 
        to identify countries where digital/AI job demand and supply are rising or lagging.
        """)
        
        rising_lagging_df = get_rising_lagging_analysis(selected_country_codes)
        
        if not rising_lagging_df.empty:
            # Show selected countries list
            if selected_country_codes:
                st.info(f"**Selected Countries:** {', '.join([next((c[1] for c in countries if c[0] == code), code) for code in selected_country_codes])}")
            # Scatter plot
            st.subheader("Growth Comparison")
            chart = create_rising_lagging_map(rising_lagging_df)
            st.altair_chart(chart, use_container_width=True)
            show_data_source_footer()

            # Map visualization
            st.subheader("🗺️ Geographic Distribution of Rising vs Lagging Countries")
            
            # Prepare data for map
            map_df = rising_lagging_df.copy()
            iso_mapping = get_country_iso3_mapping()
            map_df['iso_alpha'] = map_df['country_code'].map(iso_mapping)
            map_df = map_df[map_df['iso_alpha'].notna()]
            
            if not map_df.empty:
                # Create map with trend status
                fig = px.choropleth(
                    map_df,
                    locations='iso_alpha',
                    color='trend_status',
                    hover_name='country_name',
                    hover_data={
                        'iso_alpha': False,
                        'trend_status': True,
                        'demand_growth_pct': ':.1f',
                        'supply_growth_pct': ':.1f'
                    },
                    color_discrete_map={
                        'Rising': '#2ecc71',
                        'Moderate': '#f39c12',
                        'Lagging': '#e74c3c'
                    },
                    title='Rising vs Lagging Countries: Digital/AI Jobs Market Status',
                    projection='natural earth',
                    category_orders={'trend_status': ['Rising', 'Moderate', 'Lagging']}
                )
                
                fig.update_layout(
                    height=500,
                    geo=dict(
                        showframe=False,
                        showcoastlines=True,
                        projection_type='natural earth'
                    ),
                    margin=dict(l=0, r=0, t=50, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                show_data_source_footer()

            # Summary by status
            st.subheader("Countries by Status")
            
            cols = st.columns(3)
            statuses = ['Rising', 'Moderate', 'Lagging']
            colors = ['#2ecc71', '#f39c12', '#e74c3c']
            
            for i, (status, color) in enumerate(zip(statuses, colors)):
                with cols[i]:
                    status_df = rising_lagging_df[rising_lagging_df['trend_status'] == status]
                    st.metric(
                        label=status,
                        value=len(status_df),
                        help=f"Countries with {status.lower()} trends"
                    )
            
            # Detailed table
            with st.expander("📋 View Detailed Analysis"):
                display_df = rising_lagging_df[[
                    'country_name', 'trend_status', 'demand_growth_pct', 
                    'supply_growth_pct', 'recent_demand', 'recent_supply'
                ]].rename(columns={
                    'country_name': 'Country',
                    'trend_status': 'Status',
                    'demand_growth_pct': 'Demand Growth %',
                    'supply_growth_pct': 'Supply Growth %',
                    'recent_demand': 'Recent Demand',
                    'recent_supply': 'Recent Supply'
                })
                st.dataframe(display_df, use_container_width=True, hide_index=True)

    elif view == "MCP Server":
        st.header("🔌 MCP Server - Data Source Integration")
        st.markdown("""
        Use this section to fetch real-time data from various sources via the MCP (Model Context Protocol) server and integrate it into the dashboard.
        """)
        
        # Show installation status
        col1, col2 = st.columns(2)
        with col1:
            if MCP_AVAILABLE:
                st.success("✅ MCP client available")
            else:
                st.warning("⚠️ MCP client not available")
                st.code("pip install mcp", language="bash")
        
        with col2:
            # Check datasets availability without importing (to avoid PyArrow errors)
            try:
                import importlib.util
                spec = importlib.util.find_spec("datasets")
                if spec is not None:
                    # Library exists, but don't import it to avoid PyArrow errors
                    st.info("💡 datasets library detected (use CSV upload to avoid PyArrow issues)")
                else:
                    st.warning("⚠️ datasets library not installed")
                    st.info("💡 Use CSV upload feature as an alternative")
            except Exception:
                st.warning("⚠️ datasets library status unknown")
                st.info("💡 Use CSV upload feature as an alternative")
        
        st.markdown("---")
        
        if True:  # Always show data sources (works with or without MCP)
            # Data source selector
            data_source = st.selectbox(
                "Select Data Source",
                [
                    "🤖 Ask a Question (AI-Powered)",
                    "Anthropic EconomicIndex",
                    "Stanford AI Index",
                    "World Bank Indicator",
                    "ITU ICT Data",
                    "View Source Information"
                ],
                help="Choose a data source to fetch or ask a question"
            )
            
            # Q&A Section
            if data_source == "🤖 Ask a Question (AI-Powered)":
                st.subheader("🤖 Ask Questions About Digital/AI Jobs Data")
                st.markdown("""
                Ask questions about digital/AI jobs, employment trends, economic indicators, and more.
                The AI will search available data sources to provide accurate answers.
                """)
                
                # API Key input (store in session state)
                if "gemini_api_key" not in st.session_state:
                    st.session_state.gemini_api_key = "AIzaSyBFp9fCpl7xBtQS6fDYbBpom22YsqXimE4"
                
                api_key_input = st.text_input(
                    "Google Gemini API Key",
                    value=st.session_state.gemini_api_key,
                    type="password",
                    help="Your Google Gemini API key from Google AI Studio. Get one at https://aistudio.google.com/api-keys"
                )
                st.session_state.gemini_api_key = api_key_input
                
                # Model selection - use models that are actually available
                model_choice = st.selectbox(
                    "Model",
                    [
                        "gemini-pro-latest",
                        "gemini-flash-latest", 
                        "gemini-2.5-flash",
                        "gemini-2.5-pro",
                        "gemini-2.0-flash",
                        "gemini-pro"
                    ],
                    help="Select Gemini model. 'gemini-pro-latest' is recommended.",
                    index=0
                )
                
                # Button to check available models
                if st.button("🔍 Check Available Models", help="Check which models are available with your API key"):
                    with st.spinner("Checking available models..."):
                        try:
                            from gemini_qa import GeminiQA
                            qa_temp = GeminiQA(api_key_input)
                            models_info = qa_temp.list_available_models()
                            
                            if "error" in models_info:
                                st.error(f"Error: {models_info['error']}")
                            elif "models" in models_info:
                                st.success("✅ Available Models:")
                                available = []
                                for m in models_info["models"]:
                                    model_name = m.get("name", "").split("/")[-1]
                                    methods = m.get("supportedGenerationMethods", [])
                                    if "generateContent" in methods:
                                        available.append(model_name)
                                        st.markdown(f"- ✅ **{model_name}** (supports generateContent)")
                                
                                if available:
                                    st.info(f"💡 Recommended: Use one of these models: {', '.join(available[:3])}")
                                    # Update model dropdown if we found available models
                                    if available:
                                        st.session_state.recommended_models = available[:5]
                            else:
                                st.warning("Could not retrieve model list.")
                        except Exception as e:
                            st.error(f"Error checking models: {str(e)}")
                
                # Show recommended model if available
                if "recommended_models" in st.session_state and st.session_state.recommended_models:
                    recommended = st.session_state.recommended_models[0]
                    if recommended != model_choice:
                        st.info(f"💡 Tip: '{recommended}' is available and recommended for your API key.")
                
                # Question input - store in session state to persist
                if "qa_question" not in st.session_state:
                    st.session_state.qa_question = ""
                
                question = st.text_area(
                    "Enter your question",
                    value=st.session_state.qa_question,
                    placeholder="e.g., What is the current trend in ICT employment across countries?",
                    help="Ask questions about digital/AI jobs, employment, economic indicators, etc.",
                    key="question_input"
                )
                st.session_state.qa_question = question
                
                # Source selection
                st.markdown("**Select data sources to use:**")
                col1, col2, col3, col4 = st.columns(4)
                use_world_bank = col1.checkbox("World Bank", value=True)
                use_stanford = col2.checkbox("Stanford AI Index", value=True)
                use_anthropic = col3.checkbox("Anthropic", value=False)
                use_itu = col4.checkbox("ITU ICT", value=False)
                
                sources_to_use = []
                if use_world_bank:
                    sources_to_use.append("world_bank")
                if use_stanford:
                    sources_to_use.append("stanford")
                if use_anthropic:
                    sources_to_use.append("anthropic")
                if use_itu:
                    sources_to_use.append("itu")
                
                # Store answer in session state to persist
                if "qa_answer" not in st.session_state:
                    st.session_state.qa_answer = None
                if "qa_sources" not in st.session_state:
                    st.session_state.qa_sources = []
                if "qa_error" not in st.session_state:
                    st.session_state.qa_error = None
                
                if st.button("🔍 Get Answer", type="primary", use_container_width=True):
                    if not question.strip():
                        st.warning("Please enter a question.")
                        st.session_state.qa_error = "No question entered"
                    elif not api_key_input:
                        st.warning("Please enter your Gemini API key.")
                        st.session_state.qa_error = "No API key entered"
                    elif not sources_to_use:
                        st.warning("Please select at least one data source.")
                        st.session_state.qa_error = "No data sources selected"
                    else:
                        with st.spinner("🤔 Analyzing your question and fetching data..."):
                            try:
                                from gemini_qa import GeminiQA
                                
                                qa_system = GeminiQA(api_key_input, model_choice)
                                result = qa_system.answer_question(question, sources_to_use)
                                
                                if result.get("error"):
                                    st.session_state.qa_error = result.get("answer", "Unknown error")
                                    st.session_state.qa_answer = None
                                    st.session_state.qa_sources = []
                                else:
                                    st.session_state.qa_answer = result.get("answer")
                                    st.session_state.qa_sources = result.get("sources", [])
                                    st.session_state.qa_error = None
                            
                            except ImportError:
                                st.session_state.qa_error = "Gemini QA module not found. Please ensure gemini_qa.py exists."
                                st.session_state.qa_answer = None
                            except Exception as e:
                                st.session_state.qa_error = str(e)
                                st.session_state.qa_answer = None
                
                # Display question (always visible if entered)
                if st.session_state.qa_question:
                    st.markdown("---")
                    st.markdown("### ❓ Your Question")
                    st.info(st.session_state.qa_question)
                
                # Display answer if available
                if st.session_state.qa_answer:
                    st.markdown("### 💬 Answer")
                    st.markdown(st.session_state.qa_answer)
                    
                    # Show sources used
                    if st.session_state.qa_sources:
                        st.markdown("---")
                        st.markdown("### 📊 Data Sources Used")
                        for source in st.session_state.qa_sources:
                            st.markdown(f"- ✅ {source}")
                    
                    if st.session_state.qa_sources:
                        st.info("💡 Answer is based on real data from the selected sources.")
                    else:
                        st.warning("⚠️ Answer is based on general knowledge (data sources may not be available).")
                
                # Display error if any
                if st.session_state.qa_error:
                    st.markdown("---")
                    st.error(f"❌ Error: {st.session_state.qa_error}")
                    if "API key" in st.session_state.qa_error or "403" in st.session_state.qa_error:
                        st.info("💡 Make sure your API key is correct and you have internet connection.")
                
                # Example questions
                with st.expander("💡 Example Questions"):
                    st.markdown("""
                    - What is the trend in ICT employment across different countries?
                    - How has AI investment changed in recent years?
                    - Which countries have the highest internet penetration rates?
                    - What are the key findings from the Stanford AI Index report?
                    - Compare ICT services employment trends between developed and developing countries.
                    - What percentage of organizations are using AI in 2024?
                    """)
            
            elif data_source == "Anthropic EconomicIndex":
                st.subheader("🤖 Anthropic EconomicIndex")
                
                # Tabs for API fetch vs CSV upload
                tab1, tab2 = st.tabs(["🌐 Fetch via API", "📤 Upload CSV File"])
                
                with tab1:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        release = st.text_input("Release Version", value="release_2025_09_15", key="anth_release")
                    with col2:
                        fetch_btn = st.button("Fetch Data", type="primary", key="anth_fetch")
                
                if fetch_btn:
                    with st.spinner("Fetching data from Anthropic EconomicIndex..."):
                        result = data_fetcher.fetch_anthropic_data(release)
                        
                        if "error" in result:
                            st.error(f"❌ Error: {result['error']}")
                            
                            # Show specific error details
                            if "details" in result:
                                with st.expander("Error Details"):
                                    st.code(result["details"], language="text")
                            
                            if "install" in result:
                                st.info("💡 Installation required:")
                                st.code(result["install"], language="bash")
                                st.markdown("After installing, refresh the page and try again.")
                            elif "suggestion" in result:
                                st.info(f"💡 Suggestion: {result['suggestion']}")
                                if "alternative" in result:
                                    st.info(f"💡 Alternative: {result['alternative']}")
                            else:
                                st.info("💡 Troubleshooting:")
                                st.markdown("""
                                - Ensure you have internet connection
                                - Check if the release version is correct
                                - If you see PyArrow errors, try: `pip install --force-reinstall datasets pyarrow`
                                - Or use the CSV upload feature as an alternative
                                """)
                        else:
                            st.success(f"✅ Successfully fetched {result.get('records', 0)} records")
                            
                            # Display data
                            if "data" in result and result.get("data"):
                                df = pd.DataFrame(result["data"])
                                st.dataframe(df, use_container_width=True, hide_index=True)
                                
                                # Download button
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download as CSV",
                                    data=csv,
                                    file_name=f"anthropic_economic_index_{release}.csv",
                                    mime="text/csv"
                                )
                            else:
                                st.info("No data records to display")
                            
                            # Show statistics
                            with st.expander("📊 Data Statistics"):
                                st.json({
                                    "records": result.get("records", 0),
                                    "columns": result.get("columns", []),
                                    "source": result.get("source", "unknown")
                                })
                
                with tab2:
                    st.markdown("""
                    **Upload Anthropic EconomicIndex Data from CSV**
                    
                    If the API fetch doesn't work due to PyArrow compatibility issues, you can:
                    1. Download data from [Hugging Face](https://huggingface.co/datasets/Anthropic/EconomicIndex)
                    2. Convert to CSV format
                    3. Upload it here
                    """)
                    
                    uploaded_file = st.file_uploader(
                        "Choose a CSV file",
                        type=['csv'],
                        help="Upload Anthropic EconomicIndex data as CSV",
                        key="anth_csv"
                    )
                    
                    if uploaded_file is not None:
                        try:
                            df = pd.read_csv(uploaded_file)
                            st.success(f"✅ Successfully loaded {len(df)} rows")
                            
                            st.dataframe(df.head(20), use_container_width=True, hide_index=True)
                            
                            # Show column info
                            with st.expander("📊 File Information"):
                                st.write(f"**Rows:** {len(df)}")
                                st.write(f"**Columns:** {', '.join(df.columns.tolist())}")
                                st.write(f"**Data Types:**")
                                st.json(df.dtypes.astype(str).to_dict())
                            
                            st.info("💡 You can analyze this data in the dashboard's other views.")
                            
                        except Exception as e:
                            st.error(f"Error reading CSV file: {str(e)}")
            
            elif data_source == "Stanford AI Index":
                st.subheader("🎓 Stanford AI Index Report 2025")
                
                metric_type = st.selectbox(
                    "Metric Type",
                    ["all", "investment", "adoption", "performance"],
                    help="Select type of metric to fetch"
                )
                
                if st.button("Fetch Data", type="primary"):
                    with st.spinner("Fetching Stanford AI Index data..."):
                        result = data_fetcher.fetch_stanford_ai_index(metric_type)
                        
                        if "error" in result:
                            st.error(f"Error: {result['error']}")
                        else:
                            st.success("✅ Successfully fetched Stanford AI Index data")
                            
                            # Display key metrics
                            if "key_metrics" in result:
                                metrics = result["key_metrics"]
                                
                                cols = st.columns(3)
                                if "investment" in metrics:
                                    with cols[0]:
                                        st.metric("US Investment 2024", metrics["investment"].get("us_2024", "N/A"))
                                    with cols[1]:
                                        st.metric("China Investment 2024", metrics["investment"].get("china_2024", "N/A"))
                                    with cols[2]:
                                        st.metric("UK Investment 2024", metrics["investment"].get("uk_2024", "N/A"))
                                
                                if "adoption" in metrics:
                                    st.subheader("Adoption Metrics")
                                    st.json(metrics["adoption"])
                            
                            if "url" in result:
                                st.markdown(f"📖 [View Full Report]({result['url']})")
            
            elif data_source == "World Bank Indicator":
                st.subheader("🌍 World Bank Indicator")
                
                # Tabs for API fetch vs CSV upload
                tab1, tab2 = st.tabs(["🌐 Fetch via API", "📤 Upload CSV File"])
                
                with tab1:
                    # Info about World Bank API
                    with st.expander("ℹ️ About World Bank API Access", expanded=False):
                        st.markdown("""
                        **Note:** World Bank API may require authentication or have rate limits.
                        
                        **Alternatives:**
                        - Use [World Bank DataBank](https://databank.worldbank.org/) to download data directly
                        - Upload CSV file using the "Upload CSV File" tab
                        - The dashboard already includes sample World Bank data
                        - Check [World Bank API Documentation](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) for API access
                        
                        **Common Indicator Codes:**
                        - `SL.EMP.ICTI.ZS` - Employment in ICT services (% of total employment)
                        - `SL.EMP.ICTM.ZS` - Employment in ICT manufacturing (% of total employment)
                        - `IT.NET.USER.ZS` - Internet users (% of population)
                        - `IT.CEL.SETS.P2` - Mobile cellular subscriptions (per 100 people)
                        """)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        indicator_code = st.text_input(
                            "Indicator Code",
                            value="SL.EMP.ICTI.ZS",
                            help="e.g., SL.EMP.ICTI.ZS (ICT Services Employment)",
                            key="wb_indicator"
                        )
                        country_code = st.text_input("Country Code", value="all", help="e.g., USA, CHN, or 'all'", key="wb_country")
                    
                    with col2:
                        start_year = st.number_input("Start Year", min_value=2000, max_value=2024, value=2015, key="wb_start")
                        end_year = st.number_input("End Year", min_value=2000, max_value=2024, value=2024, key="wb_end")
                    
                    if st.button("Fetch Data", type="primary", key="wb_fetch"):
                        with st.spinner(f"Fetching {indicator_code}..."):
                            result = data_fetcher.fetch_world_bank_indicator(
                                indicator_code, country_code, start_year, end_year
                            )
                            
                            if "error" in result:
                                st.error(f"❌ Error: {result['error']}")
                                
                                # Show helpful suggestions
                                if result.get("status_code") == 401:
                                    st.warning("""
                                    **World Bank API Access Issue:**
                                    
                                    The World Bank API may require authentication or have rate limits. 
                                    Try these alternatives:
                                    
                                    1. **Use World Bank DataBank directly:**
                                       - Visit: https://databank.worldbank.org/
                                       - Search for your indicator
                                       - Download CSV data
                                    
                                    2. **Check API documentation:**
                                       - https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
                                    
                                    3. **Try a different indicator code** or use the sample data in the dashboard
                                    """)
                                
                                if "suggestion" in result:
                                    st.info(f"💡 Suggestion: {result['suggestion']}")
                                
                                if "alternative" in result:
                                    st.info(f"💡 Alternative: {result['alternative']}")
                            else:
                                st.success(f"✅ Successfully fetched {result.get('records', 0)} records")
                                
                                # Display data
                                if "data" in result and result.get("data"):
                                    df = pd.DataFrame(result["data"])
                                    st.dataframe(df, use_container_width=True, hide_index=True)
                                    
                                    # Download button
                                    csv = df.to_csv(index=False)
                                    st.download_button(
                                        label="📥 Download as CSV",
                                        data=csv,
                                        file_name=f"wb_{indicator_code}_{country_code}.csv",
                                        mime="text/csv"
                                    )
                                    
                                    # Show statistics
                                    if "statistics" in result:
                                        stats = result["statistics"]
                                        cols = st.columns(3)
                                        with cols[0]:
                                            st.metric("Mean", f"{stats.get('mean', 0):.2f}" if stats.get('mean') else "N/A")
                                        with cols[1]:
                                            st.metric("Min", f"{stats.get('min', 0):.2f}" if stats.get('min') else "N/A")
                                        with cols[2]:
                                            st.metric("Max", f"{stats.get('max', 0):.2f}" if stats.get('max') else "N/A")
                                else:
                                    st.info("No data records to display")
                
                with tab2:
                    st.markdown("""
                    **Upload World Bank Data from CSV**
                    
                    If the API doesn't work, download data from [World Bank DataBank](https://databank.worldbank.org/) 
                    and upload it here.
                    """)
                    
                    uploaded_file = st.file_uploader(
                        "Choose a CSV file",
                        type=['csv'],
                        help="Upload World Bank data downloaded from DataBank"
                    )
                    
                    if uploaded_file is not None:
                        try:
                            df = pd.read_csv(uploaded_file)
                            st.success(f"✅ Successfully loaded {len(df)} rows")
                            
                            st.dataframe(df.head(20), use_container_width=True, hide_index=True)
                            
                            # Show column info
                            with st.expander("📊 File Information"):
                                st.write(f"**Rows:** {len(df)}")
                                st.write(f"**Columns:** {', '.join(df.columns.tolist())}")
                                st.write(f"**Data Types:**")
                                st.json(df.dtypes.astype(str).to_dict())
                            
                            st.info("💡 You can analyze this data in the dashboard's other views.")
                            
                        except Exception as e:
                            st.error(f"Error reading CSV file: {str(e)}")
            
            elif data_source == "ITU ICT Data":
                st.subheader("📡 ITU ICT Data")
                
                st.info("💡 ITU data is accessed via World Bank API. If you encounter 401 errors, use World Bank DataBank as an alternative.")
                
                indicator = st.selectbox(
                    "ICT Indicator",
                    ["internet", "mobile", "broadband"],
                    help="Select ICT indicator type"
                )
                country_code = st.text_input("Country Code", value="all", help="e.g., USA, CHN, or 'all'")
                
                if st.button("Fetch Data", type="primary"):
                    with st.spinner(f"Fetching {indicator} data..."):
                        result = data_fetcher.fetch_itu_ict_data(indicator, country_code)
                        
                        if "error" in result:
                            st.error(f"❌ Error: {result['error']}")
                            
                            if result.get("status_code") == 401:
                                st.warning("""
                                **World Bank API Access Issue:**
                                
                                ITU data is accessed via World Bank API. The API may require authentication.
                                Try using World Bank DataBank directly: https://databank.worldbank.org/
                                """)
                            
                            if "suggestion" in result:
                                st.info(f"💡 Suggestion: {result['suggestion']}")
                        else:
                            st.success(f"✅ Successfully fetched {result.get('records', 0)} records")
                            
                            if "data" in result and result.get("data"):
                                df = pd.DataFrame(result["data"])
                                st.dataframe(df, use_container_width=True, hide_index=True)
                                
                                # Download button
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download as CSV",
                                    data=csv,
                                    file_name=f"itu_{indicator}_{country_code}.csv",
                                    mime="text/csv"
                                )
                            else:
                                st.info("No data records to display")
            
            elif data_source == "View Source Information":
                st.subheader("ℹ️ Data Source Information")
                
                source = st.selectbox(
                    "Select Source",
                    ["anthropic", "stanford", "world_bank", "itu", "pwc", "yale", "mckinsey"]
                )
                
                info = data_fetcher.get_data_source_info(source)
                
                if "error" not in info:
                    st.info(f"**{info['name']}** - {info['status']}")
                    st.markdown(f"**Description:** {info['description']}")
                    
                    if "url" in info:
                        st.markdown(f"**URL:** {info['url']}")
                    
                    if "fetch_function" in info:
                        st.code(f"data_fetcher.{info['fetch_function']}()", language="python")

    # Footer
    st.markdown("---")
    st.markdown("""
    **Data Sources:**
    - World Bank Global Jobs Indicators Database
    - World Bank Global Labor Database (GLD)
    - ITU ICT Data Hub
    - ILO Statistics
    - Data360 Indicators
    - World Bank Open Data API
    - Anthropic EconomicIndex Dataset (Hugging Face)
    - Stanford AI Index Report 2025
    - PwC AI Jobs Barometer
    - Yale Budget Lab - AI Labor Market Research
    - McKinsey - Economic Potential of Generative AI
    
    📋 For detailed information about all data sources, see `DATA_SOURCES.md`
    
    **Challenge Category:** Category V - Toward New Insights on Job Trends
    """)


if __name__ == "__main__":
    main()

