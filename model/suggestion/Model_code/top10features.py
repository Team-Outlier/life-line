import pandas as pd
import streamlit as st
import pickle
import matplotlib.pyplot as plt
import google.generativeai as genai
import os
import time

# Streamlit configuration for dark theme
st.set_page_config(layout="wide")
plt.style.use('dark_background')

# Load the dataset
data = pd.read_csv('G:/My Drive/Colab Notebooks/datasets/Accident_Report_PowerBI.csv')

# Drop rows with missing values
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
    model_filename = f'models/model_{target}.pkl'
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
        genai.configure(api_key="AIzaSyDhSOiqyuzXwAY6yjERzac81r0NivhZ0yc")  # Replace with your actual API key
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
