from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.app.models.complaint import Complaint
from backend.app.models.identity import ReporterIdentity
from backend.app.models.escalation import Escalation


def test_anonymous_submission_has_zero_identity_record(client: TestClient, db_session: Session):
    """Verifies that an anonymous report writes zero rows to reporter_identities."""
    payload = {
        "reporting_mode": "anonymous",
        "type": "offline",
        "category": "Following or stalking",
        "incident_date": str(date.today()),
        "location_or_platform": "Library 2nd Floor Corridor",
        "description": "Observed repeated following after late evening study hours.",
        "is_urgent": False
    }

    response = client.post("/api/complaints", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert data["reporting_mode"] == "anonymous"
    assert data["public_reference"].startswith("REF-")
    assert data["tracking_secret"].startswith("TRK-")

    # DB Verification
    complaint = db_session.query(Complaint).filter(Complaint.public_reference == data["public_reference"]).first()
    assert complaint is not None
    assert complaint.reporter_identity is None

    # Zero identity records
    identities_count = db_session.query(ReporterIdentity).filter(ReporterIdentity.complaint_id == complaint.id).count()
    assert identities_count == 0


def test_confidential_submission_stores_isolated_identity(client: TestClient, db_session: Session):
    """Verifies that a confidential report isolates identity into reporter_identities."""
    payload = {
        "reporting_mode": "confidential",
        "type": "online",
        "category": "Fake accounts or impersonation",
        "incident_date": str(date.today()),
        "location_or_platform": "Instagram Direct Message",
        "description": "Fake profile created using student identity sending abusive notes.",
        "is_urgent": False,
        "reporter_identity": {
            "full_name": "Priya Sharma",
            "email": "priya.student@test.edu",
            "phone": "+91 98765 43210",
            "department": "Biotechnology",
            "student_id_number": "BT-2024-042"
        },
        "suspect_details": [
            {
                "name": "unknown_handle_xyz",
                "other_description": "Profile active from 9pm onwards"
            }
        ]
    }

    response = client.post("/api/complaints", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert data["reporting_mode"] == "confidential"
    ref = data["public_reference"]

    complaint = db_session.query(Complaint).filter(Complaint.public_reference == ref).first()
    assert complaint is not None
    assert complaint.reporter_identity is not None
    assert complaint.reporter_identity.full_name == "Priya Sharma"
    assert complaint.reporter_identity.email == "priya.student@test.edu"
    assert len(complaint.suspect_details) == 1


def test_urgent_submission_fast_tracks_escalation(client: TestClient, db_session: Session):
    """Verifies that is_urgent=True immediately routes case to escalation Level 1."""
    payload = {
        "reporting_mode": "anonymous",
        "type": "offline",
        "category": "Threats or intimidation",
        "incident_date": str(date.today()),
        "location_or_platform": "Main Hostel Gate",
        "description": "Physical confrontation and direct verbal intimidation.",
        "is_urgent": True
    }

    response = client.post("/api/complaints", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["is_urgent"] is True
    assert data["urgent_guidance"] is not None

    complaint = db_session.query(Complaint).filter(Complaint.public_reference == data["public_reference"]).first()
    assert complaint.status == "escalated"

    esc = db_session.query(Escalation).filter(Escalation.complaint_id == complaint.id).first()
    assert esc is not None
    assert esc.level == 1
