
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "cvmaxx_classifier.joblib"

model = joblib.load(MODEL_PATH)

print("Model:", type(model))
print("Number of features:", model.n_features_in_)
print("Booster feature names:")

try:
    print(model.booster_.feature_name())
except Exception as e:
    print("Could not retrieve feature names:", e)
