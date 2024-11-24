import joblib
import time
import random

# Load the trained model
def load_model(model_path='trained_model.pkl'):
    try:
        model = joblib.load(model_path)
        print("Model loaded successfully.")
        return model
    except FileNotFoundError:
        print(f"Error: Model file '{model_path}' not found.")
        return None

# Simulate real-time login events
def simulate_login_event():
    # Generate random login data for testing
    event = [
        random.uniform(1, 30),  # Time_Taken
        random.randint(0, 4),  # Failed_Attempts
        random.randint(0, 1),  # IP_Change
        random.uniform(20, 100),  # Typing_Speed
        random.randint(0, 1),  # Device_Type
        random.randint(0, 2),  # Browser_Type
        random.randint(0, 23),  # Login_Hour
        random.randint(0, 1)   # Weekend_Login
    ]
    return event

# Real-time detection loop
def realtime_detection(model):
    print("\n--- Starting Real-Time Anomaly Detection ---\n")
    while True:
        login_event = simulate_login_event()
        prediction = model.predict([login_event])
        print(f"Login Event: {login_event} -> {'Anomaly' if prediction[0] == 1 else 'Normal'}")
        time.sleep(2)  # Simulate a delay for real-time detection

# Run real-time detection
if __name__ == "__main__":
    model = load_model()
    if model:
        realtime_detection(model)
