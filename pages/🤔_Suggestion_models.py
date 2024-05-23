import streamlit as st
from streamlit_option_menu import option_menu
from model.suggestion import suggestion
from model.top10features import top10feature



def main():
    # with st.sidebar:
    #     st.sidebar.title("Analytics Options")
    #     selected_analysis = option_menu(
    #         menu_title=None,  # Required
    #         options=["Temporal Analysis", "Road Type Analysis"],  # Required
    #         # icons=["clock", "road"],  # Optional
    #         menu_icon="cast",  # Optional
    #         default_index=0,  # Optional
    #         key="analytics_option_menu",  # Unique key for this option menu
    #         styles={
    #             "container": {"padding": "5px", "background-color": "#111111"},
    #             "icon": {"color": "orange", "font-size": "25px"},
    #             "nav-link": {
    #                 "font-size": "14px",
    #                 "text-align": "left",
    #                 "margin": "0px",
    #                 "padding": "10px",
    #                 "--hover-color": "#cccccc",
    #             },
    #             "nav-link-selected": {"background-color": "#f63366"},
    #         }
    #     )

    # # Display the appropriate analysis page based on the selection
    # if selected_analysis == "Temporal Analysis":
    #     suggestion_model1()
    # elif selected_analysis == "Road Type Analysis":
    #     suggestion_model2()
    # else:
    #     st.warning(f"Unknown analytics option: {selected_analysis}")
    s()


if __name__ == '__main__':
    main()




