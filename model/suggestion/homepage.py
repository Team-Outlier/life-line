import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
import pickle
import matplotlib.pyplot as plt
import altair as alt
from streamlit_option_menu import option_menu
API_KEY = "AIzaSyDViJruGVLEalCj6-GF00O35lUJnVhVjk0"

def ai_response_model1(highest_freq_values):
    # Configure the GenerativeAI API
    
    genai.configure(api_key=API_KEY)

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
    data = pd.read_csv("data/Accident_Report_PowerBI.csv")  # Replace with your file path
    return data


def homepage(input):
    data = load_data()
    if input==0:
        st.title("AI Suggestion System for Improvement Recommendation")

        # Load the data
        

        # Create two columns for the dropdown menus
        col1, col2 = st.columns([1, 1])

        # Column 1: Dropdown for selecting districts
        with col1:
            selected_district = st.selectbox("Select District", ["All"] + sorted(data["DISTRICTNAME"].unique().tolist()))

        # Column 2: Dropdown for selecting unit names within the selected district
        with col2:
            if selected_district != "All":
                district_df = data[data["DISTRICTNAME"] == selected_district]
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
            filtered_df = data

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
            with st.spinner('Generating AI suggestions...'):
                    # Send input text and get response
                    response = ai_response_model1(highest_freq_values_year_wise)
            
            st.write(response)
    else:
        # Drop rows with missing values
        
        plt.style.use('dark_background')

        data.dropna(inplace=True)

        # Drop specified columns
        columns_to_drop = ['DISTRICTNAME', 'UNITNAME', 'Year', 'Main_Cause', 'Hit_Run']
        data.drop(columns=columns_to_drop, inplace=True)

        # Streamlit app
        st.title("Most Impactful Factors Analysis and Suggestion")

        # Dropdown list for target variable
        target = st.selectbox("Select Target Variable:", options=data.columns)

        # Validate the target selection
        if target not in data.columns:
            st.error("Please select a valid target variable.")
        else:
            # Load the model from the pkl file named after the selected target variable
            model_filename = f'data/models/model_{target}.pkl'
            if not os.path.exists(model_filename):
                st.error(f"No model found for target variable '{target}'.")
            else:
                with open(model_filename, 'rb') as file:
                    model, label_encoders, features = pickle.load(file)

                # Define X and y
                X = data[features]
                y = data[target]

                # Encoding categorical variables using the loaded encoders
                for column in X.columns:
                    X[column] = label_encoders[column].transform(X[column])

                # Extract feature importances
                feature_importances = model.feature_importances_

                # Sort the feature importances and feature names
                sorted_indices = feature_importances.argsort()[-10:]  # Top 10 features
                sorted_features = [features[i] for i in sorted_indices]
                sorted_importances = feature_importances[sorted_indices]

                # Find the most frequent value and distinct values for each of the top features
                feature_details = []
                for feature in sorted_features:
                    most_frequent_value = data[feature].mode()[0]
                    distinct_values = data[feature].unique()
                    feature_details.append({
                        "feature": feature,
                        "importance": feature_importances[features.index(feature)],
                        "most_frequent_value": most_frequent_value,
                        "distinct_values": distinct_values
                    })

                # Plot feature importances
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.barh(sorted_features, sorted_importances, color='white')
                ax.set_xlabel('Feature Importance', color='white')
                ax.set_ylabel('Feature', color='white')
                ax.set_title('Top 10 Feature Importance Analysis', color='white')

                # Set the axis and tick colors
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                # Display the plot
                st.pyplot(fig)

                # Configure the Generative AI API
                genai.configure(api_key=API_KEY)  # Replace with your actual API key
                generation_config = {
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 64,
                    "max_output_tokens": 8192,
                    "response_mime_type": "text/plain",
                }

                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                ]

                model_ai = genai.GenerativeModel(
                    model_name="gemini-1.5-pro-latest",
                    safety_settings=safety_settings,
                    generation_config=generation_config,
                )

                # Start a chat session
                chat_session = model_ai.start_chat(history=[])

                # Create prompt
                feature_detail_strings = [
                    f"{feature['feature']}: Importance {feature['importance']:.4f}, Most Frequent Value {feature['most_frequent_value']}, "
                    f"Distinct Values: {', '.join(map(str, feature['distinct_values']))}"
                    for feature in feature_details
                ]

                prompt = (
                    f"Here are the top 10 features impacting the target variable '{target}':\n\n"
                    f"{''.join(feature_detail_strings)}\n\n"
                    "Based on these features, their importances, their most frequent values, and distinct values, please provide suggestions for improvement in each factor in 1-2 sentences each."
                )

                # Display the loading spinner while waiting for the AI response
                with st.spinner('Generating AI suggestions...'):
                    # Send input text and get response
                    response = chat_session.send_message(prompt)

                # Display AI Response
                st.write(response.text)
