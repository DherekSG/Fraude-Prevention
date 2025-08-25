from fastapi import FastAPI
from pydantic import BaseModel
import logging
from pathlib import Path
import joblib
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "model.pkl"
model = joblib.load(MODEL_PATH)

app = FastAPI()

class Transaction(BaseModel):
    valor: float
    localizacao: str
    ip: str
    cartao: str

@app.post("/classify")
def classify(transaction: Transaction):
    df = pd.DataFrame([transaction.dict()])
    proba = model.predict_proba(df)[:, 1][0]
    is_fraud = proba >= 0.5
    logger.info("Transaction classified with probability %.4f", proba)
    return {"fraud_probability": proba, "is_fraud": is_fraud}
