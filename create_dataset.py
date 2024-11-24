import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Define the function to generate synthetic data
def generate_synthetic_data():
    # Label Encoder for Device_Type and Browser_Type
    label_encoder = LabelEncoder()

    # Normal login behavior
    normal_data = pd.DataFrame({
        'Time_Taken': np.random.uniform(1, 10, 1000),  # Normal: 1–10 seconds
        'Failed_Attempts': np.random.choice([0, 1, 2], 1000, p=[0.7, 0.2, 0.1]),  # Mostly 0
        'IP_Change': np.random.choice([0], 1000),  # No IP change
        'Typing_Speed': np.random.uniform(60, 100, 1000),  # Normal typing speed
        'Device_Type': np.random.choice(['desktop', 'mobile'], 1000, p=[0.8, 0.2]),  # Mostly desktop
        'Browser_Type': np.random.choice(['Firefox', 'Chrome', 'Safari'], 1000, p=[0.5, 0.3, 0.2]),
        'Login_Hour': np.random.randint(6, 22, 1000),  # Daytime hours
        'Weekend_Login': np.random.choice([0, 1], 1000, p=[0.7, 0.3]),  # Mostly weekdays
        'Anomaly': 0  # Normal behavior
    })

    # Anomalous login behavior
    anomaly_data = pd.DataFrame({
        'Time_Taken': np.random.uniform(15, 30, 200),  # Slow login times
        'Failed_Attempts': np.random.randint(3, 5, 200),  # Multiple failed attempts
        'IP_Change': np.random.choice([1], 200),  # All IP changes
        'Typing_Speed': np.random.uniform(20, 50, 200),  # Slow typing
        'Device_Type': np.random.choice(['desktop', 'mobile'], 200, p=[0.5, 0.5]),  # Mixed devices
        'Browser_Type': np.random.choice(['Firefox', 'Chrome', 'Safari'], 200),
        'Login_Hour': np.random.randint(0, 24, 200),  # Includes odd hours
        'Weekend_Login': np.random.choice([0, 1], 200, p=[0.3, 0.7]),  # Majority on weekends
        'Anomaly': 1  # Anomalous behavior
    })

    # Label encoding for categorical variables
    normal_data['Device_Type'] = label_encoder.fit_transform(normal_data['Device_Type'])
    normal_data['Browser_Type'] = label_encoder.fit_transform(normal_data['Browser_Type'])
    
    anomaly_data['Device_Type'] = label_encoder.fit_transform(anomaly_data['Device_Type'])
    anomaly_data['Browser_Type'] = label_encoder.fit_transform(anomaly_data['Browser_Type'])

    # Combine and shuffle data
    full_data = pd.concat([normal_data, anomaly_data]).sample(frac=1).reset_index(drop=True)

    # Save to CSV
    full_data.to_csv('synthetic_data.csv', index=False)
    print("Synthetic data generated and saved as 'synthetic_data.csv'.")

# Generate the dataset when the script is run
if __name__ == "__main__":
    generate_synthetic_data()

