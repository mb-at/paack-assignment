import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.domain.enums import PackageStatus

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_healthcheck(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_packages_initially(client):
    response = client.get("/packages")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) and len(data) >= 2

    # Each object must have id, status and customer_address
    for pkg in data:
        assert "id" in pkg and "status" in pkg and "customer_address" in pkg

def test_patch_success_and_list_reflects_change(client):
    # First we get a package
    all_pkgs = client.get("/packages").json()
    pkg_id = all_pkgs[0]["id"]

    # We make valid change
    response = client.patch(f"/packages/{pkg_id}/status", json={"status": "IN_TRANSIT"})
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == pkg_id
    assert body["status"] == "IN_TRANSIT"

    # We verify that GET /packages now displays it with IN_TRANSIT
    all_pkgs2 = client.get("/packages").json()
    updated = next(p for p in all_pkgs2 if p["id"] == pkg_id)
    assert updated["status"] == "IN_TRANSIT"

def test_patch_not_found_returns_404(client):
    response = client.patch("/packages/fake-id/status", json={"status": "IN_TRANSIT"})
    assert response.status_code == 404

def test_patch_invalid_transition_returns_400(client):
    all_pkgs = client.get("/packages").json()
    pkg_id = all_pkgs[1]["id"]
    
    # That package is READY; we tried DELIVERED directly
    response = client.patch(f"/packages/{pkg_id}/status", json={"status": "DELIVERED"})
    assert response.status_code == 400

def test_patch_without_body_returns_422_and_logs(client):
    all_pkgs = client.get("/packages").json()
    pkg_id = all_pkgs[0]["id"]
    response = client.patch(f"/packages/{pkg_id}/status", json={})
    assert response.status_code == 422

def test_patch_with_invalid_status_enum_returns_422(client):
    all_pkgs = client.get("/packages").json()
    pkg_id = all_pkgs[0]["id"]
    response = client.patch(f"/packages/{pkg_id}/status", json={"status": "NOT_A_STATUS"})
    assert response.status_code == 422