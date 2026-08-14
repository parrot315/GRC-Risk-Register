# GRC Risk Register — Risk Register Development Based on ISO/IEC 27001 for a Simulated Mid-Sized Organization

**An academic Governance, Risk & Compliance (GRC) web application built with Python/Flask.**

> ⚠️ **Disclaimer:** This is an academic / simulated project built for a university Cyber Security course.
> It is **not** an officially certified ISO/IEC 27001 compliance tool, and "ParrotSec Technologies" is a
> fictional company created solely for demonstration purposes. No real organizational data is used.

---

## 1. Project Overview

This application allows a simulated mid-sized organization ("ParrotSec Technologies", ~250 employees, IT /
Software Services) to **identify, assess, treat, and monitor** information-security risks using a
structured methodology aligned with ISO/IEC 27001:2022 Annex A controls.

It is a fully functional, locally-run web application — not just a static document — demonstrating
practical GRC tooling concepts for a Cyber Security degree project.

## 2. Objectives

- Demonstrate a complete risk management lifecycle: **Asset → Threat → Vulnerability → Existing
  Controls → Likelihood → Impact → Inherent Risk → Treatment → Proposed Controls → Residual Risk →
  ISO 27001 Mapping**
- Provide a working CRUD risk register with automatic risk scoring
- Map risks to real ISO/IEC 27001:2022 Annex A controls
- Visualize risk exposure through a dashboard, 5×5 risk matrix, and exportable reports

## 3. Technologies Used

| Layer        | Technology              |
|--------------|--------------------------|
| Backend      | Python 3, Flask          |
| Database     | SQLite (built-in, file-based) |
| Templating   | Jinja2                   |
| Frontend     | HTML5, CSS3, JavaScript, Bootstrap 5, Bootstrap Icons |
| Reporting    | openpyxl (Excel export), printable HTML → browser PDF |

No Docker, cloud services, paid APIs, or external accounts are required. The app runs entirely on
your local machine.

## 4. Key Features

- **Dashboard** — total/critical/high/medium/low risk counts, open/treated/accepted counts, risk
  distribution bars, mini risk matrix, top risks, and recently added risks.
- **Risk Register (CRUD)** — add, view, edit, delete, search, filter (by level/status/treatment), and
  sort risks.
- **Automatic Risk Calculation** — Inherent and Residual risk scores/levels are calculated
  automatically server-side (and previewed live in the browser); the score field is never manually
  editable.
- **Risk Treatment** — Mitigate / Avoid / Transfer / Accept, with treatment plan and proposed controls.
- **ISO/IEC 27001:2022 Mapping** — 32 real Annex A controls across the Organizational, People,
  Physical, and Technological themes; each risk can map to one or more controls.
- **5×5 Risk Matrix** — visual matrix with drill-down into the risks in each cell.
- **Reports** — Excel export (Risk Register, Risk Summary, ISO 27001 Mapping) via openpyxl, plus
  printable HTML reports you can save as PDF from your browser.
- **Sample Data** — 17 realistic seeded risks across 12 assets on first run.
- **Validation** — server-side validation of likelihood/impact (1–5), required fields, and safe,
  parameterized SQL queries throughout.

## 5. Risk Methodology

### 5.1 Likelihood (1–5)
| Value | Label |
|-------|-------|
| 1 | Rare |
| 2 | Unlikely |
| 3 | Possible |
| 4 | Likely |
| 5 | Almost Certain |

### 5.2 Impact (1–5)
| Value | Label |
|-------|-------|
| 1 | Insignificant |
| 2 | Minor |
| 3 | Moderate |
| 4 | Major |
| 5 | Severe |

### 5.3 Risk Score & Level

```
Risk Score = Likelihood × Impact
```

| Score Range | Level |
|-------------|-------|
| 1–4   | Low |
| 5–9   | Medium |
| 10–16 | High |
| 17–25 | Critical |

The application calculates this automatically — for both **inherent risk** (before treatment) and
**residual risk** (after treatment, using residual likelihood/impact) — whenever likelihood or impact
values change. Users cannot manually override the calculated score.

**Example (R-001, Customer Database):**

```
Inherent:  Likelihood 4 × Impact 5 = 20  → Critical
Residual:  Likelihood 2 × Impact 5 = 10  → High   (after MFA + RBAC)
```

## 6. ISO/IEC 27001:2022 Mapping

The application includes 32 genuine ISO/IEC 27001:2022 Annex A controls (correct control numbers and
titles — no invented codes), covering areas such as access control (A.5.15), identity management
(A.5.16), authentication information (A.5.17), security awareness (A.6.3), malware protection (A.8.7),
vulnerability management (A.8.8), backup (A.8.13), logging (A.8.15), monitoring (A.8.16), and more.
Each risk in the register can be mapped to one or more relevant controls, and the **ISO 27001** page
lets you browse controls by theme and see which risks reference each one.

## 7. Project Structure

```
GRC_Risk_Register/
│
├── app.py                     # Main Flask application (routes, logic)
├── database_setup.py          # DB schema creation + sample data seeding
├── requirements.txt
├── README.md
│
├── database/
│   └── database.db            # SQLite database (auto-created on first run)
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── risks.html
│   ├── add_risk.html
│   ├── edit_risk.html
│   ├── risk_details.html
│   ├── matrix.html
│   ├── controls.html
│   ├── control_risks.html
│   ├── reports.html
│   ├── print_register.html
│   ├── print_iso_mapping.html
│   ├── about.html
│   ├── 404.html
│   └── 500.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── exports/                   # Generated Excel report files land here
```

## 8. Installation & Setup (Windows)

**Prerequisite:** Python 3.9+ installed and available on PATH (`python --version`).

1. Extract/copy the `GRC_Risk_Register` folder to your machine.
2. Open Command Prompt or PowerShell in that folder.
3. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 9. How to Run

```bash
python app.py
```

The database is created and seeded automatically on first run. Then open your browser to:

```
http://127.0.0.1:5000
```

To stop the server, press `CTRL+C` in the terminal.

## 10. How to Use

1. **Dashboard** — get an at-a-glance view of total/critical/high/medium/low risks and the risk matrix.
2. **Risk Register** — browse all risks; use the search box and Level/Status/Treatment filters; click
   column headers to sort.
3. **Add Risk** — walk through the guided form (Asset → Threat/Vulnerability → Likelihood/Impact →
   Treatment → Residual Risk → ISO Control Mapping). Scores update live as you choose likelihood/impact.
4. **Risk Details** — click any Risk ID to see the full inherent vs. residual comparison and mapped
   ISO controls.
5. **Edit / Delete** — from the register table or the details page.
6. **Risk Matrix** — view the full 5×5 matrix; expand a cell to see the risks that fall into it.
7. **ISO 27001** — browse Annex A controls by theme; click a control's risk count to see which risks
   reference it.
8. **Reports** — export the Risk Register, Risk Summary, or ISO 27001 Mapping to Excel, or open a
   printable HTML report and use your browser's Print → Save as PDF.

## 11. Testing

The following was manually and programmatically verified during development (via Flask's test
client, exercising every route and the full CRUD/validation/export pipeline):

1. **Adding a risk** — form submits, inherent score/level calculated automatically, saved to DB.
2. **Editing a risk** — updates persist, recalculates inherent and residual score/level.
3. **Deleting a risk** — removes the risk and its ISO control mappings; redirects to the register.
4. **Searching** — free-text search across risk code, threat, vulnerability, description, asset, owner.
5. **Filtering** — by risk level, status, and treatment type (individually and combined).
6. **Automatic risk calculation** — verified `Likelihood × Impact` always matches the stored score and
   level for both new and edited risks; manual score entry is not possible (no input field exists).
7. **Residual risk calculation** — verified independently of inherent risk using the same 1–5 scale.
8. **ISO control mapping** — verified checkboxes persist correctly on add/edit, and that the ISO 27001
   page and control drill-down page correctly reflect mapped risks.
9. **Dashboard statistics** — KPI counts cross-checked against direct SQL aggregate queries.
10. **Risk matrix** — verified cell risk counts match the underlying likelihood/impact pairs.
11. **Excel export** — verified all three export types (Register, Summary, ISO Mapping) produce valid
    `.xlsx` files openable with openpyxl, with correct headers and row counts.
12. **Database persistence** — verified data survives across app restarts (SQLite file-based storage);
    the database is only seeded once, on first creation.

To re-run these checks yourself, you can use Flask's test client:
```bash
python -c "from app import app; c = app.test_client(); print(c.get('/').status_code)"
```

## 12. Security Notes (Academic Context)

- All SQL queries use parameterized statements (`?` placeholders) — no string-concatenated SQL.
- Server-side validation enforces the 1–5 range on likelihood/impact/residual fields and required
  fields, independent of any client-side JavaScript.
- No hard-coded secrets: the Flask session secret key is generated at runtime
  (`os.urandom(24)`), or can be supplied via the `GRC_SECRET_KEY` environment variable.
- The application is intended for local, single-user academic use only and does not implement
  authentication/authorization, HTTPS, or rate limiting — see Limitations below.

## 13. Project Limitations

- No user authentication/authorization (single-user local demo).
- No real-time collaboration or multi-user locking on the SQLite database.
- ISO/IEC 27001:2022 control set included is a representative subset (32 of 93 Annex A controls),
  not the full Annex A.
- Risk scoring uses a simple multiplicative 5×5 model; it does not model qualitative risk appetite
  statements or weighted scoring.
- Not intended, tested, or certified for production/enterprise GRC use.

## 14. Future Improvements

- Add authentication and role-based access (e.g., risk owner vs. reviewer vs. admin).
- Support multiple simulated organizations/business units in one instance.
- Add trend reporting (risk exposure over time) using historical snapshots.
- Expand to the full ISO/IEC 27001:2022 Annex A control set (93 controls).
- Add PDF export natively (e.g., via a headless rendering library) instead of browser print-to-PDF.
- Add audit logging of who changed what and when.

---

*Academic project — ParrotSec Technologies and all risk data are fictional and used for demonstration only.*
