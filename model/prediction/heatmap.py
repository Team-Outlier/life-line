import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster, HeatMap
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static



st.set_page_config(layout="wide")

def create_cluster_map(df, selected_districts, add_heatmap):
    # Load GeoJSON file with district borders of Karnataka
    geojson_file_path = 'data\District_Map.geojson'
    districts = gpd.read_file(geojson_file_path)
    
    # Load state border file
    state_geojson_file_path = 'data\State_Map.geojson'
    state_borders = gpd.read_file(state_geojson_file_path)

    # Create a dark-themed map centered at Karnataka
    map_karnataka = folium.Map(
        location=[df['Latitude'].mean(), df['Longitude'].mean()], 
        zoom_start=10, 
        tiles='CartoDB dark_matter'
    )

    # Create a MarkerCluster layer
    marker_cluster = MarkerCluster().add_to(map_karnataka)

    if 'All' in selected_districts:
        # Add state borders to the map
        folium.GeoJson(state_borders.to_json()).add_to(map_karnataka)
    else:
        for selected_district in selected_districts:
            # Find district polygon based on district name
            district_polygon = districts[districts['name'] == selected_district]

            # Check if the district polygon exists
            if not district_polygon.empty:
                # Get the centroid of the district for zooming
                district_center = district_polygon.geometry.centroid.iloc[0].coords[0]
                map_karnataka.location = [district_center[1], district_center[0]]
                map_karnataka.zoom_start = 10

                # Add district borders to the map
                folium.GeoJson(district_polygon.to_json()).add_to(map_karnataka)

    # Iterate over each row in the dataframe and add markers to the MarkerCluster
    for index, row in df.iterrows():
        # Extract latitude and longitude
        latitude = row['Latitude']
        longitude = row['Longitude']

        # Create a GeoJSON representation of the point
        point_geojson = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            }
        }

        # Add the point to the MarkerCluster layer
        folium.GeoJson(point_geojson).add_to(marker_cluster)

    # Add heatmap layer if the checkbox is checked
    if add_heatmap:
        heat_data = [[row['Latitude'], row['Longitude']] for index, row in df.iterrows()]
        HeatMap(heat_data).add_to(map_karnataka)

    return map_karnataka

# Streamlit application
def heatmain():
    st.title("Karnataka Accident Hotspots: Most Frequent Spots")

    # Load data from Excel
    data_file_path = 'data\demo2.xlsx'
    df = pd.read_excel(data_file_path)

    # Dropdown menus for selecting districts and year
    districts = sorted(df['DISTRICTNAME'].unique())
    years = sorted(df['Year'].unique())

    # Add "All" options
    districts.insert(0, 'All')
    years.insert(0, 'All')

    col1, col2 = st.columns(2)
    with col1:
        selected_districts = st.multiselect("Select District(s)", districts)
    with col2:
        selected_years = st.multiselect("Select Year(s)", years)

    add_heatmap = st.checkbox("Add Heatmap Layer", value=True)

    # Filter data based on selections
    if 'All' in selected_districts:
        filtered_data = df
    else:
        filtered_data = df[df['DISTRICTNAME'].isin(selected_districts)]

    if 'All' not in selected_years:
        filtered_data = filtered_data[filtered_data['Year'].isin(selected_years)]

    # Create the map
    if not filtered_data.empty:
        map_karnataka = create_cluster_map(filtered_data, selected_districts, add_heatmap)
        folium_static(map_karnataka, width=1400, height=800)  # Adjusted height
    else:
        st.write("No data available for the selected district(s) and year(s).")


def heat_map():
    
    st.markdown('## Heat Map')
    heatmain()