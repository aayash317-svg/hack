# Campus Safety & Harassment Reporting System

A privacy-first, full-stack digital safety platform designed to empower students to report ragging, harassment, stalking, and cyberbullying while providing campus authorities with an accountable, auditable, and human-reviewed case management system.

---

---

## 🌟 Comprehensive Features Guide

### 1. Core Platform Capabilities
- **Confidential vs. Anonymous Reporting Modes**:
  - *Anonymous Mode*: Zero personal or contact data collected. Zero rows written to `reporter_identities`. No student login or session cookies required. Returns a one-time high-entropy tracking secret (`TRK-...`).
  - *Confidential Mode*: Reporter contact details (Full Name, College Email, Phone, Department, Roll No) are physically isolated into an encrypted/protected vault table (`reporter_identities`). Standard authority dashboards and case list responses strictly redact and omit identity fields. Exceptional access requires formal recorded justification and logs an immutable audit event (`IDENTITY_UNMASKED`).
- **Comprehensive Incident Taxonomy**:
  - *In-Person / Offline Ragging*: Stalking, physical abuse, verbal confrontation, hostel intimidation, and coercion.
  - *Digital / Online Harassment*: Impersonation, fake profiles, obscene or abusive content distribution, cyberbullying, and unconsented media sharing.
- **Dual-Credential Zero-Leakage Tracking**:
  - Secure tracking combines a public case identifier (`REF-YYYY-XXXX`) with a 24-byte cryptographic tracking secret (`TRK-...`) hashed using **Argon2id**.
  - Public tracking portal returns milestone timelines only (`Submitted` &rarr; `Under Review` &rarr; `Escalated` &rarr; `Resolved`), strictly stripping internal investigator remarks, suspect details, and reporter identity.
- **Private Evidence Vault**:
  - Uploaded screenshots, documents, and images (PNG, JPG, PDF up to 5MB) are renamed with unguessable UUID storage keys and stored on the private filesystem outside the web root.
  - Files are streamed strictly through the authenticated endpoint `GET /api/evidence/{id}`, which verifies user role permissions and writes an `EVIDENCE_ACCESSED` audit entry.
- **Immediate Urgent Safety Route**:
  - Reports with imminent physical risk can be flagged as urgent (`is_urgent=True`).
  - Urgent alerts bypass repeated-report thresholds, routing immediately to Level 1 safeguarding authorities with pinned visual cues (`#FF5A5F`) and emergency contact details.

### 2. Advanced Workflow & Security Features
- **Section 23 Repeat-Report Pattern Review**:
  - The `MatchingService` scans active complaints across category, type, location keywords, and voluntary suspect descriptors.
  - Candidate correlations are flagged into `case_links` in a **`pending`** status for **human review only**.
  - Algorithmic proposals never determine guilt and never automatically increment incident counts.
- **Human-in-the-Loop Review Queue (`review.html`)**:
  - Authorized officials inspect candidate reports side-by-side in a comparative matrix.
  - Explicit action deck: **Confirm Related Pattern**, **Reject Match**, or **Defer / Request More Info**.
  - A documented factual rationale is mandatory before confirming or rejecting any relationship.
- **Section 23 Progressive Escalation Ladder**:
  - When matches are confirmed, cases are bound into a `case_group` via `case_group_members` (enforcing `UNIQUE(case_group_id, complaint_id)` to prevent artificial count inflation).
  - Escalation tiers are evaluated automatically inside database transactions:
    - **1 distinct confirmed report** in group &rarr; **Level 1 (HOD)**
    - **2 distinct confirmed reports** in group &rarr; **Level 2 (Dean)**
    - **3+ distinct confirmed reports** in group &rarr; **Level 3 (Higher Authority / Ombudsman)**
- **Role-Based Access Control (RBAC) & Specialized Dashboards**:
  - Distinct access controls and interfaces for **Student**, **HOD**, **Dean**, **Higher Authority**, and **Administrator**.
  - Backend dependency guards (`require_roles(...)`) reject unauthorized role access with HTTP 403.
- **Real-Time In-App Notifications**:
  - Authority officials receive in-app notifications on case escalations and candidate match proposals.
  - External email/SMS notification integration is pluggable for a future operational phase.
- **Tamper-Evident Security Audit Trail**:
  - Immutable chronological log in `audit_logs` tracking logins, case status transitions, exceptional identity unmasking, and review decisions with actor ID, reason, and IP address.
- **Sleek Modern Dark UI/UX**:
  - Elevated dark surfaces (`#121212` canvas / `#1E1E1E` panels / `#38B6FF` interactive cyan / `#FF5A5F` urgent coral).
  - Full keyboard accessibility, custom 2px focus rings, screen-reader ARIA live regions, and `prefers-reduced-motion` compliance.
  - 1-click **Quick Demo Role Fillers** on the login page for effortless live presentations.

---

## 🗄️ Entity-Relationship (ER) Diagram

The system architecture implements data isolation (separating reporter identities from complaint logs) and explicit group membership for Section 23 repeat-report escalation.

```mermaid
erDiagram
    users {
        int id PK
        string name
        string email UK
        string password_hash
        string role
        string department
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    complaints {
        int id PK
        string public_reference UK
        string tracking_secret_hash
        string reporting_mode
        string type
        string category
        date incident_date
        string incident_time
        string location_or_platform
        text description
        boolean is_urgent
        string status
        datetime created_at
        datetime updated_at
    }
    reporter_identities {
        int id PK
        int complaint_id FK,UK
        string full_name
        string email
        string phone
        string department
        string student_id_number
        string access_policy
        datetime created_at
    }
    suspect_details {
        int id PK
        int complaint_id FK
        string name
        string department
        string phone
        text other_description
        string details_visibility
        datetime created_at
    }
    evidence {
        int id PK
        int complaint_id FK
        string storage_key UK
        string original_filename_display
        string verified_media_type
        int file_size
        datetime uploaded_at
    }
    case_links {
        int id PK
        int complaint_id FK
        int related_complaint_id FK
        string review_status
        int reviewed_by FK
        datetime reviewed_at
        text reason
        datetime created_at
    }
    case_groups {
        int id PK
        string group_reference UK
        int created_by FK
        string status
        datetime created_at
    }
    case_group_members {
        int id PK
        int case_group_id FK
        int complaint_id FK
        datetime added_at
    }
    escalations {
        int id PK
        int case_group_id FK
        int complaint_id FK
        int level
        int authority_user_id FK
        text reason
        string status
        datetime created_at
    }
    case_status_history {
        int id PK
        int complaint_id FK
        string previous_status
        string new_status
        int changed_by FK
        text reason
        datetime created_at
    }
    notifications {
        int id PK
        int recipient_user_id FK
        string case_reference
        string title
        text message
        string channel
        boolean is_read
        datetime created_at
    }
    audit_logs {
        int id PK
        int actor_user_id FK
        string action
        string resource_type
        string resource_id
        text reason
        string ip_address
        datetime timestamp
    }

    users ||--o{ complaints : "submits (optional)"
    users ||--o{ escalations : "assigned_to"
    users ||--o{ notifications : "receives"
    users ||--o{ audit_logs : "performs_action"
    users ||--o{ case_links : "reviews"
    users ||--o{ case_groups : "creates"
    users ||--o{ case_status_history : "updated_by"

    complaints ||--o| reporter_identities : "has isolated identity"
    complaints ||--o{ suspect_details : "mentions"
    complaints ||--o{ evidence : "attaches"
    complaints ||--o{ case_links : "proposes link A"
    complaints ||--o{ case_links : "proposes link B"
    complaints ||--o{ case_group_members : "belongs_to"
    complaints ||--o{ case_status_history : "logs status transitions"
    complaints ||--o{ escalations : "escalated_individually"

    case_groups ||--o{ case_group_members : "contains confirmed members"
    case_groups ||--o{ escalations : "escalated_via Section 23"
```

---

## 🚀 Quick Start Guide

### 1. Requirements
- Python 3.11+
- Git

### 2. Virtual Environment Setup
```bash
# Clone or navigate to directory
cd "/Users/manoranjankumar.s/Documents/new hack"

# Create venv and install dependencies
/opt/homebrew/bin/python3.11 -m venv backend/.venv
./backend/.venv/bin/pip install -r backend/requirements.txt
```

### 3. Seed Demo Data
```bash
PYTHONPATH=. ./backend/.venv/bin/python database/seeds/seed_demo.py
```

### 4. Run Development Server
```bash
PYTHONPATH=. ./backend/.venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```
Open your browser at: **`http://localhost:8000`**

---

## 👥 Demo Authority Accounts

Quick-fill buttons are provided on the login page (`http://localhost:8000/login.html`):

| Role | Email | Password | Department |
| :--- | :--- | :--- | :--- |
| **HOD (Level 1)** | `hod.cse@campus.edu` | `HodPass2026!` | Computer Science & Engineering |
| **Dean (Level 2)** | `dean.studentaffairs@campus.edu` | `DeanPass2026!` | Student Affairs & Welfare |
| **Higher Authority (Level 3)** | `director.office@campus.edu` | `DirectorPass2026!` | Office of the Director / Ombudsman |
| **Administrator** | `admin@campus.edu` | `AdminPass2026!` | Campus Administration |
| **Student** | `student.demo@campus.edu` | `StudentPass2026!` | Computer Science & Engineering |

---

## 🧪 Running Automated Tests

Run the complete pytest test suite (covers intake, isolation, tracking, permissions, evidence, matching, and Section 23 escalation):

```bash
PYTHONPATH=. ./backend/.venv/bin/pytest backend/tests -v
```

---

## 🧭 Page Navigation Map

- **Public Landing Page**: `http://localhost:8000/index.html` (or `/`)
- **Submit Complaint Form**: `http://localhost:8000/report.html`
- **Track Status Portal**: `http://localhost:8000/track.html`
- **Authority Login**: `http://localhost:8000/login.html`
- **Authority Dashboard**: `http://localhost:8000/dashboard.html`
- **Match Review Matrix (Section 23)**: `http://localhost:8000/review.html`
- **Administration & Audit Trail**: `http://localhost:8000/admin.html`
