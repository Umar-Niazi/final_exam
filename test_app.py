from app import app


def test_root():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.get_json() == {"message": "Hello from Flask CI/CD"}


def test_health():
    with app.test_client() as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.get_json() == {"status": "ok"}
