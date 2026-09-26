"""
Session 13 - Task 2: Python Simulation of Zapier Gmail -> Google Drive
======================================================================
This script provides an executable Python simulation of the Zapier workflow:
1. Emulates Gmail Trigger: Checks for new emails with subject 'Assignment'
2. Emulates Google Drive Action: Extracts the attachment and saves it to
   the local simulated Google Drive storage directory ('google_drive_storage/').
"""

import sys
import os
import datetime

# Ensure safe UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
GDRIVE_DIR = os.path.join(CURRENT_DIR, "google_drive_storage", "Assignments")

# Simulated Gmail Inbox Payloads
MOCK_GMAIL_INBOX = [
    {
        "id": "msg_001",
        "sender": "student1@university.edu",
        "subject": "Assignment 13 Submission - MultiModal Agent",
        "received_at": "2026-09-26 14:10:00",
        "has_attachment": True,
        "attachment": {
            "filename": "Session13_Patel_Assignment.pdf",
            "content": b"%PDF-1.4 Simulated PDF binary payload for Assignment 13 submission..."
        }
    },
    {
        "id": "msg_002",
        "sender": "newsletter@techupdates.com",
        "subject": "Weekly Tech Digest",
        "received_at": "2026-09-26 14:15:00",
        "has_attachment": False,
        "attachment": None
    },
    {
        "id": "msg_003",
        "sender": "student2@university.edu",
        "subject": "Re: Query regarding Course Schedule",
        "received_at": "2026-09-26 14:20:00",
        "has_attachment": True,
        "attachment": {"filename": "syllabus.pdf", "content": b"%PDF-1.4 Syllabus..."}
    },
    {
        "id": "msg_004",
        "sender": "student3@university.edu",
        "subject": "Assignment 14 Final Draft",
        "received_at": "2026-09-26 14:25:00",
        "has_attachment": True,
        "attachment": {
            "filename": "Session14_MCP_Report.docx",
            "content": b"PK\x03\x04 Simulated DOCX binary content for MCP Assignment..."
        }
    }
]

def zapier_workflow_simulation():
    print("=" * 70)
    print("   SESSION 13 - TASK 2: ZAPIER GMAIL -> GOOGLE DRIVE SIMULATION")
    print("=" * 70)

    os.makedirs(GDRIVE_DIR, exist_ok=True)
    print(f"[*] Google Drive Destination: {GDRIVE_DIR}")
    print("[*] Zapier Rule: Trigger when subject contains 'Assignment' AND has_attachment=True\n")

    processed_count = 0

    for email in MOCK_GMAIL_INBOX:
        print(f"--> Incoming Email: ID={email['id']}")
        print(f"    From:    {email['sender']}")
        print(f"    Subject: \"{email['subject']}\"")

        # Zapier Trigger Filter
        is_match = ("assignment" in email["subject"].lower()) and email["has_attachment"]

        if is_match:
            attachment = email["attachment"]
            filename = attachment["filename"]
            target_path = os.path.join(GDRIVE_DIR, filename)

            # Zapier Action: Upload to Google Drive
            with open(target_path, "wb") as f:
                f.write(attachment["content"])

            print(f"    [MATCH] Zap Triggered! Uploading attachment to Google Drive...")
            print(f"    [ACTION] Saved '{filename}' to Google Drive: {target_path}")
            processed_count += 1
        else:
            print(f"    [FILTERED] Ignored (Does not match subject filter 'Assignment' or no attachment).")
        print("-" * 70)

    print(f"\n[SUCCESS] Zapier simulation complete! {processed_count} attachment(s) saved to Google Drive.")
    print("=" * 70)

if __name__ == "__main__":
    zapier_workflow_simulation()
