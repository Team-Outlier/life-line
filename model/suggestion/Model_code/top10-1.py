import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load the dataset
data = pd.read_csv('G:/My Drive/Colab Notebooks/datasets/Accident_Report_PowerBI.csv')

# Drop rows with missing values
data.dropna(inplace=True)

# Drop specified columns
columns_to_drop = ['DISTRICTNAME', 'UNITNAME', 'Year', 'Main_Cause', 'Hit_Run']
data.drop(columns=columns_to_drop, inplace=True)

# Iterate over all possible target variables
for target in data.columns:
    # Define features excluding the current target
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

    # Save the model to a pkl file named after the target variable
    model_filename = f'models/model_{target}.pkl'
    with open(model_filename, 'wb') as file:
        pickle.dump((model, label_encoders, features), file)

    print(f"Model for target variable '{target}' has been trained and saved as {model_filename}")
