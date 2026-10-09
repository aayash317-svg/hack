from fastapi.testclient import TestClient


def test_auth_login_and_me(client: TestClient):
    # 1. Login with valid credentials
    login_res = client.post("/api/auth/login", json={
        "email": "hod@test.edu",
        "password": "TestPass123!"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    assert data["role"] == "hod"
    token = data["access_token"]

    # 2. Get /me
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["email"] == "hod@test.edu"
    assert me_data["role"] == "hod"

    # 3. Login with bad password -> 401
    bad_login = client.post("/api/auth/login", json={
        "email": "hod@test.edu",
        "password": "WrongPassword!"
    })
    assert bad_login.status_code == 401


def test_role_permissions_enforced(client: TestClient):
    # Student logs in
    student_login = client.post("/api/auth/login", json={
        "email": "student@test.edu",
        "password": "TestPass123!"
    })
    student_token = student_login.json()["access_token"]

    # Student attempts to access authority case list -> Forbidden (403)
    cases_res = client.get("/api/cases", headers={"Authorization": f"Bearer {student_token}"})
    assert cases_res.status_code == 403

    # HOD attempts to access authority case list -> Success (200)
    hod_login = client.post("/api/auth/login", json={
        "email": "hod@test.edu",
        "password": "TestPass123!"
    })
    hod_token = hod_login.json()["access_token"]
    hod_cases = client.get("/api/cases", headers={"Authorization": f"Bearer {hod_token}"})
    assert hod_cases.status_code == 200
