"""Tests for the FastAPI API endpoints."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from api import app


@pytest.fixture()
def client():
    return TestClient(app)


class TestListInvestors:
    def test_returns_list(self, client: TestClient):
        resp = client.get("/investors")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_investor_fields(self, client: TestClient):
        resp = client.get("/investors")
        data = resp.json()
        if data:  # Only check if there are investors
            investor = data[0]
            assert "name" in investor
            assert "slug" in investor
            assert "fund" in investor


class TestGetInvestor:
    def test_known_investor(self, client: TestClient):
        # Use a slug we know exists from the fixture data
        resp = client.get("/investors")
        data = resp.json()
        if data:
            slug = data[0]["slug"]
            resp = client.get(f"/investors/{slug}")
            assert resp.status_code == 200
            detail = resp.json()
            assert detail["slug"] == slug
            assert "appearances" in detail

    def test_unknown_investor_404(self, client: TestClient):
        resp = client.get("/investors/nonexistent-slug")
        assert resp.status_code == 404


class TestEntities:
    def test_returns_entities(self, client: TestClient):
        resp = client.get("/entities")
        assert resp.status_code == 200
        data = resp.json()
        assert "companies" in data
        assert "topics" in data
        assert isinstance(data["companies"], list)
        assert isinstance(data["topics"], list)

    def test_months_param(self, client: TestClient):
        resp = client.get("/entities?months=1")
        assert resp.status_code == 200


class TestAnalyze:
    def test_rejects_empty_question(self, client: TestClient):
        resp = client.post("/analyze", json={"question": ""})
        assert resp.status_code == 422

    def test_rejects_missing_question(self, client: TestClient):
        resp = client.post("/analyze", json={})
        assert resp.status_code == 422


class TestCORS:
    def test_cors_headers_present(self, client: TestClient):
        resp = client.options(
            "/investors",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert "access-control-allow-origin" in resp.headers
