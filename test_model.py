import joblib
import pandas as pd

def test_model_with_input(input_data, model_path=r'SecureSphere copy 3\ml-anomaly-detection\trained_model.pkl'):
    # Load the trained model
    try:
        model = joblib.load(model_path)  # Ensure model is loaded correctly
    except FileNotFoundError:
        print(f"Error: Model file '{model_path}' not found.")
        return

    # Define column names (same as the training dataset)
    feature_columns = [
        'Time_Taken', 'Failed_Attempts', 'IP_Change', 'Typing_Speed',
        'Device_Type', 'Browser_Type', 'Login_Hour', 'Weekend_Login'
    ]

    # Convert the input data to a DataFrame
    input_df = pd.DataFrame([input_data], columns=feature_columns)

    # Make a prediction
    prediction = model.predict(input_df)

    # Map the output to a human-readable label
    result = "Anomaly" if prediction[0] == 1 else "Normal"

    print(f"Testing with input: {input_data}")
    print(f"Prediction: {result}")


# Example input (matches the feature order used during training)
# Format: [Time_Taken, Failed_Attempts, IP_Change, Typing_Speed, Device_Type, Browser_Type, Login_Hour, Weekend_Login]
input_data = [8.5, 1, 5, 35.0, 0, 1, 10, 3]

# Test the model with the example input
if __name__ == "__main__":
    test_model_with_input(input_data)
