"""Publish every document in the Released folder as released/<slug>.pdf.

Google Docs are exported to PDF; PDFs (e.g. Form ADV and Form CRS as filed) are copied
as-is. The slug comes from the Drive file name, so name files after their URL:
disclosure, form-crs, form-adv-part2a, form-adv-part1, privacy-notice.

Reads GOOGLE_SERVICE_ACCOUNT_JSON (service account key, read-only access to the folder)
and RELEASED_FOLDER_ID from the environment. Prints the slugs whose PDF changed, one per
line, so the workflow knows what to commit, publish and send to Green Board.
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

OUT = Path("released")
DOC_MIME = "application/vnd.google-apps.document"
PDF_MIME = "application/pdf"


def slug(title: str) -> str:
    # The slug is the permanent URL, so it comes from the Doc title, not the Doc id.
    title = re.sub(r"\.pdf$", "", title, flags=re.I)
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def fingerprint(data: bytes) -> str:
    # Each export stamps a new creation time into the PDF; ignore it so an
    # unchanged Doc doesn't count as a new release.
    return hashlib.sha256(re.sub(rb"/(CreationDate|ModDate)\s*\([^)]*\)", b"", data)).hexdigest()


def main() -> None:
    creds = service_account.Credentials.from_service_account_info(
        json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]),
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
    )
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    folder = os.environ["RELEASED_FOLDER_ID"]

    files = drive.files().list(
        q=f"'{folder}' in parents and (mimeType = '{DOC_MIME}' or mimeType = '{PDF_MIME}')"
        " and trashed = false",
        fields="files(id, name, mimeType)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()["files"]
    if not files:
        sys.exit("No Google Docs or PDFs found in the Released folder; refusing to publish an empty site.")

    OUT.mkdir(exist_ok=True)
    changed = []
    for f in files:
        name = slug(f["name"])
        if f["mimeType"] == DOC_MIME:
            pdf = drive.files().export(fileId=f["id"], mimeType=PDF_MIME).execute()
        else:
            pdf = drive.files().get_media(fileId=f["id"], supportsAllDrives=True).execute()
        path = OUT / f"{name}.pdf"
        if not path.exists() or fingerprint(path.read_bytes()) != fingerprint(pdf):
            path.write_bytes(pdf)
            changed.append(name)

    print("\n".join(changed))


if __name__ == "__main__":
    main()
