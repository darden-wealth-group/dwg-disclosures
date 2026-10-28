# DWG disclosures

Publishes Darden Wealth Group's disclosure documents from Google Docs to permanent
addresses that don't depend on where dardenwealth.com is hosted:

- https://disclosures.dardenwealth.com/ (list of all documents)
- https://disclosures.dardenwealth.com/<name>.pdf for these five (the names the redesigned
  site's Disclosures page links to):

| File name in the Released folder | Document | Usual source |
|---|---|---|
| `disclosure` | General Disclosure | Google Doc |
| `privacy-notice` | Privacy Notice | Google Doc |
| `form-crs` | Form CRS | PDF as filed |
| `form-adv-part2a` | Form ADV Part 2A brochure | PDF as filed |
| `form-adv-part1` | Form ADV Part 1 | PDF from IARD |

The Released folder may hold Google Docs (exported to PDF) or PDFs (published as-is). The
file name sets the URL, so keep these names exactly. Word files must be saved as PDF or
opened as a Google Doc first.

## How staff work (no GitHub needed)

1. **Draft:** edit the Doc in the Google Drive **Drafts** folder. The Doc is the online
   preview; File › Download › PDF is the PDF preview.
2. **Release:** once approved, copy the content into the matching Doc in the **Released**
   folder, or replace the matching PDF there (keep the same file name).
3. Within the hour (or right away via Actions › *Publish disclosures from Google Docs* ›
   Run workflow) the PDF is live, a copy is committed to `released/` as the version
   history, and each changed PDF is emailed to the Green Board archive.

## One-time setup

1. Google Cloud: create a service account (Drive API enabled), download its JSON key, and
   share the **Released** folder with the service account's email as Viewer.
2. Repository secrets (Settings › Secrets and variables › Actions):
   `GOOGLE_SERVICE_ACCOUNT_JSON` (the key file's contents), `GREENBOARD_JOURNAL_ADDRESS`
   (from the Green Board portal or account team), and `SMTP_SERVER`, `SMTP_PORT`,
   `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM` (Google Workspace: `smtp.gmail.com`, `465`,
   an app password). Until the Green Board ones are set, releases still publish with a warning.
3. Repository variable `RELEASED_FOLDER_ID`: the id at the end of the Released folder's URL.
4. Settings › Pages › Source: **GitHub Actions**.
5. DNS: `CNAME disclosures → <owner>.github.io`, then set the custom domain in Settings › Pages
   and tick **Enforce HTTPS**.
6. Point email signatures and the website footer at the PDF URLs.
