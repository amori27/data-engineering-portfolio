from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


class TestAPIHealth:
    def test_health_returns_ok(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_recent_pageviews_returns_empty_when_no_data(self):
        response = client.get("/api/pageviews/recent?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "count" in data

    def test_recent_pageviews_rejects_invalid_limit(self):
        response = client.get("/api/pageviews/recent?limit=2000")
        assert response.status_code == 422

    def test_top_pages_returns_empty_when_no_data(self):
        response = client.get("/api/pageviews/top-pages")
        assert response.status_code == 200

    def test_country_breakdown_returns_empty_when_no_data(self):
        response = client.get("/api/pageviews/country-breakdown")
        assert response.status_code == 200

    def test_country_detail_returns_404(self):
        response = client.get("/api/pageviews/country/ZZ")
        assert response.status_code == 404
