/**
 * Cloudflare Worker: Secure Relay for Tcl Quiz Challenge Results & Leaderboard
 *
 * Repository: SJTU-YONGFU-RESEARCH-GRP/tcl-language-lab
 * Features:
 * - Transparent background submission of quiz results to GitHub Issues
 * - Server-side GITHUB_TOKEN storage (never exposed to client browser)
 * - Schema validation for tcl_quiz_result_v1 and quiz_challenge_result_v1
 * - Leaderboard aggregation and ranking API (GET /leaderboard)
 * - Health verification endpoint (GET /health)
 */

function corsHeaders(env) {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "86400",
  };
}

function json(data, status = 200, env = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      ...corsHeaders(env),
    },
  });
}

async function sha256Hex(text) {
  const enc = new TextEncoder().encode(String(text || ""));
  const buf = await crypto.subtle.digest("SHA-256", enc);
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

function maskName(name) {
  const s = String(name || "Anonymous").trim();
  if (s.length <= 2) return s;
  return s[0] + "***" + s[s.length - 1];
}

function extractPayloadFromIssue(body) {
  if (!body) return null;
  const match = body.match(/```json\s*([\s\S]*?)\s*```/);
  if (!match) return null;
  try {
    return JSON.parse(match[1]);
  } catch (_) {
    return null;
  }
}

async function fetchIssues(env, label) {
  const owner = env.GITHUB_OWNER || "SJTU-YONGFU-RESEARCH-GRP";
  const repo = env.GITHUB_REPO || "tcl-language-lab";
  const token = env.GITHUB_TOKEN;

  const url = `https://api.github.com/repos/${owner}/${repo}/issues?labels=${encodeURIComponent(
    label
  )}&state=all&per_page=100`;

  const headers = {
    Accept: "application/vnd.github+json",
    "User-Agent": "tcl-quiz-results-worker",
  };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(url, { headers });
  if (!res.ok) {
    const err = new Error(`GitHub fetch failed with HTTP ${res.status}`);
    err.status = res.status;
    throw err;
  }
  const data = await res.json();
  return Array.isArray(data) ? data : [];
}

async function buildLeaderboard(env, mode) {
  const wantMode = mode === "quick" || mode === "test" ? "quick" : "full";
  const label = wantMode === "quick" ? "quiz-result,quick-mode" : "quiz-result,full-mode";

  let issues = [];
  try {
    issues = await fetchIssues(env, "quiz-result");
  } catch (err) {
    return { ok: false, error: err.message, rows: [] };
  }

  const bestByKey = new Map();

  for (const iss of issues) {
    if (iss.pull_request) continue;
    const payload = extractPayloadFromIssue(iss.body);
    if (!payload) continue;

    const schema = payload.schema;
    if (schema !== "tcl_quiz_result_v1" && schema !== "quiz_challenge_result_v1") {
      continue;
    }

    const perf = payload.performance || payload.summary || {};
    const ident = payload.identity || {};
    const payloadMode = (perf.mode || (payload.quest && payload.quest.mode) || "full").toLowerCase();

    // Match requested mode
    const isQuick = payloadMode.includes("quick") || payloadMode.includes("test");
    if (wantMode === "quick" && !isQuick) continue;
    if (wantMode === "full" && isQuick) continue;

    const certId = perf.certId || `TCL-ISSUE-${iss.number}`;
    const name = ident.name || "Anonymous";
    const score = Number(perf.score) || 0;
    const accuracy = Number(perf.accuracy) || 0;
    const time = perf.time || "00:00";
    const cleared = perf.cleared || "0/0";
    const location = ident.location || "Global";
    const date = (perf.date || iss.created_at || "").slice(0, 10);

    const personKey = ident.email ? await sha256Hex(ident.email) : certId;
    const existing = bestByKey.get(personKey);

    const candidateRow = {
      candidate: name,
      score,
      accuracy,
      time,
      cleared,
      date,
      certId,
      mode: wantMode === "quick" ? "Quick Assessment" : "Full Assessment",
    };

    if (!existing || candidateRow.score > existing.score) {
      bestByKey.set(personKey, candidateRow);
    }
  }

  const rows = Array.from(bestByKey.values());
  rows.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    if (b.accuracy !== a.accuracy) return b.accuracy - a.accuracy;
    return a.time.localeCompare(b.time);
  });

  rows.forEach((r, idx) => {
    r.rank = idx + 1;
  });

  return {
    ok: true,
    mode: wantMode,
    generated_at: new Date().toISOString(),
    count: rows.length,
    rows,
  };
}

async function handlePost(request, env) {
  const token = env.GITHUB_TOKEN;
  const owner = env.GITHUB_OWNER || "SJTU-YONGFU-RESEARCH-GRP";
  const repo = env.GITHUB_REPO || "tcl-language-lab";

  if (!token) {
    return json({ ok: false, error: "GITHUB_TOKEN secret is not configured on worker" }, 500, env);
  }

  let payload;
  try {
    payload = await request.json();
  } catch (_) {
    return json({ ok: false, error: "Invalid JSON payload" }, 400, env);
  }

  if (!payload || (payload.schema !== "tcl_quiz_result_v1" && payload.schema !== "quiz_challenge_result_v1")) {
    return json({ ok: false, error: "Unsupported schema" }, 400, env);
  }

  const ident = payload.identity || {};
  const perf = payload.performance || payload.summary || {};
  const name = String(ident.name || "Anonymous").slice(0, 100);
  const email = String(ident.email || "").slice(0, 150);
  const accuracy = Number(perf.accuracy) || 100;
  const mode = String(perf.mode || "full").toLowerCase().includes("quick") ? "quick" : "full";
  const modeLabel = mode === "quick" ? "Quick Assessment" : "Full Assessment";
  const certId = String(perf.certId || `TCL-CERT-${Date.now().toString(36).toUpperCase()}`);
  const dateStr = String(perf.date || new Date().toISOString().slice(0, 10));
  const timeFormatted = String(perf.time || "00:00");
  const cleared = String(perf.cleared || "N/A");
  const score = Number(perf.score) || 0;

  const title = `[quiz-result] ${name} — ${accuracy}% (${modeLabel}) — ${certId}`;

  const body = [
    "### Candidate Information",
    `- **Candidate Name**: ${name}`,
    `- **Email**: ${email ? email.replace(/(.{2})(.*)(@.*)/, "$1***$3") : "_none_"}`,
    `- **Award Date**: ${dateStr}`,
    "",
    "### Assessment Summary",
    `- **Mode**: ${modeLabel}`,
    `- **Total Score**: ${score}`,
    `- **Accuracy**: ${accuracy}%`,
    `- **Elapsed Time**: ${timeFormatted}`,
    `- **Questions Cleared**: ${cleared}`,
    `- **Verification Credential Hash**: \`${certId}\``,
    "",
    "## Full payload",
    "```json",
    JSON.stringify(payload, null, 2),
    "```",
  ].join("\n");

  const ghRes = await fetch(`https://api.github.com/repos/${owner}/${repo}/issues`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "User-Agent": "tcl-quiz-results-worker",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title,
      body,
      labels: ["quiz-result", `${mode}-mode`],
    }),
  });

  const ghData = await ghRes.json().catch(() => ({}));
  if (!ghRes.ok) {
    return json(
      {
        ok: false,
        error: "GitHub API rejected issue creation",
        status: ghRes.status,
        detail: ghData,
      },
      502,
      env
    );
  }

  return json(
    {
      ok: true,
      certId,
      issue_number: ghData.number,
      issue_url: ghData.html_url,
      submitted_at: new Date().toISOString(),
    },
    200,
    env
  );
}

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders(env) });
    }

    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";

    if (request.method === "GET" && (path === "/leaderboard" || path.endsWith("/leaderboard"))) {
      const mode = url.searchParams.get("mode") || "full";
      const board = await buildLeaderboard(env, mode);
      return json(board, board.ok ? 200 : 502, env);
    }

    if (request.method === "GET" && (path === "/health" || path.endsWith("/health"))) {
      const owner = env.GITHUB_OWNER || "SJTU-YONGFU-RESEARCH-GRP";
      const repo = env.GITHUB_REPO || "tcl-language-lab";
      const token = env.GITHUB_TOKEN;

      const headers = {
        Accept: "application/vnd.github+json",
        "User-Agent": "tcl-quiz-results-worker",
      };
      if (token) headers.Authorization = `Bearer ${token}`;

      const res = await fetch(`https://api.github.com/repos/${owner}/${repo}`, { headers });
      const repoData = await res.json().catch(() => ({}));

      return json(
        {
          ok: res.ok,
          has_token: !!token,
          owner,
          repo,
          github_status: res.status,
          repo_full_name: repoData.full_name || null,
          has_issues: repoData.has_issues ?? null,
        },
        res.ok ? 200 : 502,
        env
      );
    }

    if (request.method === "POST" && (path === "/" || path === "" || path === "/submit")) {
      return handlePost(request, env);
    }

    return json({ ok: false, error: "Not found" }, 404, env);
  },
};
