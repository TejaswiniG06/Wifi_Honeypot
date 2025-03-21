import joblib
import pandas as pd

# Load trained model
try:
    model = joblib.load("wifi_risk_model.pkl")
except Exception as e:
    print(f"ERROR: Could not load model - {e}")

def analyze_risk(ssid, bssid, encryption):
    """Analyze risk score based on Wi-Fi encryption and model prediction."""
    
    # Mapping encryption types
    encryption_map = {'Open': 1, 'WEP': 2, 'WPA': 3, 'WPA2': 4, 'WPA3': 5}
    enc_value = encryption_map.get(encryption, 1)  # Default to Open

    # Prepare input data
    data = pd.DataFrame([[enc_value]], columns=["Encryption"])

    # Debug: Print model inputs
    print(f"DEBUG: Checking risk for {ssid} ({encryption}) → Enc Value: {enc_value}")

    try:
        # Get model prediction
        risk_prob = model.predict_proba(data)[0][1]  
        print(f"DEBUG: Model Probability: {risk_prob:.4f}")  # Show actual probability

        # Map probability to risk score
        risk_score = round(risk_prob * 100, 2)

        # Prevent risk from always being 100%
        return risk_score  # Max cap at 95%

    except Exception as e:
        print(f"ERROR: Model failed - {e}")
        return 50  # Default risk if model fails
