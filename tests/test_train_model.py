from sklearn.pipeline import Pipeline
from model.train import load_data, prepare_data, train_and_evaluate, DATA_PATH

def test_train_and_evaluate_metrics(capsys):
    df = load_data(DATA_PATH)
    X_train, X_test, y_train, y_test, preprocessor = prepare_data(df)
    pipeline = train_and_evaluate(X_train, X_test, y_train, y_test, preprocessor)
    captured = capsys.readouterr()
    metrics = {}
    for line in captured.out.strip().splitlines():
        if ':' in line:
            name, value = line.split(':')
            metrics[name.strip().lower()] = float(value.strip())
    for key in ['accuracy', 'precision', 'recall', 'f1_score']:
        assert key in metrics
        assert 0.0 <= metrics[key] <= 1.0
    assert isinstance(pipeline, Pipeline)
    assert hasattr(pipeline.named_steps['model'], 'coef_')
