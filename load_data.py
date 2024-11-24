import pandas as pd

def load_and_preview_data(file_path=r'SecureSphere copy 3\ml-anomaly-detection\synthetic_data.csv'):
    try:
        # Load the dataset
        data = pd.read_csv(file_path)

        # Display the first few rows
        print("\n--- Preview of the Dataset ---\n")
        print(data.head())

        # Display summary statistics
        print("\n--- Summary Statistics ---\n")
        print(data.describe())

        # Display class distribution
        print("\n--- Class Distribution ---\n")
        print(data['Anomaly'].value_counts())
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Please ensure it exists.")

# Load and preview the dataset when the script is run
if __name__ == "__main__":
    load_and_preview_data()
