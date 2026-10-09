import io
from datetime import date
from fastapi.testclient import TestClient


def test_evidence_upload_and_authorized_download(client: TestClient):
    # 1. Create a complaint
    complaint_res = client.post("/api/complaints", json={
        "reporting_mode": "anonymous",
        "type": "online",
        "category": "Obscene or abusive content",
        "incident_date": str(date.today()),
        "location_or_platform": "Discord Server",
        "description": "Circulation of unconsented screenshots in student group.",
        "is_urgent": False
    })
    assert complaint_res.status_code == 201
    ref = complaint_res.json()["public_reference"]

    # Authority login to get ID
    hod_login = client.post("/api/auth/login", json={
        "email": "hod@test.edu",
        "password": "TestPass123!"
    })
    hod_token = hod_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {hod_token}"}

    # Get case details to get case id
    cases = client.get("/api/cases", headers=headers).json()
    case = next(c for c in cases if c["public_reference"] == ref)
    case_id = case["id"]

    # 2. Upload file
    file_bytes = b"Sample simulated image byte stream for testing purposes"
    upload_res = client.post(
        f"/api/cases/{case_id}/evidence",
        files={"file": ("screenshot.png", io.BytesIO(file_bytes), "image/png")}
    )
    assert upload_res.status_code == 201
    ev_data = upload_res.json()
    assert ev_data["original_filename_display"] == "screenshot.png"
    assert ev_data["verified_media_type"] == "image/png"
    ev_id = ev_data["id"]

    # 3. Download as authorized HOD -> Success (200)
    dl_res = client.get(f"/api/evidence/{ev_id}", headers=headers)
    assert dl_res.status_code == 200
    assert dl_res.content == file_bytes

    # 4. Download without authorization -> 401
    client.cookies.clear()
    dl_unauth = client.get(f"/api/evidence/{ev_id}")
    assert dl_unauth.status_code == 401
