import streamlit as st
import google.generativeai as genai
import pandas as pd
import altair as alt

def ai_response(highest_freq_values):
    # Configure the GenerativeAI API
    genai.configure(api_key="AIzaSyDhSOiqyuzXwAY6yjERzac81r0NivhZ0yc")

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    # Start a chat session
    chat_session = model.start_chat(history=[])

    # Convert dataframes to strings
    highest_freq_str = highest_freq_values.to_string(index=False)

    # Create prompt
    prompt = (
        f"This is my data for the district name and unit name refers to the unit in each district:\n\n"
        f"Each highest frequency column describes:\n{highest_freq_str}\n\n"
        f"I want to give analysis based on these highest frequency data and provide recommendations on actions needed. "
        f"Please give suggestions for improvement, focusing on 1.analysis, 2.actionable steps, and 3.locations for improvement in 3-4 bulletpoints each"
    )

    # Send input text and get response
    response = chat_session.send_message(prompt)

    return response.text

def load_data():
    df = pd.read_csv("G:/My Drive/Colab Notebooks/datasets/Accident_Report_PowerBI.csv")  # Replace with your file path
    return df

def suggestion():
    st.set_page_config(layout="wide")  # Set the layout to wide
    st.title("AI Suggestion System for Improvement Recommendation")

    # Load the data
    df = load_data()

    # Create two columns for the dropdown menus
    col1, col2 = st.columns([1, 1])

    # Column 1: Dropdown for selecting districts
    with col1:
        selected_district = st.selectbox("Select District", ["All"] + sorted(df["DISTRICTNAME"].unique().tolist()))

    # Column 2: Dropdown for selecting unit names within the selected district
    with col2:
        if selected_district != "All":
            district_df = df[df["DISTRICTNAME"] == selected_district]
            unit_names = ["All"] + sorted(district_df["UNITNAME"].unique().tolist())
            selected_unit = st.selectbox("Select Unit", unit_names)
        else:
            selected_unit = "All"

    # Filter the dataframe based on the selected district and unit
    if selected_district != "All":
        if selected_unit != "All":
            filtered_df = district_df[district_df["UNITNAME"] == selected_unit]
        else:
            filtered_df = district_df
    else:
        filtered_df = df

    # Display the filtered dataframe in an expander (minimized by default)
    with st.expander("Filtered Data", expanded=False):
        if not filtered_df.empty:
            filtered_df.reset_index(drop=True, inplace=True)
            st.write(filtered_df)
        else:
            st.write("No data to display.")
    
    # Split the layout into two columns for chart and table
    chart_col, table_col = st.columns([1, 1])
    
    with chart_col:
        st.header("Accident Trend Across Units in " + selected_district)
        if selected_district != "All":
            # Always use all units within the selected district
            comparison_data = district_df["UNITNAME"].value_counts().reset_index()
            comparison_data.columns = ['UNITNAME', 'count']
            
            # Create the bar chart using Altair
            chart = alt.Chart(comparison_data).mark_bar(color='white').encode(
                x=alt.X('UNITNAME', sort='-y', title='Unit Name'),
                y=alt.Y('count', title='Count'),
                tooltip=['UNITNAME', 'count']
            ).properties(
                width=400,
                height=400
            )
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("Please select a district to see the comparison chart.")
    
    with table_col:
        # AI input dataframe 
        if not filtered_df.empty:
            filtered_df.reset_index(drop=True, inplace=True)

            # Create a new dataframe for highest frequency values year-wise
            highest_freq_values_year_wise = filtered_df.groupby('Year').apply(lambda x: x.mode().iloc[0]).reset_index(drop=True)

            # Add the selected district and unit to the result
            highest_freq_values_year_wise['DISTRICTNAME'] = selected_district
            highest_freq_values_year_wise['UNITNAME'] = selected_unit

            # Display the highest frequency values year-wise
            st.write(f"### Most Significant Accidents in {selected_district}: {selected_unit} Year-wise")
            st.write(highest_freq_values_year_wise)

    # AI Response
    if not filtered_df.empty:
        st.write("### AI Suggestion:")
        response = ai_response(highest_freq_values_year_wise)
        st.write(response)

if __name__ == "__main__":
    suggestion()
