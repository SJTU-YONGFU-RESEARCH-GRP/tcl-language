# Cloudflare Worker Deployment Guide for Transparent Quiz Submission

This Cloudflare Worker allows the **SJTU VLSI Tcl Quiz Challenge** to automatically submit verified scores directly to **GitHub Issues** in the background, completely transparent to the user, without exposing any GitHub Personal Access Token (PAT) on the client side.

---

## Architecture Overview

```
[Student finishes quiz in browser]
              │
              ▼ (Silent background fetch - POST /)
   [Cloudflare Worker Relay]
              │
              ▼ (Authenticated with server secret GITHUB_TOKEN)
   [GitHub Issues API: SJTU-YONGFU-RESEARCH-GRP/tcl-language-lab]
              │
              ▼
   [Public Leaderboard (GET /leaderboard or GitHub API)]
```

---

## 1. Create a GitHub Personal Access Token (PAT)

1. Go to **GitHub Settings** → **Developer Settings** → **Personal Access Tokens** → **Fine-grained tokens**.
2. Click **Generate new token**.
3. **Repository access**: Select **Only select repositories** → choose `SJTU-YONGFU-RESEARCH-GRP/tcl-language-lab`.
4. **Permissions**: Under **Repository permissions**, select:
   - **Issues**: `Read and write`
5. Click **Generate token** and copy the token (`github_pat_...`).

---

## 2. Deploy via Wrangler CLI

From this directory (`release/backend`):

```bash
# 1. Install dependencies
npm install

# 2. Login to Cloudflare
npx wrangler login

# 3. Store the GitHub Token securely in Cloudflare's encrypted secret store
npx wrangler secret put GITHUB_TOKEN
# (Paste your token when prompted)

# 4. Deploy the worker
npm run deploy
```

Wrangler will output your live worker URL:
```text
https://tcl-quiz-results.<YOUR_SUBDOMAIN>.workers.dev
```

---

## 3. Alternative: Deploy via Cloudflare Dashboard (No CLI)

1. Log into [Cloudflare Dashboard](https://dash.cloudflare.com/) → **Compute (Workers) & Pages**.
2. Click **Create Application** → **Create Worker** → Name it `tcl-quiz-results` → **Deploy**.
3. Go to **Settings** → **Variables and Secrets**:
   - Add Secret: `GITHUB_TOKEN` → paste your token value.
   - Add Variable (Plain text): `GITHUB_OWNER` = `SJTU-YONGFU-RESEARCH-GRP`
   - Add Variable (Plain text): `GITHUB_REPO` = `tcl-language-lab`
4. In the worker editor, paste the contents of `cloudflare-worker.js` and click **Save and Deploy**.

---

## 4. Verification

Test the health of your worker endpoint:

```bash
curl -sL https://<YOUR_WORKER_URL>/health
```

Expected response:
```json
{
  "ok": true,
  "has_token": true,
  "owner": "SJTU-YONGFU-RESEARCH-GRP",
  "repo": "tcl-language-lab",
  "github_status": 200,
  "repo_full_name": "SJTU-YONGFU-RESEARCH-GRP/tcl-language-lab",
  "has_issues": true
}
```
