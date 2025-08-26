from faker import Faker
import random
import pandas as pd
import os
import argparse
import csv
from typing import Any, Optional

fake = Faker()

def gerar_transacao(fraude: bool = False) -> dict[str, Any]:
    """Gera uma transação sintética.

    Args:
        fraude: Indica se a transação deve ser marcada como fraude.

    Returns:
        Dicionário contendo os dados da transação.
    """

    return {
        "id_transacao": fake.uuid4(),
        "nome": fake.name(),
        "email": fake.email(),
        "cartao": fake.credit_card_number(),
        "data": fake.date_time_between(start_date="-30d", end_date="now"),
        "valor": round(random.uniform(10.0, 5000.0), 2),
        "localizacao": fake.city(),
        "ip": fake.ipv4(),
        "fraude": int(fraude),
    }

def gerar_dados(
    qtd_legit: int = 900,
    qtd_fraude: int = 100,
    seed: Optional[int] = None,
) -> pd.DataFrame:
    """Gera um ``DataFrame`` embaralhado com transações sintéticas.

    Args:
        qtd_legit: Quantidade de transações legítimas a gerar.
        qtd_fraude: Quantidade de transações fraudulentas a gerar.
        seed: Valor de seed para garantir reprodutibilidade.

    Returns:
        ``DataFrame`` com as transações geradas.
    """

    if seed is not None:
        random.seed(seed)
        fake.seed_instance(seed)

    dados = []

    for _ in range(qtd_legit):
        dados.append(gerar_transacao(fraude=False))
    for _ in range(qtd_fraude):
        dados.append(gerar_transacao(fraude=True))

    df = pd.DataFrame(dados)
    df = df.sample(frac=1).reset_index(drop=True)  # embaralhar
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de transações sintéticas")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed para reprodutibilidade",
    )
    args = parser.parse_args()

    df = gerar_dados(seed=args.seed)

    os.makedirs("data/raw", exist_ok=True)
    caminho_arquivo = "data/raw/transacoes_sinteticas.csv"
    df.to_csv(caminho_arquivo, index=False, quoting=csv.QUOTE_MINIMAL)

    print(f"✅ Arquivo gerado com {len(df)} transações em: {caminho_arquivo}")
