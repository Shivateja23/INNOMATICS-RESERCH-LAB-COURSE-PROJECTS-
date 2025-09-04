import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

# To run this app, you need a 'Body_Performance.csv' file in the same directory.
# This function is cached to prevent re-loading the data every time.
@st.cache_data
def load_data():
    if not os.path.exists("Body_Performance.csv"):
        st.error("Error: 'Body_Performance.csv' not found. Please place the file in the same directory as this script.")
        st.stop()
    return pd.read_csv("Body_Performance.csv")

# This function preprocesses the data and trains the model, and is also cached for efficiency.
# @st.cache_resource tells Streamlit to only run this once.
@st.cache_resource
def preprocess_and_train(df):
    le = LabelEncoder()
    # Create a copy to avoid SettingWithCopyWarning
    df_copy = df.copy()

    # Drop the "Unnamed: 0" column if it exists, which is a common CSV artifact.
    df_copy = df_copy.drop('Unnamed: 0', axis=1, errors='ignore')

    # Explicitly rename the columns to ensure consistency with the user input function.
    # This is the most reliable way to avoid the ValueError.
    df_copy.columns = ['age', 'gender', 'height_cm', 'weight_kg', 'body_fat', 'diastolic', 'systolic',
                      'grip_force', 'sit_and_bend_forward_cm', 'sit_ups_counts', 'broad_jump_cm', 'performance']
    
    # Use the now-standardized 'gender' column for label encoding
    df_copy['gender'] = le.fit_transform(df_copy['gender'])
    
    # Drop 'performance' and other columns not used for training
    X = df_copy.drop('performance', axis=1)
    y = df_copy['performance']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train the model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train_scaled, y_train)
    
    return model, scaler, X_train_scaled, X_test_scaled, y_train, y_test

# Streamlit application
st.title("Body Performance Classification App")
st.sidebar.title("Navigation")

# Load and preprocess data only once at the beginning of the script run
data = load_data()
model, scaler, X_train, X_test, y_train, y_test = preprocess_and_train(data.copy())

# Load and display data
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(data)

# Exploratory Data Analysis (EDA)
if st.sidebar.checkbox("Show EDA"):
    st.subheader("Exploratory Data Analysis")
    st.write("Dataset Shape:", data.shape)
    st.write("Summary Statistics:")
    st.write(data.describe())

    st.subheader("Feature Correlations")
    fig, ax = plt.subplots()
    sns.heatmap(data.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# Train and evaluate a model
if st.sidebar.checkbox("Show Model Evaluation"):
    st.subheader("Model Evaluation")

    # Predictions
    y_pred = model.predict(X_test)

    # Results
    st.write("Classification Report:")
    st.text(classification_report(y_test, y_pred))
    st.write("Accuracy:", accuracy_score(y_test, y_pred))

# User input for prediction
if st.sidebar.checkbox("Make Predictions", value=True):
    st.subheader("Make Predictions")

    def user_input():
        age = st.number_input("Age", min_value=0, max_value=100, value=25)
        gender = st.selectbox("Gender", options=['Male', 'Female'])
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        body_fat = st.number_input("Body Fat (%)", min_value=5.0, max_value=50.0, value=20.0)
        diastolic = st.number_input("Diastolic BP", min_value=50.0, max_value=150.0, value=80.0)
        systolic = st.number_input("Systolic BP", min_value=90.0, max_value=200.0, value=120.0)
        grip_force = st.number_input("Grip Force", min_value=0.0, max_value=100.0, value=50.0)
        sit_bend = st.number_input("Sit & Bend Forward (cm)", min_value=-50.0, max_value=50.0, value=10.0)
        sit_up = st.number_input("Sit Up Counts", min_value=0, max_value=100, value=30)
        broad_jump = st.number_input("Broad Jump (cm)", min_value=0.0, max_value=300.0, value=200.0)

        # Encode gender to match the training data format
        gender_encoded = 1 if gender == 'Male' else 0

        # Create a DataFrame with a single row. The column names here are
        # hardcoded to perfectly match the cleaned names used for training.
        input_data = pd.DataFrame([[age, gender_encoded, height, weight, body_fat, diastolic, systolic, grip_force, sit_bend, sit_up, broad_jump]],
                                  columns=['age', 'gender', 'height_cm', 'weight_kg', 'body_fat', 'diastolic', 'systolic', 'grip_force', 'sit_and_bend_forward_cm', 'sit_ups_counts', 'broad_jump_cm'])
        
        return input_data

    user_data = user_input()

    if st.button("Predict Performance"):
        # The model and scaler are already trained and cached at the start, so we can reuse them.
        scaled_input = scaler.transform(user_data)
        prediction = model.predict(scaled_input)
        st.write("Predicted Performance:", prediction[0])
