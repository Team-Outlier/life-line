import streamlit as st
from predict import create_Scatterplot_map
from streamlit_option_menu import option_menu
import pandas as pd

# CSS styling
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df_lat_lon = pd.read_excel('data/data_for_maps-88k.xlsx')

def prediction_page_2():
    st.title("## Prediction 2")
    # Add your content for the "Time Series" page here
    st.write("This is the Time Series prediction page.")

def spot_prediction_page():
    
    
    # Example of showing a map using data
    map_plotly = create_Scatterplot_map(df_lat_lon)
    st.plotly_chart(map_plotly, use_container_width=True)

# Main function
def main():
    js = "window.location.href = 'https://practice.geeksforgeeks.org/contest/job-a-thon-hiring-challenge-1';"
    html = f'<script>{js}</script>'
    st.markdown(html, unsafe_allow_html=True)
    st.markdown("## Analysis of Black spots of accidents as well as predicting future black spots")
    
    with st.sidebar:
        st.sidebar.title("Analytics Options")
        selected_analysis = option_menu(
            menu_title=None,  # Required
            options=["Black Spot Prediction", "Grey Spot Prediction","Heat map"],  # Required
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
    if selected_analysis == "Black Spot Prediction":
        prediction_page_2()
    elif selected_analysis == "Grey Spot Prediction":
        spot_prediction_page()
    else:
        st.warning(f"Unknown analytics option: {selected_analysis}")

if __name__ == '__main__':
    main()



