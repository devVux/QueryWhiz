
from fastapi.testclient import TestClient
from main import app  # Adjust the import based on your project structure

client = TestClient(app)

def test_status():
    response = client.get("/qw/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_query():
    payload = {
        "prompt": "SELECT * FROM users WHERE age > 30;",
        "context": "Database with users"
    }
    
    response = client.post("/qw/query", json=payload)
    
    # Check the response status code
    assert response.status_code == 200
    
    # Extract and print the response content for debugging
    print(response.json())
    
    # Perform your assertions on the response
    assert "llm_response" in response.json()

if __name__ == "__main__":
    test_status()
    test_query()
