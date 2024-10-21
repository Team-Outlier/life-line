import streamlit as st
import plotly.graph_objs as go
from sklearn.cluster import KMeans
from streamlit_option_menu import option_menu
import pandas as pd
#from heatmap import heat_map
from model.prediction.heatmap import heat_map
# # CSS styling




def create_Scatterplot_map_black(df):
    # Define the center and zoom level for the map
    center_lat = 15.05  # Center latitude
    center_lon = 76.8  # Center longitude
    zoom = 6  # Zoom level

    # Perform KMeans clustering on the DataFrame
    # kmeans = KMeans(n_clusters=25, random_state=42)
    # kmeans.fit(df[['Latitude', 'Longitude']])
    # centers = kmeans.cluster_centers_
    freq_df = df.groupby(['Longitude', 'Latitude']).size().reset_index(name='count')

# Sort the DataFrame by the count in descending order
    freq_df = freq_df.sort_values(by='count', ascending=False)

# Select the top 25 pairs
    centers = freq_df.head(25)
    
    # Define the cluster centers and their marker properties
    centers_df = pd.DataFrame(centers, columns=['Latitude', 'Longitude', 'count'])
    center_marker_size = 15
    center_marker_color = 'gold'

    # Create Scattermapbox traces for each cluster center with only circle outline
    traces_centers = go.Scattermapbox(
        lon=centers_df['Longitude'],
        lat=centers_df['Latitude'],

        mode='markers',
        marker=dict(
            size=center_marker_size,
            color=center_marker_color,
            opacity=1
        ),
        hoverinfo='text',
        hovertext='Latitude: ' + centers_df['Latitude'].astype(str) + '<br>Longitude: ' + centers_df['Longitude'].astype(str)+'<br>Count:' + centers_df['count'].astype(str) +'<br>'+ '<a href="https://www.gps-coordinates.net/street-view/@' + centers_df['Latitude'].astype(str) + ',' + centers_df['Longitude'].astype(str) + ',h237,p9,z1">Open Street View</a>'
        
    )

    # Create the layout for the map
    layout = go.Layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=500,
        width=1000,
        hovermode='closest',
        mapbox=dict(
            accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
            center=dict(lat=center_lat, lon=center_lon),
            style='dark',
            zoom=zoom
        ),
        autosize=True
    )

    # Create the figure including both original data and cluster centers
    fig = go.Figure(data=[traces_centers], layout=layout)

    
    return fig


# CSS styling


df_lat_lon = pd.read_csv('data/demo.csv')

def prediction_page_2(df_lat_lon_selected_year):
    st.markdown("")
    # Display the Folium map
    map_plotly = create_Scatterplot_map_grey(df_lat_lon_selected_year)
    st.plotly_chart(map_plotly, use_container_width=True)

def spot_prediction_page(filtered_df):
    
    
    # Example of showing a map using data
    map_plotly = create_Scatterplot_map_black(filtered_df)
    st.plotly_chart(map_plotly, use_container_width=True)


def create_Scatterplot_map_grey(df):
    # Define the center and zoom level for the map
    center_lat = 15.05  # Center latitude
    center_lon = 76.8  # Center longitude
    zoom = 6  # Zoom level

    # Perform KMeans clustering on the DataFrame
    kmeans = KMeans(n_clusters=25, random_state=42)
    kmeans.fit(df[['Latitude', 'Longitude']])
    centers = kmeans.cluster_centers_

    # Define the cluster centers and their marker properties
    centers_df = pd.DataFrame(centers, columns=['Latitude', 'Longitude'])
    center_marker_size = 15
    center_marker_color = 'gold'

    # Create Scattermapbox traces for each cluster center with only circle outline
    traces_centers = go.Scattermapbox(
        lon=centers_df['Longitude'],
        lat=centers_df['Latitude'],
        mode='markers',
        marker=dict(
            size=center_marker_size,
            color=center_marker_color,
            opacity=1
        ),
        hoverinfo='text',
        hovertext='Latitude: ' + centers_df['Latitude'].astype(str) + '<br>Longitude: ' + centers_df['Longitude'].astype(str)+'<br> <a href="https://www.gps-coordinates.net/street-view/@' + centers_df['Latitude'].astype(str) + ',' + centers_df['Longitude'].astype(str) + ',h237,p9,z1">Open Street View</a>'
        
    )

    # Create the layout for the map
    layout = go.Layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        hovermode='closest',
        mapbox=dict(
            accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
            center=dict(lat=center_lat, lon=center_lon),
            style='dark',
            zoom=zoom
        ),
        autosize=True
    )

    # Create the figure including both original data and cluster centers
    fig = go.Figure(data=[traces_centers], layout=layout)

    # Add a custom data URL to each marker
    for idx, row in centers_df.iterrows():
        lon = row['Longitude']
        lat = row['Latitude']
        url = f"https://www.gps-coordinates.net/street-view/@{lon},{lat},h237,p9,z1"
        fig.add_annotation(
            x=row['Longitude'],
            y=row['Latitude'],
            text=f'<a href="{url}" target="_blank">Open Street View</a>',
            showarrow=False,
            font=dict(color='white', size=10),
        )

    return fig


# Main function
def prediction():
    
    
    with st.sidebar:
        st.sidebar.title("Analytics Options")
        selected_analysis = option_menu(
            menu_title=None,  # Required
            options=["Black Spot Predictions", "Grey Zone Predictions","Heat Map"],  # Required
            # icons=["clock", "road", "map-marker", "sign", "walking"],  # Optional
            menu_icon="cast",  # Optional
            default_index=0,  # Optional
            key="analytics_option_menu",  # Unique key for this option menu
            styles={
                "container": {"padding": "5px", "background-color": "#111111"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px",
                    "--hover-color": "#cccccc",
                },
                "nav-link-selected": {"background-color": "#f63366"},
            }
        )

    # Display the appropriate analysis page based on the selection
    if selected_analysis == "Grey Zone Predictions":
        st.markdown("## Analysis of Black spots of accidents as well as predicting future grey zones.")
        district_options = ['All'] + list(df_lat_lon['DISTRICTNAME'].unique())
        selected_districts = st.sidebar.multiselect('Select District(s)', district_options, default=['All'])

    # Filter dataframe based on selected districts
        if 'All' in selected_districts:
            filtered_df = df_lat_lon
        else:
            filtered_df = df_lat_lon[df_lat_lon['DISTRICTNAME'].isin(selected_districts)]
        prediction_page_2(filtered_df)
    elif selected_analysis == "Black Spot Predictions":
        st.markdown("## Analysis of Black spots of accidents as well as predicting future black spots.")
        district_options = ['All'] + list(df_lat_lon['DISTRICTNAME'].unique())
        selected_districts = st.sidebar.multiselect('Select District(s)', district_options, default=['All'])

    # Filter dataframe based on selected districts
        if 'All' in selected_districts:
            filtered_df = df_lat_lon
        else:
            filtered_df = df_lat_lon[df_lat_lon['DISTRICTNAME'].isin(selected_districts)]

        spot_prediction_page(filtered_df)
    elif selected_analysis == "Heat Map":
        heat_map()
    else:
        st.warning(f"Unknown analytics option: {selected_analysis}")


