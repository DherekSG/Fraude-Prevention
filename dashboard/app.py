import io
from typing import Optional

import pandas as pd
import requests
import streamlit as st
import plotly.express as px

DATA_SOURCE = st.secrets.get("DATA_SOURCE", "data/raw/transacoes_sinteticas.csv")


@st.cache_data
def load_data(source: Optional[str] = None) -> pd.DataFrame:
    """Load transactions from a CSV file or an HTTP endpoint."""
    src = source or DATA_SOURCE
    if src.startswith("http"):
        response = requests.get(src, timeout=10)
        response.raise_for_status()
        return pd.read_csv(io.StringIO(response.text))
    return pd.read_csv(src)


def main() -> None:
    st.title("Dashboard de Detecção de Fraudes")
    df = load_data()

    total_transacoes = len(df)
    fraudes = int(df["fraude"].sum())
    legitimas = total_transacoes - fraudes

    st.subheader("Métricas Gerais")
    col1, col2, col3 = st.columns(3)
    col1.metric("Transações", total_transacoes)
    col2.metric("Fraudes", fraudes)
    col3.metric("Legítimas", legitimas)

    st.subheader("Visualizações")
    contagem = pd.DataFrame({"tipo": ["Fraudes", "Legítimas"], "quantidade": [fraudes, legitimas]})
    st.plotly_chart(px.bar(contagem, x="tipo", y="quantidade", title="Fraudes vs. Legítimas"), use_container_width=True)

    df["data"] = pd.to_datetime(df["data"])
    serie_tempo = df.set_index("data")["fraude"].resample("D").sum().reset_index()
    st.plotly_chart(px.line(serie_tempo, x="data", y="fraude", title="Fraudes por Dia"), use_container_width=True)


if __name__ == "__main__":
    main()
