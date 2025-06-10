from faker import Faker
import random
import pandas as pd
from datetime import datetime, timedelta
import os

fake = Faker()

def gerar_transacao(fraude=False):
    return {
        "id_transacao": fake.uuid4(),
        "nome": fake.name(),
        "email": fake.email(),
        "cartao": fake.credit_card_number(),
        "data": fake.date_time_between(start_date="-30d", end_date="now"),
        "valor": round(random.uniform(10.0, 5000.0), 2),
        "localizacao": fake.city(),
        "ip": fake.ipv4(),
        "fraude": int(fraude)
    }

def gerar_dados(qtd_legit=900, qtd_fraude=100):
    dados = []
    
    for _ in range(qtd_legit):
        dados.append(gerar_transacao(fraude=False))
    for _ in range(qtd_fraude):
        dados.append(gerar_transacao(fraude=True))

    df = pd.DataFrame(dados)
    df = df.sample(frac=1).reset_index(drop=True)  # embaralhar
    return df

if __name__ == "__main__":
    df = gerar_dados()

    os.makedirs("data/raw", exist_ok=True)
    caminho_arquivo = "data/raw/transacoes_sinteticas.csv"
    df.to_csv(caminho_arquivo, index=False)
    
    print(f"✅ Arquivo gerado com {len(df)} transações em: {caminho_arquivo}")
