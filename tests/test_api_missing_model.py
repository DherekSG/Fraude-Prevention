import os
from pathlib import Path
import importlib
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
model_path = Path("model/model.pkl")
model_path.unlink(missing_ok=True)

import api.main
app = importlib.reload(api.main).app


def test_classify_without_model():
    with TestClient(app) as client:
        payload = {
            "valor": 123.45,
            "localizacao": "Sao Paulo",
            "ip": "192.168.0.1",
            "cartao": "1234567890123456",
        }
        response = client.post("/classify", json=payload)
        assert response.status_code == 500
        assert response.json() == {
            "detail": "Model not found. Please train and provide the model file before starting the API."
        }


def teardown_module(module):
    db_url = os.environ.get("DATABASE_URL", "")
    if db_url.startswith("sqlite:///"):
        db_path = Path(db_url.replace("sqlite:///", ""))
        if db_path.exists():
            db_path.unlink()
    os.environ.pop("DATABASE_URL", None)
