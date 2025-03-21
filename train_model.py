import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load dataset
df = pd.read_csv("training_data.csv")

# Ensure dataset balance
print("Dataset Class Distribution:\n", df["Risk"].value_counts())

# Convert categorical data to numeric
encryption_map = {'Open': 1, 'WEP': 2, 'WPA2': 3}
df['Encryption'] = df['Encryption'].map(encryption_map)

# Prepare dataset
X = df[['Encryption']]
y = df['Risk']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "wifi_risk_model.pkl")

print("✅ Model trained & saved as wifi_risk_model.pkl")
