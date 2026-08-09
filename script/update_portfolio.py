#!/usr/bin/env python3
"""
Portfolio Update Script
Automatically updates portfolio HTML content from CV PDF
Usage: python update_portfolio.py [--watch] [--deploy]
"""

import os
import sys
import re
import json
import fitz  # PyMuPDF
from datetime import datetime
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
HTML_FILE = BASE_DIR / "index.html"
CV_PDF = BASE_DIR / "RESUME-ALWARD-JEVON-PUTRA.pdf"
DATA_FILE = BASE_DIR / "data.json"

def extract_text_from_pdf(pdf_path):
    """Extract text content from CV PDF"""
    try:
        doc = fitz.open(str(pdf_path))
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def parse_cv_content(text):
    """Parse CV text into structured data"""
    data = {
        "name": "ALWARD JEVON SOEMINTO PUTRA",
        "title": "PRODUCT MANAGER",
        "email": "alwardjevon@yahoo.com",
        "phone": "+62-811-3498-134",
        "website": "https://je8-stack.github.io/portfolio/",
        "summary": "",
        "expertise": [],
        "achievements": [],
        "experience": [],
        "education": [],
        "additional": {
            "languages": ["Bahasa", "English", "Mandarin"],
            "certifications": ["IELTS 6.5"]
        }
    }
    
    # Extract summary
    summary_match = re.search(
        r"(?i)(AI-driven Product Manager[^.]*\.)",
        text
    )
    if summary_match:
        data["summary"] = summary_match.group(1)
    
    # Extract expertise
    expertise_section = re.search(
        r"AREA OF EXPERTISE\s+([\s\S]*?)PROFESSIONAL EXPERIENCE",
        text,
        re.IGNORECASE
    )
    if expertise_section:
        expertise_text = expertise_section.group(1)
        # Extract expertise items
        expertise_items = re.findall(r"([A-Z][a-zA-Z\s]+)", expertise_text)
        data["expertise"] = [item.strip() for item in expertise_items if len(item) > 5]
    
    # Extract achievements
    achievements_section = re.search(
        r"KEY ACHIEVEMENTS\s+([\s\S]*?)PROFESSIONAL EXPERIENCE",
        text,
        re.IGNORECASE
    )
    if achievements_section:
        achievement_text = achievements_section.group(1)
        # Extract bullet points
        achievements = re.findall(r"�\s*(.+?)(?=�|$)", achievement_text, re.DOTALL)
        data["achievements"] = [ach.strip() for ach in achievements if ach.strip()]
    
    return data

def update_html_file(cv_data):
    """Update HTML file with CV data"""
    try:
        html_content = HTML_FILE.read_text(encoding="utf-8")
        
        # Update meta tags
        html_content = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{cv_data["summary"]}"',
            html_content
        )
        
        # Update OG description
        html_content = re.sub(
            r'<meta property="og:description" content="[^"]*"',
            f'<meta property="og:description" content="{cv_data["summary"][:200]}"',
            html_content
        )
        
        # Update hero lead
        html_content = re.sub(
            r'<p class="hero-lead">[^<]*</p>',
            f'<p class="hero-lead">\n            {cv_data["summary"]}\n          </p>',
            html_content
        )
        
        # Update email and phone
        if cv_data["email"]:
            html_content = re.sub(
                r'href="mailto:[^"]*"',
                f'href="mailto:{cv_data["email"]}"',
                html_content
            )
            html_content = re.sub(
                r'data-email="[^"]*"',
                f'data-email="{cv_data["email"]}"',
                html_content
            )
        
        if cv_data["phone"]:
            phone_link = cv_data["phone"].replace("-", "")
            html_content = re.sub(
                r'href="https://wa\.me/\d+"',
                f'href="https://wa.me/{phone_link}"',
                html_content
            )
        
        # Update website
        if cv_data["website"]:
            html_content = re.sub(
                r'<meta property="og:url" content="[^"]*"',
                f'<meta property="og:url" content="{cv_data["website"]}"',
                html_content
            )
            html_content = re.sub(
                r'<link href="[^"]+" rel="canonical"',
                f'<link href="{cv_data["website"]}" rel="canonical"',
                html_content
            )
        
        # Update copyright
        current_year = datetime.now().year
        html_content = re.sub(
            r'© <span id="year"></span>',
            f'© {current_year}',
            html_content
        )
        
        HTML_FILE.write_text(html_content, encoding="utf-8")
        print(f"[OK] HTML updated: {HTML_FILE}")
        return True

    except Exception as e:
        print(f"Error updating HTML: {e}")
        return False

def update_data_file(cv_data):
    """Update data.json with CV data"""
    try:
        data = {
            "lastUpdated": datetime.now().isoformat(),
            "cv": cv_data,
            "projects": [
                {
                    "id": "product-intelligence-platform",
                    "title": "Product Intelligence Platform",
                    "category": "Product Intelligence",
                    "year": "2026",
                    "summary": "Built an AI-powered product intelligence platform that accelerated product decisions, strengthened competitive positioning, and supported profitable growth across multiple product lines.",
                    "features": [
                        "Market data aggregation & competitive analysis",
                        "AI-driven insights for faster decisions",
                        "Supports Notebook, AIO, Smartboard & Videotron"
                    ],
                    "tags": ["Product Intelligence", "AI", "Market Research", "Competitive Analysis"]
                },
                {
                    "id": "tender-intelligence-platform",
                    "title": "Tender Intelligence Platform",
                    "category": "Business Intelligence",
                    "year": "2026",
                    "summary": "Built an AI-powered tender intelligence platform that transformed government procurement data into actionable product opportunities, enabling faster opportunity identification and smarter portfolio decisions.",
                    "features": [
                        "Procurement data analysis",
                        "Product matching",
                        "Automated insights"
                    ],
                    "tags": ["AI Tender Intelligence", "Procurement Analytics", "Product Matching", "Automated Insights"]
                },
                {
                    "id": "inventory-intelligence-platform",
                    "title": "Inventory Intelligence Platform",
                    "category": "Operations Intelligence",
                    "year": "2026",
                    "summary": "Proactive inventory management, faster operational decisions, and improved distributor readiness.",
                    "features": [
                        "Inventory risk monitoring",
                        "Operational decision support",
                        "Distributor readiness tracking"
                    ],
                    "tags": ["Inventory Intelligence", "Automated Analytics", "Decision Support", "Operational Risk"]
                }
            ],
            "expertise": cv_data.get("expertise", [
                "Product Strategy",
                "Market Data Intelligence", 
                "Product Management",
                "Sales Enablement",
                "Business Process",
                "Vendor Negotiation"
            ])
        }
        
        DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"[OK] Data updated: {DATA_FILE}")
        return True

    except Exception as e:
        print(f"Error updating data file: {e}")
        return False

def deploy_to_github():
    """Deploy to GitHub Pages"""
    try:
        import subprocess
        repo_url = "https://github.com/je8-stack/portfolio.git"
        
        # Add files
        subprocess.run(["git", "add", "."], cwd=str(BASE_DIR))
        
        # Commit
        commit_msg = f"Portfolio update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(BASE_DIR))
        
        # Push
        subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR))
        
        print("[OK] Deployed to GitHub")
        return True

    except Exception as e:
        print(f"Error deploying: {e}")
        return False

def watch_mode():
    """Watch for CV file changes and update automatically"""
    try:
        import time
        import hashlib
        
        print("Watching for CV file changes...")
        last_hash = None
        
        while True:
            if CV_PDF.exists():
                with open(CV_PDF, "rb") as f:
                    current_hash = hashlib.md5(f.read()).hexdigest()
                
                if current_hash != last_hash:
                    print(f"\nCV file updated! Updating portfolio...")
                    process_update()
                    last_hash = current_hash
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nStopped watching.")
    except Exception as e:
        print(f"Error in watch mode: {e}")

def process_update():
    """Main update process"""
    print(f"Processing update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"Reading CV: {CV_PDF}")
    cv_text = extract_text_from_pdf(CV_PDF)
    if not cv_text:
        print("[FAIL] Failed to extract CV text")
        return False
    
    print("Parsing CV content...")
    cv_data = parse_cv_content(cv_text)
    
    print("Updating HTML file...")
    html_success = update_html_file(cv_data)
    
    print("Updating data file...")
    data_success = update_data_file(cv_data)
    
    if html_success and data_success:
        print("[OK] Update complete!")
        return True
    return False

def main():
    print("Portfolio Update Script")
    print("=" * 40)
    
    if "--watch" in sys.argv:
        watch_mode()
    elif "--deploy" in sys.argv:
        process_update()
        deploy_to_github()
    else:
        process_update()

if __name__ == "__main__":
    main()
