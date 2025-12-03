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


def create_demand_supply_chart(df, x_col, color_col, title):
    """Create a dual-axis chart showing demand and supply trends."""
    # Prepare data for Altair
    df_melted = df.melt(
        id_vars=[x_col, color_col],
        value_vars=['avg_demand', 'avg_supply'],
        var_name='metric',
        value_name='value'
    )
    
    # Map metric names
    df_melted['metric'] = df_melted['metric'].map({
        'avg_demand': 'Demand',
        'avg_supply': 'Supply'
    })
    
    chart = alt.Chart(df_melted).mark_line(point=True, strokeWidth=2).encode(
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
            alt.Tooltip('value:Q', title='Value', format='.1f')
        ]
    ).properties(
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
    view = st.sidebar.radio(
        "Analysis View",
        ["Country Trends", "Industry Trends", "Skill Trends", "Rising vs Lagging"],
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
                    chart = create_demand_supply_chart(
                        country_df, 
                        'year', 
                        'country_name',
                        'Demand vs Supply Trends by Country'
                    )
                    st.altair_chart(chart, use_container_width=True)
                
                with col2:
                    gap_chart = create_gap_chart(
                        country_df.groupby(['country_name', 'year'])['avg_gap'].mean().reset_index(),
                        'year',
                        'country_name',
                        'Demand-Supply Gap Over Time'
                    )
                    st.altair_chart(gap_chart, use_container_width=True)
                
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

