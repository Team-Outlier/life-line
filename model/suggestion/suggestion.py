import streamlit as st
import streamlit.components.v1 as stc
from model.suggestion.homepage import homepage
from streamlit_option_menu import option_menu


# Page configuration



def new_sidebar():
    with st.sidebar:
        st.sidebar.title("Suggestion Models")
        selected_analysis = option_menu(
            menu_title=None,  # Required
            options=["AI Recommendation", "Factor Evaluation Model"],  # Required
            # icons=["clock", "road"],  # Optional
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
    if selected_analysis == "AI Recommendation":
        homepage(0)
    elif selected_analysis == "Factor Evaluation Model":
        homepage(1)
    else:
        st.warning(f"Unknown analytics option: {selected_analysis}")




def suggestion():
    
        

    # Load Excel file


    # HomePage function
    new_sidebar()
