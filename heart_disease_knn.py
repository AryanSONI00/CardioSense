import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from ucimlrepo import fetch_ucirepo

# Define essential features to keep
SELECTED_FEATURES = [
    'age',          # Age
    'sex',          # Sex
    'cp',           # Chest Pain Type
    'trestbps',     # Resting Blood Pressure
    'chol',         # Cholesterol
    'thalach',      # Maximum Heart Rate
    'exang'         # Exercise Induced Angina
]

# Load and preprocess data
def load_data():
    # Fetch dataset from UCI repository
    heart_disease = fetch_ucirepo(id=45)

    # Get features and targets
    df = pd.DataFrame(heart_disease.data.features, columns=heart_disease.data.features_names)
    df['target'] = (heart_disease.data.targets > 0).astype(int)

    # Keep only selected features
    df = df[SELECTED_FEATURES + ['target']]

    return df

def preprocess_data(df):
    # Categorical features to one-hot encode
    categorical_features = ['cp']  # Only chest pain type remains categorical

    # One-hot encode categorical features
    df_encoded = pd.get_dummies(df, columns=categorical_features)

    # Split features and target
    X = df_encoded.drop('target', axis=1)
    y = df_encoded['target']

    # Save feature names for later use
    with open('feature_names.pkl', 'wb') as f:
        pickle.dump(X.columns.tolist(), f)

    return X, y

def train_model(X, y):
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train KNN model
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)

    # Save the model and scaler
    with open('knn_model.pkl', 'wb') as f:
        pickle.dump((knn, scaler), f)

    # Make predictions
    y_pred = knn.predict(X_test_scaled)

    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Create and save confusion matrix visualization
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig('confusion_matrix.png')
    plt.close()

    return knn, scaler

def main():
    print("Loading data...")
    df = load_data()

    print("Preprocessing data...")
    X, y = preprocess_data(df)

    print("Training model...")
    knn, scaler = train_model(X, y)

    print("\nModel training completed! Files saved:")
    print("- knn_model.pkl (model and scaler)")
    print("- feature_names.pkl (feature names)")
    print("- confusion_matrix.png (confusion matrix visualization)")

if __name__ == "__main__":
    main()
