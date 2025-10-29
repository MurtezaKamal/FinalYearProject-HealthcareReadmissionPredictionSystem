# utils/model_loader.py
import joblib

def load_model(path):
    try:
        return joblib.load(path)
    except Exception as e:
        raise FileNotFoundError(f"Failed to load model at {path}: {e}")
