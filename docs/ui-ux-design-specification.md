# Campus Safety & Harassment Reporting System
## Comprehensive UI/UX Design Specification

**Document Version:** 1.0  
**Status:** Approved Specification  
**Design Foundations:** Dark Modern Elevation (`#121212` Workspace / `#1E1E1E` Panels / `#38B6FF` Primary Accent / `#FF5A5F` Urgent Accent)  
**Target Compliance:** WCAG 2.1 AA / AAA Accessibility Standards  

---

## 1. Executive Design Philosophy & Visual Language

### 1.1 Guiding Principles
1. **Psychological Safety & Calmness:** Reporting trauma, harassment, or ragging is stressful. The interface avoids frantic visual noise, aggressive full-screen sirens, or intimidating bureaucratic jargon.
2. **Immediate Cognitive Clarity:** Critical paths (e.g., *Report Now*, *Emergency Contacts*, *Track Status*) are immediately identifiable with distinct visual hierarchy.
3. **Data Protection through Interface Cues:** Clear, visible distinctions between **Anonymous** and **Confidential** modes reassure the student before they type a single word.
4. **Accountable & Unambiguous Authority Tools:** Authority views (HOD, Dean, Higher Authority) prioritize objective facts, highlight urgent safety flags, and present human-reviewable match comparisons side-by-side.

### 1.2 Color Architecture & Token System
The design system operates on an elevated dark surface hierarchy to reduce eye strain and provide contrast for status indicators.

| Token Name | Hex Code | Purpose & Application | Accessibility Contrast |
| :--- | :--- | :--- | :--- |
| `--color-bg-workspace` | `#121212` | Main viewport canvas, global background | Deep background |
| `--color-bg-panel` | `#1E1E1E` | Primary cards, panels, navigation bars, modal bodies | Surface layer 1 |
| `--color-bg-surface-elevated`| `#282828` | Hover states, table headers, dropdown menus, inputs | Surface layer 2 |
| `--color-bg-input` | `#181818` | Form field background with 1px border | Clean input depth |
| `--color-primary-accent` | `#38B6FF` | Interactive buttons, active tabs, focus rings, links | 8.4:1 contrast on `#121212` |
| `--color-primary-hover` | `#60C5FF` | Hover state for primary interactive elements | Increased luminosity |
| `--color-urgent-accent` | `#FF5A5F` | Urgent report flags, emergency banner, critical badges | 5.8:1 contrast on `#121212` |
| `--color-urgent-subtle` | `rgba(255, 90, 95, 0.15)` | Background fill for urgent rows and highlight cards | Subtle alert layer |
| `--color-text-primary` | `#F5F5F7` | Headings, primary labels, core data values | 15.6:1 contrast ratio |
| `--color-text-secondary` | `#A0A0A5` | Helper text, secondary descriptions, table headers | 6.8:1 (exceeds AA) |
| `--color-text-muted` | `#6E6E73` | Disabled states, timestamps, placeholder text | 4.6:1 minimum |
| `--color-border-subtle` | `#2D2D2D` | Panel borders, horizontal rules, card outlines | 1px clean separation |
| `--color-border-focused` | `#38B6FF` | 2px solid active input ring with glow | Maximum focus clarity |
| `--color-status-submitted` | `#38B6FF` | Badge for newly received report | Blue pill |
| `--color-status-review` | `#F59E0B` | Badge for reports actively under review | Amber pill |
| `--color-status-escalated` | `#A855F7` | Badge for cases escalated to Dean/Higher Authority | Purple pill |
| `--color-status-resolved` | `#10B981` | Badge for successfully closed/resolved cases | Emerald pill |

### 1.3 Typography Hierarchy
- **Primary Typeface:** `Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`, sans-serif.
- **Monospace Typeface:** `JetBrains Mono`, `Fira Code`, `ui-monospace`, monospace (for Report References, Tracking Secrets, and Audit IDs).
- **Scale:**
  - `Display / Hero Title`: 32px / 40px, Semi-Bold (700)
  - `H1 (Section Header)`: 24px / 32px, Semi-Bold (600)
  - `H2 (Card Title / Step Header)`: 18px / 26px, Medium (500)
  - `H3 / Subheading`: 15px / 22px, Medium (500)
  - `Body Regular`: 14px / 20px, Regular (400)
  - `Body Small / Caption`: 12px / 16px, Regular (400)
  - `Code / Token`: 13px / 18px, Monospace (500)

---

## 2. Accessibility & Usability (a11y) Specifications

### 2.1 WCAG 2.1 Compliance Targets
1. **Perceivable:**
   - Text elements maintain at least 4.5:1 contrast for normal text and 7:1 for headers.
   - Status indicators pair color with text and icons (e.g., an urgent badge includes both `#FF5A5F` and an exclamation mark icon `[!] URGENT`).
2. **Operable:**
   - 100% Keyboard Navigable: Full `Tab` order without keyboard traps.
   - Explicit Focus Rings: Custom 2px outline in `#38B6FF` with `outline-offset: 2px` across all buttons, inputs, links, and select elements.
   - Escape Key dismissal for modals, toasts, and drawers.
3. **Understandable:**
   - Every input has an explicitly linked `<label for="...">`.
   - Error messages are announced using `aria-live="polite"` and linked to invalid fields via `aria-describedby="field-error"`.
4. **Robust & Screen-Reader Optimized:**
   - Appropriate ARIA roles (`role="alert"`, `role="dialog"`, `aria-expanded`, `aria-controls`).
   - Screen-reader text for icon-only buttons via `.sr-only` class.

### 2.2 Reduced Motion Mode
Respect user OS preference via CSS:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 3. Global Layout & Components

### 3.1 Pinned Emergency Safeguarding Banner
- **Location:** Pinned at top of public pages (`index.html`, `report.html`, `track.html`).
- **Visual Style:** Surface `#1E1E1E` with left accent border 4px in `#FF5A5F` and subtle red glow.
- **Copy:** 
  > 🚨 **Immediate Danger Alert:** If you or someone else is in immediate physical danger, call the 24/7 Campus Emergency Line: **+91 00000 00000** or visit **Campus Security Gate 1** immediately. This web portal is an administrative reporting channel and is not a real-time dispatch service.

### 3.2 Global Header & Navigation
- **Background:** `#1E1E1E` with bottom border 1px `#2D2D2D`.
- **Left:** System shield logo + title `"Campus Safety & Harassment Reporting System"`.
- **Right:** Navigation links:
  - `Home` (`index.html`)
  - `Submit Report` (Highlighted Button in `#38B6FF` with `#121212` text)
  - `Track Report` (`track.html`)
  - `Staff Portal` (`login.html` / `dashboard.html`)

### 3.3 Status Badges Specification
All status badges feature rounded pill geometry (`padding: 4px 10px; border-radius: 9999px; font-size: 12px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;`).
- **Urgent Case:** Background `rgba(255, 90, 95, 0.2)`, Text `#FF5A5F`, Border `1px solid rgba(255, 90, 95, 0.4)`.
- **Submitted:** Background `rgba(56, 182, 255, 0.15)`, Text `#38B6FF`, Border `1px solid rgba(56, 182, 255, 0.3)`.
- **Under Review:** Background `rgba(245, 158, 11, 0.15)`, Text `#F59E0B`, Border `1px solid rgba(245, 158, 11, 0.3)`.
- **Pending Match:** Background `rgba(236, 72, 153, 0.15)`, Text `#F472B6`, Border `1px solid rgba(236, 72, 153, 0.3)`.
- **Escalated (Level 1/2/3):** Background `rgba(168, 85, 247, 0.15)`, Text `#C084FC`, Border `1px solid rgba(168, 85, 247, 0.3)`.
- **Resolved:** Background `rgba(16, 185, 129, 0.15)`, Text `#34D399`, Border `1px solid rgba(16, 185, 129, 0.3)`.

---

## 4. Screen-by-Screen UI/UX Specifications

### 4.1 Screen 1: Public Landing Page (`index.html`)
- **Hero Section:**
  - Headline: *"Speak Up in Complete Safety."*
  - Subheadline: *"A secure, confidential, and accountable platform for students to report ragging, harassment, and campus safety concerns."*
  - Primary Action CTAs:
    - `[Submit a Report]` (Primary Accent `#38B6FF`, large button with shield icon)
    - `[Track Existing Report]` (Outline button with search icon)
- **Reporting Mode Clarity Cards:**
  - Two parallel comparative cards on `#1E1E1E` panels:
    - **Card A: Anonymous Reporting**
      - Icon: Eye-off / Ghost shield
      - Highlights: No name or ID requested; zero login needed; generates a one-time secret tracking key; identity is never stored.
    - **Card B: Confidential Reporting**
      - Icon: Lock / Verified badge
      - Highlights: Contact details securely stored in an isolated, encrypted vault; accessible only by authorized clearance; allows authorities to reach out with updates.
- **Incident Category Overview:**
  - Interactive tab/card split between **Offline Ragging** (stalking, hostel intimidation, physical threats) and **Online / Cyber Ragging** (impersonation, malicious messaging, harassment).
- **Process Walkthrough (3 Steps):**
  - `Step 1: Submit Details` $\rightarrow$ `Step 2: Human Review & Matching` $\rightarrow$ `Step 3: Accountable Escalation (HOD → Dean → Higher Authority)`.

---

### 4.2 Screen 2: Incident Reporting Form (`report.html`)

#### Form Architecture & Visual Flow
The reporting form is contained in an elevated `#1E1E1E` card with `#2D2D2D` border, divided into 5 logical sections:

#### Section 1: Reporting Mode Selector
- Interactive two-way toggle card selector (Radio-based accessible component):
  - `[Option 1: Anonymous Report]`
  - `[Option 2: Confidential Report]`
- Dynamic helper banner below selector:
  - If Anonymous selected: *"No personal details will be collected or stored. You will receive a private Tracking Secret after submission."*
  - If Confidential selected: Form smoothly reveals optional contact fields (Full Name, College Email, Phone Number, Department) with clear privacy notice: *"Stored in separated identity storage; never displayed in standard staff case queues."*

#### Section 2: Incident Classification & Category
- **Incident Type:** Dual selector cards:
  - `[In-Person / Offline Ragging]` vs `[Digital / Cyber Harassment]`
- **Category Dropdown:** Accessible styled `<select>` populated dynamically:
  - *Offline:* Following/Stalking, Physical/Verbal Harassment, Hostel Intimidation, Coercion, Other.
  - *Online:* Fake Profiles/Impersonation, Abusive Messages, Unconsented Photo/Video Sharing, Online Threats, Other.

#### Section 3: Incident Details & Urgent Flag
- **Incident Date & Approximate Time:** Date picker and time input styled on `#181818` input background.
- **Location / Platform:** Text input (e.g., *"Library 2nd Floor"* or *"Instagram Direct Messages"*).
- **Incident Description:** Multiline textarea (minimum 5 rows) with character counter and calm guidance text: *"Describe what occurred in your own words. Please avoid sharing sensitive third-party details unless relevant."*
- **Urgent Safety Flag Toggle:**
  - Distinct card with left border `#FF5A5F`:
  - Checkbox: `[x] This incident involves ongoing or immediate safety risks.`
  - Helper note: *"Flagging as urgent prioritizes immediate safeguarding evaluation without waiting for repeated report matches."*

#### Section 4: Voluntary Suspect Details (Accordion / Collapsible)
- Header: *"Suspect Details (Optional — Leave blank if unknown)"*
- Explanatory note: *"These details are recorded as unverified allegations for investigation purposes only."*
- Fields: Suspect Name / Nickname, Department / Year, Phone / Social Media handle, Physical/identifying description.

#### Section 5: Private Evidence Upload
- **Dropzone Component:**
  - Dashed border `2px dashed #38B6FF` with `#181818` background.
  - Text: *"Drag & drop screenshots, photos, or documents (PNG, JPG, PDF up to 5MB)"*.
  - Upload security reassurance: *"Files are stored in private, unguessable storage. Never exposed via public web links."*
  - File preview pill with sanitized filename, file size, and remove button.

#### Section 6: Submission & Success Modal
- Submit Button: `[Submit Secure Report]` (Large `#38B6FF` button with lock icon).
- **Post-Submission Credential Modal:**
  - Dark modal with `#1E1E1E` surface and `#38B6FF` border.
  - Success message: *"Your report has been securely registered."*
  - **Public Reference Box:** Monospace text (e.g. `REF-2026-9842`) with `[Copy]` button.
  - **Private Tracking Secret Box:** Highlighted gold/cyan box (e.g. `TRK-8f2a9c41...`) with warning:
    > ⚠️ **IMPORTANT:** Save this tracking secret now. It will never be shown again. You need both the Reference and Tracking Secret to check case progress.
  - One-click `[Copy All Credentials]` and `[Download Credentials as Text]` actions.

---

### 4.3 Screen 3: Secure Report Tracking (`track.html`)

#### Layout & Workflow
- **Search Panel (`#1E1E1E`):**
  - Input 1: `Public Report Reference` (e.g., `REF-2026-9842`)
  - Input 2: `Tracking Secret` (Password-masked with show/hide eye toggle)
  - CTA: `[Check Case Status]` (Primary Accent `#38B6FF`)
- **Status Results Card:**
  - Header: Public Reference, Incident Category, Submission Date, Current Status Badge.
  - **Milestone Progress Stepper:**
    1. *Submitted* (Completed - Date stamped)
    2. *Under Initial Review* (Active / Completed)
    3. *Escalation / Action Taken* (E.g. Routed to Department Authority)
    4. *Resolution / Closure*
  - **Safe Public Guidance Box:**
    - Displays approved public updates (e.g., *"Case acknowledged by Department Committee; inquiries underway"*).
    - **Strict Security Guard:** Never renders internal investigator notes, suspect details, evidence links, or reporter identities.

---

### 4.4 Screen 4: Authority Portal Login (`login.html`)
- **Card Centerpiece (`#1E1E1E`):**
  - University Shield & Header: *"Campus Safety Authority Access"*.
  - Subheader: *"Authorized personnel only: HOD, Dean, Higher Authority & Admin"*.
  - Email / Username input.
  - Password input with secure password manager support.
  - Rate-limiting feedback area (displays cool-down timer on failed attempts).
  - Security Notice: *"All logins and case views are logged to an immutable audit trail."*

---

### 4.5 Screen 5: Authority Dashboard (`dashboard.html`)

#### Header & Role Context Bar
- Displays logged-in official: e.g., *"Dr. S. Sharma — Head of Department (Computer Science)"*.
- Active Level Badge: `[Level 1: HOD Scope]`.

#### Metrics Overview (4 KPI Cards on `#1E1E1E` Panels)
1. **Assigned Active Cases:** Total open complaints within scope.
2. **Urgent Safety Alerts:** Count highlighted in `#FF5A5F` with pulsing dot.
3. **Pending Match Reviews:** Candidate related reports requiring human review.
4. **Escalated Cases:** Cases transferred to Dean / Higher Authority.

#### Filter & Search Bar
- Quick search by Reference ID, Category, or Date range.
- Status filters: `All`, `Urgent Only`, `Under Review`, `Pending Match`, `Escalated`.

#### Interactive Case Queue Table
- **Columns:**
  1. `Ref ID` (Monospace, e.g., `REF-2026-1102`)
  2. `Type & Category` (e.g., *Offline — Stalking*)
  3. `Date Reported` (Formatted local date)
  4. `Urgent Flag` (If true, renders bold `🚨 URGENT` pill in `#FF5A5F`)
  5. `Status` (Color-coded badge)
  6. `Related Reports` (e.g., `[Group #4 - 2 Reports]`)
  7. `Actions` (`[View Case Details]` button in `#38B6FF` outline)

---

### 4.6 Screen 6: Case Detail View (`case-detail.html`)

#### Dual-Column Layout
- **Left Column (Primary Incident Data — 65% width):**
  - **Case Summary Card:** Reference, Category, Incident Timestamp, Location.
  - **Incident Narrative:** Full statement submitted by the reporter.
  - **Voluntary Suspect Allegations Card:** Explicitly marked *"Allegation details provided by reporter — Unverified"* (Name, Department, Details).
  - **Private Evidence Vault:**
    - List of uploaded files with mime-type icons.
    - `[Download Protected File]` button (streams through authenticated endpoint `/api/evidence/{id}`; logs access to audit trail).
  - **Protected Identity Banner:**
    - If Anonymous: Green-shield badge *"Anonymous Submission — No identity data exists."*
    - If Confidential: Shielded card *"Reporter Identity Protected under Confidentiality Policy"*.
    - Button: `[Request Exceptional Identity Access]`: Opens modal requiring documented legal/safeguarding justification; triggers an immediate high-priority audit record.

- **Right Column (Workflow & Action Controls — 35% width):**
  - **Case Status Transition Card:**
    - Dropdown: `Under Review`, `Awaiting Information`, `Resolved`, `Closed`.
    - Mandatory reason textarea.
    - `[Update Status]` button.
  - **Escalation Management Card:**
    - Current Level indicator: `Level 1 (HOD)`.
    - Button: `[Escalate to Dean (Level 2)]` with justification input.
  - **Audit & Status History Timeline:**
    - Chronological list of past status changes, review decisions, and escalations with actor and timestamp.

---

### 4.7 Screen 7: Related-Case Match Review (`review.html`)

#### Purpose & Safeguards
Complies with **Section 23 Final Repeat-Report Counting Policy**: flags potential similarities for human review without assuming guilt.

#### Visual Interface
- **Split Comparison Matrix:**
  - **Left Panel:** Candidate Report A (`REF-2026-1011`)
  - **Right Panel:** Candidate Report B (`REF-2026-1089`)
- **Comparison Attributes Row:**
  - Location Match: Both cite *"Mechanical Lab Corridor"*.
  - Time Window: 48 hours apart.
  - Suspect Descriptor Match: Both cite similar nicknames/descriptions.
  - Category Match: Both flagged as *Offline / Verbal Harassment*.
- **Reviewer Action Deck:**
  - Option 1: `[Confirm Related Pattern]` (Green `#10B981` border) — Assigns both reports to an explicit `case_group` and recalculates escalation count.
  - Option 2: `[Reject Match (Independent Incidents)]` (Muted red outline) — Marks link as rejected; prevents count increase.
  - Option 3: `[Defer / Needs More Information]`.
- **Mandatory Review Rationale Box:** Textarea required before confirming or rejecting.
- Confirmation dialog before submitting decision to prevent accidental clicks.

---

### 4.8 Screen 8: Administrator & Audit Console (`admin.html`)
- **Account Management Table:** List authorized staff, roles (HOD, Dean, Higher Authority, Admin), assigned departments, and active toggles.
- **System Configuration:** View placeholder institution settings (Helpline numbers, contact offices, allowed upload types).
- **Immutable Audit Log Viewer:**
  - Searchable by Actor ID, Action (`CASE_VIEW`, `IDENTITY_ACCESSED`, `STATUS_CHANGE`, `MATCH_CONFIRMED`), and Date.
  - Sensitive parameters automatically sanitized.

---

## 5. CSS Design Token Architecture

This token architecture will be placed directly in `frontend/css/variables.css`:

```css
:root {
  /* Surface & Background Palette */
  --bg-workspace: #121212;
  --bg-panel: #1E1E1E;
  --bg-surface-elevated: #282828;
  --bg-input: #181818;
  --bg-input-focus: #222222;

  /* Primary Interactive Accent */
  --color-primary: #38B6FF;
  --color-primary-hover: #60C5FF;
  --color-primary-subtle: rgba(56, 182, 255, 0.12);
  --color-primary-border: rgba(56, 182, 255, 0.35);

  /* Urgent & Alert Accent */
  --color-urgent: #FF5A5F;
  --color-urgent-hover: #FF7B7F;
  --color-urgent-subtle: rgba(255, 90, 95, 0.15);
  --color-urgent-border: rgba(255, 90, 95, 0.4);

  /* Status Colors */
  --color-success: #10B981;
  --color-success-subtle: rgba(16, 185, 129, 0.15);
  --color-warning: #F59E0B;
  --color-warning-subtle: rgba(245, 158, 11, 0.15);
  --color-escalated: #A855F7;
  --color-escalated-subtle: rgba(168, 85, 247, 0.15);

  /* Typography Colors */
  --text-primary: #F5F5F7;
  --text-secondary: #A0A0A5;
  --text-muted: #6E6E73;
  --text-on-accent: #0A192F;

  /* Borders & Dividers */
  --border-subtle: #2D2D2D;
  --border-hover: #3E3E3E;
  --border-active: #38B6FF;

  /* Geometry & Shadows */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-full: 9999px;
  --shadow-panel: 0 4px 20px rgba(0, 0, 0, 0.45);
  --shadow-modal: 0 10px 40px rgba(0, 0, 0, 0.7);

  /* Transitions */
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## 6. Implementation Readiness
This UI/UX specification adheres strictly to the primary project design in `campus-safety-system-design.md`, implements the full `#121212` / `#1E1E1E` / `#38B6FF` / `#FF5A5F` palette, and ensures full consistency with Section 23 repeat-report review workflows and WCAG 2.1 accessibility requirements.
