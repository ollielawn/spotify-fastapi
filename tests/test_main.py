from fastapi.testclient import TestClient
from main import app

class TestGettingTreasures:
    def test_initialisation_of_api(self):

        client = TestClient(app)

        # Send a GET request to the root endpoint
        response = client.get("/")

        # Check that the status code is 200 OK
        assert response.status_code == 200

        # Check that the response JSON matches the expected output
        assert response.json() == {"message": "Hello world"}