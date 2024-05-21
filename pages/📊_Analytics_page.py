import streamlit as st
from streamlit_option_menu import option_menu

# Define functions for each analysis type
def analytics_page_1():
    st.title("Temporal Analysis")
    st.components.v1.iframe(
        src="https://app.powerbi.com/view?r=eyJrIjoiYjU3ZDkzMTAtZDEyYy00MTFmLWJjZGItYzA0YzcxMDJhZTYxIiwidCI6IjUyMjVmOWFhLWJiZjctNDA2MS04YTdhLTI0OGM3M2MyNTRhOCJ9",
        width=1200,
        height=800,
        scrolling=True
    )

def analytics_page_2():
    st.title("Road Type Analysis")
    st.components.v1.iframe(
        src="https://app.powerbi.com/view?r=eyJrIjoiODAwZjYwNTYtNWI1NC00ZjEzLWEyNjItZWU4YjE2MjZjMjExIiwidCI6IjUyMjVmOWFhLWJiZjctNDA2MS04YTdhLTI0OGM3M2MyNTRhOCJ9",
        width=1200,
        height=800,
        scrolling=True
    )
    st.write("This is the content for Road Type Analysis.")
#<iframe title="Landmark_Vicinity_Analysis" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiN2E2NGMxNDAtNjQ1MC00NjgwLWI4NGItZTMyMzgyOGZiYTVkIiwidCI6IjUyMjVmOWFhLWJiZjctNDA2MS04YTdhLTI0OGM3M2MyNTRhOCJ9" frameborder="0" allowFullScreen="true"></iframe>
def analytics_page_3():
    st.title("Landmark Analysis")
    st.components.v1.iframe(
        src="https://app.powerbi.com/view?r=eyJrIjoiN2E2NGMxNDAtNjQ1MC00NjgwLWI4NGItZTMyMzgyOGZiYTVkIiwidCI6IjUyMjVmOWFhLWJiZjctNDA2MS04YTdhLTI0OGM3M2MyNTRhOCJ9",
        width=1200,
        height=800,
        scrolling=True
    )

def analytics_page_4():
    st.title("Road Signage Analysis")
    st.components.v1.iframe(
        src="https://app.powerbi.com/view?r=eyJrIjoiYWNkZjNkMzctNDUzNy00ZGU2LTk5NGEtMWU2YTM4YWUzOTIwIiwidCI6IjUyMjVmOWFhLWJiZjctNDA2MS04YTdhLTI0OGM3M2MyNTRhOCJ9",
        width=1200,
        height=800,
        scrolling=True
    )

def analytics_page_5():
    st.title("Pedestrian Analysis")
    st.components.v1.iframe(
        src="https://app.powerbi.com/view?r=eyJrIjoiYWQ5NDlhMjUtOWI0NS00MGU4LTkwNDYtNTc0NjQ3Nzg2NmE3IiwidCI6IjUyMjVmOWFhLWJiZjctNDA2MS04YTdhLTI0OGM3M2MyNTRhOCJ9",
        width=1200,
        height=800,
        scrolling=True
    )

# Main function
def main():
    st.set_page_config(layout="wide")
    
    with st.sidebar:
        st.sidebar.title("Analytics Options")
        selected_analysis = option_menu(
            menu_title=None,  # Required
            options=["Temporal Analysis", "Road Type Analysis", "Landmark Analysis", "Road Signage Analysis", "Pedestrian Analysis"],  # Required
            # icons=["clock", "road", "map-marker", "sign", "walking"],  # Optional
            menu_icon="cast",  # Optional
            default_index=0,  # Optional
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
    if selected_analysis == "Temporal Analysis":
        analytics_page_1()
    elif selected_analysis == "Road Type Analysis":
        analytics_page_2()
    elif selected_analysis == "Landmark Analysis":
        analytics_page_3()
    elif selected_analysis == "Road Signage Analysis":
        analytics_page_4()
    elif selected_analysis == "Pedestrian Analysis":
        analytics_page_5()
    else:
        st.warning(f"Unknown analytics option: {selected_analysis}")

if __name__ == '__main__':
    main()
