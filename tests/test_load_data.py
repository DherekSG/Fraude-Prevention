import csv
import pandas as pd
from model.train import load_data

def test_load_data_handles_newline(tmp_path):
    data = {
        "id_transacao": ["1"],
        "nome": ["Nome Teste"],
        "email": ["a@a.com"],
        "cartao": ["123456"],
        "data": ["2025-01-01"],
        "valor": [100.0],
        "localizacao": ["Linha\nQuebra"],
        "ip": ["127.0.0.1"],
        "fraude": [0],
    }
    df = pd.DataFrame(data)
    file = tmp_path / "dados.csv"
    df.to_csv(file, index=False, quoting=csv.QUOTE_MINIMAL)
    loaded = load_data(str(file))
    assert loaded.loc[0, "localizacao"] == "Linha\nQuebra"
    assert len(loaded) == 1
    assert list(loaded.columns) == list(df.columns)
