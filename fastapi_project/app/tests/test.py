from fastapi.testclient import TestClient

def test_client(Client):
    assert type(Client) == TestClient