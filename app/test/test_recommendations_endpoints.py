import os
import sys
import pytest
from unittest.mock import MagicMock, AsyncMock

# Añadir el directorio raíz de este microservicio al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi.testclient import TestClient
from app.main import app
from app.routers.recommendation_router import get_use_case

# Mock del caso de uso GetRecommendationUseCase
mock_use_case = MagicMock()

def override_get_use_case():
    return mock_use_case

@pytest.fixture(autouse=True)
def setup_overrides():
    app.dependency_overrides[get_use_case] = override_get_use_case
    yield
    app.dependency_overrides.pop(get_use_case, None)
    mock_use_case.reset_mock()

def test_recommendations_health():
    client = TestClient(app)
    response = client.get("/api/v1/recommendations/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "ms-Recommendations"

def test_get_zone_recommendation_success():
    client = TestClient(app)
    
    # Creamos un mock de la entidad de recomendación del dominio
    mock_rec = MagicMock()
    mock_rec.zone_code = "12345"
    mock_rec.zone_name = "Zona Centro"
    mock_rec.current_score = 0.75
    mock_rec.potential_value = 0.90
    mock_rec.business_label = "HIGH"
    
    mock_factor_rec = MagicMock()
    mock_factor_rec.factor = "Poblacion"
    mock_factor_rec.impact = "HIGH"
    mock_factor_rec.weight = 0.4
    mock_factor_rec.action_text = "Fomentar comercio"
    mock_rec.top_recommendations = [mock_factor_rec]
    
    mock_use_case.execute = AsyncMock(return_value=mock_rec)
    
    response = client.get("/api/v1/recommendations/dataset_abc/12345")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["zone_code"] == "12345"
    assert data["data"]["current_score"] == 0.75
    assert len(data["data"]["top_recommendations"]) == 1
    mock_use_case.execute.assert_called_once_with("dataset_abc", "12345")

def test_get_zone_recommendation_invalid_zone_code():
    client = TestClient(app)
    
    # zone_code inválido (no numérico)
    response = client.get("/api/v1/recommendations/dataset_abc/abc_zone")
    assert response.status_code == 422
    data = response.json()
    assert data["detail"]["success"] is False
    assert data["detail"]["error"]["code"] == "INVALID_ZONE_CODE_FORMAT"

def test_get_zone_recommendation_not_found():
    client = TestClient(app)
    mock_use_case.execute = AsyncMock(return_value=None)
    
    response = client.get("/api/v1/recommendations/dataset_abc/99999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"]["success"] is False
    assert data["detail"]["error"]["code"] == "NOT_FOUND"
