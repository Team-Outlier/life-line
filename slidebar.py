import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

import pandas as pd



def sideBar():

    
    df_lat_lon = pd.read_excel('data/data_for_maps-88k.xlsx')

    with st.sidebar:
        
        

        # File uploader in the sidebar
        data = st.file_uploader("Upload a Dataset", type=["csv", "xlsx", "xls"])
        if data is not None:
            if data.name.endswith('.csv'):
                df_lat_lon = pd.read_csv(data)
            elif data.name.endswith(('.xlsx', '.xls')):
                df_lat_lon = pd.read_excel(data)
        else:
            df_lat_lon = pd.read_excel('data/data_for_maps-88k.xlsx')

        # Year selection
        year_list = list(df_lat_lon.Year.unique())[::-1]
        selected_year = st.selectbox('Select a year', ['All']+year_list)
        
        # Filter data by selected year
        if selected_year != 'All':
            df_lat_lon_filtered = df_lat_lon[df_lat_lon['Year'] == selected_year]
        else :
            df_lat_lon_filtered = df_lat_lon

        # District selection
        district_list = list(df_lat_lon_filtered['DISTRICTNAME'].unique())
        selected_district = st.selectbox('Select a district', ['All'] + district_list)

        # Filter data by selected district if a specific district is selected
        if selected_district != 'All':
            df_lat_lon_filtered = df_lat_lon_filtered[df_lat_lon_filtered['DISTRICTNAME'] == selected_district]

        color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


        # Sidebar menu for page navigation
        # selected = option_menu(
        #     menu_title="Menu",
        #     options=["Home", "Predicted Spot", "Analytics","Suggestion Models"],
        #     icons=["house", "eye", "bar-chart","eye"],
        #     menu_icon="cast",
        #     default_index=0,
        # )

        # Nested menu for Analytics
        # if selected == "Analytics":
        #     analytics_option = option_menu(
        #         menu_title="Analytics",
        #         options=["Temporal Analysis", "Road Type Analysis", "Landmark Analysis", "Road Signage Analysis","Pedestrian Analysis"],
        #         icons=["chart-line", "chart-pie", "chart-bar", "chart-area","chart-bar"],
        #         menu_icon="cast",
        #         default_index=0,
        #     )
        #     return df_lat_lon_filtered, selected_district,selected_color_theme, analytics_option
        
        # if selected =="Suggestion Models":
        #     suggestion_models_option = option_menu(
        #         menu_title="Suggestion Models",
        #         options=["Suggestion Model 1", "Suggestion Model 2"],
        #         icons=["chart-line","chart-pie"],
        #         menu_icon="cast",
        #         default_index=0,

        #     )

    return df_lat_lon_filtered,selected_district,selected_color_theme, None