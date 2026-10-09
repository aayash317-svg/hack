from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.app.models.case_group import CaseGroup, CaseGroupMember
from backend.app.models.escalation import Escalation


def test_section_23_matching_and_escalation_flow(client: TestClient, db_session: Session):
    # Log in as HOD
    hod_login = client.post("/api/auth/login", json={
        "email": "hod@test.edu",
        "password": "TestPass123!"
    })
    hod_token = hod_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {hod_token}"}

    # 1. Submit Report 1
    r1 = client.post("/api/complaints", json={
        "reporting_mode": "anonymous",
        "type": "offline",
        "category": "Following or stalking",
        "incident_date": str(date.today()),
        "location_or_platform": "Mechanical Engineering Workshop",
        "description": "Repeated following observed near workshop doors.",
        "is_urgent": False,
        "suspect_details": [{"name": "Senior Batch Group A"}]
    }).json()

    # 2. Submit Report 2 (Similar attributes)
    r2 = client.post("/api/complaints", json={
        "reporting_mode": "confidential",
        "type": "offline",
        "category": "Following or stalking",
        "incident_date": str(date.today()),
        "location_or_platform": "Mechanical Engineering Corridor",
        "description": "Another student reporting intimidation near the same workshop area.",
        "is_urgent": False,
        "reporter_identity": {
            "full_name": "Test Reporter",
            "email": "test.reporter@test.edu"
        },
        "suspect_details": [{"name": "Senior Batch Group A"}]
    }).json()

    # 3. Check pending review queue
    reviews_res = client.get("/api/authority/match-reviews", headers=headers)
    assert reviews_res.status_code == 200
    reviews = reviews_res.json()
    assert len(reviews) >= 1

    link_item = reviews[0]
    link_id = link_item["link_id"]

    # 4. Confirm match per Section 23
    decide_res = client.post(
        f"/api/cases/match-reviews/{link_id}/decide",
        json={
            "decision": "confirm",
            "reason": "Confirmed repeated pattern around Mechanical block workshop by Senior Batch Group A"
        },
        headers=headers
    )
    assert decide_res.status_code == 200
    group_id = decide_res.json()["case_group_id"]
    assert group_id is not None

    # Verify group has 2 distinct reports
    group_count = db_session.query(CaseGroupMember).filter(CaseGroupMember.case_group_id == group_id).count()
    assert group_count == 2

    # Verify Section 23 escalation: 2 distinct confirmed reports in group -> Level 2 (Dean)
    esc = db_session.query(Escalation).filter(
        Escalation.case_group_id == group_id,
        Escalation.level == 2
    ).first()
    assert esc is not None
    assert "Dean" in esc.reason or esc.level == 2
