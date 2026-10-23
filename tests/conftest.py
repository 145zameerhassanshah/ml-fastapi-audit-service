import os, tempfile, pytest
from fastapi.testclient import TestClient

@pytest.fixture()
def client():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f: db_path=f.name
    os.environ['AUDIT_DB_PATH']=db_path
    from app.database import init_database
    from app.main import app
    init_database()
    with TestClient(app) as c: yield c
    os.environ.pop('AUDIT_DB_PATH',None)
    try: os.remove(db_path)
    except FileNotFoundError: pass
