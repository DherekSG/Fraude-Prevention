import importlib
import sys


def test_insert_and_retrieve_transaction(tmp_path, monkeypatch):
    db_file = tmp_path / 'test.db'
    monkeypatch.setenv('DATABASE_URL', f'sqlite:///{db_file}')
    sys.modules.pop('db.database', None)
    sys.modules.pop('db.models', None)
    database = importlib.import_module('db.database')
    models = importlib.import_module('db.models')
    database.init_db()
    session = database.SessionLocal()
    trans = models.Transacao(
        valor=123.45,
        localizacao='BR',
        ip='127.0.0.1',
        cartao='0000',
        probabilidade_fraude=0.9,
        is_fraud=True,
    )
    session.add(trans)
    session.commit()
    session.refresh(trans)
    fetched = session.query(models.Transacao).filter_by(id=trans.id).first()
    assert fetched is not None
    assert fetched.valor == 123.45
    assert fetched.localizacao == 'BR'
    assert fetched.ip == '127.0.0.1'
    assert fetched.cartao == '0000'
    assert fetched.probabilidade_fraude == 0.9
    assert fetched.is_fraud is True
    session.close()
