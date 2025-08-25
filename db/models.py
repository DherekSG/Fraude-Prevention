from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from sqlalchemy.sql import func

from db.database import Base


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, nullable=False)
    localizacao = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    cartao = Column(String, nullable=False)
    probabilidade_fraude = Column(Float, nullable=False)
    is_fraud = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
