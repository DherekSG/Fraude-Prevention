from fastapi import FastAPI, Depends
from pydantic import BaseModel
import logging
from pathlib import Path
import joblib
import pandas as pd
from sqlalchemy.orm import Session

from db import models
from db.database import SessionLocal, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PIPELINE_PATH = Path(__file__).resolve().parents[1] / "model" / "model.pkl"
pipeline = joblib.load(PIPELINE_PATH)

app = FastAPI()


class Transaction(BaseModel):
    valor: float
    localizacao: str
    ip: str
    cartao: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/classify")
def classify(transaction: Transaction, db: Session = Depends(get_db)):
    df = pd.DataFrame([transaction.dict()])
    proba = pipeline.predict_proba(df)[:, 1][0]
    is_fraud = proba >= 0.5
    logger.info("Transaction classified with probability %.4f", proba)

    db_transacao = models.Transacao(
        valor=transaction.valor,
        localizacao=transaction.localizacao,
        ip=transaction.ip,
        cartao=transaction.cartao,
        probabilidade_fraude=proba,
        is_fraud=is_fraud,
    )
    db.add(db_transacao)
    db.commit()

    return {"fraud_probability": proba, "is_fraud": is_fraud}
