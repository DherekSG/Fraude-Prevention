import os
from pathlib import Path
import numpy as np
import joblib
from fastapi.testclient import TestClient


class DummyModel:
    def predict_proba(self, X):
        return np.array([[0.1, 0.9]] * len(X))


model_path = Path("model/model.pkl")
model_path.parent.mkdir(exist_ok=True)
joblib.dump(DummyModel(), model_path)

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
from api.main import app


def test_classify_endpoint():
    with TestClient(app) as client:
        payload = {
            "valor": 123.45,
            "localizacao": "Sao Paulo",
            "ip": "192.168.0.1",
            "cartao": "1234567890123456",
        }
        response = client.post("/classify", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert set(data.keys()) == {"fraud_probability", "is_fraud"}
        assert isinstance(data["fraud_probability"], float)
        assert isinstance(data["is_fraud"], bool)


def teardown_module(module):
    model_path.unlink(missing_ok=True)
    db_url = os.environ.get("DATABASE_URL", "")
    if db_url.startswith("sqlite:///"):
        db_path = Path(db_url.replace("sqlite:///", ""))
        if db_path.exists():
            db_path.unlink()
    os.environ.pop("DATABASE_URL", None)
