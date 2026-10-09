from datetime import date
from fastapi.testclient import TestClient


def test_tracking_with_valid_and_invalid_credentials(client: TestClient):
    # 1. Submit complaint
    payload = {
        "reporting_mode": "anonymous",
        "type": "offline",
        "category": "Unwanted behaviour",
        "incident_date": str(date.today()),
        "location_or_platform": "Cafeteria Outdoor Seating",
        "description": "Repeated disruptive taunts and intimidation during lunch break.",
        "is_urgent": False
    }

    sub_res = client.post("/api/complaints", json=payload)
    assert sub_res.status_code == 201
    sub_data = sub_res.json()
    ref = sub_data["public_reference"]
    secret = sub_data["tracking_secret"]

    # 2. Track with correct secret
    track_res = client.get(f"/api/complaints/track?reference={ref}&secret={secret}")
    assert track_res.status_code == 200
    track_data = track_res.json()
    assert track_data["public_reference"] == ref
    assert track_data["status"] == "submitted"
    assert len(track_data["timeline"]) >= 1
    assert "suspect_details" not in track_data
    assert "reporter_identity" not in track_data

    # 3. Track with wrong secret -> 401
    bad_res = client.get(f"/api/complaints/track?reference={ref}&secret=TRK-wrong-secret-key-12345")
    assert bad_res.status_code == 401

    # 4. Track with nonexistent reference -> 404
    missing_res = client.get("/api/complaints/track?reference=REF-9999-XXXX&secret=TRK-any-secret")
    assert missing_res.status_code == 404
