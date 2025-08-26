import os
from io import StringIO
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "raw", "transacoes_sinteticas.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

def load_data(path: str) -> pd.DataFrame:
    """Load dataset handling lines split across two rows."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    header = lines[0]
    rows = []
    for i in range(1, len(lines), 2):
        if i + 1 < len(lines):
            rows.append(lines[i].strip() + lines[i + 1].strip())
    csv_data = "\n".join([header] + rows)
    return pd.read_csv(StringIO(csv_data))

def prepare_data(df: pd.DataFrame):
    df["valor"] = df["valor"].astype(float)
    df["fraude"] = df["fraude"].astype(int)
    X = df[["valor", "localizacao", "ip", "cartao"]]
    y = df["fraude"]

    categorical_features = ["localizacao", "ip", "cartao"]
    numeric_features = ["valor"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", "passthrough", numeric_features),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    return X_train, X_test, y_train, y_test, preprocessor

def train_and_evaluate(X_train, X_test, y_train, y_test, preprocessor):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
    }
    for name, value in metrics.items():
        print(f"{name.capitalize()}: {value:.4f}")

    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
    return pipeline

def main():
    df = load_data(DATA_PATH)
    X_train, X_test, y_train, y_test, preprocessor = prepare_data(df)
    pipeline = train_and_evaluate(X_train, X_test, y_train, y_test, preprocessor)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Pipeline salvo em {MODEL_PATH}")

if __name__ == "__main__":
    main()
