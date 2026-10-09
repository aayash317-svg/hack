from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from backend.app.models.complaint import Complaint
from backend.app.models.case_link import CaseLink
from backend.app.models.suspect import SuspectDetail
from backend.app.models.notification import Notification
from backend.app.models.user import User


class MatchingService:
    @classmethod
    def check_and_flag_candidates(cls, db: Session, new_complaint: Complaint) -> List[CaseLink]:
        """
        Scans existing complaints to find candidate related reports.
        Per Section 23: creates pending CaseLink records for authorized human review only.
        """
        created_links: List[CaseLink] = []

        # Find existing active complaints (excluding this one)
        existing_complaints = db.query(Complaint).filter(
            Complaint.id != new_complaint.id,
            Complaint.status.notin_(["closed", "resolved"])
        ).all()

        new_loc = new_complaint.location_or_platform.lower().strip()
        new_suspects = [s.name.lower().strip() for s in new_complaint.suspect_details if s.name]

        for existing in existing_complaints:
            matched_features = []

            # 1. Category and type match
            if existing.type == new_complaint.type and existing.category == new_complaint.category:
                matched_features.append(f"Identical category ({new_complaint.category}) & incident type ({new_complaint.type})")

            # 2. Location or platform keyword overlap
            exist_loc = existing.location_or_platform.lower().strip()
            if exist_loc and new_loc:
                if exist_loc in new_loc or new_loc in exist_loc:
                    matched_features.append(f"Similar location/platform: '{existing.location_or_platform}'")
                else:
                    stop_words = {"the", "and", "near", "in", "at", "of", "on", "to", "for", "block", "floor", "area"}
                    exist_tokens = set(exist_loc.replace(",", " ").replace("-", " ").split())
                    new_tokens = set(new_loc.replace(",", " ").replace("-", " ").split())
                    shared_words = {w for w in exist_tokens.intersection(new_tokens) if len(w) > 2 and w not in stop_words}
                    if shared_words:
                        matched_features.append(f"Matching location keywords: {', '.join(sorted(shared_words))}")

            # 3. Suspect details comparison
            exist_suspects = [s.name.lower().strip() for s in existing.suspect_details if s.name]
            common_suspects = set(new_suspects).intersection(set(exist_suspects))
            if common_suspects:
                matched_features.append(f"Allegation cites overlapping suspect identifier: {', '.join(common_suspects)}")

            # If 2 or more features match, or 1 high-confidence suspect match
            if (len(matched_features) >= 2) or common_suspects:
                # Check if case link already exists between these two in either direction
                existing_link = db.query(CaseLink).filter(
                    or_(
                        and_(CaseLink.complaint_id == new_complaint.id, CaseLink.related_complaint_id == existing.id),
                        and_(CaseLink.complaint_id == existing.id, CaseLink.related_complaint_id == new_complaint.id)
                    )
                ).first()

                if not existing_link:
                    link = CaseLink(
                        complaint_id=new_complaint.id,
                        related_complaint_id=existing.id,
                        review_status="pending",
                        reason="; ".join(matched_features)
                    )
                    db.add(link)
                    created_links.append(link)

        if created_links:
            # Set status to pending_match_review if currently submitted
            if new_complaint.status == "submitted":
                new_complaint.status = "pending_match_review"

            # Create notification for HOD
            hod_users = db.query(User).filter(User.role == "hod", User.is_active == True).all()
            for hod in hod_users:
                notif = Notification(
                    recipient_user_id=hod.id,
                    case_reference=new_complaint.public_reference,
                    title="Potential Related Report Flagged",
                    message=f"Report {new_complaint.public_reference} shares attributes with existing cases and requires human review."
                )
                db.add(notif)

        db.flush()
        return created_links
