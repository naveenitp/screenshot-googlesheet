# Sheet Screenshot

Turns filtered Google Sheet data into an auto-sized PNG screenshot, daily, via GitHub Actions.
Change filters/columns by editing `config.yaml` on GitHub.

## One-time setup

1. **Google service account**
   - Google Cloud Console → create project → enable **Google Sheets API**.
   - IAM & Admin → Service Accounts → create one → Keys → Add key → JSON (downloads a file).
2. **Share your sheet** with the service account's email (`...@...iam.gserviceaccount.com`) as Viewer.
3. **Add the secret in GitHub**: repo → Settings → Secrets and variables → Actions → New secret
   - Name: `GOOGLE_CREDENTIALS`
   - Value: paste the entire contents of the JSON key file.
4. **Edit `config.yaml`**: set `sheet_id`, `worksheet`, `filters`, `columns`.
5. **Run it**: Actions tab → *Daily sheet screenshot* → Run workflow.

## Getting the image
- `output/latest.png` in the repo (updated each run), or
- download from the run's **Artifacts** section.

## Run locally
```
pip install -r requirements.txt
# save your key as credentials.json (git-ignored)
python sheet_to_image.py
```

## Schedule
Edit the `cron` line in `.github/workflows/screenshot.yml` (times are UTC; IST = UTC+5:30).
