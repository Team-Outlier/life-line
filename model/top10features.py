import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import google.generativeai as genai

# Streamlit configuration for dark theme
st.set_page_config(layout="wide")
plt.style.use('dark_background')

def top10feature():
    # Load the dataset
    data = pd.read_csv('G:/My Drive/Colab Notebooks/datasets/Accident_Report_PowerBI.csv')

    # Drop rows with missing values
    data.dropna(inplace=True)

    # Drop specified columns
    columns_to_drop = ['DISTRICTNAME', 'UNITNAME', 'Year', 'Main_Cause', 'Hit_Run']
    data.drop(columns=columns_to_drop, inplace=True)

    # Streamlit app
    st.title("Most Impactful Factors Analysis")
    st.write("Select the target variable from the dropdown list.")

    # Dropdown list for target variable
    target = st.selectbox("Select Target Variable:", options=data.columns)

    # Validate the target selection
    if target not in data.columns:
        st.error("Please select a valid target variable.")
    else:
        # Define X and y
        features = [col for col in data.columns if col != target]
        X = data[features]
        y = data[target]

        # Encoding categorical variables
        label_encoders = {}
        for column in X.columns:
            label_encoders[column] = LabelEncoder()
            X[column] = label_encoders[column].fit_transform(X[column])

        # Splitting the dataset into train, test, and validation sets
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=2/3, random_state=42)

        # Training the decision tree classifier
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)

        # Extract feature importances
        feature_importances = model.feature_importances_

        # Sort the feature importances and feature names
        sorted_indices = feature_importances.argsort()[-10:]  # Top 10 features
        sorted_features = [features[i] for i in sorted_indices]
        sorted_importances = feature_importances[sorted_indices]

        # Find the most frequent value for each of the top features
        most_frequent_values = {}
        for feature in sorted_features:
            most_frequent_values[feature] = data[feature].mode()[0]

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

        # Create the model
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

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            safety_settings=safety_settings,
            generation_config=generation_config,
        )

        # Start a chat session
        chat_session = model.start_chat(history=[])

        # Create prompt
        feature_details = "\n".join([f"{feature}: Importance {importance:.4f}, Most Frequent Value {most_frequent_values[feature]}" 
                                    for feature, importance in zip(sorted_features, sorted_importances)])

        prompt = (
            f"Here are the top 10 features impacting the target variable '{target}':\n\n"
            f"{feature_details}\n\n"
            "Based on these features, their importances, and their most frequent values, please provide suggestions for improvement. "
            "Focus on 1. Analysis, 2. Actionable steps, and 3. Locations for improvement in 3-4 bullet points each."
        )

        # Send input text and get response
        response = chat_session.send_message(prompt)

        # Display AI Response
        st.write("### AI Suggestion:")
        st.write(response.text)

if __name__ == "__main__":
    top10feature()