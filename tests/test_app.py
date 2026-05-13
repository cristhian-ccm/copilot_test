import pytest
from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)

# Ejemplo de prueba usando el patrón AAA

def test_root_endpoint():
    # Arrange
    url = "/"
    
    # Act
    response = client.get(url)
    
    # Assert
    assert response.status_code == 200
    # Puedes ajustar el assert según la respuesta esperada
    # assert response.json() == {"message": "Hello World"}


def test_get_activities():
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity_success():
    # Arrange
    activity = "Chess Club"
    email = "nuevo@mergington.edu"
    url = f"/activities/{activity}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Cleanup
    client.post(f"/activities/{activity}/unregister?email={email}")


def test_signup_for_activity_already_registered():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_not_found():
    # Arrange
    activity = "NoExiste"
    email = "nuevo@mergington.edu"
    url = f"/activities/{activity}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_success():
    # Arrange
    activity = "Chess Club"
    email = "nuevo2@mergington.edu"
    # Primero inscribir
    client.post(f"/activities/{activity}/signup?email={email}")
    url = f"/activities/{activity}/unregister?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"


def test_unregister_from_activity_not_registered():
    # Arrange
    activity = "Chess Club"
    email = "noexiste@mergington.edu"
    url = f"/activities/{activity}/unregister?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_unregister_from_activity_not_found():
    # Arrange
    activity = "NoExiste"
    email = "alguien@mergington.edu"
    url = f"/activities/{activity}/unregister?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
