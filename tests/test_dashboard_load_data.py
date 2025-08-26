import pandas as pd
import requests


def _setup_secrets(tmp_path):
    import streamlit.config as config
    secrets_file = tmp_path / "secrets.toml"
    secrets_file.write_text("")
    config.set_option("secrets.files", [str(secrets_file)])


def test_load_data_local(tmp_path):
    _setup_secrets(tmp_path)
    from dashboard.app import load_data
    df = pd.DataFrame({'col':[1,2],'fraude':[0,1]})
    file = tmp_path / 'data.csv'
    df.to_csv(file, index=False)
    loaded = load_data(str(file))
    pd.testing.assert_frame_equal(loaded, df)


def test_load_data_remote(tmp_path, monkeypatch):
    _setup_secrets(tmp_path)
    from dashboard.app import load_data
    csv_text = 'col,fraude\n1,0\n2,1\n'

    class MockResponse:
        def __init__(self, text):
            self.text = text
        def raise_for_status(self):
            pass
    def mock_get(url, timeout=10):
        return MockResponse(csv_text)
    monkeypatch.setattr(requests, 'get', mock_get)
    loaded = load_data('http://example.com/data.csv')
    assert list(loaded.columns) == ['col','fraude']
    assert loaded['col'].tolist() == [1,2]
