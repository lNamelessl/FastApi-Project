from fastapi import FastAPI
from fastapi.testclient import TestClient
#from .database import client,session
from app.main import app
client = TestClient(app)
def test_root():
    res = client.get("/posts/")
    print(res.json().get('message'))
    assert res.json().get('message') == "Hello,World"
    assert res.status_code == 200