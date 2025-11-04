import pytest
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)


class TestHealthCheck:
    """Tests for the health check endpoint"""
    
    def test_health_check(self):
        """Test that health check endpoint works"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "max_input_size" in data

class TestAnalyzeEndpoint:
    def test_word_count(self):
        response = client.post(
            "/analyze?analyses=word_count",
            json={"text": "Hello world!"}
        )
        assert response.status_code == 200
        data = response.json()
        analyses = data["analyses"]
        assert "word_count" in analyses
        assert analyses["word_count"] == 2
        
    def test_char_count(self):
        response = client.post(
            "/analyze?analyses=char_count",
            json={"text": "Hello world!"}
        )
        assert response.status_code == 200
        data = response.json()
        analyses = data["analyses"]
        assert "char_count" in analyses
        assert analyses["char_count"] == 12

    def test_specific_analyses(self):
        response = client.post(
            "/analyze?analyses=word_count&analyses=char_count",
            json={"text": "Hello world!"}
        )
        assert response.status_code == 200
        data = response.json()
        analyses = data["analyses"]
        assert "word_count" in analyses
        assert "char_count" in analyses
        assert analyses["word_count"] == 2
        assert analyses["char_count"] == 12
        
    def test_invalid_analysis_type(self):
        """Test that invalid analysis types are rejected"""
        response = client.post(
            "/analyze?analyses=invalid_analysis",
            json={"text": "Hello world"}
        )
        assert response.status_code == 400
        assert "invalid" in response.json()["detail"].lower()

class TestAvailableAnalyses:
    """Tests for the available analyses endpoint"""
    
    def test_available_analyses(self):
        """Test that available analyses endpoint returns all options"""
        response = client.get("/available-analyses")
        assert response.status_code == 200
        data = response.json()
        assert "available_analyses" in data
        assert "descriptions" in data
        assert len(data["available_analyses"]) > 0
        # Check that some expected analyses are present
        assert "word_count" in data["available_analyses"]
        assert "char_count" in data["available_analyses"]
