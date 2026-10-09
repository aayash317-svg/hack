import os
import sys
from datetime import date, datetime, timezone

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.app.db.session import engine, SessionLocal
from backend.app.db.base import Base
from backend.app.core.security import get_password_hash, generate_public_reference, generate_tracking_secret, hash_tracking_secret
from backend.app.models.user import User
from backend.app.models.complaint import Complaint
from backend.app.models.identity import ReporterIdentity
from backend.app.models.suspect import SuspectDetail
from backend.app.models.status_history import CaseStatusHistory
from backend.app.models.case_link import CaseLink
from backend.app.models.case_group import CaseGroup, CaseGroupMember
from backend.app.models.escalation import Escalation
from backend.app.models.audit_log import AuditLog


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(Complaint).count() > 0:
            print("Demo data already seeded.")
            return

        print("Seeding synthetic demo records...")

        # 1. Authority Accounts
        admin = db.query(User).filter(User.email == "admin@campus.edu").first()
        if not admin:
            admin = User(
                name="System Administrator",
                email="admin@campus.edu",
                password_hash=get_password_hash("AdminPass2026!"),
                role="administrator",
                department="Campus Administration"
            )
            db.add(admin)

        hod = db.query(User).filter(User.email == "hod.cse@campus.edu").first()
        if not hod:
            hod = User(
                name="Dr. S. Sharma (HOD)",
                email="hod.cse@campus.edu",
                password_hash=get_password_hash("HodPass2026!"),
                role="hod",
                department="Computer Science & Engineering"
            )
            db.add(hod)

        dean = db.query(User).filter(User.email == "dean.studentaffairs@campus.edu").first()
        if not dean:
            dean = User(
                name="Prof. M. Verma (Dean)",
                email="dean.studentaffairs@campus.edu",
                password_hash=get_password_hash("DeanPass2026!"),
                role="dean",
                department="Student Affairs & Welfare"
            )
            db.add(dean)

        higher_auth = db.query(User).filter(User.email == "director.office@campus.edu").first()
        if not higher_auth:
            higher_auth = User(
                name="Dr. R. Kapoor (Higher Authority)",
                email="director.office@campus.edu",
                password_hash=get_password_hash("DirectorPass2026!"),
                role="higher_authority",
                department="Office of the Director / Ombudsman"
            )
            db.add(higher_auth)

        db.flush()

        # 2. Case 1: Anonymous Offline Stalking
        c1 = Complaint(
            public_reference="REF-2026-1042",
            tracking_secret_hash=hash_tracking_secret("TRK-demo-secret-key-1042"),
            reporting_mode="anonymous",
            type="offline",
            category="Following or stalking",
            incident_date=date(2026, 10, 5),
            incident_time="8:15 PM",
            location_or_platform="Central Library East Corridor",
            description="A group of seniors repeatedly blocked the passage and followed junior students heading towards the residential blocks after late study hours.",
            is_urgent=False,
            status="under_review"
        )
        db.add(c1)
        db.flush()

        db.add(SuspectDetail(
            complaint_id=c1.id,
            name="Senior Batch Group B",
            department="Mechanical 3rd Year",
            other_description="Observed near the bike stand around 8 PM"
        ))
        db.add(CaseStatusHistory(
            complaint_id=c1.id,
            previous_status="none",
            new_status="submitted",
            reason="Initial intake"
        ))
        db.add(CaseStatusHistory(
            complaint_id=c1.id,
            previous_status="submitted",
            new_status="under_review",
            changed_by=hod.id,
            reason="Acknowledged by HOD for enquiry"
        ))

        # 3. Case 2: Confidential Online Harassment
        c2 = Complaint(
            public_reference="REF-2026-2189",
            tracking_secret_hash=hash_tracking_secret("TRK-demo-secret-key-2189"),
            reporting_mode="confidential",
            type="online",
            category="Fake accounts or impersonation",
            incident_date=date(2026, 10, 7),
            incident_time="11:00 PM",
            location_or_platform="Instagram Messaging (@apex_confessions_unofficial)",
            description="An anonymous Instagram account posted defamatory remarks and forwarded photos claiming to represent first-year hostel residents.",
            is_urgent=False,
            status="under_review"
        )
        db.add(c2)
        db.flush()

        db.add(ReporterIdentity(
            complaint_id=c2.id,
            full_name="Meera Sen",
            email="meera.sen@campus.edu",
            phone="+91 91234 56789",
            department="Computer Science 1st Year",
            student_id_number="CS-2026-034"
        ))
        db.add(CaseStatusHistory(
            complaint_id=c2.id,
            previous_status="none",
            new_status="submitted",
            reason="Initial intake"
        ))

        # 4. Case 3 & Case 4: Candidate Match Pair (Section 23 Candidate)
        c3 = Complaint(
            public_reference="REF-2026-3301",
            tracking_secret_hash=hash_tracking_secret("TRK-demo-secret-key-3301"),
            reporting_mode="anonymous",
            type="offline",
            category="Hostel intimidation or coercion",
            incident_date=date(2026, 10, 8),
            incident_time="10:30 PM",
            location_or_platform="Hostel Block C 2nd Floor Common Room",
            description="Seniors forced new hostellers to remain standing and perform demeaning tasks during late night hours.",
            is_urgent=False,
            status="pending_match_review"
        )
        db.add(c3)
        db.flush()
        db.add(SuspectDetail(
            complaint_id=c3.id,
            name="Block C Senior Council",
            department="Civil Engineering 4th Year"
        ))

        c4 = Complaint(
            public_reference="REF-2026-3302",
            tracking_secret_hash=hash_tracking_secret("TRK-demo-secret-key-3302"),
            reporting_mode="anonymous",
            type="offline",
            category="Hostel intimidation or coercion",
            incident_date=date(2026, 10, 8),
            incident_time="11:15 PM",
            location_or_platform="Hostel Block C Corridor",
            description="Another student reporting that the same Block C group demanded hostel room entry and intimidated residents.",
            is_urgent=False,
            status="pending_match_review"
        )
        db.add(c4)
        db.flush()
        db.add(SuspectDetail(
            complaint_id=c4.id,
            name="Block C Senior Council",
            department="Civil Engineering 4th Year"
        ))

        # Create candidate match proposal in case_links
        db.add(CaseLink(
            complaint_id=c3.id,
            related_complaint_id=c4.id,
            review_status="pending",
            reason="Identical category (Hostel intimidation) & incident type (offline); Similar location/platform: 'Hostel Block C'; Overlapping suspect: Block C Senior Council"
        ))

        # 5. Case 5: Urgent Safety Incident
        c5 = Complaint(
            public_reference="REF-2026-9901",
            tracking_secret_hash=hash_tracking_secret("TRK-demo-secret-key-9901"),
            reporting_mode="confidential",
            type="offline",
            category="Threats or intimidation",
            incident_date=date(2026, 10, 9),
            incident_time="10:00 AM",
            location_or_platform="Campus Sports Complex Gate",
            description="Direct verbal threats and physical confrontation demanding withdrawal of a complaint. High physical risk.",
            is_urgent=True,
            status="escalated"
        )
        db.add(c5)
        db.flush()
        db.add(ReporterIdentity(
            complaint_id=c5.id,
            full_name="Karan Malhotra",
            email="karan.m@campus.edu",
            phone="+91 99887 76655",
            department="Electrical Engineering 2nd Year"
        ))
        db.add(Escalation(
            complaint_id=c5.id,
            level=1,
            authority_user_id=hod.id,
            reason="Immediate safety alert flagged by reporter during intake",
            status="notified"
        ))
        db.add(CaseStatusHistory(
            complaint_id=c5.id,
            previous_status="submitted",
            new_status="escalated",
            changed_by=hod.id,
            reason="Fast-tracked due to urgent safety alert"
        ))

        # Log seed audit
        db.add(AuditLog(
            action="SYSTEM_SEEDED",
            resource_type="system",
            resource_id="init",
            reason="Synthetic demo cases and accounts initialized"
        ))

        db.commit()
        print("Demo data successfully seeded!")

    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
