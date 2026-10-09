# Campus Safety & Harassment Reporting System
## Master Implementation Plan

**Target System:** Campus Safety & Harassment Reporting System  
**Primary Specification Reference:** `campus-safety-system-design.md` (Including Section 23: Final Repeat-Report Counting Policy)  
**UI/UX Standard:** `docs/ui-ux-design-specification.md` (`#121212` / `#1E1E1E` / `#38B6FF` / `#FF5A5F`)  
**Technology Stack:**
- **Frontend:** Semantic HTML5, CSS3 Custom Properties, Vanilla JavaScript (Fetch API, zero framework dependencies)
- **Backend:** Python 3.11 + FastAPI (REST, Pydantic v2 schemas)
- **ORM & Migrations:** SQLAlchemy 2.x + Alembic
- **Database:** MySQL 9.x (`campus_safety_db`, InnoDB) with dual-mode SQLite support for automated unit tests
- **Authentication & Cryptography:** Argon2id password hashing, Cryptographic tracking secrets, JWT/HttpOnly session tokens, SHA-256 audit chaining

---

## 1. System Overview & Core Principles

The platform serves as an accessible, confidential, and accountable mechanism for reporting in-person and digital harassment/ragging across college campuses. It bridges the trust deficit through strict data isolation while providing authorities with auditable case management and repeated-incident pattern detection.

### Core Non-Negotiable Tenets:
1. **Confidentiality by Data Separation:** Reporter contact information is physically isolated in `reporter_identities` from the main `complaints` record. Standard authority endpoints never return reporter details.
2. **True Anonymity:** Anonymous reports write zero rows to `reporter_identities` and require no user account or tracking cookie.
3. **No Automated Adjudication:** Repeated reports are flagged as potential matches for **human review only**. The system never automates guilt or disciplinary sanctions.
4. **Section 23 Repeat-Report Counting Policy:**
   - 1st confirmed report in a case group -> **Level 1 (HOD)**
   - 2nd distinct confirmed related report in that group -> **Level 2 (Dean)**
   - 3rd distinct confirmed related report in that group -> **Level 3 (Higher Authority)**
   - Unreviewed (pending) or rejected candidate links never inflate repeat-report counts.
   - Urgent reports (`is_urgent=True`) bypass repeat thresholds and route immediately.

---

## 2. Target Directory & Workspace Structure

```text
campus-safety-system/
├── frontend/
│   ├── index.html                  # Public landing, safety guidance, emergency banner
│   ├── report.html                 # Confidential & anonymous submission form
│   ├── track.html                  # Public reference & secret tracking portal
│   ├── login.html                  # Authority portal sign-in
│   ├── dashboard.html              # Authority case queue & KPI metrics
│   ├── case-detail.html            # Case narrative, timeline, evidence & escalation
│   ├── review.html                 # Side-by-side related-case review interface
│   ├── admin.html                  # User administration & audit logs
│   ├── css/
│   │   ├── variables.css           # Tokens (#121212, #1E1E1E, #38B6FF, #FF5A5F)
│   │   ├── base.css                # Typography, reset, accessibility rules
│   │   ├── layout.css              # Nav, container, footer, grid structures
│   │   ├── components.css          # Buttons, badges, modals, cards, alerts
│   │   ├── forms.css               # Form fields, upload dropzone, radio cards
│   │   ├── dashboard.css           # Tables, filters, KPI cards, timeline
│   │   └── responsive.css          # Mobile (<768px) and tablet adaptations
│   └── js/
│       ├── api.js                  # Centralized fetch wrapper & error interceptor
│       ├── auth.js                 # Session token management & route guards
│       ├── report.js               # Submission logic, file validation, credential modal
│       ├── tracking.js             # Tracking lookup & public milestone timeline
│       ├── dashboard.js            # Case filtering, sorting, pagination, role view
│       ├── case-detail.js          # Detail view, status update, identity access modal
│       ├── review.js               # Pairwise comparison & match decision actions
│       ├── admin.js                # User management & audit log table
│       └── components.js           # Modal dialogs, toast notifications, copy-to-clipboard
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application, CORS, exception handlers
│   │   ├── api/
│   │   │   ├── auth.py             # Login, logout, me
│   │   │   ├── complaints.py       # Public submission endpoint (confidential/anon)
│   │   │   ├── tracking.py         # Public tracking endpoint
│   │   │   ├── cases.py            # Authority case listings & single-case view
│   │   │   ├── evidence.py         # Private upload & authorized stream download
│   │   │   ├── match_reviews.py    # Potential match list & review decisions
│   │   │   ├── escalations.py      # Case escalation actions & history
│   │   │   └── admin.py            # User provisioning & audit log inspection
│   │   ├── core/
│   │   │   ├── config.py           # Pydantic Settings (.env configuration)
│   │   │   ├── security.py         # Argon2id hashing, tracking secret generator & verify
│   │   │   ├── permissions.py      # Role-based dependency injection
│   │   │   └── errors.py           # Structured error models
│   │   ├── db/
│   │   │   ├── session.py          # SQLAlchemy engine & session factory (MySQL + SQLite)
│   │   │   └── base.py             # Declarative Base
│   │   ├── models/
│   │   │   ├── user.py             # User accounts & roles
│   │   │   ├── complaint.py        # Core complaints table
│   │   │   ├── identity.py         # Separated reporter identities
│   │   │   ├── suspect.py          # Voluntary suspect allegation details
│   │   │   ├── evidence.py         # Metadata for privately stored files
│   │   │   ├── case_link.py        # Pairwise candidate match links & reviews
│   │   │   ├── case_group.py       # Confirmed case groups & case_group_members
│   │   │   ├── escalation.py       # Escalation records & levels (1, 2, 3)
│   │   │   ├── status_history.py   # State transitions & timestamps
│   │   │   ├── notification.py     # In-app notifications
│   │   │   └── audit_log.py        # Immutable security audit log
│   │   ├── schemas/
│   │   │   ├── auth.py             # Login credentials, tokens, user response
│   │   │   ├── complaint.py        # Submission input, public response
│   │   │   ├── tracking.py         # Tracking query & sanitized response
│   │   │   ├── case.py             # Authority case detail & update schemas
│   │   │   └── review.py           # Match decision schema
│   │   ├── services/
│   │   │   ├── complaint_service.py # Core complaint intake transaction
│   │   │   ├── identity_service.py  # Exceptional identity access with audit log
│   │   │   ├── matching_service.py  # Candidate match detection engine
│   │   │   ├── escalation_service.py# Section 23 repeat-report counter & router
│   │   │   ├── evidence_service.py  # Private disk read/write & mime validation
│   │   │   ├── notification_service.py# In-app notification creation
│   │   │   └── audit_service.py     # Tamper-evident audit logging
│   │   └── utils/
│   │       ├── ids.py              # Secure reference (REF-XXXX) & tracking token generators
│   │       └── validators.py       # File magic bytes & sanitize input
│   ├── tests/
│   │   ├── conftest.py             # Pytest fixtures & in-memory test DB
│   │   ├── test_auth.py            # Login, password hashing, JWT checks
│   │   ├── test_complaints.py      # Confidential vs anonymous intake
│   │   ├── test_tracking.py        # Public reference + secret verification
│   │   ├── test_permissions.py     # Role isolation & RBAC enforcement
│   │   ├── test_matching.py        # Candidate flagging & pairwise links
│   │   ├── test_escalation.py      # Section 23 multi-level escalation tests
│   │   └── test_evidence.py        # Private upload & unauthorized stream block
│   ├── alembic/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env.example
├── database/
│   ├── schema.sql
│   └── seeds/
│       └── demo_data.sql           # Synthetic authority accounts & demo incidents
├── storage/
│   └── evidence/                   # Private upload folder (never web accessible)
├── docs/
│   ├── system-design.md
│   ├── ui-ux-design-specification.md
│   └── implementation-plan.md
├── .gitignore
└── README.md
```

---

## 3. Database Schema Architecture

```text
users 1 ------ * complaints (optional submitter link)
users 1 ------ * escalations (assigned authority)
users 1 ------ * notifications (recipient)
users 1 ------ * audit_logs (actor)
complaints 1 ------ 0..1 reporter_identities (isolated)
complaints 1 ------ * suspect_details
complaints 1 ------ * evidence
complaints * ------ * case_links (pairwise proposal)
case_groups 1 ------ * case_group_members (explicit confirmed membership)
case_groups 1 ------ * escalations
complaints 1 ------ * case_status_history
```

### Table Details
1. `users`: `id`, `name`, `email` (UNIQUE), `password_hash`, `role` (`student`, `hod`, `dean`, `higher_authority`, `administrator`), `department`, `is_active`, timestamps.
2. `complaints`: `id`, `public_reference` (UNIQUE indexed), `tracking_secret_hash`, `reporting_mode` (`confidential`, `anonymous`), `type` (`offline`, `online`), `category`, `incident_date`, `incident_time`, `location_or_platform`, `description`, `is_urgent` (BOOLEAN DEFAULT FALSE), `status` (`submitted`, `under_review`, `pending_match_review`, `escalated`, `awaiting_information`, `resolved`, `closed`), timestamps.
3. `reporter_identities`: `id`, `complaint_id` (UNIQUE FK), `full_name`, `email`, `phone`, `department`, `student_id_number`, `access_policy` (DEFAULT 'restricted'), `created_at`.
4. `suspect_details`: `id`, `complaint_id` (FK), `name`, `department`, `phone`, `other_description`, `details_visibility` (DEFAULT 'authority_only'), `created_at`.
5. `evidence`: `id`, `complaint_id` (FK), `storage_key` (UNIQUE), `original_filename_display`, `verified_media_type`, `file_size`, `uploaded_at`.
6. `case_links`: `id`, `complaint_id` (FK), `related_complaint_id` (FK), `review_status` (`pending`, `confirmed`, `rejected`, `needs_more_review`), `reviewed_by` (FK users), `reviewed_at`, `reason`, `created_at`.
7. `case_groups`: `id`, `group_reference` (UNIQUE), `created_by` (FK users), `status`, `created_at`.
8. `case_group_members`: `id`, `case_group_id` (FK), `complaint_id` (FK), `added_at`, `UNIQUE(case_group_id, complaint_id)`.
9. `escalations`: `id`, `case_group_id` (FK), `complaint_id` (FK), `level` (1=HOD, 2=Dean, 3=Higher Authority), `authority_user_id` (FK users), `reason`, `status`, `created_at`.
10. `case_status_history`: `id`, `complaint_id` (FK), `previous_status`, `new_status`, `changed_by` (FK users), `reason`, `created_at`.
11. `notifications`: `id`, `recipient_user_id` (FK users), `case_reference`, `title`, `message`, `channel` (`in_app`), `is_read`, `created_at`.
12. `audit_logs`: `id`, `actor_user_id` (FK users, nullable), `action`, `resource_type`, `resource_id`, `reason`, `timestamp`, `ip_address`.

---

## 4. Matching & Section 23 Escalation Engine

1. **Candidate Matching (`MatchingService`):**
   - Flags reports based on category, timeframe, location keywords, and voluntary suspect attributes.
   - Inserts pair into `case_links` as `pending`.
   - Never modifies report counts until reviewed.
2. **Review Workflow:**
   - Authorised official reviews candidates side-by-side in `review.html`.
   - Action requires mandatory documented rationale.
   - **Confirm**: Forms/joins `case_group` via `case_group_members`, calculates distinct count.
   - **Reject**: Marks link as `rejected`, no count change.
3. **Escalation Rules:**
   - 1 confirmed distinct complaint in group -> Level 1 (HOD)
   - 2 confirmed distinct complaints in group -> Level 2 (Dean)
   - 3+ confirmed distinct complaints in group -> Level 3 (Higher Authority)
   - Urgent flag (`is_urgent=True`) initiates immediate safeguarding review regardless of report count.

---

## 5. Security & Privacy Controls

1. **Zero-leakage Tracking:** `GET /api/complaints/track` queries by reference + secret hash and returns ONLY public sanitized status history. Internal notes, suspect details, and reporter identities are strictly omitted.
2. **Identity Vault Isolation:** `reporter_identities` is query-isolated. Authority case detail responses redact identity fields. Exceptional access requires formal request endpoint and logs `IDENTITY_UNMASKED` to `audit_logs`.
3. **Private File Storage:** Evidence files are stored with random UUID keys in `storage/evidence/` outside the web root. Files are streamed only via authenticated endpoints that check user access privileges.

---

## 6. Phased Implementation Roadmap

- **Milestone 1:** Backend Foundation, Database Models, Complaint Intake & Tracking Endpoints with Tests.
- **Milestone 2:** User Authentication, Role-Based Access Control, Private Evidence Storage & Audit Service with Tests.
- **Milestone 3:** Candidate Match Engine, Human Review Queue, Case Groups & Section 23 Escalation Service with Tests.
- **Milestone 4:** Frontend Delivery (Semantic HTML5, CSS3 Custom Properties with `#121212`/`#1E1E1E`/`#38B6FF`/`#FF5A5F` theme, Vanilla JS).
- **Milestone 5:** Synthetic Seed Data, End-to-End Verification, Documentation & Final Walkthrough.
