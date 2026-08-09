#!/usr/bin/env python3
"""
Portfolio Update Script
Extracts structured data from CV PDF and generates data.json.
Usage:
  python update_portfolio.py              # Extract CV data
  python update_portfolio.py --watch      # Watch mode (auto-update)
  python update_portfolio.py --deploy     # Deploy to GitHub
"""

import json
import os
import re
import sys
import hashlib
from datetime import datetime
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
HTML_FILE = BASE_DIR / "index.html"
CV_PDF = BASE_DIR / "RESUME-ALWARD-JEVON-PUTRA.pdf"
DATA_FILE = BASE_DIR / "data.json"


def extract_pdf_text(pdf_path):
    """Extract all text from PDF using PyMuPDF."""
    import fitz
    doc = fitz.open(str(pdf_path))
    text = "\n".join(page.get_text().strip() for page in doc)
    doc.close()
    return text.strip()


def parse_cv(text):
    """Parse raw CV text into structured dictionary."""
    data = {
        "profile": {
            "name": "",
            "title": "",
            "email": "",
            "phone": "",
            "website": "",
            "location": "Depok, Indonesia",
            "summary": ""
        },
        "expertise": [],
        "achievements": [],
        "experience": [],
        "education": [],
        "additional": {}
    }

    # --- Name & Title ---
    lines = text.splitlines()
    if lines:
        data["profile"]["name"] = lines[0].strip()
    if len(lines) > 1:
        data["profile"]["title"] = lines[1].strip()

    # --- Contact (email, phone, website) ---
    email_match = re.search(r"([\w.+-]+@[\w-]+\.[\w.-]+)", text)
    if email_match:
        data["profile"]["email"] = email_match.group(1)

    phone_match = re.search(r"(\+?\d[\d-]{7,}\d)", text)
    if phone_match:
        data["profile"]["phone"] = phone_match.group(1)

    url_match = re.search(r"(https?://[^\s\"]+)", text)
    if url_match:
        data["profile"]["website"] = url_match.group(1)

    # --- Summary ---
    summary_match = re.search(
        r"(AI-driven Product Manager[^.]*\.)", text
    )
    if summary_match:
        data["profile"]["summary"] = summary_match.group(1).strip()

    # --- Expertise ---
    expertise_block = re.search(
        r"AREA OF EXPERTISE\s+([\s\S]*?)(?:KEY ACHIEVEMENTS|PROFESSIONAL EXPERIENCE)",
        text, re.IGNORECASE
    )
    if expertise_block:
        raw = expertise_block.group(1).strip()
        data["expertise"] = [
            line.strip() for line in raw.splitlines()
            if line.strip() and len(line.strip()) > 3
        ]

    # --- Achievements ---
    ach_block = re.search(
        r"KEY ACHIEVEMENTS\s+([\s\S]*?)PROFESSIONAL EXPERIENCE",
        text, re.IGNORECASE
    )
    if ach_block:
        raw = ach_block.group(1).strip()
        bullets = re.split(r"(?:\u2022|�|\*)\s*", raw)
        data["achievements"] = [
            b.strip() for b in bullets if b.strip() and len(b.strip()) > 5
        ]

    # --- Experience ---
    exp_block = re.search(
        r"PROFESSIONAL EXPERIENCE\s+([\s\S]*?)EDUCATION",
        text, re.IGNORECASE
    )
    if exp_block:
        raw = exp_block.group(1).strip()
        roles = re.split(r"\n\s*\n", raw)
        for role in roles:
            role = role.strip()
            if not role:
                continue

            # Try to pull out title, company, period, bullets
            role_lines = role.splitlines()
            title = role_lines[0].strip() if role_lines else ""
            company = ""
            period = ""
            bullets = []

            for line in role_lines[1:]:
                line = line.strip()
                if not line:
                    continue
                date_match = re.match(
                    r"(Sep|Oct|Nov|Dec|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug)\s+\d{4}\s*\S*\s*(?:\u2014|to|-)\s*\S+",
                    line, re.IGNORECASE
                )
                if date_match:
                    period = date_match.group(0)
                    continue
                if re.match(r"(?:PT|Company|Inc\.|Corp|Ltd|B2G|Account|Manager|Sales|Marketing)\b", line, re.IGNORECASE):
                    company = line
                if re.match(r"(?:\u2022|\+|-|\*|�)\s", line):
                    bullets.append(line.lstrip("*+.-\u2022\u2606 "))

            if title or company:
                data["experience"].append({
                    "title": title,
                    "company": company,
                    "period": period,
                    "responsibilities": bullets
                })

    # --- Education ---
    edu_block = re.search(
        r"EDUCATION\s+([\s\S]*?)ADDITIONAL INFORMATION",
        text, re.IGNORECASE
    )
    if edu_block:
        raw = edu_block.group(1).strip()
        entries = re.split(r"\n\s*\n", raw)
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            lines_e = entry.splitlines()
            degree = ""
            school = ""
            period = ""
            details = []
            for line in lines_e:
                line = line.strip()
                date_match = re.match(
                    r"(Sep|Oct|Nov|Dec|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug)\s+\d{4}\s*\S*\s*(?:\u2014|to|-)\s*\S+",
                    line, re.IGNORECASE
                )
                if date_match:
                    period = date_match.group(0)
                elif re.match(r"(?:MSc|BA|BBA|BBM|BS|BSc|MA|MS|PhD|Diploma|Certificate)\b", line, re.IGNORECASE):
                    degree = line
                elif re.match(r"(?:University|College|Academy|Institute)\b", line, re.IGNORECASE):
                    school = line
                elif re.match(r"(?:\u2022|\+|-|\*|�)\s", line):
                    details.append(line.lstrip("*+.-\u2022\u2606 "))
            if degree or school:
                data["education"].append({
                    "degree": degree,
                    "school": school,
                    "period": period,
                    "details": details
                })

    # --- Additional ---
    add_block = re.search(
        r"ADDITIONAL INFORMATION\s+([\s\S]*)",
        text, re.IGNORECASE
    )
    if add_block:
        raw = add_block.group(1).strip()
        add_data = {}
        for line in raw.splitlines():
            line = line.strip()
            if re.match(r"Languages[:\u2022-]*", line, re.IGNORECASE):
                add_data["languages"] = [
                    l.strip() for l in line.split(":")[-1].strip().split(",")
                ]
            elif re.match(r"Certifications?[:\u2022-]*", line, re.IGNORECASE):
                add_data["certifications"] = [
                    c.strip() for c in line.split(":")[-1].strip().split(",")
                ]
            elif re.match(r"Activities?[:\u2022-]*", line, re.IGNORECASE):
                add_data["activities"] = [
                    a.strip() for a in line.split(":")[-1].strip().split(";")
                ]
        data["additional"] = add_data

    return data


def build_data_json(cv_data):
    """Combine CV data with predefined projects into data.json."""
    return {
        "lastUpdated": datetime.now().isoformat(),
        "profile": cv_data["profile"],
        "expertise": cv_data["expertise"] if cv_data["expertise"] else [
            "Product Strategy",
            "Market Data Intelligence",
            "Product Management",
            "Sales Enablement",
            "Business Process",
            "Vendor Negotiation"
        ],
        "achievements": cv_data["achievements"],
        "projects": [
            {
                "id": "product-intelligence-platform",
                "title": "Product Intelligence Platform",
                "category": "Product Intelligence",
                "year": "2026",
                "summary": "Built an AI-powered product intelligence platform that transformed fragmented product data into faster decisions, stronger market positioning, and scalable business growth.",
                "challenge": "Product decisions relied on fragmented data, slow market research, and manual competitive tracking.",
                "solution": "Developed a centralized AI platform that unified product, market, and competitive intelligence into a single decision-making system.",
                "impact": "Reduced decision time, improved portfolio visibility, and enabled faster go-to-market planning across multiple product lines.",
                "stack": ["Product Intelligence", "AI", "Market Research", "Competitive Analysis"],
                "image": "project-tkdn.jpg"
            },
            {
                "id": "tender-intelligence-platform",
                "title": "Tender Intelligence Platform",
                "category": "Business Intelligence",
                "year": "2026",
                "summary": "Built an AI-powered tender intelligence platform that transformed government procurement data into actionable product opportunities, enabling faster opportunity identification and smarter portfolio decisions.",
                "challenge": "Government procurement were scattered across millions of RUP records, making it difficult to identify relevant tenders and quickly match them with the right product portfolio.",
                "solution": "Developed an automated intelligence platform that continuously analyzes INAPROC procurement data, maps opportunities to Axioo's product catalog, and recommends the most suitable products based on specifications, pricing, and portfolio readiness.",
                "impact": "Accelerated product recommendation for B2G procurement opportunities and enabled faster commercial decision-making between sales and product teams.",
                "stack": ["AI Tender Intelligence", "Procurement Analytics", "Product Matching", "Automated Insights"],
                "image": "project-keyaccount.jpg"
            },
            {
                "id": "inventory-intelligence-platform",
                "title": "Inventory Intelligence Platform",
                "category": "Operations Intelligence",
                "year": "2026",
                "summary": "An automated decision support platform that identifies operational risks, prioritizes actions, and delivers real-time recommendations for management and distributors.",
                "challenge": "Inventory risks such as stockouts, last-buy products, and lifecycle changes required significant manual monitoring across multiple product lines.",
                "solution": "Built an automated decision support platform that identifies operational risks, prioritizes actions, and delivers real-time recommendations for management and distributors.",
                "impact": "Proactive inventory management, faster operational decisions, improved distributor readiness.",
                "stack": ["Inventory Intelligence", "Automated Analytics", "Decision Support", "Operational Risk"],
                "image": "project-lean.jpg"
            }
        ],
        "career": [],
        "education": cv_data["education"],
        "additional": cv_data["additional"],
        "skills": [
            {"group": "Product", "tags": cv_data["expertise"][:2]},
            {"group": "Management", "tags": cv_data["expertise"][2:4]},
            {"group": "Business", "tags": cv_data["expertise"][4:]}
        ] if cv_data["expertise"] else []
    }


def run_update():
    """Main update flow: extract CV, write data.json."""
    print(f"Portfolio Update — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    if not CV_PDF.exists():
        print(f"ERROR: CV file not found: {CV_PDF}")
        return False

    print(f"Reading CV: {CV_PDF.name}")
    text = extract_pdf_text(CV_PDF)
    if not text:
        print("ERROR: Could not extract text from PDF.")
        return False
    print(f"  -> extracted {len(text)} characters")

    print("Parsing CV content...")
    cv = parse_cv(text)
    print(f"  -> {len(cv['expertise'])} expertise areas")
    print(f"  -> {len(cv['achievements'])} achievements")
    print(f"  -> {len(cv['experience'])} experiences")
    print(f"  -> {len(cv['education'])} education entries")

    print("Writing data.json...")
    full_data = build_data_json(cv)
    DATA_FILE.write_text(json.dumps(full_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  -> saved {DATA_FILE.name} ({DATA_FILE.stat().st_size} bytes)")

    print("\nDone! Portfolio data updated.")
    return True


def watch_mode():
    """Watch CV file for changes and auto-update."""
    print("Watching for CV changes (Ctrl+C to stop)...")
    last_hash = None
    while True:
        if CV_PDF.exists():
            with open(CV_PDF, "rb") as f:
                current_hash = hashlib.md5(f.read()).hexdigest()
            if current_hash != last_hash:
                print(f"\n[Change detected] Updating portfolio...")
                run_update()
                last_hash = current_hash
        import time
        time.sleep(3)

def deploy():
    """Deploy to GitHub (requires git repo)."""
    if not (BASE_DIR / ".git").exists():
        print("ERROR: No git repository found. Run 'git init' first.")
        return False
    import subprocess
    subprocess.run(["git", "add", "."], cwd=str(BASE_DIR), check=True)
    subprocess.run(["git", "commit", "-m", f"Auto-update: {datetime.now().isoformat()}"], cwd=str(BASE_DIR), check=True)
    subprocess.run(["git", "push"], cwd=str(BASE_DIR), check=True)
    print("Deployed!")
    return True


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--watch" in args:
        try:
            watch_mode()
        except KeyboardInterrupt:
            print("\nWatch stopped.")
    elif "--deploy" in args:
        run_update()
        deploy()
    else:
        run_update()
