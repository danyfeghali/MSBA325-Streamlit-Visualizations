import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import math

# Load the data
df = pd.read_csv('/.world-data-2023 - clean.csv')
df_clean = df.dropna()

# Add GDP per Capita column
df_clean['GDP_per_Capita'] = df_clean['GDP ($)'] / df_clean['Population']

# Set page config
st.set_page_config(
    page_title="Interactive Visualizations",
    layout="wide"
)

# Title
col1, col2, col3 = st.columns([1,3,1])
with col1:
    st.write("")
    st.image('/.world-image-1.jpg', use_column_width = True)
with col2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("""<div style='display: flex; justify-content: center; align-items: center;'><p style='color: black; font-size: 35px; font-weight: bold; text-align: center; width: 100%;'>World Data Dashboard</p></div>""", unsafe_allow_html=True)
with col3:
    st.write("")
    st.image('/.data-analysis-1.jpg', use_column_width = True)

st.write("## Overview")
st.write("This dashboard visualizes key global metrics for the year 2023, sourced from Kaggle. Through interactive visualizations, explore the relationships between economic prosperity, environmental conservation, and health indicators.")

# Interactive Features

# Selection box for countries
# List of all countries
countries = list(df_clean['Country'].unique())

# Create a checkbox for "Select All Countries"
select_all = st.checkbox('Select All Countries', value=True)

# If checkbox is checked, select all countries and disable the multiselect box
if select_all:
    selected_countries = countries
    st.multiselect('Select countries', countries, countries, disabled=True)
else:
    selected_countries = st.multiselect('Select countries', countries, default=[])

# Ensure relevant columns are of type float
df_clean['GDP_per_Capita'] = df_clean['GDP_per_Capita'].astype(float)
df_clean['Life expectancy'] = df_clean['Life expectancy'].astype(float)
df_clean['Density\n(P/Km2)'] = df_clean['Density\n(P/Km2)'].astype(float)

# Slider for GDP per Capita range
min_gdp_per_capita, max_gdp_per_capita = st.slider('Filter by GDP per Capita Range', float(df_clean['GDP_per_Capita'].min()), float(df_clean['GDP_per_Capita'].max()), (float(df_clean['GDP_per_Capita'].min()), float(df_clean['GDP_per_Capita'].max())))

# Slider for Life Expectancy
min_life_expectancy, max_life_expectancy = st.slider('Filter by Life Expectancy Range', float(df_clean['Life expectancy'].min()), float(df_clean['Life expectancy'].max()), (float(df_clean['Life expectancy'].min()), float(df_clean['Life expectancy'].max())))

# Slider for Urban Population Percentage
min_density, max_density = st.slider('Filter by Population Density (P/Km2)', float(df_clean['Density\n(P/Km2)'].min()), float(df_clean['Density\n(P/Km2)'].max()), (float(df_clean['Density\n(P/Km2)'].min()), float(df_clean['Density\n(P/Km2)'].max())))

# Filter the dataframe based on interactive inputs
df_clean = df_clean[df_clean['Country'].isin(selected_countries)]
df_clean = df_clean[(df_clean['GDP_per_Capita'] >= min_gdp_per_capita) & (df_clean['GDP_per_Capita'] <= max_gdp_per_capita)]
df_clean = df_clean[(df_clean['Life expectancy'] >= min_life_expectancy) & (df_clean['Life expectancy'] <= max_life_expectancy)]
df_clean = df_clean[(df_clean['Density\n(P/Km2)'] >= min_density) & (df_clean['Density\n(P/Km2)'] <= max_density)]

# Create fig1
country_by_land = df_clean.sort_values(by='Land Area (Km2)', ascending=False)
fig1 = px.scatter(country_by_land, x="Co2-Emissions (tons)", y="Forested Area (%)",
                 size="Land Area (Km2)", color="Country")
fig1.update_layout(height=600, xaxis=dict(title='CO2 Emissions (tons)'), legend=dict(itemclick='toggleothers'))

# Create fig2
df_clean['Log_GDP_per_Capita'] = df_clean['GDP_per_Capita'].apply(lambda x: math.log(x))
fig2 = px.scatter(df_clean, x="Birth Rate (per 1000)", y="Life expectancy", color="Log_GDP_per_Capita",
                 color_continuous_scale="sunset", hover_data=df_clean[['Country']])
fig2.update_layout(height=600, template='gridon', plot_bgcolor='white', paper_bgcolor='white')

# For the first visualization and its insights
st.write("## Visualizations")
st.write("### CO2 Emissions vs. Forested Area")
st.write("This scatter plot visualizes the relationship between CO2 emissions and the percentage of forested area for the selected countries by land area. The size of each point represents the land area of the country.")

# Create columns for the first visualization and its key insights
col_viz1, col_insight1 = st.columns([3,1])
with col_viz1:
    st.plotly_chart(fig1, use_container_width=True)
with col_insight1:
    st.write("")
    st.write("#### Key Insights")
    st.write("- The USA, Russia, India, and China distinctly stand out as the major contributors to CO2 emissions, overshadowing the vast majority of other nations.")
    st.write("- While forests are essential for carbon sequestration, their presence doesn't necessarily correlate with low CO2 emissions for all countries.")

# For the second visualization and its insights
st.write("### Birth Rate & Life Expectancy vs. GDP per Capita")
st.write("This scatter plot showcases the correlation between birth rates and life expectancy across the selected countries. The color intensity signifies the GDP per capita, providing an economic context to the health indicators.")

# Create columns for the second visualization and its key insights
col_viz2, col_insight2 = st.columns([3,1])
with col_viz2:
    st.plotly_chart(fig2, use_container_width=True)
with col_insight2:
    st.write("#### Key Insights")
    st.write("- There's a noticeable trend that countries with higher birth rates tend to have lower life expectancies.")
    st.write("- The decrease in GDP per capita with increasing birth rate suggests that wealthier countries tend to have lower birth rates.")

# # Create fig1
# country_by_land = df_clean.sort_values(by='Land Area (Km2)', ascending=False)
# fig1 = px.scatter(country_by_land, x="Co2-Emissions (tons)", y="Forested Area (%)",
#                  size="Land Area (Km2)", color="Country")
# fig1.update_layout(height=600, title_text='CO2 Emissions vs Forest and Land Area', xaxis=dict(title='CO2 Emissions (tons)'), legend=dict(itemclick='toggleothers'))
# st.write("## Visualizations")
# st.write("### CO2 Emissions vs. Forested Area")
# st.write("This scatter plot visualizes the relationship between CO2 emissions and the percentage of forested area for the selected countries by land area. The size of each point represents the land area of the country.")
# st.plotly_chart(fig1, use_container_width=True)

# # Create fig2
# df_clean['Log_GDP_per_Capita'] = df_clean['GDP_per_Capita'].apply(lambda x: math.log(x))
# fig2 = px.scatter(df_clean, x="Birth Rate (per 1000)", y="Life expectancy", color="Log_GDP_per_Capita",
#                  color_continuous_scale="sunset", hover_data=df_clean[['Country']])
# fig2.update_layout(height=600, title='Scatterplot of Birth Rate & Life Expectancy', template='gridon', plot_bgcolor='white', paper_bgcolor='white')
# st.write("### Birth Rate & Life Expectancy vs. GDP per Capita")
# st.write("This scatter plot showcases the correlation between birth rates and life expectancy across the selected countries. The color intensity signifies the GDP per capita, providing an economic context to the health indicators.")
# st.plotly_chart(fig2, use_container_width=True)

# # ... (Key Insights, Methodology, Legend, Conclusion, References as previously detailed)

# st.write("## Key Insights")
# st.write("- The USA, Russia, India, and China distinctly stand out as the major contributors to CO2 emissions, overshadowing the vast majority of other nations. Their substantial emissions highlight the importance of focusing on these countries when aiming for global emission reductions.")
# st.write("- While forests are essential for carbon sequestration, their presence doesn't necessarily correlate with low CO2 emissions for all countries. The vertical clustering of many countries suggests that other factors, such as industrial activities and energy sources, play a significant role in determining a country's carbon footprint.")
# st.write("- There's a noticeable trend that countries with higher birth rates tend to have lower life expectancies. This might be indicative of socio-economic factors, where countries with lower development levels often have both higher birth rates and challenges that impact life expectancy, such as limited healthcare access, malnutrition, and other socio-economic challenges.")
# st.write("- The decrease in GDP per capita with increasing birth rate suggests that wealthier countries tend to have lower birth rates. This could be attributed to factors like better education, more career opportunities, and improved access to contraception. In wealthier societies, there's often a shift in priorities, with families choosing to have fewer children and invest more in their upbringing.")

st.write("## Glossary")
st.write("- **GDP per Capita**: The total economic output of a country divided by its population. It represents the average economic output per person if a country's total production is distributed evenly.")
st.write("- **CO2 Emissions**: The total carbon dioxide emissions of a country in tons.")
st.write("- **Forested Area (%)**: The percentage of a country's land area covered by forests.")
st.write("- **Population Density**: The total number of people divided by the land area of the country, given in persons per square kilometer.")

st.write("## Conclusion")
st.write("The dashboard provides insights into the intricate balance between economic prosperity, environmental health, and overall well-being of populations. As global citizens, understanding these metrics can guide informed decisions and actions. We encourage users to delve deep, explore the data, and draw their own conclusions.")

st.write("## References")
st.write("1. [Kaggle Data Source](https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023?datasetId=3495122&sortBy=voteCount) - The data source for the 2023 global metrics.")