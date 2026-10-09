# Campus Safety & Harassment Reporting System

## System Design and Antigravity Implementation Specification

**Document status:** Finalized design specification --- ready for
implementation\
**Application type:** Full-stack web application\
**Frontend:** HTML, CSS, JavaScript\
**Backend:** Python + FastAPI\
**Database:** MySQL\
**Primary users:** Students, HODs, Deans, Higher Authority, designated
administrators\
**Core principles:** Student safety, confidentiality, anonymity where
requested, least-privilege access, human-reviewed matching, accountable
escalation

------------------------------------------------------------------------

# 1. Project Overview

The Campus Safety & Harassment Reporting System is a secure digital
platform intended to make it easier for students to report ragging,
harassment, stalking, intimidation, threats, and other safety concerns
that occur on campus, around campus, or through digital channels.

The platform must give students a clear, accessible way to submit a
report without having to determine the correct authority themselves. It
must support both **confidential reporting** and **anonymous
reporting**, allow evidence to be submitted when available, provide a
safe method to check report status, and help authorized campus staff
identify possible repeated incidents.

When several reports may relate to the same person, event, location, or
pattern, the system should flag them for authorized human review. It
must not treat a similarity score, a name match, or a number of reports
as proof that an allegation is true. Once a relationship has been
reviewed and confirmed according to the institution's process, the
system can route the case through the configured escalation levels.

The application is designed to support timely action while limiting
unnecessary exposure of a reporter's identity and other sensitive
details.

## 1.1 Product vision

Build a simple, trustworthy, privacy-conscious reporting platform that
helps students speak up, gives authorized staff the information they
need to respond, and makes the handling of reported concerns traceable
and accountable.

## 1.2 Core product goals

1.  Make submitting a safety report simple and accessible.
2.  Offer both confidential and anonymous reporting options.
3.  Protect reporter identity through data separation and server-side
    access controls.
4.  Support offline/in-person and online/cyber ragging report types.
5.  Allow optional evidence uploads without requiring evidence when it
    is unavailable.
6.  Provide secure report tracking without exposing reports through
    predictable identifiers.
7.  Flag possible related reports for authorized human review.
8.  Implement the configured escalation route: HOD → Dean → Higher
    Authority.
9.  Maintain a reliable history of case status, reviews, escalations,
    and access to sensitive information.
10. Make the user interface calm, respectful, accessible, responsive,
    and easy to understand.

## 1.3 What the system is not

-   It is not an emergency response service and must not promise
    immediate emergency assistance.
-   It does not determine guilt or make disciplinary findings
    automatically.
-   It does not guarantee absolute anonymity if a reporter voluntarily
    includes identifying details in a description or uploaded evidence.
-   It does not automatically classify two reports as the same incident
    solely because they mention the same name, department, phone number,
    or location.
-   It is not a substitute for the institution's official safeguarding,
    disciplinary, legal, or emergency procedures.

The interface must clearly tell users how to contact the institution's
designated emergency or safeguarding contact if someone is in immediate
danger. These contact details must be configured by the institution
before production use.

------------------------------------------------------------------------

# 2. Detailed Problem Statement

## 2.1 Background

Students can experience unwanted following, stalking, verbal or physical
harassment, intimidation, threats, ragging, online abuse, impersonation,
fake social-media accounts, or the circulation of offensive content.
These events may occur in classrooms, hostels, corridors, transport
areas, campus grounds, nearby public places, messaging applications,
social networks, or other digital spaces.

A student who experiences such conduct may be unsure how to report it,
which authority is responsible, what information is required, whether
evidence is necessary, and who will see the complaint. A student may
also fear retaliation, embarrassment, social pressure, being identified
by peers, or having sensitive information shared more widely than
necessary.

A second problem arises when more than one student reports similar
behaviour. Separate reports may remain in separate inboxes or be handled
without a consistent way to notice possible patterns. Authorities may
not know that several reports could concern the same incident or
repeated conduct. Conversely, reports that appear similar may concern
different events or people, so careless matching can create unfair
assumptions.

A digital reporting system can reduce these barriers by giving students
a consistent submission process, limiting access to sensitive
information, recording the status of each case, and helping authorized
reviewers notice possible relationships between reports.

## 2.2 Current problems to address

### Problem A --- Unclear reporting channels

Students may not know whether to contact a class tutor, HOD, Dean,
anti-ragging committee, student welfare office, security team, or
another designated authority. Different reporting channels can produce
inconsistent records and uncertainty about follow-up.

**Required response:** Provide one clear entry point for submitting a
report and route the report to the configured authority workflow.

### Problem B --- Fear of exposure

Students may hesitate to report if they believe their name, phone
number, department, statement, or evidence will be visible to too many
people.

**Required response:** Provide clearly explained confidential and
anonymous modes. Separate reporter identity data from ordinary complaint
data. Enforce access controls in the backend, not only by hiding fields
in the interface.

### Problem C --- Difficulty reporting different incident types

Offline harassment and online harassment may require different
descriptions and evidence. A single vague form can cause students to
omit important details or become confused.

**Required response:** Provide a shared report form with an incident
category, relevant type-specific fields, and clear guidance for optional
evidence.

### Problem D --- Evidence handling risks

Screenshots, photographs, documents, or other attachments can contain
names, phone numbers, account handles, faces, location information, or
other sensitive data. Storing files in public folders or displaying
unrestricted file links could expose reporters and other people.

**Required response:** Validate uploads on the server, store files
privately, generate non-guessable storage keys, restrict access by role
and case assignment, and log sensitive evidence access. Do not require
evidence as a condition for getting help when evidence is unavailable.

### Problem E --- Repeated reports may go unnoticed

Reports about similar conduct may arrive from different students and at
different times. If they are not reviewed together, staff may miss a
possible pattern.

**Required response:** Flag potential matches using appropriate case
attributes and let authorized staff confirm or reject the relationship.
Preserve a record of the review decision and reason.

### Problem F --- Inconsistent escalation

Without a documented workflow, staff may not know when a concern should
move from the HOD to the Dean or Higher Authority. Manual handoffs can
also be difficult to audit.

**Required response:** Configure a transparent escalation workflow,
record every escalation, notify the assigned authority, and retain a
status history.

### Problem G --- No clear status feedback

After submitting a report, a student may not know whether it was
received, reviewed, escalated, or closed. Repeatedly contacting staff
can increase stress and administrative workload.

**Required response:** Issue a random public reference and a separate
secure tracking credential. Display only approved status information and
avoid revealing sensitive internal notes.

### Problem H --- Limited accountability

If a report's details are viewed, changed, or escalated, there may be no
consistent record of who performed the action or why.

**Required response:** Keep protected audit events for important
actions, including case access, identity access, match decisions, status
changes, and escalations. Audit records must not unnecessarily duplicate
sensitive complaint content.

## 2.3 Problem statement

**Students need a secure, simple, and accessible way to report offline
and online ragging or harassment without unnecessary exposure of their
identity. Campus authorities need a consistent process to receive
reports, review possible repeated incidents, track case progress, and
escalate concerns to the appropriate authority. The system must balance
privacy, fair treatment, timely response, evidence protection, and
institutional accountability.**

## 2.4 Stakeholders

-   **Student/reporting person:** Needs a respectful and understandable
    reporting process and safe status tracking.
-   **HOD:** Reviews cases assigned at the first escalation level.
-   **Dean:** Reviews cases escalated to the second level.
-   **Higher Authority:** Reviews cases escalated to the third level and
    may receive additional details when authorized and necessary.
-   **Designated system administrator:** Manages authorized accounts,
    role assignments, system configuration, and operational settings.
-   **Safeguarding or student-welfare office:** May be the institution's
    designated contact for urgent or sensitive cases, depending on
    institutional policy.
-   **Institution/college:** Owns policy decisions, retention rules,
    escalation procedures, and lawful handling of personal data.

## 2.5 Expected outcomes

-   Fewer barriers to reporting.
-   Clearer separation between confidential and anonymous reporting.
-   Better tracking of report progress.
-   More consistent handling of potential repeated incidents.
-   Faster routing to the designated authority.
-   Less unnecessary access to personal information.
-   Better auditability of case handling.

------------------------------------------------------------------------

# 3. Scope

## 3.1 Included in the initial version

-   Public landing page with safety information.
-   Confidential report submission.
-   Anonymous report submission.
-   Offline and online incident categories.
-   Incident date, time, location, description, and optional suspect
    details.
-   Optional protected evidence uploads.
-   Random report reference and secure status tracking.
-   Role-based authority dashboards.
-   Human review queue for potential related reports.
-   HOD → Dean → Higher Authority escalation workflow.
-   Case status timeline.
-   In-app notification records; email or SMS integration can be added
    after provider details are confirmed.
-   Audit records for important actions.
-   Input validation and access-control tests.
-   Responsive and accessible interface.

## 3.2 Out of scope for the first version

-   Automated determination that an allegation is true.
-   Facial recognition or identification of people from images.
-   Automated disciplinary decisions.
-   Publicly searchable complaint records.
-   Public display of suspect details.
-   Automatic matching based only on a name or phone number.
-   Real-time emergency dispatch.
-   Integration with police, legal, campus access-control, or external
    student-information systems without formal approval.
-   Production deployment before institutional policy, access rules,
    retention, and incident-response procedures are reviewed.

------------------------------------------------------------------------

# 4. Final Technology Stack

## Frontend

-   HTML5
-   CSS3
-   Vanilla JavaScript
-   Responsive layouts and accessible form controls
-   Fetch API for backend REST endpoints

## Backend

-   Python 3.11 or another supported Python version selected during
    setup
-   FastAPI
-   Pydantic request and response schemas
-   SQLAlchemy ORM
-   Alembic database migrations
-   Argon2id or another appropriately configured password-hashing method
    for passwords
-   Server-side authorization for every protected endpoint

## Database

-   MySQL with InnoDB tables, foreign keys, indexes, transactions, and
    restricted database credentials

## Evidence storage

-   Private filesystem storage for a local development environment or
    private object storage for deployment
-   Files must not be served directly from a public static directory
-   The backend authorizes every file download

## Testing

-   pytest
-   FastAPI test client
-   Unit tests for escalation and matching review
-   API authorization tests
-   Manual accessibility and responsive-layout checks

## Development configuration

-   `.env` for local secrets (never commit it)
-   `.env.example` containing placeholder values only
-   `.gitignore` excluding secrets, uploaded evidence, logs, virtual
    environments, and generated files
-   `README.md` with setup, run, test, and demo instructions

------------------------------------------------------------------------

# 5. High-Level Architecture

``` text
Student / HOD / Dean / Higher Authority / Administrator
                         |
                         v
             Frontend: HTML + CSS + JS
                         |
                   HTTPS / REST API
                         |
                         v
                  FastAPI Backend
                         |
      +------------------+--------------------+
      |                  |                    |
      v                  v                    v
 Authentication     Complaint Service    Authorization
 and Sessions       and Tracking          and Audit
      |                  |                    |
      +------------------+--------------------+
                         |
          +--------------+-----------------+
          |              |                 |
          v              v                 v
       MySQL       Related-Case        Notification
       Database       Review              Service
          |              |
          v              v
   Protected records  Escalation engine
                         |
               HOD -> Dean -> Higher Authority

Evidence upload -> validation -> private file storage
                         |
                authorized download only
```

## 5.1 Architecture rules

1.  The frontend is untrusted. It cannot grant itself a role or
    authorize access to a case.
2.  Every protected API endpoint checks the authenticated user and their
    permissions.
3.  The backend determines the permitted case fields returned to each
    role.
4.  Reporter identity is stored separately from ordinary case details.
5.  Anonymous reporting does not create a reporter identity record.
6.  The backend, not browser JavaScript, calculates escalation state.
7.  Possible report matches are flagged for authorized human review.
8.  Evidence is private by default.
9.  Sensitive actions are recorded in an audit log.
10. All secret keys and database credentials come from environment
    configuration, not source code.

------------------------------------------------------------------------

# 6. User Roles and Permissions

## 6.1 Student

Can: - Read safety information. - Select confidential or anonymous
reporting. - Submit a report. - Receive a random report reference. -
Track a report using the reference and a separate secret credential. -
See approved status updates for their own report.

Cannot: - Browse other students' complaints. - View internal staff
notes. - See private evidence unless the institution explicitly supports
a permitted process. - Change escalation levels. - Access authority
dashboards.

## 6.2 HOD

Can: - View cases assigned to the HOD role or specific HOD account. -
See the case information needed for the current review. - Record
actions, add authorized notes, and update permitted statuses. - Review
potential matches if assigned.

Default identity policy: - Reporter identity is not displayed in the
normal HOD case view. - Any exceptional identity access must require a
specific authorization policy, a documented reason, and an audit event.

## 6.3 Dean

Can: - View cases assigned to the Dean escalation level. - Review the
case summary and the authorized history of previous actions. - Confirm
or reject potential case links when assigned. - Escalate the case to
Higher Authority according to policy.

Default identity policy: - Reporter identity remains restricted unless
specifically authorized and necessary.

## 6.4 Higher Authority

Can: - View cases escalated to the third level. - Review the authorized
case history and previous decisions. - Access additional sensitive
details only if a defined policy permits it and the access is
necessary. - Record final handling decisions and case status.

## 6.5 Administrator

Can: - Create, disable, and manage authorized authority accounts. -
Assign roles and department relationships. - Configure escalation
recipients and non-secret application settings. - View operational audit
records according to policy.

An administrator should not automatically receive unrestricted access to
all reporter identities merely because they manage the application.

## 6.6 Authorization principle

Use least privilege. Permissions must be enforced by backend
dependencies or service-level policy checks for every request, including
file downloads and status tracking. Hiding a button in the frontend is
not a security control.

------------------------------------------------------------------------

# 7. Reporting Modes

## 7.1 Confidential report

A confidential report allows a reporter's identity or contact
information to be retained for authorized follow-up. The application
must explain what information is collected, who may access it, and under
what circumstances it could be disclosed.

Implementation: - Store identity/contact data in `reporter_identities`,
separate from the main complaint record. - Encrypt sensitive fields
where appropriate and protect encryption keys outside the database. -
Restrict identity access to a specifically authorized workflow. - Record
identity access in the audit log. - Do not expose identity fields in
ordinary HOD, Dean, or Higher Authority responses unless the access
policy allows it.

## 7.2 Anonymous report

An anonymous report does not ask for the reporter's name or account
identity. It must not create a reporter identity record.

Implementation: - Allow report submission without login. - Generate a
random public reference and a separate high-entropy tracking secret. -
Show the tracking secret once and instruct the reporter to keep it
safe. - Store only a secure hash of the tracking secret when feasible. -
Do not claim that anonymous reports are impossible to trace:
descriptions, uploaded files, browser/infrastructure logs, or
voluntarily supplied details may reveal identity. - Avoid collecting
unnecessary analytics or identifying metadata.

## 7.3 Confidential versus anonymous

The interface must explain the distinction before the student chooses. A
confidential report can support follow-up using retained contact
details. An anonymous report minimizes identity collection, but
follow-up may be limited if the student loses the tracking credential.

## 7.4 Tracking security

Use a random, unguessable public reference and a separate secret
tracking credential. Do not allow anyone who knows a short sequential
complaint ID to read the complaint. Rate-limit tracking attempts and
return only approved status fields.

------------------------------------------------------------------------

# 8. Incident Categories and Complaint Form

## 8.1 Offline / in-person ragging

Possible categories: - Following or stalking - Unwanted behaviour -
Threats or intimidation - Physical or verbal harassment - Other
in-person incident

## 8.2 Online / cyber ragging

Possible categories: - Fake accounts or impersonation - Obscene or
abusive content - Online threats - Cyber harassment - Other online
incident

## 8.3 Core form fields

-   Reporting mode: confidential or anonymous
-   Incident type: offline or online
-   Incident category
-   Incident date
-   Approximate time or time range
-   Location or digital platform
-   Description in the reporter's own words
-   Suspect details, if known and voluntarily provided
-   Evidence attachment, if available
-   Optional contact details for confidential reporting
-   A clear privacy notice
-   A statement that submitted allegations are reviewed and are not
    automatically treated as proven facts

Do not ask for unnecessary sensitive information. Avoid leading
questions. Do not require a student to identify a suspected person when
they do not know the identity.

## 8.4 Evidence upload rules

-   Accept only approved file types.
-   Enforce file-size and request-size limits.
-   Validate actual file content rather than trusting the filename or
    browser-provided MIME type.
-   Generate a random storage key.
-   Store files outside public static directories.
-   Scan uploads for malware when the deployment environment supports
    it.
-   Authorize every evidence preview/download on the server.
-   Record evidence access where required by policy.
-   Avoid embedding evidence directly in publicly accessible links.
-   Explain that screenshots can contain information about other people
    and should only be uploaded when appropriate.

For online incidents, the interface may encourage screenshot evidence if
available. Lack of a screenshot must not prevent a student from
reporting or seeking assistance.

------------------------------------------------------------------------

# 9. Page Structure

## 9.1 `index.html` --- Landing page

Sections: - Header and navigation - Clear "Report a Concern" action -
Short explanation of confidential and anonymous reporting - Offline and
online incident summaries - "How reporting works" steps - Privacy and
access explanation - Institution-approved emergency/safeguarding contact
information - Accessibility and language options

## 9.2 `report.html` --- Complaint form

Sections: - Reporting mode choice - Incident type selection - Date,
time, location/platform, and description - Optional suspect details -
Optional evidence upload - Privacy notice and submission confirmation -
Field-level validation and accessible error messages

## 9.3 `track.html` --- Report tracking

Fields: - Public report reference - Separate tracking secret - Approved
status and timeline - Safe guidance about what to do if the tracking
credential is lost

Do not display reporter identity, suspect contact information, evidence,
or internal notes in the tracking response.

## 9.4 `login.html` --- Authority login

-   Email/username
-   Password
-   Accessible validation and error messages
-   Secure session behavior
-   Rate limiting and login audit events
-   No public self-registration for authority roles

## 9.5 `dashboard.html` --- Authority dashboard

-   Assigned cases
-   Status and escalation filters
-   Review queue
-   Case reference and minimum-necessary summary
-   Actions available to the signed-in role
-   No identity fields by default

## 9.6 `case-detail.html` --- Case details

-   Case summary
-   Incident information
-   Evidence access when authorized
-   Status history
-   Related-report review history
-   Escalation actions available to the current role
-   Restricted identity section only where policy authorizes access

## 9.7 `review.html` --- Related-case review

-   Two or more candidate case summaries
-   Reasons they were flagged
-   Explicit "Confirm related", "Reject match", or "Needs more review"
    options
-   Reviewer reason/comment
-   Confirmation before committing the decision
-   Audit event

The review interface should show only the minimum information needed to
make a decision. Do not automatically reveal reporter identity to
reviewers just because a match is being assessed.

## 9.8 `admin.html` --- Administration

-   Authority account management
-   Role and department assignments
-   Escalation recipient configuration
-   Non-secret system configuration
-   Audit-log search for authorized administrators

## 9.9 Shared UI components

-   Header and navigation
-   Accessible alert/notification region
-   Status badge
-   Confirmation dialog
-   Loading, empty, and error states
-   Evidence upload component
-   Privacy notice
-   Footer with approved help contacts

------------------------------------------------------------------------

# 10. Database Design

Database name: `campus_safety_db`

Use MySQL with InnoDB, foreign keys, suitable indexes, transactions, and
migration-managed schema changes.

## 10.1 `users`

Purpose: Authorized user accounts.

Fields: - `id` --- primary key - `name` - `email` --- unique -
`password_hash` - `role` --- student, HOD, dean, higher_authority,
administrator - `department_id` --- nullable foreign key if departments
are modeled - `is_active` - `created_at` - `updated_at`

Never store plaintext passwords. Authority role assignment must be
controlled by an authorized administrative workflow.

## 10.2 `complaints`

Purpose: Main incident record, without unnecessary reporter identity
fields.

Fields: - `id` --- internal primary key - `public_reference` --- random
unique public identifier - `reporting_mode` --- confidential or
anonymous - `type` --- offline or online - `category` -
`incident_date` - `incident_time` --- nullable/approximate if not
known - `location_or_platform` - `description` - `status` --- submitted,
under_review, escalated, resolved, closed - `created_at` - `updated_at`

Do not expose internal database IDs as secret access credentials.

## 10.3 `reporter_identities`

Purpose: Separate reporter identity/contact data from the complaint
record.

Fields: - `id` --- primary key - `complaint_id` --- foreign key -
`user_id` --- nullable foreign key if a confidential report is linked to
an account - `encrypted_contact` --- nullable encrypted field or
encrypted structured contact fields - `access_policy` - `created_at`

Anonymous reports must not create an identity row. Access to this table
should be restricted independently from normal complaint access.

## 10.4 `suspect_details`

Purpose: Store voluntarily provided information about a suspected person
separately.

Fields: - `id` - `complaint_id` - `name` --- nullable - `department` ---
nullable - `phone` --- nullable - `other_description` --- nullable -
`details_visibility` - `created_at`

These fields represent allegations or unverified information, not
confirmed findings. Access must be restricted and retention must follow
policy.

## 10.5 `evidence`

Purpose: Metadata for privately stored uploaded files.

Fields: - `id` - `complaint_id` - `storage_key` -
`original_filename_display` --- sanitized and optional -
`verified_media_type` - `file_size` - `uploaded_at` -
`uploaded_by_user_id` --- nullable for anonymous submission, where
appropriate

Store file bytes in protected storage, not as a public URL. Download
routes must enforce authorization.

## 10.6 `case_links`

Purpose: Link reports that a reviewer has determined may be related.

Fields: - `id` - `complaint_id` - `related_complaint_id` -
`review_status` --- pending, confirmed, rejected, needs_more_review -
`reviewed_by` - `reviewed_at` - `reason` - `created_at`

Use database constraints to prevent self-links and duplicate
relationships. Potential matches must be distinguished from confirmed
links.

## 10.7 `case_groups`

Purpose: Optional case grouping when several complaints are confirmed to
be related.

Fields: - `id` - `group_reference` - `created_at` - `created_by` -
`status`

A case group should be created or updated only through an authorized,
auditable workflow. It must not silently merge independent reports.

## 10.8 `escalations`

Purpose: Record escalation actions and assigned authorities.

Fields: - `id` - `case_group_id` --- nullable if policy permits a single
complaint to be escalated independently - `complaint_id` --- nullable
depending on the chosen case model; ensure a valid parent relationship -
`level` --- 1, 2, or 3 - `authority_user_id` - `reason` - `status` ---
pending, notified, acknowledged, completed, cancelled - `created_at` -
`acknowledged_at` - `resolved_at`

The implementation must choose and document one consistent parent model
for escalation records before migrations are written; do not allow a row
with no valid case reference.

## 10.9 `case_status_history`

Purpose: Record status changes.

Fields: - `id` - `complaint_id` - `previous_status` - `new_status` -
`changed_by` - `reason` - `created_at`

## 10.10 `notifications`

Purpose: Track notification delivery state.

Fields: - `id` - `recipient_user_id` - `case_reference` -
`notification_type` - `channel` --- in_app, email, sms if configured -
`delivery_status` - `created_at` - `sent_at`

Notification content should not include unnecessary sensitive details.
Email/SMS should generally say that an authorized user should sign in to
review a case rather than including complaint narratives or evidence.

## 10.11 `audit_logs`

Purpose: Record important security and case-management events.

Fields: - `id` - `actor_user_id` --- nullable for a system event -
`action` - `resource_type` - `resource_id` - `reason` --- where
required - `timestamp` - `request_correlation_id` --- optional

Do not copy full complaint descriptions, passwords, tracking secrets, or
file contents into logs. Protect logs from unauthorized modification and
define a retention policy.

## 10.12 Database relationships

``` text
users 1 ------ * complaints (only where a permitted account link exists)
complaints 1 ------ 0..1 reporter_identities
complaints 1 ------ * suspect_details
complaints 1 ------ * evidence
complaints * ------ * complaints through case_links
case_groups 1 ------ * confirmed group memberships (if modeled explicitly)
complaints/case_groups 1 ------ * escalations
complaints 1 ------ * case_status_history
users 1 ------ * notifications
users 1 ------ * audit_logs (actor relationship, nullable for system events)
```

Before implementation, decide whether a confidential reporter's user
link is stored in `reporter_identities` only or also represented through
another explicit relationship. Do not duplicate identity links
unnecessarily.

------------------------------------------------------------------------

# 11. Repeated-Report Matching and Escalation

## 11.1 Required behavior

The system must flag potential matches for authorized staff review.
Matching can consider permitted information such as incident timing,
location, category, description, or voluntarily provided suspect
details. Matching must be designed carefully because shared names,
departments, locations, or words are not proof that reports are related.

## 11.2 Workflow

1.  A student submits a complaint.
2.  The backend validates and stores the complaint.
3.  The system generates a random reference and secure tracking
    credential.
4.  The matching service identifies candidate reports using approved
    criteria.
5.  The system creates a pending review item without treating the match
    as confirmed.
6.  An authorized reviewer examines the permitted summaries and records
    a decision.
7.  If the relationship is confirmed, the backend updates the case
    relationship/group inside a transaction.
8.  The escalation service evaluates the configured policy.
9.  The system creates an escalation record and notification for the
    designated authority.
10. The case status and audit history are updated.

## 11.3 Escalation levels

-   **Level 1 --- HOD:** Initial report/case routed to the designated
    HOD.
-   **Level 2 --- Dean:** Second confirmed related report, according to
    the institution's approved policy, routes the case to the Dean.
-   **Level 3 --- Higher Authority:** Third confirmed related report
    routes the case to Higher Authority.

The precise counting rule must be approved by the institution. The
proposed default is to count distinct, confirmed related reports within
a configured case group, not the number of duplicate submissions. The
system must not count a pending or rejected match.

## 11.4 Important safeguards

-   Three reports are not proof of three confirmed offences.
-   No student should be required to wait for a third report if they
    need urgent help.
-   A reviewer can reject a false match or request more review.
-   The reason for confirming a match must be recorded.
-   The system should prevent duplicate submissions from inflating the
    count where feasible.
-   Every escalation must record its level, recipient, reason, and
    timestamp.
-   The institution must define how cases are reassigned if a reviewer
    has a conflict of interest.
-   Escalation must not expose the reporter's identity by default.
-   The third level may access additional details only if policy
    explicitly permits it and the access is necessary.
-   A match review or escalation is an administrative workflow, not a
    determination of guilt.

## 11.5 Urgent cases

If the report indicates immediate danger, the interface must show
institution-approved emergency or safeguarding guidance. A designated
urgent-review path may be configured. Do not delay urgent handling until
a repeat-report threshold is met.

------------------------------------------------------------------------

# 12. Case Status Lifecycle

Suggested states:

-   `submitted`
-   `under_review`
-   `pending_match_review`
-   `escalated`
-   `awaiting_information` (only if follow-up is possible and
    appropriate)
-   `resolved`
-   `closed`

The implementation should define valid transitions. For example, a case
should not be marked resolved by an unauthorized role, and a closed case
should not silently return to an active state without a recorded reason.

Each status change should create a `case_status_history` record. The
student tracking view should expose only approved status labels and safe
explanatory messages.

------------------------------------------------------------------------

# 13. REST API Design

Base prefix: `/api`

## 13.1 Authentication

-   `POST /api/auth/login` --- sign in an authorized account
-   `POST /api/auth/logout` --- end session
-   `GET /api/auth/me` --- retrieve current account and permitted role
    information

Use secure session cookies or another carefully configured
authentication method. For a browser-based application, prefer HttpOnly,
Secure, SameSite cookies with CSRF protection where applicable. Do not
store long-lived authentication secrets in localStorage.

## 13.2 Complaints

-   `POST /api/complaints` --- submit confidential or anonymous report
-   `GET /api/complaints/track` --- check approved status using
    reference and separate secret
-   `GET /api/authority/cases` --- list cases visible to the signed-in
    authority
-   `GET /api/cases/{case_id}` --- retrieve an authorized case view
-   `PATCH /api/cases/{case_id}/status` --- update permitted status
-   `POST /api/cases/{case_id}/evidence` --- upload evidence
-   `GET /api/evidence/{evidence_id}` --- download/preview evidence
    after authorization

## 13.3 Match review and escalation

-   `GET /api/authority/match-reviews` --- list pending reviews for an
    authorized reviewer
-   `POST /api/cases/{case_id}/review-match` --- confirm, reject, or
    request further review
-   `POST /api/cases/{case_id}/escalate` --- perform a permitted
    escalation
-   `GET /api/cases/{case_id}/history` --- retrieve permitted status and
    escalation history

## 13.4 Administration

-   `GET /api/admin/users`
-   `POST /api/admin/users`
-   `PATCH /api/admin/users/{user_id}`
-   `GET /api/admin/audit-logs`
-   `GET /api/admin/configuration`
-   `PATCH /api/admin/configuration`

All admin endpoints require server-side authorization. Do not expose
secret configuration values through the configuration endpoint.

## 13.5 API rules

-   Validate every request using Pydantic schemas.
-   Use consistent error responses that do not leak private data.
-   Add rate limits to login, tracking, report submission, and upload
    endpoints.
-   Use pagination and maximum page sizes for lists.
-   Avoid including reporter identity in general case-list responses.
-   Use database transactions for operations that create case links,
    groups, escalations, or status history.
-   Use a notification outbox or reliable retry mechanism if
    notification delivery is added.
-   Generate and log a request correlation ID for troubleshooting
    without logging secrets.

------------------------------------------------------------------------

# 14. Recommended Project Folder Structure

``` text
campus-safety-system/
├── frontend/
│   ├── index.html
│   ├── report.html
│   ├── track.html
│   ├── login.html
│   ├── dashboard.html
│   ├── case-detail.html
│   ├── review.html
│   ├── admin.html
│   ├── css/
│   │   ├── variables.css
│   │   ├── base.css
│   │   ├── layout.css
│   │   ├── components.css
│   │   ├── forms.css
│   │   ├── dashboard.css
│   │   └── responsive.css
│   ├── js/
│   │   ├── api.js
│   │   ├── auth.js
│   │   ├── report.js
│   │   ├── tracking.js
│   │   ├── dashboard.js
│   │   ├── case-detail.js
│   │   ├── review.js
│   │   ├── admin.js
│   │   └── components.js
│   └── assets/
│       ├── icons/
│       └── images/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── complaints.py
│   │   │   ├── tracking.py
│   │   │   ├── cases.py
│   │   │   ├── evidence.py
│   │   │   ├── match_reviews.py
│   │   │   ├── escalations.py
│   │   │   └── admin.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── permissions.py
│   │   │   └── errors.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   └── base.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── complaint.py
│   │   │   ├── identity.py
│   │   │   ├── evidence.py
│   │   │   ├── case_link.py
│   │   │   ├── escalation.py
│   │   │   ├── status_history.py
│   │   │   ├── notification.py
│   │   │   └── audit_log.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── complaint.py
│   │   │   ├── tracking.py
│   │   │   ├── case.py
│   │   │   └── review.py
│   │   ├── services/
│   │   │   ├── complaint_service.py
│   │   │   ├── identity_service.py
│   │   │   ├── matching_service.py
│   │   │   ├── escalation_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── evidence_service.py
│   │   │   └── audit_service.py
│   │   └── utils/
│   │       ├── ids.py
│   │       └── validators.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_permissions.py
│   │   ├── test_complaints.py
│   │   ├── test_tracking.py
│   │   ├── test_match_review.py
│   │   ├── test_escalation.py
│   │   └── test_evidence.py
│   ├── migrations/
│   ├── requirements.txt
│   └── .env.example
├── database/
│   ├── schema.sql
│   └── seeds/
│       └── demo_data.sql
├── docs/
│   ├── system-design.md
│   ├── api-documentation.md
│   ├── privacy-and-security.md
│   └── test-plan.md
├── .gitignore
├── README.md
└── LICENSE
```

## Folder rules

-   Do not commit `.env`, passwords, API keys, real complaint records,
    real evidence, database dumps containing personal data, or
    production logs.
-   Only synthetic, clearly labeled demo data may be included in seed
    files.
-   Store uploaded files outside `frontend/assets` and any public static
    directory.
-   Do not put authentication logic or escalation decisions only in
    frontend JavaScript.
-   Keep business logic in backend services, request validation in
    schemas, and data access in database models/repositories.
-   Keep migrations as the authoritative way to evolve the schema.

------------------------------------------------------------------------

# 15. Security and Privacy Requirements

## 15.1 Authentication and sessions

-   Hash passwords using a suitable password-hashing algorithm.
-   Use secure session handling and appropriate cookie settings.
-   Protect state-changing cookie-authenticated requests against CSRF.
-   Apply login rate limits and generic login error messages.
-   Provide a controlled account-disable and session-revocation process.
-   Do not create authority accounts through unrestricted public
    registration.

## 15.2 Authorization

-   Enforce role and case-assignment checks on every protected API.
-   Use least privilege and field-level response filtering.
-   Restrict reporter identity and suspect detail access separately from
    general case access.
-   Authorize evidence downloads every time.
-   Prevent users from changing role IDs or case ownership through
    manipulated request bodies.
-   Test direct API access, not only page navigation.

## 15.3 Data protection

-   Use HTTPS in deployment.
-   Encrypt sensitive identity fields where appropriate.
-   Keep encryption keys separate from the database.
-   Minimize collection of IP addresses, browser metadata, and analytics
    identifiers.
-   Define retention, deletion, legal hold, and backup rules with the
    institution.
-   Avoid sensitive content in email/SMS notifications.
-   Keep audit logs protected and minimize sensitive content in them.

## 15.4 Anonymous reporting limitations

The system should minimize identifying data collection, but it must not
promise that anonymity is absolute. A description may name the reporter,
an image may reveal a face, and infrastructure logs may contain
metadata. Explain these limitations before submission.

## 15.5 Evidence security

-   Restrict allowed file types and maximum sizes.
-   Validate file signatures and content.
-   Generate random storage names.
-   Keep uploads private.
-   Prevent path traversal and unsafe file serving.
-   Scan files when an appropriate scanning service is available.
-   Apply retention rules to evidence.
-   Do not expose original filenames or private storage keys
    unnecessarily.

## 15.6 Abuse prevention

-   Rate-limit report submissions and tracking attempts.
-   Validate and normalize inputs.
-   Escape user-generated content when rendering it in HTML.
-   Use parameterized database operations/ORM methods.
-   Prevent cross-site scripting, SQL injection, CSRF where relevant,
    insecure direct-object references, and unsafe uploads.
-   Do not allow public enumeration of complaints.
-   Provide a policy for malicious, duplicate, or abusive submissions
    without discouraging good-faith reporting.

## 15.7 Safety and fairness

-   Treat complaint content as allegations until appropriately reviewed.
-   Do not publicly expose names or suspect information.
-   Do not automatically punish or label a person because multiple
    reports exist.
-   Support a reviewer rejecting a false match.
-   Record why a match was confirmed or rejected.
-   Allow urgent handling without waiting for a repeat-report threshold.
-   Configure conflict-of-interest reassignment where needed.
-   Ensure a reporter's identity is not exposed by default when a case
    is escalated.

------------------------------------------------------------------------

# 16. User Experience and Accessibility

Visual direction: - Calm, professional navy/blue/white foundation with
restrained safety-focused accents. - Avoid aggressive warning-heavy
visuals on the landing page. - Use clear language, short instructions,
and predictable navigation. - Responsive layout for mobile phones,
tablets, and desktop. - Accessible form labels, keyboard navigation,
visible focus states, readable contrast, and meaningful error
messages. - Do not rely on color alone to indicate status. - Respect
reduced-motion preferences if animations are added. - Provide a clear
confirmation after submission, without displaying sensitive content on a
shared screen. - Explain the difference between confidential and
anonymous reporting in plain language. - Keep emergency guidance visible
without implying that a web form is monitored in real time.

Suggested status labels: - Submitted - Under Review - Awaiting Review -
Escalated - Resolved - Closed

Status definitions and closure rules must be agreed with the
institution.

------------------------------------------------------------------------

# 17. Testing Plan

## 17.1 Functional tests

-   Submit an offline complaint.
-   Submit an online complaint.
-   Submit a confidential report.
-   Submit an anonymous report.
-   Upload a valid evidence file.
-   Reject an invalid or oversized upload.
-   Generate unique report references and tracking credentials.
-   Retrieve a report's safe status with valid credentials.
-   Reject tracking attempts with an invalid secret.
-   Confirm that status changes create history records.
-   Confirm that notification and escalation records are created as
    expected.

## 17.2 Matching and escalation tests

-   A potential match is flagged but not counted before review.
-   A reviewer can confirm a relationship with a recorded reason.
-   A reviewer can reject a relationship.
-   A pending or rejected match does not increase the confirmed
    related-report count.
-   Duplicate submissions do not silently inflate escalation counts.
-   The first confirmed related report routes according to the
    configured HOD rule.
-   The second confirmed related report routes according to the
    configured Dean rule.
-   The third confirmed related report routes according to the
    configured Higher Authority rule.
-   Urgent handling is not blocked by the repeat threshold.
-   Concurrent submissions cannot create inconsistent escalation levels;
    use transactions and suitable locking/constraints.

## 17.3 Authorization tests

-   A student cannot list other complaints.
-   A student cannot view internal notes.
-   An HOD cannot access a case outside their permission scope.
-   A Dean cannot access reporter identity without authorization.
-   A Higher Authority cannot bypass identity-access rules.
-   A disabled account cannot continue using protected endpoints.
-   A user cannot change their own role by editing a request.
-   Evidence downloads are denied to unauthorized users.
-   Tracking credentials cannot be guessed through sequential IDs.

## 17.4 Privacy tests

-   Anonymous submission creates no reporter identity record.
-   Anonymous tracking does not require a user account.
-   Identity fields do not appear in ordinary authority responses.
-   Logs do not contain passwords, tracking secrets, or full sensitive
    descriptions unnecessarily.
-   Notifications do not reveal complaint narratives to unauthorized
    recipients.
-   Evidence storage cannot be accessed through public URLs.

## 17.5 UI tests

-   Mobile responsiveness.
-   Keyboard-only navigation.
-   Form labels and error messages.
-   Empty/loading/error states.
-   Confirmation before sensitive review or escalation actions.
-   Reduced-motion behavior.
-   Readability and accessible contrast.

------------------------------------------------------------------------

# 18. Development Plan

## Phase 1 --- Repository and environment

1.  Create the folder structure.
2.  Initialize Git and `.gitignore`.
3.  Create Python virtual environment.
4.  Install FastAPI, Uvicorn, SQLAlchemy, database driver, Alembic,
    password-hashing library, and testing dependencies.
5.  Configure `.env.example`.
6.  Create the FastAPI health endpoint.

## Phase 2 --- Database

1.  Design SQLAlchemy models.
2.  Create migrations.
3.  Add foreign keys, unique constraints, indexes, and transaction
    boundaries.
4.  Seed only synthetic demo accounts and cases.
5.  Verify schema creation and migrations.

## Phase 3 --- Backend security foundation

1.  Implement login/session handling.
2.  Implement role and case-assignment authorization.
3.  Implement error handling and request validation.
4.  Add audit service.
5.  Add permission tests before implementing sensitive case operations.

## Phase 4 --- Complaint workflow

1.  Implement confidential report submission.
2.  Implement anonymous report submission.
3.  Implement tracking references and secure tracking credentials.
4.  Implement private evidence storage.
5.  Implement safe status history.

## Phase 5 --- Match review and escalation

1.  Implement candidate-match flagging.
2.  Implement reviewer decision workflow.
3.  Implement confirmed case links/groups.
4.  Implement escalation rules and transactions.
5.  Implement notification records and audit events.
6.  Test the three escalation levels and urgent path.

## Phase 6 --- Frontend

1.  Build the landing page.
2.  Build the report form.
3.  Build the tracking page.
4.  Build the authority login and dashboard.
5.  Build case detail and match-review pages.
6.  Build the admin page.
7.  Connect each page to the backend using the shared API client.
8.  Add accessibility and responsive behavior.

## Phase 7 --- Verification and demo

1.  Run backend tests.
2.  Run authorization and privacy tests.
3.  Run end-to-end workflows using synthetic data.
4.  Confirm evidence is not publicly accessible.
5.  Verify the escalation history.
6.  Prepare a demo walkthrough with fictional reports.
7.  Document remaining limitations before any deployment.

------------------------------------------------------------------------

# 19. Acceptance Criteria

The first implementation is considered functionally complete when:

-   A student can submit either confidential or anonymous reports.
-   Both offline and online incident types are supported.
-   Evidence can be uploaded privately and is not publicly accessible.
-   The system issues a report reference and secure tracking credential.
-   The student can retrieve approved status information.
-   Authority users can sign in and see only cases they are permitted to
    access.
-   Potential related reports enter a human-review queue.
-   Confirmed and rejected matches are recorded with reviewer and
    decision history.
-   The configured HOD → Dean → Higher Authority escalation workflow
    operates correctly.
-   An urgent case can be routed without waiting for repeat reports.
-   Important case actions create audit records.
-   Automated tests cover core permissions, matching, tracking, uploads,
    and escalation.
-   The README explains setup, configuration, test commands, demo
    accounts, and limitations.
-   No real student information or real complaint evidence is committed
    to the repository.

------------------------------------------------------------------------

# 20. Configuration Decisions Still Required

Use safe placeholders during development. Before real deployment, obtain
institution approval for these items:

1.  Official name of the institution and its safeguarding/reporting
    office.
2.  Exact names and account assignments for HOD, Dean, and Higher
    Authority roles.
3.  Whether escalation counts reports across the same alleged person,
    same incident, or another institution-approved case grouping.
4.  The urgent-report recipient and response procedure.
5.  Whether email/SMS notifications are required and which approved
    provider to use.
6.  Evidence file types, size limits, scanning, retention, and deletion
    rules.
7.  Confidential identity-access policy and approval process.
8.  Anonymous reporting limitations and whether any non-essential
    network logs can be disabled or minimized.
9.  Data-retention periods and applicable institutional/legal
    obligations.
10. Hosting environment, domain, HTTPS, backups, and operational
    ownership.

These are policy and deployment decisions; they should not be guessed by
the coding agent.

------------------------------------------------------------------------

# 21. Instructions for Antigravity

Use this document as the source of truth.

**Before coding:** 1. Inspect the existing workspace and report whether
it contains files that must be preserved. 2. Present a concise
implementation plan and identify any conflicts with this specification.
3. Create the folder structure. 4. Implement the database schema and
backend security foundation before connecting the frontend. 5. Keep code
modular and readable. 6. Use environment variables for secrets. 7.
Include migrations, tests, synthetic seed data, and a useful README. 8.
Do not invent production credentials, institution contacts, policies, or
real student data. 9. Do not claim security is guaranteed merely because
encryption or role-based UI is present. 10. Run the tests and report
what passed, failed, or remains incomplete.

**Implementation priorities:** - Correct privacy boundaries and
authorization. - Reliable report submission and secure tracking. -
Human-reviewed related-case matching. - Correct escalation transactions
and audit trail. - Accessible, responsive frontend. - Polished visual
design after the critical workflows are correct.

**Important:** Do not replace the required HTML/CSS/JavaScript frontend
with a different framework unless the project owner explicitly approves
the change. Do not implement the entire application as a static mockup;
connect the frontend to the FastAPI backend and MySQL database.

------------------------------------------------------------------------

# 22. Suggested README Summary

Campus Safety & Harassment Reporting System is a full-stack web
application designed to help students report offline and online ragging
or harassment through confidential or anonymous reporting modes. It
supports secure status tracking, protected evidence handling, role-based
authority dashboards, human-reviewed related-report matching, and a
configurable escalation workflow from HOD to Dean to Higher Authority.

The project prioritizes privacy, minimum-necessary access, transparent
review, and accountable case handling. It is a reporting and
case-management aid, not an automated adjudication system or
emergency-response service.

------------------------------------------------------------------------

# 23. Final Repeat-Report Counting Policy

## Decision

For the hackathon prototype, repeat-report escalation is based on a **confirmed pattern of related incidents**, not merely a matching suspect name, a matching location, or a text-similarity score. This policy is the default until the institution formally approves its operational rules.

## What counts

- A report is initially an independent complaint.
- The matching service may flag candidate reports using approved attributes such as incident timing, location/platform, category, narrative similarity, and voluntarily supplied suspect details.
- A candidate match remains **pending** until an authorized reviewer assesses it.
- Only reports that an authorized reviewer confirms as related may contribute to the repeat-report count for a case group.
- Duplicate submissions, pending matches, and rejected matches must not increase the count.
- A confirmed relationship means the reports are considered related for case-management purposes; it does **not** prove that an allegation is true or that a named person is responsible.

## Escalation rule for the prototype

1. **First confirmed report in a case group → HOD.**
2. **Second distinct confirmed related report in that group → Dean.**
3. **Third distinct confirmed related report in that group → Higher Authority.**

The escalation service must calculate the level on the backend and perform related database changes in a transaction. It must record the case group, report count used, target authority, reason, timestamp, and notification status. Reprocessing the same report must not create duplicate escalation events.

## Review and fairness safeguards

- Reviewers must be able to confirm a match, reject it, or request further review.
- The reviewer must record a reason for a confirmed or rejected match.
- The review interface should display only the minimum information needed and must not reveal reporter identity by default.
- Suspect details are unverified allegations and must not be presented as established facts.
- If a match is rejected, it must not contribute to the case group's count. If an earlier decision is corrected, the system must retain an audit trail and recalculate future escalation eligibility safely.
- A case must never wait for a second or third report when urgent assistance is needed. Use the institution-configured urgent-response path.
- A reviewer with a conflict of interest must be able to refer the review to another authorized person according to institutional policy.

## Implementation note

For the prototype, create a `case_group` only through an authorized review workflow and store confirmed membership explicitly (for example, with a `case_group_members` table linking a group to each complaint). Enforce uniqueness so one complaint cannot be counted multiple times in the same group. Keep `case_links` as the record of proposed and reviewed pairwise relationships. Use transactions and appropriate locking or constraints to prevent concurrent submissions from generating inconsistent escalation levels.

Before real deployment, the college must approve the matching criteria, who may review matches, the definition of a distinct report, urgent handling, escalation recipients, and retention rules.


**End of system design specification.**
