# Import important modules
import streamlit as st
import pandas as pd
import plost

# Read in video game sale data from GitHub repo
vg_sales = pd.read_csv('https://raw.githubusercontent.com/JahanzebMK/videogame-sales/main/Data/scraped_vgsales.csv')

# Add total sales column and convert year column to int dtype
vg_sales = vg_sales.rename(columns={c: c+' (millions)' for c in vg_sales.columns if c in ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']})
vg_sales['Global Sales (millions)'] = vg_sales['NA_Sales (millions)']+vg_sales['EU_Sales (millions)']+vg_sales['JP_Sales (millions)']+vg_sales['Other_Sales (millions)']
vg_sales['Year']=vg_sales['Year'].astype(int)

# Config layout of page and add important info
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.sidebar.header('Video Game Sales (1980-2020)')
st.sidebar.subheader('By Jahanzeb Khan')
st.sidebar.markdown('Data obtained from vgchartz.com')

# Double slider to allow user to select which years to focus on
st.sidebar.subheader('Year Slider')
year_range = st.sidebar.slider('Select a range of values', vg_sales['Year'].min(), vg_sales['Year'].max(), (vg_sales['Year'].min(), vg_sales['Year'].max()))
vg_sales = vg_sales[vg_sales['Year'].between(year_range[0],year_range[1])]

# Multiselect filter to allow user to select which platforms to focus on
st.sidebar.subheader('Platform Filter')
platform_choice = vg_sales['Platform'].unique().tolist()
with st.sidebar.expander("Select specific platforms"):
    platform_container = st.container()
    platform_all = st.checkbox("Select all", value = True, key='platform')
    if platform_all:
        selected_platforms = platform_container.multiselect("Select specific platforms",platform_choice,platform_choice, )
    else:
        selected_platforms =   platform_container.multiselect("Select specific platforms",platform_choice, )
vg_sales = vg_sales[vg_sales['Platform'].isin(selected_platforms)]

# Multiselect filter to allow user to select which genres to focus on
st.sidebar.subheader('Genre Filter')
genre_choice = vg_sales['Genre'].unique().tolist()
with st.sidebar.expander("Select specific genres"):
    genre_container = st.container()
    genre_all = st.checkbox("Select all", value = True, key='genre')
    if genre_all:
        selected_genres = genre_container.multiselect("Select specific genres",genre_choice,genre_choice)
    else:
        selected_genres =  genre_container.multiselect("Select specific genres",genre_choice)
vg_sales = vg_sales[vg_sales['Genre'].isin(selected_genres)]


# Multiselect filter to allow user to select which publishers to focus on
st.sidebar.subheader('Publisher Filter')
publisher_choice = vg_sales['Publisher'].unique().tolist()
with st.sidebar.expander("Select specific publishers"):
    publisher_container = st.container()
    publisher_all = st.checkbox("Select all", value = True, key='publisher')
    if publisher_all:
        selected_publishers = publisher_container.multiselect("Select specific publishers",publisher_choice,publisher_choice)
    else:
        selected_publishers =  publisher_container.multiselect("Select specific publishers",publisher_choice)
vg_sales = vg_sales[vg_sales['Publisher'].isin(selected_publishers)]
    

# Create aggregates of data depending on user selections to be used for visualisations
platform_sales = vg_sales.groupby(['Platform'])['Global Sales (millions)'].agg('sum').reset_index()
publisher_sales = vg_sales.groupby(['Publisher'])['Global Sales (millions)'].agg('sum').reset_index()
genre_sales = vg_sales.groupby(['Genre'])['Global Sales (millions)'].agg('sum').reset_index()
market_vg_sales = vg_sales.groupby(['Year'])[['NA_Sales (millions)', 'EU_Sales (millions)', 'JP_Sales (millions)', 'Other_Sales (millions)']].agg('sum').reset_index()
market_vg_sales.Year = market_vg_sales.Year.astype(str)

# Seperate visualisations into columns
c1, c2, c3,c4 = st.columns((2.5,2.5,2.5,2.5))
with c1:
    st.markdown('### Top 10')
    st.dataframe(vg_sales.head(10), hide_index = True, column_order=("Name", "Platform", "Global Sales (M)")) 
with c2:
    st.markdown('### Platform Donut Chart')
    plost.donut_chart(
        data=platform_sales,
        theta='Global Sales (millions)',
        color='Platform',
        legend=False, 
        use_container_width=True)
with c3:
    st.markdown('### Publisher Donut Chart')
    plost.donut_chart(
        data=publisher_sales,
        theta='Global Sales (millions)',
        color='Publisher',
        legend=False, 
        use_container_width=True)
with c4:
    st.markdown('### Genre Donut Chart')
    plost.donut_chart(
        data=genre_sales,
        theta='Global Sales (millions)',
        color='Genre',
        legend=False, 
        use_container_width=True)
    
st.markdown('### Market Sales Over Time')
st.line_chart(market_vg_sales, x = 'Year', y = ['NA_Sales (millions)', 'EU_Sales (millions)', 'JP_Sales (millions)', 'Other_Sales (millions)'])


