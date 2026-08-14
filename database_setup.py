"""
database_setup.py
------------------
Handles SQLite database initialization, schema creation, and seeding of
realistic sample data for the GRC Risk Register academic project.

This module is imported by app.py. The database is automatically created
and populated the first time the application is run.
"""

import sqlite3
import os

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
DB_PATH = os.path.join(DB_DIR, "database.db")


def get_connection():
    """Return a SQLite connection with foreign keys enabled and row access by name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def calculate_level(score):
    """Map a numeric risk score (1-25) to a risk level label."""
    if score is None:
        return None
    if score <= 4:
        return "Low"
    elif score <= 9:
        return "Medium"
    elif score <= 16:
        return "High"
    else:
        return "Critical"


def init_db(force_reseed=False):
    """
    Create database tables if they do not exist, and populate them with
    sample data on first run. If force_reseed is True, existing data in
    the risks table is wiped and reseeded (used only for demo resets).
    """
    os.makedirs(DB_DIR, exist_ok=True)
    is_new_db = not os.path.exists(DB_PATH)

    conn = get_connection()
    cur = conn.cursor()

    # ---------------------------------------------------------------
    # ORGANIZATION TABLE (single fictional organization profile)
    # ---------------------------------------------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organization (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT NOT NULL,
            industry TEXT NOT NULL,
            size TEXT NOT NULL,
            employees INTEGER NOT NULL,
            description TEXT
        )
    """)

    # ---------------------------------------------------------------
    # ASSETS TABLE
    # ---------------------------------------------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT,
            owner TEXT,
            description TEXT
        )
    """)

    # ---------------------------------------------------------------
    # ISO 27001:2022 ANNEX A CONTROLS TABLE
    # ---------------------------------------------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS iso_controls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            control_id TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            theme TEXT NOT NULL,
            description TEXT
        )
    """)

    # ---------------------------------------------------------------
    # RISKS TABLE (core risk register)
    # ---------------------------------------------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS risks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            risk_code TEXT NOT NULL UNIQUE,
            asset_id INTEGER,
            asset_owner TEXT,
            threat TEXT NOT NULL,
            vulnerability TEXT NOT NULL,
            risk_description TEXT,
            existing_controls TEXT,

            likelihood INTEGER NOT NULL CHECK (likelihood BETWEEN 1 AND 5),
            impact INTEGER NOT NULL CHECK (impact BETWEEN 1 AND 5),
            inherent_score INTEGER NOT NULL,
            inherent_level TEXT NOT NULL,

            risk_treatment TEXT NOT NULL CHECK (risk_treatment IN ('Mitigate','Avoid','Transfer','Accept')),
            treatment_description TEXT,
            proposed_controls TEXT,
            risk_owner TEXT,
            target_date TEXT,
            status TEXT NOT NULL DEFAULT 'Open' CHECK (status IN ('Open','In Progress','Treated','Accepted','Closed')),

            residual_likelihood INTEGER CHECK (residual_likelihood BETWEEN 1 AND 5),
            residual_impact INTEGER CHECK (residual_impact BETWEEN 1 AND 5),
            residual_score INTEGER,
            residual_level TEXT,

            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (asset_id) REFERENCES assets (id)
        )
    """)

    # ---------------------------------------------------------------
    # RISK <-> ISO CONTROL MAPPING TABLE (many-to-many)
    # ---------------------------------------------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS risk_controls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            risk_id INTEGER NOT NULL,
            control_id INTEGER NOT NULL,
            FOREIGN KEY (risk_id) REFERENCES risks (id) ON DELETE CASCADE,
            FOREIGN KEY (control_id) REFERENCES iso_controls (id) ON DELETE CASCADE,
            UNIQUE(risk_id, control_id)
        )
    """)

    conn.commit()

    if is_new_db or force_reseed:
        if force_reseed:
            cur.execute("DELETE FROM risk_controls")
            cur.execute("DELETE FROM risks")
            cur.execute("DELETE FROM assets")
            cur.execute("DELETE FROM iso_controls")
            cur.execute("DELETE FROM organization")
            conn.commit()
        seed_data(conn)

    conn.close()


def seed_data(conn):
    """Populate the database with the fictional organization, assets,
    ISO 27001:2022 controls, and sample risk register entries."""
    cur = conn.cursor()

    # --- Fictional organization -------------------------------------------------
    cur.execute("""
        INSERT OR IGNORE INTO organization (id, name, industry, size, employees, description)
        VALUES (1, ?, ?, ?, ?, ?)
    """, (
        "ParrotSec Technologies",
        "IT / Software Services",
        "Mid-Sized Organization",
        250,
        "ParrotSec Technologies is a fictional, simulated IT / Software Services "
        "company created solely for academic GRC demonstration purposes. "
        "It employs approximately 250 staff."
    ))

    # --- Assets -------------------------------------------------------------
    assets = [
        ("Customer Database", "Data", "Database Administrator", "Stores customer records, contact details, and service history."),
        ("Employee Database", "Data", "HR Manager", "Stores employee personal and payroll information."),
        ("Web Application", "Application", "Application Owner", "Customer-facing SaaS web application."),
        ("Email System", "Communication", "IT Manager", "Corporate email and messaging platform."),
        ("File Server", "Infrastructure", "IT Administrator", "Central file storage for internal departments."),
        ("Employee Laptops", "Endpoint", "IT Administrator", "Laptops issued to staff for daily work."),
        ("Network Firewall", "Network", "Network Administrator", "Perimeter firewall protecting the internal network."),
        ("Backup Server", "Infrastructure", "IT Administrator", "Stores nightly backups of critical systems."),
        ("Cloud Storage", "Cloud", "Cloud Administrator", "Third-party cloud storage used for project files."),
        ("Internal Network", "Network", "Network Administrator", "Internal LAN connecting offices and data center."),
        ("Authentication System", "Identity", "Security Administrator", "Centralized identity and access management system."),
        ("Development Environment", "Application", "Development Lead", "Environment used for building and testing software."),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO assets (name, category, owner, description) VALUES (?, ?, ?, ?)",
        assets
    )
    conn.commit()

    # --- ISO/IEC 27001:2022 Annex A Controls (real control numbers/titles) ---
    controls = [
        ("A.5.1", "Policies for information security", "Organizational", "Management direction and support for information security."),
        ("A.5.9", "Inventory of information and other associated assets", "Organizational", "Assets must be identified and an inventory maintained."),
        ("A.5.10", "Acceptable use of information and other associated assets", "Organizational", "Rules for acceptable use of assets are identified and implemented."),
        ("A.5.15", "Access control", "Organizational", "Rules to control physical and logical access based on business requirements."),
        ("A.5.16", "Identity management", "Organizational", "The full lifecycle of identities is managed."),
        ("A.5.17", "Authentication information", "Organizational", "Allocation and management of authentication information is controlled."),
        ("A.5.18", "Access rights", "Organizational", "Access rights are provisioned, reviewed, and revoked in line with policy."),
        ("A.5.19", "Information security in supplier relationships", "Organizational", "Processes to manage information security risks from supplier use."),
        ("A.5.23", "Information security for use of cloud services", "Organizational", "Processes for acquisition, use, and management of cloud services."),
        ("A.5.24", "Information security incident management planning and preparation", "Organizational", "Plan and prepare for managing information security incidents."),
        ("A.5.29", "Information security during disruption", "Organizational", "Maintain information security during disruptive events."),
        ("A.5.30", "ICT readiness for business continuity", "Organizational", "ICT readiness is planned and maintained to ensure availability."),
        ("A.5.31", "Legal, statutory, regulatory and contractual requirements", "Organizational", "Legal and regulatory requirements are identified and met."),
        ("A.6.3", "Information security awareness, education and training", "People", "Personnel receive appropriate awareness and training."),
        ("A.6.7", "Remote working", "People", "Security measures are implemented for remote working."),
        ("A.7.4", "Physical security monitoring", "Physical", "Premises are continuously monitored for unauthorized access."),
        ("A.7.10", "Storage media", "Physical", "Storage media is managed through its lifecycle."),
        ("A.8.1", "User endpoint devices", "Technological", "Information stored on, processed by, or accessible via endpoint devices is protected."),
        ("A.8.2", "Privileged access rights", "Technological", "Allocation and use of privileged access rights is restricted and managed."),
        ("A.8.3", "Information access restriction", "Technological", "Access to information is restricted in line with access control policy."),
        ("A.8.5", "Secure authentication", "Technological", "Secure authentication technologies and procedures are implemented."),
        ("A.8.7", "Protection against malware", "Technological", "Protection against malware is implemented and supported by awareness."),
        ("A.8.8", "Management of technical vulnerabilities", "Technological", "Technical vulnerabilities are identified, evaluated, and remediated."),
        ("A.8.9", "Configuration management", "Technological", "Configurations of hardware, software, and networks are managed."),
        ("A.8.12", "Data leakage prevention", "Technological", "Measures applied to systems handling sensitive information to prevent leakage."),
        ("A.8.13", "Information backup", "Technological", "Backup copies of information and software are maintained and tested."),
        ("A.8.15", "Logging", "Technological", "Logs recording activities, exceptions, and events are produced and retained."),
        ("A.8.16", "Monitoring activities", "Technological", "Networks, systems, and applications are monitored for anomalous behavior."),
        ("A.8.20", "Networks security", "Technological", "Networks and network devices are secured, managed, and controlled."),
        ("A.8.23", "Web filtering", "Technological", "Access to external websites is managed to reduce exposure to malicious content."),
        ("A.8.24", "Use of cryptography", "Technological", "Rules for effective use of cryptography, including key management."),
        ("A.8.28", "Secure coding", "Technological", "Secure coding principles are applied to software development."),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO iso_controls (control_id, title, theme, description) VALUES (?, ?, ?, ?)",
        controls
    )
    conn.commit()

    # Helper lookups
    asset_map = {row["name"]: row["id"] for row in cur.execute("SELECT id, name FROM assets")}
    control_map = {row["control_id"]: row["id"] for row in cur.execute("SELECT id, control_id FROM iso_controls")}

    def level(score):
        if score <= 4:
            return "Low"
        elif score <= 9:
            return "Medium"
        elif score <= 16:
            return "High"
        return "Critical"

    # --- Sample risk register (15+ realistic risks) --------------------------
    # Each tuple: (code, asset, owner, threat, vulnerability, description,
    #              existing_controls, likelihood, impact, treatment,
    #              treatment_description, proposed_controls, risk_owner,
    #              target_date, status, res_like, res_impact, notes, [iso controls])
    sample_risks = [
        ("R-001", "Customer Database", "Database Administrator", "Unauthorized Access", "Weak access controls",
         "An attacker could gain unauthorized access to sensitive customer records due to insufficiently restricted database permissions.",
         "Basic username/password authentication", 4, 5, "Mitigate",
         "Implement multi-factor authentication and role-based access control for all database access.",
         "MFA + RBAC", "Database Administrator", "2026-03-15", "In Progress", 2, 5,
         "High-value target due to volume of PII stored.", ["A.5.15", "A.8.2", "A.8.5"]),

        ("R-002", "Employee Laptops", "IT Administrator", "Phishing Attack", "Lack of email filtering and user awareness",
         "Employees may be tricked into clicking malicious links or attachments in phishing emails, leading to credential theft or malware installation.",
         "Basic spam filter", 5, 4, "Mitigate",
         "Deploy advanced email filtering, run quarterly phishing simulations, and mandate security awareness training.",
         "Email security gateway + Security Awareness Training", "IT Manager", "2026-02-28", "Open", 3, 3,
         "Frequent attack vector observed across the industry.", ["A.6.3", "A.8.7", "A.8.23"]),

        ("R-003", "File Server", "IT Administrator", "Ransomware Infection", "Unpatched operating system and no endpoint protection",
         "Ransomware could encrypt files on the file server, disrupting business operations and demanding payment for decryption.",
         "Antivirus software (outdated definitions)", 3, 5, "Mitigate",
         "Implement endpoint detection and response (EDR), enforce patch management, and maintain isolated backups.",
         "EDR solution + Patch Management Process", "IT Administrator", "2026-03-01", "Open", 2, 5,
         "Backups currently stored on same network segment.", ["A.8.7", "A.8.8", "A.8.13"]),

        ("R-004", "Authentication System", "Security Administrator", "Credential Stuffing", "Weak password policy",
         "Attackers may use lists of breached credentials to gain unauthorized access to user accounts due to weak password requirements.",
         "Minimum 6-character password policy", 4, 4, "Mitigate",
         "Enforce strong password policy, implement MFA, and deploy account lockout/rate limiting.",
         "MFA + Strong Password Policy + Rate Limiting", "Security Administrator", "2026-02-20", "In Progress", 2, 4,
         "Related to increasing credential-stuffing attempts noted in login logs.", ["A.5.17", "A.8.5"]),

        ("R-005", "Development Environment", "Development Lead", "SQL Injection", "Insecure coding practices",
         "Improperly sanitized user input in web application forms could allow attackers to execute arbitrary SQL commands.",
         "Manual code review only", 3, 5, "Mitigate",
         "Implement parameterized queries, input validation, and automated static code analysis in the CI/CD pipeline.",
         "Secure Coding Standards + SAST Tooling", "Development Lead", "2026-04-01", "Open", 1, 5,
         "Identified during internal code review of the web application.", ["A.8.28", "A.8.8"]),

        ("R-006", "Network Firewall", "Network Administrator", "Firewall Misconfiguration", "Overly permissive firewall rules",
         "Misconfigured firewall rules could expose internal systems to the internet, allowing unauthorized network access.",
         "Firewall reviewed annually", 3, 4, "Mitigate",
         "Implement quarterly firewall rule reviews and automated configuration auditing.",
         "Configuration Management + Periodic Firewall Audit", "Network Administrator", "2026-03-10", "Open", 2, 4,
         "Legacy rule set has not been fully reviewed in over a year.", ["A.8.9", "A.8.20"]),

        ("R-007", "Backup Server", "IT Administrator", "Backup Failure", "No automated backup verification",
         "Backups may silently fail or become corrupted, resulting in inability to recover data after an incident.",
         "Manual nightly backup script", 3, 4, "Mitigate",
         "Implement automated backup verification, offsite replication, and periodic restore testing.",
         "Automated Backup Monitoring + Offsite Replication", "IT Administrator", "2026-03-20", "Open", 1, 4,
         "No successful restore test performed in the last 6 months.", ["A.8.13", "A.5.29"]),

        ("R-008", "Cloud Storage", "Cloud Administrator", "Cloud Storage Misconfiguration", "Publicly accessible storage bucket",
         "Misconfigured access permissions on cloud storage could expose confidential company files to the public internet.",
         "Default cloud provider settings", 3, 5, "Mitigate",
         "Apply least-privilege access policies, enable bucket-level logging, and use automated misconfiguration scanning.",
         "Cloud Security Posture Management (CSPM)", "Cloud Administrator", "2026-02-25", "Open", 1, 5,
         "Similar misconfigurations are a leading cause of cloud data breaches industry-wide.", ["A.5.23", "A.8.3", "A.8.16"]),

        ("R-009", "Employee Laptops", "IT Administrator", "Device Loss/Theft", "No full-disk encryption enforced",
         "A lost or stolen laptop without encryption could expose sensitive company and customer data stored locally.",
         "Laptop screen-lock password", 3, 4, "Mitigate",
         "Enforce full-disk encryption, remote-wipe capability, and mobile device management (MDM) enrollment.",
         "Full-Disk Encryption + MDM", "IT Administrator", "2026-03-05", "Open", 1, 4,
         "Two laptops reported lost in the past year (no data exposure confirmed).", ["A.8.1", "A.7.10"]),

        ("R-010", "Internal Network", "Network Administrator", "Insider Threat", "Excessive standing privileged access",
         "A malicious or negligent insider with excessive access privileges could misuse or leak sensitive information.",
         "Standard onboarding access provisioning", 2, 5, "Mitigate",
         "Implement least-privilege access, periodic access reviews, and user activity monitoring/logging.",
         "Privileged Access Management (PAM) + Activity Logging", "Security Administrator", "2026-04-10", "Open", 1, 5,
         "No formal periodic access review process currently exists.", ["A.8.2", "A.8.15", "A.8.16"]),

        ("R-011", "Web Application", "Application Owner", "Distributed Denial of Service (DDoS)", "No DDoS mitigation service",
         "A volumetric DDoS attack could overwhelm the web application, causing extended downtime and loss of customer trust.",
         "Basic cloud provider rate limiting", 2, 4, "Transfer",
         "Subscribe to a managed DDoS protection / CDN service to absorb and filter malicious traffic.",
         "Managed DDoS Protection Service (CDN)", "Application Owner", "2026-03-25", "Open", 1, 3,
         "Risk transferred via third-party service subscription.", ["A.8.20", "A.5.19"]),

        ("R-012", "Web Application", "Application Owner", "Data Leakage", "Verbose error messages exposing system details",
         "Detailed error messages returned to end users could leak information useful to an attacker, such as stack traces or database structure.",
         "Default framework error handling", 3, 3, "Mitigate",
         "Implement generic error pages for end users and centralized, secure logging of detailed errors server-side.",
         "Secure Error Handling + Centralized Logging", "Development Lead", "2026-03-18", "Open", 2, 2,
         "Identified during a routine penetration test.", ["A.8.12", "A.8.15"]),

        ("R-013", "Email System", "IT Manager", "Business Email Compromise", "Lack of email authentication protocols",
         "Attackers could spoof internal email addresses to impersonate executives and request fraudulent wire transfers.",
         "Standard SMTP configuration", 3, 4, "Mitigate",
         "Implement SPF, DKIM, and DMARC email authentication, plus staff awareness training for financial requests.",
         "SPF/DKIM/DMARC + Awareness Training", "IT Manager", "2026-02-15", "In Progress", 2, 3,
         "Increase in spoofed domain reports over the last quarter.", ["A.6.3", "A.8.20", "A.5.24"]),

        ("R-014", "Customer Database", "Database Administrator", "Privilege Escalation", "Unpatched database management software",
         "An attacker exploiting a known software vulnerability could escalate privileges and gain administrative control of the database.",
         "Patching performed on ad-hoc basis", 3, 5, "Mitigate",
         "Establish a formal patch management schedule and vulnerability scanning program for all database servers.",
         "Vulnerability Management Program + Patch Schedule", "Database Administrator", "2026-03-08", "Open", 1, 5,
         "Vendor released a critical patch two months ago, not yet applied.", ["A.8.8", "A.8.9"]),

        ("R-015", "Internal Network", "Network Administrator", "Malware Infection", "Outdated antivirus signatures on endpoints",
         "Outdated malware protection could allow malicious software to spread across endpoints connected to the internal network.",
         "Legacy antivirus with manual updates", 3, 3, "Mitigate",
         "Deploy centrally managed EDR with automatic signature and behavioral updates across all endpoints.",
         "Centrally Managed EDR", "IT Administrator", "2026-03-12", "Open", 2, 2,
         "Update compliance currently below 80% across managed devices.", ["A.8.7", "A.8.1"]),

        ("R-016", "Employee Database", "HR Manager", "Data Leakage", "No data loss prevention tooling",
         "Sensitive employee personal and payroll data could be exfiltrated via email or removable media without detection.",
         "No DLP controls in place", 2, 4, "Mitigate",
         "Deploy a data loss prevention (DLP) solution to monitor and restrict transfer of sensitive HR data.",
         "DLP Solution + USB Restriction Policy", "HR Manager", "2026-04-05", "Open", 1, 3,
         "Payroll data classified as highly sensitive under company policy.", ["A.8.12", "A.5.10"]),

        ("R-017", "Cloud Storage", "Cloud Administrator", "Unauthorized Access", "Shared/reused cloud administrator credentials",
         "Reused or shared administrative credentials for the cloud environment increase the risk of unauthorized access if compromised.",
         "Single shared admin account", 3, 4, "Mitigate",
         "Implement individual named accounts, MFA, and just-in-time privileged access for all cloud administrators.",
         "Individual Accounts + MFA + JIT Access", "Cloud Administrator", "2026-02-22", "Accepted", 2, 4,
         "Interim risk accepted by management pending completion of identity project (Q2 2026).", ["A.5.16", "A.8.2", "A.8.5"]),
    ]

    for row in sample_risks:
        (code, asset_name, owner, threat, vuln, description, existing_ctrl,
         likelihood, impact, treatment, treat_desc, proposed_ctrl, risk_owner,
         target_date, status, res_like, res_impact, notes, iso_ctrl_list) = row

        inherent_score = likelihood * impact
        inherent_level = level(inherent_score)
        residual_score = res_like * res_impact if res_like and res_impact else None
        residual_level = level(residual_score) if residual_score else None
        asset_id = asset_map.get(asset_name)

        cur.execute("""
            INSERT OR IGNORE INTO risks (
                risk_code, asset_id, asset_owner, threat, vulnerability, risk_description,
                existing_controls, likelihood, impact, inherent_score, inherent_level,
                risk_treatment, treatment_description, proposed_controls, risk_owner,
                target_date, status, residual_likelihood, residual_impact,
                residual_score, residual_level, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            code, asset_id, owner, threat, vuln, description, existing_ctrl,
            likelihood, impact, inherent_score, inherent_level,
            treatment, treat_desc, proposed_ctrl, risk_owner,
            target_date, status, res_like, res_impact,
            residual_score, residual_level, notes
        ))

        risk_row = cur.execute("SELECT id FROM risks WHERE risk_code = ?", (code,)).fetchone()
        if risk_row:
            risk_id = risk_row["id"]
            for ctrl_code in iso_ctrl_list:
                ctrl_id = control_map.get(ctrl_code)
                if ctrl_id:
                    cur.execute(
                        "INSERT OR IGNORE INTO risk_controls (risk_id, control_id) VALUES (?, ?)",
                        (risk_id, ctrl_id)
                    )

    conn.commit()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at: {DB_PATH}")
