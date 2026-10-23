from pathlib import Path
import joblib
import numpy as np

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "risk_model.joblib"
MODEL_VERSION = "1.0.0"
_model = None

def load_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError("Model artifact not found. Run: python scripts/train_model.py")
        _model = joblib.load(MODEL_PATH)
    return _model

def predict(features: dict) -> tuple[int, float]:
    model = load_model()
    ordered = np.array([[features['age'], features['systolic'], features['diastolic'], features['glucose'], features['bmi']]], dtype=float)
    predicted_class = int(model.predict(ordered)[0])
    probability = float(model.predict_proba(ordered)[0][1])
    return predicted_class, probability
