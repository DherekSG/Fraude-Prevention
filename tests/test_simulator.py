import pandas as pd
from simulator.generate import gerar_dados


def test_generate_default_volume():
    df = gerar_dados()
    assert len(df) == 1000
    assert df["fraude"].sum() == 100


def test_generate_fields_presence():
    df = gerar_dados(1, 1)
    expected_columns = {"id_transacao", "nome", "email", "cartao", "data", "valor", "localizacao", "ip", "fraude"}
    assert set(df.columns) == expected_columns
