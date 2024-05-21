import streamlit as st
import altair as alt
import plotly.express as px
from streamlit_folium import st_folium
from slidebar import sideBar
from clustermap_severity import create_cluster_map
from map_road_type import map_road_type

# Page configuration
st.set_page_config(
    page_title="KSP Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

# CSS styling
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df_lat_lon_filtered, selected_district, selected_color_theme, analytics_option = sideBar()

# Clean and standardize district names
df_lat_lon_filtered['DISTRICTNAME'] = df_lat_lon_filtered['DISTRICTNAME'].str.strip().str.upper()

# Count the number of latitude entries per district
df_accident_count = df_lat_lon_filtered.groupby('DISTRICTNAME')['Latitude'].count().reset_index()
df_accident_count.columns = ['district', 'accident_count']

# Sort the districts by accident count in descending order
df_accident_count_sorted = df_accident_count.sort_values(by='accident_count', ascending=False)

st.markdown('## Karnataka State Police Dashboard')

with st.expander("🧭 My database"):
    shwdata = st.multiselect('Filter:', df_lat_lon_filtered.columns, default=[])
    if shwdata:
        st.dataframe(df_lat_lon_filtered[shwdata], use_container_width=True)
    else:
        st.dataframe(df_lat_lon_filtered, use_container_width=True)

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown('##### Total Accidents')
    total_accidents = df_lat_lon_filtered['Latitude'].count()
    st.metric(label="Total Accidents", value=total_accidents)

with col2:
    df_accident_count = df_lat_lon_filtered.groupby('DISTRICTNAME').size().reset_index(name='accident_count')
    highest_accidents_district = df_accident_count.loc[df_accident_count['accident_count'].idxmax()]
    st.markdown('##### Highest Accidents District')
    st.metric(label=highest_accidents_district['DISTRICTNAME'], value=highest_accidents_district['accident_count'])

with col3:
    st.markdown('##### Total Fatal Injuries')
    total_fatal_injuries = df_lat_lon_filtered[df_lat_lon_filtered['Severity'] == 'Fatal'].shape[0]
    st.metric(label="Total Fatal Injuries", value=total_fatal_injuries)

with col4:
    st.markdown('##### Most Frequent Accidents .. ')
    most_frequent_cause = df_lat_lon_filtered['Main_Cause'].mode()[0]
    st.metric(label="Most Frequent Cause", value=most_frequent_cause)


cols = st.columns((2, 3.5, 3.5), gap='medium')

with cols[0]:
    st.markdown('##### Top Districts by Accident Count')
    st.dataframe(df_accident_count_sorted,
                 column_order=["district", "accident_count"],
                 hide_index=True,
                 width=300,
                 column_config={
                     "district": st.column_config.TextColumn("District"),
                     "accident_count": st.column_config.ProgressColumn(
                         "Accident Count",
                         max_value=max(df_accident_count_sorted.accident_count),
                         format="%d",
                         min_value=0,
                     )
                 }
                 )
    
    st.markdown('##### Main Causes of Accidents by Locations ')
    pivot_causes = df_lat_lon_filtered.pivot_table(
        index='Accident_Location',
        columns='Main_Cause',
        values='DISTRICTNAME',
        aggfunc='count',
        fill_value=0
    ).reset_index()
    st.dataframe(pivot_causes)

with cols[1]:
    tab1, tab2 = st.tabs(["Road Map", "Cluster Map"])
    with tab1:
        # st.markdown('#### Road Map')
        map_folium = map_road_type(df_lat_lon_filtered)
        st.plotly_chart(map_folium, use_container_width=True, height=600)
    with tab2:
        # st.markdown('#### Severity Map')
        map_folium = create_cluster_map(df_lat_lon_filtered, selected_district)
        st_folium(map_folium, height=600)

    
with cols[2]:
    # st.markdown('### Number of Accidents Per Year')
    df_yearly_accidents = df_lat_lon_filtered.groupby('Year').size().reset_index(name='Total Accidents')

    bar_chart = alt.Chart(df_yearly_accidents).mark_bar().encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Total Accidents:Q', title='Number of Accidents'),
        tooltip=['Year', 'Total Accidents']
    ).properties(
        title='Number of Accidents Per Year',
        width=600,
        height=400
    )

    st.altair_chart(bar_chart, use_container_width=True)
    
    with st.expander('About', expanded=True):
        st.write('''
            - Data: [KSP Data](https://drive.google.com/drive/folders/1J_Mah7cR4J2Jek8H0XXi9CFeYg_0-Klc).
            - :orange[**Road Type Map**]: Showing the severity based on selected Year and District by Various colourspot
            - :orange[**Cluster Map**]: Here we formed the Cluster showing the number of accidents count within that cluster
        ''')