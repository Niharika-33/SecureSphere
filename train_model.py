import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

def load_and_preview_data(file_path=r'SecureSphere copy 3\ml-anomaly-detection\synthetic_data.csv'):
    try:
        # Load the dataset
        data = pd.read_csv(file_path)

        # Label encoding for Device_Type and Browser_Type
        label_encoder = LabelEncoder()
        data['Device_Type'] = label_encoder.fit_transform(data['Device_Type'])
        data['Browser_Type'] = label_encoder.fit_transform(data['Browser_Type'])

        # Display the first few rows
        print("\n--- Preview of the Dataset ---\n")
        print(data.head())

        # Display summary statistics
        print("\n--- Summary Statistics ---\n")
        print(data.describe())

        # Display class distribution
        print("\n--- Class Distribution ---\n")
        print(data['Anomaly'].value_counts())

        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Please ensure it exists.")
        return None

# Train the model
def train_model(data):
    # Separate features and labels
    X = data.drop(columns=['Anomaly'])
    y = data['Anomaly']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print("\n--- Classification Report ---\n")
    print(classification_report(y_test, y_pred))

    return model

# Save the model
def save_model(model):
    joblib.dump(model,'ml-anomaly-detection/trained_model.pkl')  # Save with the correct path
    print("\nModel saved as 'ml-anomaly-detection/trained_model.pkl'.")

# Main function
if __name__ == "__main__":
    data = load_and_preview_data(r'SecureSphere copy 3\ml-anomaly-detection\synthetic_data.csv')
    if data is not None:
        model = train_model(data)
        save_model(model)