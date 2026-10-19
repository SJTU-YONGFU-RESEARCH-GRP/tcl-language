#!/usr/bin/env python3
"""Quiz Challenge and Leaderboard generator for Tcl for VLSI Portal.

Implements the 3-tier difficulty quiz challenge, silent grading,
dynamic time scaling (thinking time allowance), reinforcement loop
(reinforcement questions on mistakes), SVG verifiable certificate,
and interactive public leaderboard with Hall of Fame rankings.
"""

from __future__ import annotations
from pathlib import Path


def write_quiz_challenge_pages(docs_dir: Path) -> None:
    en_content = _build_quiz_page("en")
    zh_content = _build_quiz_page("zh")
    ms_content = _build_quiz_page("ms")
    fr_content = _build_quiz_page("fr")

    (docs_dir / "quiz.md").write_text(en_content, encoding="utf-8")
    (docs_dir / "quiz.zh.md").write_text(zh_content, encoding="utf-8")
    (docs_dir / "quiz.ms.md").write_text(ms_content, encoding="utf-8")
    (docs_dir / "quiz.fr.md").write_text(fr_content, encoding="utf-8")


def write_leaderboard_pages(docs_dir: Path) -> None:
    en_content = _build_leaderboard_page("en")
    zh_content = _build_leaderboard_page("zh")
    ms_content = _build_leaderboard_page("ms")
    fr_content = _build_leaderboard_page("fr")

    (docs_dir / "leaderboard.md").write_text(en_content, encoding="utf-8")
    (docs_dir / "leaderboard.zh.md").write_text(zh_content, encoding="utf-8")
    (docs_dir / "leaderboard.ms.md").write_text(ms_content, encoding="utf-8")
    (docs_dir / "leaderboard.fr.md").write_text(fr_content, encoding="utf-8")


def _build_quiz_page(lang: str) -> str:
    i18n_strings = {
        "en": {
            "title": "🎯 VLSI Tcl Quiz Challenge & Certification",
            "badges": ["3-Tier Mastery Model", "Silent Grading", "Thinking Timer", "Verifiable Certificate", "Hall of Fame"],
            "desc": "An industrial-grade diagnostic quest. Questions scale across 3 difficulty tiers (Easy → Medium → Hard). Time limits provide a fair thinking allowance to support your problem-solving pace, with targeted reinforcement questions to confirm mastery before unlocking subsequent tiers.",
            "mode_select": "Choose Quest Mode & Candidate Name",
            "full_mode": "Full Grand Prix (All 4 Modules · 12 Tiers)",
            "sprint_mode": "Sprint Diagnostic (6 Core Benchmark Questions)",
            "candidate_placeholder": "Enter your name or callsign (e.g. VLSI_Cadence_Pro)...",
            "start_btn": "🚀 Launch Quiz Challenge",
            "mod_label": "Current Module",
            "tier_label": "Difficulty Tier",
            "timer_label": "Thinking Timer",
            "submit_btn": "Submit Answer (Enter)",
            "thinking_bonus": "Thinking Time Allowance Granted",
            "report_title": "📊 Post-Quest Analytical Mastery Report",
            "cert_title": "🎓 Claim Your Industrial Mastery Certificate",
            "dl_cert": "📥 Download Certificate (SVG)",
            "print_cert": "🖨️ Print Certificate",
            "view_leaderboard": "🏆 View Standing on Public Leaderboard →",
            "retake": "🔄 Retake Challenge"
        },
        "zh": {
            "title": "🎯 交互式 VLSI Tcl 随堂评测挑战与认证",
            "badges": ["三阶能力递进", "盲测静默评分", "深度思考计时", "工业级防伪证书", "全网排行榜"],
            "desc": "工业级芯片自动化随堂测评系统。题目分为初阶、中阶、高阶三层难度阶梯（Easy → Medium → Hard）。提供充裕的单题思考保护时间，并配置同难度强化题以确保知识点闭环，唯有完全掌握方可通关评级。",
            "mode_select": "选择挑战模式与考生代号",
            "full_mode": "全体系大奖赛 (覆盖 4 大核心模块 · 共 12 阶)",
            "sprint_mode": "疾速冲刺自测 (6 道核心基准诊断题)",
            "candidate_placeholder": "请输入您的姓名或代号 (例如: 张工_EDA_Signoff)...",
            "start_btn": "🚀 开启随堂评测挑战",
            "mod_label": "当前评估模块",
            "tier_label": "题目难度阶梯",
            "timer_label": "思考倒计时",
            "submit_btn": "确认提交选项 (Enter)",
            "thinking_bonus": "已追加思考保护时间",
            "report_title": "📊 赛后深度诊断分析报告",
            "cert_title": "🎓 领取工业级芯片自动化掌握证书",
            "dl_cert": "📥 下载防伪认证证书 (SVG)",
            "print_cert": "🖨️ 打印 / 导出 PDF",
            "view_leaderboard": "🏆 前往全网荣誉排行榜查看名次 →",
            "retake": "🔄 重新挑战"
        },
        "ms": {
            "title": "🎯 Cabaran Kuiz VLSI Tcl & Pensijilan",
            "badges": ["Kemajuan 3-Tahap", "Penggredan Senyap", "Pemasa Berfikir", "Sijil Sah Digital", "Papan Pendahulu"],
            "desc": "Sistem diagnostik gred industri. Soalan berkembang merentasi 3 tahap kesukaran (Mudah → Sederhana → Sukar). Had masa menyokong langkah pembelajaran anda—memberikan peruntukan masa berfikir apabila diperlukan, sambil memerlukan soalan peneguhan untuk memastikan penguasaan sebelum melepasi sesuatu tahap.",
            "mode_select": "Pilih Mod Cabaran & Nama Calon",
            "full_mode": "Grand Prix Penuh (Semua 4 Modul · 12 Tahap)",
            "sprint_mode": "Diagnostik Pecut (6 Soalan Penanda Aras Teras)",
            "candidate_placeholder": "Masukkan nama atau alias anda (cth: Jurutera_VLSI)...",
            "start_btn": "🚀 Lancarkan Cabaran Kuiz",
            "mod_label": "Modul Semasa",
            "tier_label": "Tahap Kesukaran",
            "timer_label": "Pemasa Berfikir",
            "submit_btn": "Hantar Jawapan (Enter)",
            "thinking_bonus": "Masa Berfikir Tambahan Diberikan",
            "report_title": "📊 Laporan Analisis Penguasaan Pasca-Cabaran",
            "cert_title": "🎓 Tuntut Sijil Penguasaan Industri Anda",
            "dl_cert": "📥 Muat Turun Sijil (SVG)",
            "print_cert": "🖨️ Cetak Sijil",
            "view_leaderboard": "🏆 Lihat Kedudukan di Papan Pendahulu →",
            "retake": "🔄 Ulang Semula Cabaran"
        },
        "fr": {
            "title": "🎯 Défi Quiz VLSI Tcl & Certification",
            "badges": ["Progression 3 Niveaux", "Notation Silencieuse", "Minuteur de Réflexion", "Certificat Vérifiable", "Classement Public"],
            "desc": "Système de diagnostic de niveau industriel. Les questions progressent sur 3 niveaux de difficulté (Facile → Moyen → Difficile). Le temps alloué s'adapte à votre démarche : du temps de réflexion supplémentaire est accordé lorsque nécessaire, avec des questions de renforcement pour consolider la maîtrise avant de passer au niveau supérieur.",
            "mode_select": "Choisissez le Mode & Nom du Candidat",
            "full_mode": "Grand Prix Complet (4 Modules · 12 Niveaux)",
            "sprint_mode": "Sprint Diagnostic (6 Questions Clés d'Évaluation)",
            "candidate_placeholder": "Entrez votre nom ou pseudonyme (ex: Ingénieur_VLSI)...",
            "start_btn": "🚀 Lancer le Défi Quiz",
            "mod_label": "Module en Cours",
            "tier_label": "Niveau de Difficulté",
            "timer_label": "Minuteur de Réflexion",
            "submit_btn": "Valider la Réponse (Entrée)",
            "thinking_bonus": "Temps de Réflexion Supplémentaire Accordé",
            "report_title": "📊 Rapport Analytique de Maîtrise",
            "cert_title": "🎓 Obtenez Votre Certificat de Maîtrise Industrielle",
            "dl_cert": "📥 Télécharger le Certificat (SVG)",
            "print_cert": "🖨️ Imprimer le Certificat",
            "view_leaderboard": "🏆 Voir Votre Rang au Classement Public →",
            "retake": "🔄 Recommencer le Défi"
        }
    }
    t = i18n_strings.get(lang, i18n_strings["en"])
    badges_html = "\n".join([f'  <span class="tcl-badge blue">{b}</span>' if i % 2 == 0 else f'  <span class="tcl-badge purple">{b}</span>' for i, b in enumerate(t["badges"])])

    html_shell = f"""# {t["title"]}

<div class="tcl-badge-cluster">
{badges_html}
</div>

{t["desc"]}

---

<div id="quiz-app-container" style="background: var(--tcl-surface); border: 1px solid var(--tcl-border); border-radius: 12px; padding: 24px; margin: 24px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
  
  <!-- Step 1: Start Screen -->
  <div id="quiz-start-screen">
    <h3 style="margin-top:0; font-size:1.15rem; color:var(--tcl-heading);">⚙️ {t["mode_select"]}</h3>
    
    <div style="margin: 16px 0;">
      <label style="display:block; font-size:13px; font-weight:700; margin-bottom:8px; color:var(--tcl-heading);">Candidate Name / Callsign:</label>
      <input type="text" id="candidateNameInput" placeholder="{t["candidate_placeholder"]}" style="width:100%; max-width:420px; padding:10px 14px; font-size:14px; border:1px solid var(--tcl-border); border-radius:8px; background:var(--md-default-bg-color); color:var(--tcl-heading); outline:none; box-sizing:border-box;">
    </div>

    <div style="margin: 18px 0;">
      <label style="display:block; font-size:13px; font-weight:700; margin-bottom:8px; color:var(--tcl-heading);">Quest Mode:</label>
      <div style="display:flex; gap:12px; flex-wrap:wrap;">
        <label style="display:flex; align-items:center; gap:8px; background:var(--tcl-surface-card); border:1px solid var(--tcl-border); padding:10px 16px; border-radius:8px; cursor:pointer;">
          <input type="radio" name="questMode" value="full" checked style="cursor:pointer;">
          <span style="font-size:13.5px; font-weight:600; color:var(--tcl-heading);">{t["full_mode"]}</span>
        </label>
        <label style="display:flex; align-items:center; gap:8px; background:var(--tcl-surface-card); border:1px solid var(--tcl-border); padding:10px 16px; border-radius:8px; cursor:pointer;">
          <input type="radio" name="questMode" value="sprint" style="cursor:pointer;">
          <span style="font-size:13.5px; font-weight:600; color:var(--tcl-heading);">{t["sprint_mode"]}</span>
        </label>
      </div>
    </div>

    <div style="margin-top: 24px;">
      <button onclick="startChallenge()" class="tcl-btn tcl-btn-primary" style="padding:10px 24px; font-size:14px;">{t["start_btn"]}</button>
    </div>
  </div>

  <!-- Step 2: Active Challenge Screen -->
  <div id="quiz-active-screen" style="display:none;">
    
    <!-- Header HUD -->
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding-bottom:14px; border-bottom:1px solid var(--tcl-border); margin-bottom:18px;">
      <div>
        <div style="font-size:11px; text-transform:uppercase; letter-spacing:1px; font-weight:700; color:var(--tcl-blue-600); margin-bottom:2px;" id="hudModuleCategory">MODULE 1 / 4</div>
        <div style="font-size:15px; font-weight:800; color:var(--tcl-heading);" id="hudModuleName">Syntax & Brent Welch Model</div>
      </div>
      
      <div style="display:flex; gap:10px; align-items:center;">
        <span id="hudDifficultyBadge" style="display:inline-block; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:700; background:rgba(16, 185, 129, 0.15); color:#10b981;">🟢 Tier 0 (Easy)</span>
        <span id="hudTierClearMeter" style="font-size:12.5px; font-weight:600; font-family:monospace; color:var(--md-default-fg-color--lighter);">[Easy: ⏳] [Med: 🔒] [Hard: 🔒]</span>
      </div>
    </div>

    <!-- Timer HUD with Dynamic Thinking Time -->
    <div style="background:var(--md-default-bg-color); border:1px solid var(--tcl-border); border-radius:8px; padding:12px 16px; margin-bottom:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; font-size:12px; font-weight:700;">
        <span style="color:var(--tcl-heading);">⏱️ {t["timer_label"]}: <span id="timerSecondsText" style="color:var(--tcl-blue-600); font-size:14px;">30s</span></span>
        <span id="thinkingAllowanceTag" style="color:#d97706; font-size:11.5px; display:none;">⚠️ {t["thinking_bonus"]}: +15s</span>
      </div>
      <div style="width:100%; height:8px; background:rgba(0,0,0,0.08); border-radius:4px; overflow:hidden;">
        <div id="timerBar" style="width:100%; height:100%; background:#10b981; transition:width 0.2s linear, background-color 0.3s ease;"></div>
      </div>
    </div>

    <!-- Question Box -->
    <div style="margin-bottom: 20px;">
      <div id="questionPrompt" style="font-size:1.05rem; font-weight:700; color:var(--tcl-heading); margin-bottom:12px; line-height:1.5;"></div>
      
      <div id="questionCodeContainer" style="display:none; margin-bottom:16px;">
        <pre style="background:var(--tcl-code-bg); color:#f8fafc; border-radius:8px; padding:12px 16px; font-family:'JetBrains Mono', monospace; font-size:13px; overflow-x:auto; border:1px solid rgba(255,255,255,0.1);"><code id="questionCodeBlock"></code></pre>
      </div>

      <div id="choicesGrid" style="display:grid; grid-template-columns:1fr; gap:10px;"></div>
    </div>

    <!-- Feedback Toast -->
    <div id="feedbackToast" style="display:none; padding:12px 16px; border-radius:8px; margin-bottom:16px; font-size:13px; font-weight:600;"></div>

    <!-- Action Bar -->
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding-top:14px; border-top:1px solid var(--tcl-border);">
      <div style="font-size:12.5px; color:var(--md-default-fg-color--lighter);">
        💡 Press keys <kbd style="background:var(--tcl-surface); border:1px solid var(--tcl-border); padding:2px 6px; border-radius:4px; font-size:11px;">1</kbd>–<kbd style="background:var(--tcl-surface); border:1px solid var(--tcl-border); padding:2px 6px; border-radius:4px; font-size:11px;">4</kbd> or click to choose
      </div>
      <button onclick="submitCurrentAnswer()" id="btnSubmitAnswer" class="tcl-btn tcl-btn-primary" style="padding:9px 22px; font-size:13.5px;" disabled>{t["submit_btn"]}</button>
    </div>

  </div>

  <!-- Step 3: Analytical Report & Certificate Screen -->
  <div id="quiz-report-screen" style="display:none;">
    
    <div style="text-align:center; margin-bottom:28px;">
      <div style="display:inline-block; font-size:3rem; margin-bottom:8px;">🏆</div>
      <h2 style="font-size:1.6rem; font-weight:800; color:var(--tcl-heading); margin:4px 0 8px;">{t["report_title"]}</h2>
      <div style="color:var(--md-default-fg-color--light); font-size:14px;">Official competency diagnostic completed under 3-tier rules.</div>
    </div>

    <!-- Summary Metrics Cards -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px, 1fr)); gap:14px; margin-bottom:28px;">
      <div style="background:var(--md-default-bg-color); border:1px solid var(--tcl-border); border-radius:10px; padding:16px; text-align:center;">
        <div style="font-size:1.6rem; font-weight:800; color:var(--tcl-blue-600);" id="reportScoreVal">0</div>
        <div style="font-size:11.5px; text-transform:uppercase; letter-spacing:0.5px; font-weight:700; color:var(--md-default-fg-color--lighter); margin-top:4px;">Total Score</div>
      </div>
      <div style="background:var(--md-default-bg-color); border:1px solid var(--tcl-border); border-radius:10px; padding:16px; text-align:center;">
        <div style="font-size:1.6rem; font-weight:800; color:#10b981;" id="reportAccuracyVal">0%</div>
        <div style="font-size:11.5px; text-transform:uppercase; letter-spacing:0.5px; font-weight:700; color:var(--md-default-fg-color--lighter); margin-top:4px;">Accuracy</div>
      </div>
      <div style="background:var(--md-default-bg-color); border:1px solid var(--tcl-border); border-radius:10px; padding:16px; text-align:center;">
        <div style="font-size:1.6rem; font-weight:800; color:#8b5cf6;" id="reportTimeVal">0m 0s</div>
        <div style="font-size:11.5px; text-transform:uppercase; letter-spacing:0.5px; font-weight:700; color:var(--md-default-fg-color--lighter); margin-top:4px;">Elapsed Time</div>
      </div>
      <div style="background:var(--md-default-bg-color); border:1px solid var(--tcl-border); border-radius:10px; padding:16px; text-align:center;">
        <div style="font-size:1.6rem; font-weight:800; color:#f59e0b;" id="reportClearedVal">0/12</div>
        <div style="font-size:11.5px; text-transform:uppercase; letter-spacing:0.5px; font-weight:700; color:var(--md-default-fg-color--lighter); margin-top:4px;">Tiers Cleared</div>
      </div>
    </div>

    <!-- Module Mastery Breakdown -->
    <div style="background:var(--md-default-bg-color); border:1px solid var(--tcl-border); border-radius:10px; padding:20px; margin-bottom:28px;">
      <h3 style="margin-top:0; font-size:1.1rem; color:var(--tcl-heading); margin-bottom:16px;">Core Module Mastery Radar</h3>
      <div id="moduleCompetencyBars" style="display:flex; flex-direction:column; gap:12px;"></div>
    </div>

    <!-- Certificate Section -->
    <div style="border-top:1px dashed var(--tcl-border); padding-top:28px;">
      <h3 style="text-align:center; font-size:1.25rem; font-weight:800; color:var(--tcl-heading); margin-bottom:16px;">{t["cert_title"]}</h3>

      <div id="certificateContainer" style="background:#ffffff; color:#0f172a; border:4px double #d4af37; border-radius:12px; padding:28px; max-width:680px; margin:0 auto 20px; box-shadow:0 8px 30px rgba(0,0,0,0.12); position:relative; font-family:'Inter', sans-serif; text-align:center;">
        <div style="font-size:11px; text-transform:uppercase; letter-spacing:2px; color:#b45309; font-weight:800; margin-bottom:6px;">SJTU-YONGFU-RESEARCH-GRP · VLSI AUTOMATION LAB</div>
        <h2 style="font-size:1.5rem; font-weight:900; margin:6px 0; color:#1e293b; letter-spacing:0.5px;">CERTIFICATE OF INDUSTRIAL MASTERY</h2>
        <div style="font-size:12.5px; color:#64748b; margin-bottom:16px;">IN RECOGNITION OF OUTSTANDING DEMONSTRATED PROFICIENCY IN TCL SCRIPTING FOR VLSI DESIGN</div>
        
        <div style="font-size:13px; color:#475569;">This official certificate is proudly presented to:</div>
        <div id="certStudentName" style="font-size:1.85rem; font-weight:800; color:#0f172a; margin:10px 0; border-bottom:2px solid #e2e8f0; display:inline-block; padding:0 30px 4px;">Candidate Name</div>
        
        <div style="font-size:12.5px; color:#475569; max-width:520px; margin:10px auto; line-height:1.6;">
          Has successfully passed all 3 tiers of the VLSI Tcl Challenge, demonstrating full mastery across the Brent Welch 3-step evaluation model, advanced data structures, DRV-Lite physical layout objects, and STA timing sign-off gatekeeping.
        </div>

        <div style="display:flex; justify-content:space-around; align-items:center; margin-top:20px; padding-top:16px; border-top:1px solid #f1f5f9; font-size:12px; color:#475569;">
          <div>
            <div style="font-weight:700; color:#0f172a;" id="certDateVal">Date</div>
            <div style="font-size:10.5px; color:#94a3b8;">Issue Date</div>
          </div>
          <div>
            <div style="display:inline-block; width:44px; height:44px; line-height:44px; border-radius:50%; background:#fef3c7; color:#b45309; font-size:22px; font-weight:900;">★</div>
            <div style="font-size:10.5px; font-weight:700; color:#b45309; margin-top:2px;">GOLD VERIFIED</div>
          </div>
          <div>
            <div style="font-weight:700; color:#0f172a; font-family:monospace;" id="certHashVal">TCL-VLSI-XXXX</div>
            <div style="font-size:10.5px; color:#94a3b8;">Credential Hash</div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap; margin-top:16px;">
        <button onclick="downloadCertificateSVG()" class="tcl-btn tcl-btn-primary" style="padding:9px 20px; font-size:13.5px;">{t["dl_cert"]}</button>
        <button onclick="window.print()" class="tcl-btn tcl-btn-secondary" style="padding:9px 18px; font-size:13.5px;">{t["print_cert"]}</button>
        <a href="leaderboard.md" class="tcl-btn tcl-btn-accent" style="padding:9px 18px; font-size:13.5px; text-decoration:none;">{t["view_leaderboard"]}</a>
        <button onclick="restartChallenge()" class="tcl-btn tcl-btn-secondary" style="padding:9px 16px; font-size:13.5px;">{t["retake"]}</button>
      </div>
    </div>

  </div>

</div>
"""
    return html_shell + "\n\n" + QUIZ_JS


def _build_leaderboard_page(lang: str) -> str:
    i18n_strings = {
        "en": {
            "title": "🏆 Public Leaderboard & Certified Hall of Fame",
            "badges": ["Live Cohort Rankings", "Verified Certificates", "E/M/H Difficulty Metrics"],
            "desc": "Real-time ranking table of certified engineers and students who cleared the VLSI Tcl Quiz Challenge. Sorted by total weighted score, accuracy, and elapsed time.",
            "search_ph": "Search candidate name or callsign...",
            "all_mode": "All Modes",
            "full_mode": "Full Grand Prix",
            "sprint_mode": "Sprint Diagnostic",
            "col_rank": "Rank",
            "col_name": "Candidate / Handle",
            "col_mode": "Quest Mode",
            "col_score": "Score",
            "col_acc": "Accuracy",
            "col_time": "Time",
            "col_emh": "Cleared (E/M/H)",
            "col_date": "Date",
            "verify_title": "🔍 Instant Certificate Verification",
            "verify_ph": "Enter Certificate Hash (e.g. TCL-VLSI-2026-X89F)...",
            "verify_btn": "Verify Credential",
            "take_quiz_btn": "🎯 Take the Quiz Challenge →"
        },
        "zh": {
            "title": "🏆 荣誉排行榜与认证证书中心",
            "badges": ["全网实时排名", "工业认证核验", "易/中/难三阶通关指标"],
            "desc": "汇聚通过 VLSI Tcl 随堂评测挑战的工程师与学生成绩榜单。按加权总分、答题正确率与耗时进行综合排位，记录通过初阶/中阶/高阶题目分布。",
            "search_ph": "搜索考生姓名或代号...",
            "all_mode": "全部模式",
            "full_mode": "全体系大奖赛",
            "sprint_mode": "疾速冲刺自测",
            "col_rank": "名次",
            "col_name": "考生姓名 / 代号",
            "col_mode": "挑战模式",
            "col_score": "加权得分",
            "col_acc": "正确率",
            "col_time": "耗时",
            "col_emh": "通关阶梯 (易/中/难)",
            "col_date": "完成日期",
            "verify_title": "🔍 认证证书真伪即时核验",
            "verify_ph": "输入证书凭证编号 (例如: TCL-VLSI-2026-X89F)...",
            "verify_btn": "立即核验凭证",
            "take_quiz_btn": "🎯 参与随堂评测挑战 →"
        },
        "ms": {
            "title": "🏆 Papan Pendahulu Awam & Dewan Kemasyhuran",
            "badges": ["Kedudukan Kohort Langsung", "Sijil Sah Digital", "Metrik Kesukaran E/M/H"],
            "desc": "Jadual kedudukan masa nyata jurutera dan pelajar yang berjaya melepasi Cabaran Kuiz VLSI Tcl. Disusun mengikut skor wajaran, ketepatan, dan masa diambil.",
            "search_ph": "Cari nama calon atau alias...",
            "all_mode": "Semua Mod",
            "full_mode": "Grand Prix Penuh",
            "sprint_mode": "Diagnostik Pecut",
            "col_rank": "Kedudukan",
            "col_name": "Calon / Alias",
            "col_mode": "Mod Cabaran",
            "col_score": "Skor",
            "col_acc": "Ketepatan",
            "col_time": "Masa",
            "col_emh": "Pelepasan (E/M/H)",
            "col_date": "Tarikh",
            "verify_title": "🔍 Pengesahan Sijil Segera",
            "verify_ph": "Masukkan Kod Sijil (cth: TCL-VLSI-2026-X89F)...",
            "verify_btn": "Sahkan Sijil",
            "take_quiz_btn": "🎯 Ambil Cabaran Kuiz →"
        },
        "fr": {
            "title": "🏆 Tableau des Scores Public & Salle des Notabilités",
            "badges": ["Classement en Direct", "Certificats Vérifiés", "Mesures de Difficulté E/M/H"],
            "desc": "Classement en temps réel des ingénieurs et étudiants ayant validé le Défi Quiz VLSI Tcl. Trié par score pondéré, précision et temps écoulé.",
            "search_ph": "Rechercher un candidat ou pseudo...",
            "all_mode": "Tous les Modes",
            "full_mode": "Grand Prix Complet",
            "sprint_mode": "Sprint Diagnostic",
            "col_rank": "Rang",
            "col_name": "Candidat / Pseudo",
            "col_mode": "Mode de Quête",
            "col_score": "Score",
            "col_acc": "Précision",
            "col_time": "Temps",
            "col_emh": "Niveaux Validés (E/M/H)",
            "col_date": "Date",
            "verify_title": "🔍 Vérification Instantanée de Certificat",
            "verify_ph": "Entrez le Hash du Certificat (ex: TCL-VLSI-2026-X89F)...",
            "verify_btn": "Vérifier le Certificat",
            "take_quiz_btn": "🎯 Participer au Défi Quiz →"
        }
    }
    t = i18n_strings.get(lang, i18n_strings["en"])
    badges_html = "\n".join([f'  <span class="tcl-badge blue">{b}</span>' if i % 2 == 0 else f'  <span class="tcl-badge purple">{b}</span>' for i, b in enumerate(t["badges"])])

    html_shell = f"""# {t["title"]}

<div class="tcl-badge-cluster">
{badges_html}
</div>

{t["desc"]}

<div style="margin: 20px 0;">
  <a href="quiz.md" class="tcl-btn tcl-btn-primary" style="padding:9px 20px; font-size:14px; text-decoration:none;">{t["take_quiz_btn"]}</a>
</div>

---

<div class="leaderboard-container" style="background: var(--tcl-surface); border: 1px solid var(--tcl-border); border-radius: 12px; padding: 24px; margin: 24px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
  
  <!-- Search & Filter Controls -->
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px; margin-bottom:20px;">
    <input type="text" id="boardSearchInput" oninput="filterLeaderboard()" placeholder="{t["search_ph"]}" style="padding:8px 14px; border:1px solid var(--tcl-border); border-radius:8px; background:var(--md-default-bg-color); color:var(--tcl-heading); font-size:13.5px; width:100%; max-width:320px; outline:none;">
    
    <div style="display:flex; gap:8px; align-items:center;">
      <button onclick="setBoardMode('all')" class="tcl-btn tcl-btn-secondary board-mode-btn" id="btnModeAll" style="padding:6px 14px; font-size:12.5px; background:var(--tcl-blue-600); color:#ffffff;">{t["all_mode"]}</button>
      <button onclick="setBoardMode('full')" class="tcl-btn tcl-btn-secondary board-mode-btn" id="btnModeFull" style="padding:6px 14px; font-size:12.5px;">{t["full_mode"]}</button>
      <button onclick="setBoardMode('sprint')" class="tcl-btn tcl-btn-secondary board-mode-btn" id="btnModeSprint" style="padding:6px 14px; font-size:12.5px;">{t["sprint_mode"]}</button>
    </div>
  </div>

  <!-- Table -->
  <div style="overflow-x:auto;">
    <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left;">
      <thead>
        <tr style="border-bottom: 2px solid var(--tcl-border); background: var(--tcl-surface-card);">
          <th style="padding:10px 14px; font-weight:700; width:60px;">{t["col_rank"]}</th>
          <th style="padding:10px 14px; font-weight:700;">{t["col_name"]}</th>
          <th style="padding:10px 14px; font-weight:700;">{t["col_mode"]}</th>
          <th style="padding:10px 14px; font-weight:700; text-align:right;">{t["col_score"]}</th>
          <th style="padding:10px 14px; font-weight:700; text-align:right;">{t["col_acc"]}</th>
          <th style="padding:10px 14px; font-weight:700; text-align:right;">{t["col_time"]}</th>
          <th style="padding:10px 14px; font-weight:700; text-align:center;">{t["col_emh"]}</th>
          <th style="padding:10px 14px; font-weight:700; text-align:right;">{t["col_date"]}</th>
        </tr>
      </thead>
      <tbody id="leaderboardTbody">
        <!-- Dynamically rendered via JS -->
      </tbody>
    </table>
  </div>

</div>

<!-- Hash Verification Tool -->
<div style="background:var(--tcl-surface); border:1px solid var(--tcl-border); border-radius:12px; padding:20px; margin-top:24px;">
  <h3 style="margin-top:0; font-size:1.15rem; color:var(--tcl-heading);">{t["verify_title"]}</h3>
  <div style="display:flex; gap:10px; flex-wrap:wrap; max-width:580px;">
    <input type="text" id="verifyHashInput" placeholder="{t["verify_ph"]}" style="flex:1; min-width:260px; padding:8px 14px; border:1px solid var(--tcl-border); border-radius:8px; background:var(--md-default-bg-color); color:var(--tcl-heading); outline:none; font-family:monospace; font-size:13px;">
    <button onclick="verifyCertificateHash()" class="tcl-btn tcl-btn-primary" style="padding:8px 18px; font-size:13px;">{t["verify_btn"]}</button>
  </div>
  <div id="verifyResultBox" style="margin-top:14px; display:none; padding:12px 16px; border-radius:8px; font-size:13px;"></div>
</div>
"""
    return html_shell + "\n\n" + LEADERBOARD_JS


QUIZ_JS = r"""<script>
const QUESTION_BANK = {
  m10: {
    name: "M10: Syntax & Brent Welch Model",
    easy: [
      {
        id: "m10_e1",
        prompt: "Under the Brent Welch 3-step evaluation model, in which exact order does the Tcl interpreter evaluate every command line?",
        code: null,
        choices: [
          "Grouping -> Substitution -> Invocation",
          "Substitution -> Compilation -> Grouping",
          "Parsing -> Linking -> Execution",
          "Invocation -> Expansion -> Substitution"
        ],
        answer: 0
      },
      {
        id: "m10_e2",
        prompt: "Which delimiters disable all variable and command substitutions, treating the enclosed content strictly as literal characters?",
        code: "set x 100\nputs {The value is $x}",
        choices: [
          "Double quotes: \"...\"",
          "Curly braces: { ... }",
          "Square brackets: [ ... ]",
          "Parentheses: ( ... )"
        ],
        answer: 1
      },
      {
        id: "m10_e3",
        prompt: "In Tcl syntax, where is a comment starting with '#' validly recognized?",
        code: "set a 10 ;# comment here\n# whole line comment",
        choices: [
          "Only at the beginning of a command line, or preceded by a semicolon ';'",
          "Anywhere on the line, even inside command arguments",
          "Only after double slashes '//'",
          "Inside double quotes without backslashes"
        ],
        answer: 0
      }
    ],
    medium: [
      {
        id: "m10_m1",
        prompt: "Why should expressions in 'expr' always be enclosed in curly braces like 'expr {$a + $b}'?",
        code: "set sum [expr {$a + $b}]\nset bad [expr $a + $b]",
        choices: [
          "To enable bytecode compilation and prevent double-substitution code injection",
          "Curly braces are strictly required by syntax; unbraced expr causes an immediate parser crash",
          "To force floating point division instead of integer arithmetic",
          "To disable mathematical operators from running"
        ],
        answer: 0
      },
      {
        id: "m10_m2",
        prompt: "What is the return value of evaluating the following nested command?",
        code: "set cell \"INV_X1\"\nexpr {[string length $cell] * 2}",
        choices: ["12", "6", "14", "INV_X1INV_X1"],
        answer: 0
      },
      {
        id: "m10_m3",
        prompt: "How do you escape a dollar sign in double quotes so it is printed literally?",
        code: "puts \"Price: \\$100\"",
        choices: [
          "Prefix it with a backslash: \\$",
          "Double the dollar sign: $$",
          "Surround it in single quotes: '$'",
          "Use triple double-quotes: \"\"\"$\"\"\""
        ],
        answer: 0
      }
    ],
    hard: [
      {
        id: "m10_h1",
        prompt: "In a procedure, how do you access a variable defined in the global namespace?",
        code: "set tech \"TSMC28\"\nproc print_tech {} {\n    global tech\n    puts $tech\n}",
        choices: [
          "Use 'global tech' or refer to '::tech'",
          "Variables in global scope are always automatically inherited by all procs",
          "Use 'extern tech' like in C",
          "Use 'import ::tech'"
        ],
        answer: 0
      },
      {
        id: "m10_h2",
        prompt: "What is the output of: subst -nobackslashes {Count: [expr {2 * 3}] \\n}?",
        code: "subst -nobackslashes {Count: [expr {2 * 3}] \\n}",
        choices: [
          "Count: 6 \\n (command evaluated, backslash preserved literally)",
          "Count: 6 on a new line (newline interpreted)",
          "Count: [expr {2 * 3}] \\n",
          "Syntax error: -nobackslashes is invalid"
        ],
        answer: 0
      }
    ]
  },
  m20: {
    name: "M20: Data Structures, Regex & TclOO",
    easy: [
      {
        id: "m20_e1",
        prompt: "Which command extracts the second item from list 'layers' (0-indexed)?",
        code: "set layers [list M1 M2 M3 M4 VIA1]",
        choices: [
          "[lindex $layers 1]",
          "[lindex $layers 2]",
          "$layers(1)",
          "[list_get $layers 1]"
        ],
        answer: 0
      },
      {
        id: "m20_e2",
        prompt: "Which command appends 'VIA2' to the existing list variable 'layers'?",
        code: "set layers [list M1 M2 M3]",
        choices: [
          "lappend layers VIA2",
          "append layers VIA2",
          "set layers [concat $layers VIA2]",
          "list_push layers VIA2"
        ],
        answer: 0
      }
    ],
    medium: [
      {
        id: "m20_m1",
        prompt: "Which statement correctly describes a Tcl 'dict' introduced in Tcl 8.5?",
        code: "set cell [dict create name \"NAND2\" area 2.4]",
        choices: [
          "Dicts are first-class pass-by-value objects that can be nested and passed into procs",
          "Dicts can only store string keys with integer values",
          "Dicts require global namespace declaration to be accessed",
          "Dicts are identical to legacy associative arrays"
        ],
        answer: 0
      },
      {
        id: "m20_m2",
        prompt: "How do you extract all word tokens starting with 'pin_' using 'regexp'?",
        code: "set line \"CONNECT pin_clk pin_rstn u_core\"\nset pins [regexp -all -inline {\\mpin_\\w+\\M} $line]",
        choices: [
          "regexp -all -inline {\\mpin_\\w+\\M} $line",
          "regexp {pin_.*} $line",
          "string match {pin_*} $line",
          "regsub -all {pin_} $line"
        ],
        answer: 0
      }
    ],
    hard: [
      {
        id: "m20_h1",
        prompt: "In TclOO, which command instantiates a new object 'c1' from class 'StandardCell'?",
        code: "oo::class create StandardCell {\n    constructor {name area} { ... }\n}",
        choices: [
          "StandardCell create c1 \"INV_X1\" 1.2",
          "new StandardCell c1 \"INV_X1\" 1.2",
          "set c1 [StandardCell->new \"INV_X1\" 1.2]",
          "StandardCell.instantiate c1 \"INV_X1\" 1.2"
        ],
        answer: 0
      },
      {
        id: "m20_h2",
        prompt: "What does 'fconfigure $fp -buffering line -blocking 0' configure on an open channel?",
        code: "fconfigure $fp -buffering line -blocking 0",
        choices: [
          "Line-buffered non-blocking I/O (reads return immediately without hanging)",
          "Disables file read permissions",
          "Sets binary transfer mode with 1MB blocks",
          "Forces synchronous write locks on the file"
        ],
        answer: 0
      }
    ]
  },
  m30: {
    name: "M30: Physical Design & DRV-Lite",
    easy: [
      {
        id: "m30_e1",
        prompt: "What unit system is standardly used by GDS II and Calibre layout databases?",
        code: "Database Units (DBU)",
        choices: [
          "Database Units (DBU), typically 1000 or 2000 per micron",
          "Raw floating point millimeters",
          "Picoseconds per grid unit",
          "Screen pixel coordinates"
        ],
        answer: 0
      },
      {
        id: "m30_e2",
        prompt: "In DRV-Lite, which method creates a new top layout cell container?",
        code: "set L [layout create]\n$L create cell TOP",
        choices: [
          "$L create cell TOP",
          "$L add_cell TOP",
          "cell TOP create",
          "layout_new_cell TOP"
        ],
        answer: 0
      }
    ],
    medium: [
      {
        id: "m30_m1",
        prompt: "Given cell bounding box [0 0 1400 2800] at 1000 DBU/um, what is the cell area?",
        code: "# Width: 1.4 um, Height: 2.8 um\nset area [expr {1.4 * 2.8}]",
        choices: [
          "3.92 um²",
          "4.20 um²",
          "2.80 um²",
          "3920 um²"
        ],
        answer: 0
      },
      {
        id: "m30_m2",
        prompt: "In DRV-Lite, which command draws a rectangle on Metal 1 (layer 1) from (0,0) to (400,200)?",
        code: "$L create box TOP 1 0 0 400 200",
        choices: [
          "$L create box TOP 1 0 0 400 200",
          "$L draw_rect TOP 1 0 400 200",
          "$L polygon TOP 1 400 200",
          "create_shape box -layer 1 0 0 400 200"
        ],
        answer: 0
      }
    ],
    hard: [
      {
        id: "m30_h1",
        prompt: "When placing a subcell instance with transform 'MY' (Mirror Y) followed by 'R90', what happens to coordinate (x, y)?",
        code: "Transform: MY then R90",
        choices: [
          "Reflected across Y-axis (-x, y), then rotated 90° CCW -> (-y, -x)",
          "Shifted 90 DBU to the right",
          "Coordinates remain unchanged",
          "Scales the cell width by 90%"
        ],
        answer: 0
      },
      {
        id: "m30_h2",
        prompt: "Which GDS II binary record defines the start of a cell structure boundary?",
        code: "GDS II Streamout Records",
        choices: [
          "BGNSTR (Begin Structure)",
          "BGNLIB (Begin Library)",
          "BOUNDARY (Start Polygon)",
          "ENDSTR (End Structure)"
        ],
        answer: 0
      }
    ]
  },
  m40: {
    name: "M40: STA Timing, Sign-Off & Verification",
    easy: [
      {
        id: "m40_e1",
        prompt: "What is the standard definition of Static Timing Analysis (STA) Setup Slack?",
        code: "Slack = Required Arrival Time - Actual Arrival Time",
        choices: [
          "Slack = Required Time - Arrival Time",
          "Slack = Arrival Time - Required Time",
          "Slack = Clock Period * Data Delay",
          "Slack = Clock Skew + Jitter"
        ],
        answer: 0
      },
      {
        id: "m40_e2",
        prompt: "A timing path has Required Time = 1.15 ns and Arrival Time = 1.05 ns. What is the Slack?",
        code: "Required: 1.15 ns, Arrival: 1.05 ns",
        choices: [
          "+0.100 ns (MET / Pass)",
          "-0.100 ns (VIOLATION / Fail)",
          "+2.200 ns",
          "0.000 ns"
        ],
        answer: 0
      }
    ],
    medium: [
      {
        id: "m40_m1",
        prompt: "Given T_clk = 1000 ps, T_unc = 40 ps, T_setup = 50 ps, T_clk_q = 90 ps, T_data = 720 ps. Compute Setup Slack:",
        code: "Required = 1000 - 40 - 50 = 910 ps\nArrival = 90 + 720 = 810 ps\nSlack = 910 - 810",
        choices: [
          "+100 ps (+0.100 ns)",
          "-100 ps (-0.100 ns)",
          "+190 ps (+0.190 ns)",
          "+90 ps (+0.090 ns)"
        ],
        answer: 0
      },
      {
        id: "m40_m2",
        prompt: "What is Total Negative Slack (TNS) in digital IC timing closure?",
        code: "TNS = sum(min(0, Slack_i))",
        choices: [
          "The sum of all negative slacks across all violating endpoints",
          "The total number of clock cycles",
          "The difference between longest and shortest path",
          "The total hold time margin"
        ],
        answer: 0
      }
    ],
    hard: [
      {
        id: "m40_h1",
        prompt: "A tapeout sign-off rule requires WNS >= 0.000 ns. Path 1 has Slack = -0.015 ns, while 99 paths pass. Can the chip tape out?",
        code: "Sign-Off Rule: WNS >= 0.000 ns\nCurrent WNS: -0.015 ns",
        choices: [
          "NO: Sign-off gatekeeper blocked; all paths must have non-negative slack",
          "YES: 99% pass rate is sufficient for silicon tapeout",
          "YES: Negative slack below 20 ps is ignored by foundries",
          "NO: Only if TNS is less than -1.0 ns"
        ],
        answer: 0
      },
      {
        id: "m40_h2",
        prompt: "How does 'Useful Skew' scheduling fix a setup violation on path A -> B without violating hold timing?",
        code: "Useful Skew: Adjust clock arrival at capturing register B",
        choices: [
          "Deliberately delays clock arrival at register B, borrowing time from subsequent cycle",
          "Increases power rail voltage across all flip-flops",
          "Eliminates clock tree synthesis entirely",
          "Reverses the direction of signal propagation"
        ],
        answer: 0
      }
    ]
  }
};

let currentQuest = {
  candidate: "Anonymous",
  mode: "full",
  modules: ["m10", "m20", "m30", "m40"],
  modIdx: 0,
  diffTiers: ["easy", "medium", "hard"],
  tierIdx: 0,
  mistakesAtTier: 0,
  tierCleared: {},
  usedQuestions: {},
  totalAttempts: 0,
  correctAttempts: 0,
  score: 0,
  startTime: null,
  timerInterval: null,
  timeLeft: 0,
  maxTime: 30,
  currentQuestion: null,
  selectedChoice: null
};

const BASE_LIMITS = {
  easy: 30,
  medium: 45,
  hard: 60
};

function startChallenge() {
  const nameInput = document.getElementById('candidateNameInput').value.trim();
  currentQuest.candidate = nameInput || "VLSI_Candidate_" + Math.floor(Math.random() * 899 + 100);

  const modeRadios = document.getElementsByName('questMode');
  for (const r of modeRadios) {
    if (r.checked) currentQuest.mode = r.value;
  }

  if (currentQuest.mode === 'sprint') {
    currentQuest.modules = ["m10", "m40"]; // 2 modules x 3 tiers = 6 questions
  } else {
    currentQuest.modules = ["m10", "m20", "m30", "m40"]; // 4 modules x 3 tiers = 12 tiers
  }

  currentQuest.modIdx = 0;
  currentQuest.tierIdx = 0;
  currentQuest.mistakesAtTier = 0;
  currentQuest.totalAttempts = 0;
  currentQuest.correctAttempts = 0;
  currentQuest.score = 0;
  currentQuest.startTime = Date.now();

  currentQuest.modules.forEach(m => {
    currentQuest.tierCleared[m] = { easy: false, medium: false, hard: false };
    currentQuest.usedQuestions[m] = { easy: [], medium: [], hard: [] };
  });

  document.getElementById('quiz-start-screen').style.display = 'none';
  document.getElementById('quiz-report-screen').style.display = 'none';
  document.getElementById('quiz-active-screen').style.display = 'block';

  loadNextQuestion();
}

function loadNextQuestion() {
  clearInterval(currentQuest.timerInterval);
  currentQuest.selectedChoice = null;
  document.getElementById('btnSubmitAnswer').disabled = true;
  document.getElementById('feedbackToast').style.display = 'none';

  const modKey = currentQuest.modules[currentQuest.modIdx];
  const diffKey = currentQuest.diffTiers[currentQuest.tierIdx];

  // Update HUD elements
  document.getElementById('hudModuleCategory').innerText = `MODULE ${currentQuest.modIdx + 1} / ${currentQuest.modules.length}`;
  document.getElementById('hudModuleName').innerText = QUESTION_BANK[modKey].name;

  const diffBadges = {
    easy: "🟢 Tier 0 (Easy · Foundational)",
    medium: "🟡 Tier 1 (Medium · Engineering)",
    hard: "🔴 Tier 2 (Hard · Sign-Off Expert)"
  };
  document.getElementById('hudDifficultyBadge').innerText = diffBadges[diffKey];

  const tc = currentQuest.tierCleared[modKey];
  document.getElementById('hudTierClearMeter').innerText = 
    `[Easy: ${tc.easy ? '✓' : (diffKey==='easy'?'⏳':'🔒')}] [Med: ${tc.medium ? '✓' : (diffKey==='medium'?'⏳':'🔒')}] [Hard: ${tc.hard ? '✓' : (diffKey==='hard'?'⏳':'🔒')}]`;

  // Pick question from bank (tier question queue)
  const pool = QUESTION_BANK[modKey][diffKey];
  let available = pool.filter(q => !currentQuest.usedQuestions[modKey][diffKey].includes(q.id));
  if (available.length === 0) {
    // If all used in pool due to repeated mistakes, recycle
    currentQuest.usedQuestions[modKey][diffKey] = [];
    available = pool;
  }
  const q = available[Math.floor(Math.random() * available.length)];
  currentQuest.usedQuestions[modKey][diffKey].push(q.id);
  currentQuest.currentQuestion = q;

  // Render Prompt & Code
  document.getElementById('questionPrompt').innerText = q.prompt;
  const codeBox = document.getElementById('questionCodeContainer');
  if (q.code) {
    document.getElementById('questionCodeBlock').innerText = q.code;
    codeBox.style.display = 'block';
  } else {
    codeBox.style.display = 'none';
  }

  // Render Choices
  const grid = document.getElementById('choicesGrid');
  grid.innerHTML = '';
  const letters = ['A', 'B', 'C', 'D'];
  q.choices.forEach((choiceText, idx) => {
    const btn = document.createElement('div');
    btn.className = 'choice-item';
    btn.style.cssText = 'background:var(--md-default-bg-color); border:1px solid var(--tcl-border); border-radius:8px; padding:12px 16px; cursor:pointer; display:flex; align-items:center; gap:12px; transition:all 0.15s ease;';
    btn.innerHTML = `<span style="display:inline-block; width:26px; height:26px; line-height:26px; text-align:center; border-radius:50%; background:var(--tcl-surface); border:1px solid var(--tcl-border); font-weight:800; font-size:12px; color:var(--tcl-heading);">${letters[idx]}</span><span style="font-size:13.5px; color:var(--tcl-heading);">${choiceText}</span>`;
    btn.onclick = () => selectChoice(idx);
    grid.appendChild(btn);
  });

  // Calculate Dynamic Time: Base + (Mistakes * 15s)
  const baseTime = BASE_LIMITS[diffKey];
  const dynamicTime = baseTime + (currentQuest.mistakesAtTier * 15);
  currentQuest.maxTime = dynamicTime;
  currentQuest.timeLeft = dynamicTime;

  const allowanceTag = document.getElementById('thinkingAllowanceTag');
  if (currentQuest.mistakesAtTier > 0) {
    allowanceTag.style.display = 'inline';
    allowanceTag.innerText = `⚠️ Thinking Allowance: +${currentQuest.mistakesAtTier * 15}s (Extra Time Granted)`;
  } else {
    allowanceTag.style.display = 'none';
  }

  updateTimerDisplay();
  currentQuest.timerInterval = setInterval(onTimerTick, 1000);
}

function selectChoice(idx) {
  currentQuest.selectedChoice = idx;
  const items = document.querySelectorAll('.choice-item');
  items.forEach((item, i) => {
    if (i === idx) {
      item.style.borderColor = '#2563eb';
      item.style.background = 'rgba(37, 99, 235, 0.08)';
    } else {
      item.style.borderColor = 'var(--tcl-border)';
      item.style.background = 'var(--md-default-bg-color)';
    }
  });
  document.getElementById('btnSubmitAnswer').disabled = false;
}

function onTimerTick() {
  currentQuest.timeLeft--;
  updateTimerDisplay();
  if (currentQuest.timeLeft <= 0) {
    clearInterval(currentQuest.timerInterval);
    handleTimeout();
  }
}

function updateTimerDisplay() {
  const tText = document.getElementById('timerSecondsText');
  tText.innerText = currentQuest.timeLeft + 's';
  const bar = document.getElementById('timerBar');
  const pct = Math.max(0, (currentQuest.timeLeft / currentQuest.maxTime) * 100);
  bar.style.width = pct + '%';

  if (currentQuest.timeLeft <= 10) {
    bar.style.backgroundColor = '#ef4444';
    tText.style.color = '#ef4444';
  } else if (currentQuest.timeLeft <= 20) {
    bar.style.backgroundColor = '#f59e0b';
    tText.style.color = '#f59e0b';
  } else {
    bar.style.backgroundColor = '#10b981';
    tText.style.color = 'var(--tcl-blue-600)';
  }
}

function submitCurrentAnswer() {
  if (currentQuest.selectedChoice === null) return;
  clearInterval(currentQuest.timerInterval);
  
  currentQuest.totalAttempts++;
  const isCorrect = (currentQuest.selectedChoice === currentQuest.currentQuestion.answer);
  const modKey = currentQuest.modules[currentQuest.modIdx];
  const diffKey = currentQuest.diffTiers[currentQuest.tierIdx];

  const toast = document.getElementById('feedbackToast');
  toast.style.display = 'block';

  if (isCorrect) {
    currentQuest.correctAttempts++;
    const points = (diffKey === 'easy' ? 100 : (diffKey === 'medium' ? 200 : 300)) + Math.round(currentQuest.timeLeft * 2);
    currentQuest.score += points;
    currentQuest.tierCleared[modKey][diffKey] = true;
    currentQuest.mistakesAtTier = 0; // reset mistakes for cleared tier

    toast.style.background = 'rgba(16, 185, 129, 0.15)';
    toast.style.color = '#10b981';
    toast.style.border = '1px solid #10b981';
    toast.innerText = `✓ Correct! Tier cleared (+${points} pts). Advancing...`;

    setTimeout(() => {
      // Advance to next tier or module
      if (currentQuest.tierIdx < 2) {
        currentQuest.tierIdx++;
      } else {
        currentQuest.tierIdx = 0;
        currentQuest.modIdx++;
      }

      if (currentQuest.modIdx >= currentQuest.modules.length) {
        finishQuest();
      } else {
        loadNextQuestion();
      }
    }, 900);

  } else {
    // Mistake made: dynamic branching!
    currentQuest.mistakesAtTier++;
    currentQuest.score = Math.max(0, currentQuest.score - 20);

    toast.style.background = 'rgba(239, 68, 68, 0.12)';
    toast.style.color = '#ef4444';
    toast.style.border = '1px solid #ef4444';
    toast.innerText = `✗ Misconception detected! Tier not cleared. Additional reinforcement question queued (+15s thinking time granted).`;

    setTimeout(() => {
      loadNextQuestion();
    }, 1500);
  }
}

function handleTimeout() {
  currentQuest.totalAttempts++;
  currentQuest.mistakesAtTier++;
  const toast = document.getElementById('feedbackToast');
  toast.style.display = 'block';
  toast.style.background = 'rgba(239, 68, 68, 0.12)';
  toast.style.color = '#ef4444';
  toast.style.border = '1px solid #ef4444';
  toast.innerText = `⏱️ Time Expired! Tier not cleared. Queuing replacement question with +15s thinking time...`;

  setTimeout(() => {
    loadNextQuestion();
  }, 1500);
}

function finishQuest() {
  clearInterval(currentQuest.timerInterval);
  const elapsedMs = Date.now() - currentQuest.startTime;
  const elapsedSec = Math.round(elapsedMs / 1000);
  const minutes = Math.floor(elapsedSec / 60);
  const seconds = elapsedSec % 60;
  const timeFormatted = `${minutes}m ${seconds}s`;
  const accuracy = Math.round((currentQuest.correctAttempts / Math.max(1, currentQuest.totalAttempts)) * 100);

  let clearedCount = 0;
  let easyCount = 0, medCount = 0, hardCount = 0;
  currentQuest.modules.forEach(m => {
    if (currentQuest.tierCleared[m].easy) { clearedCount++; easyCount++; }
    if (currentQuest.tierCleared[m].medium) { clearedCount++; medCount++; }
    if (currentQuest.tierCleared[m].hard) { clearedCount++; hardCount++; }
  });

  const totalPossible = currentQuest.modules.length * 3;

  document.getElementById('quiz-active-screen').style.display = 'none';
  document.getElementById('quiz-report-screen').style.display = 'block';

  document.getElementById('reportScoreVal').innerText = currentQuest.score.toLocaleString();
  document.getElementById('reportAccuracyVal').innerText = accuracy + '%';
  document.getElementById('reportTimeVal').innerText = timeFormatted;
  document.getElementById('reportClearedVal').innerText = `${clearedCount}/${totalPossible}`;

  // Render Module Competency Bars
  const barsContainer = document.getElementById('moduleCompetencyBars');
  barsContainer.innerHTML = '';
  currentQuest.modules.forEach(m => {
    const cl = currentQuest.tierCleared[m];
    const modScore = (cl.easy ? 1 : 0) + (cl.medium ? 1 : 0) + (cl.hard ? 1 : 0);
    const modPct = Math.round((modScore / 3) * 100);
    barsContainer.innerHTML += `
      <div>
        <div style="display:flex; justify-content:space-between; font-size:12.5px; font-weight:700; margin-bottom:4px; color:var(--tcl-heading);">
          <span>${QUESTION_BANK[m].name}</span>
          <span style="color:var(--tcl-blue-600);">${modScore}/3 Tiers (${modPct}%)</span>
        </div>
        <div style="width:100%; height:8px; background:rgba(0,0,0,0.08); border-radius:4px; overflow:hidden;">
          <div style="width:${modPct}%; height:100%; background:${modPct === 100 ? '#10b981' : (modPct > 50 ? '#f59e0b' : '#38bdf8')};"></div>
        </div>
      </div>
    `;
  });

  // Setup Certificate
  const dateStr = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  const certId = 'TCL-VLSI-' + Date.now().toString(36).toUpperCase() + '-' + Math.floor(Math.random()*1000).toString(16).toUpperCase();
  
  document.getElementById('certStudentName').innerText = currentQuest.candidate;
  document.getElementById('certDateVal').innerText = dateStr;
  document.getElementById('certHashVal').innerText = certId;

  // Record to localStorage for Leaderboard
  try {
    const raw = localStorage.getItem('tcl_vlsi_leaderboard');
    const board = raw ? JSON.parse(raw) : [];
    board.push({
      candidate: currentQuest.candidate,
      mode: currentQuest.mode === 'full' ? 'Full Grand Prix' : 'Sprint Diagnostic',
      score: currentQuest.score,
      accuracy: accuracy,
      time: timeFormatted,
      cleared: `${easyCount}/${medCount}/${hardCount}`,
      date: new Date().toISOString().slice(0, 10),
      certId: certId
    });
    localStorage.setItem('tcl_vlsi_leaderboard', JSON.stringify(board));
  } catch(e) {}
}

function downloadCertificateSVG() {
  const name = document.getElementById('certStudentName').innerText;
  const dateStr = document.getElementById('certDateVal').innerText;
  const hash = document.getElementById('certHashVal').innerText;

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560" width="800" height="560">
    <rect width="800" height="560" fill="#ffffff" />
    <rect x="20" y="20" width="760" height="520" fill="none" stroke="#d4af37" stroke-width="4" stroke-dasharray="8 4" />
    <rect x="30" y="30" width="740" height="500" fill="none" stroke="#1e293b" stroke-width="1.5" />
    
    <text x="400" y="80" text-anchor="middle" font-family="'Inter', sans-serif" font-size="14" font-weight="800" fill="#b45309" letter-spacing="3">SJTU-YONGFU-RESEARCH-GRP · VLSI AUTOMATION LAB</text>
    <text x="400" y="130" text-anchor="middle" font-family="'Inter', sans-serif" font-size="28" font-weight="900" fill="#0f172a">CERTIFICATE OF INDUSTRIAL MASTERY</text>
    <text x="400" y="160" text-anchor="middle" font-family="'Inter', sans-serif" font-size="13" fill="#64748b">IN RECOGNITION OF DEMONSTRATED PROFICIENCY IN TCL SCRIPTING FOR VLSI DESIGN</text>
    
    <line x1="250" y1="185" x2="550" y2="185" stroke="#e2e8f0" stroke-width="2" />
    
    <text x="400" y="225" text-anchor="middle" font-family="'Inter', sans-serif" font-size="14" fill="#475569">This official certificate is proudly conferred upon:</text>
    <text x="400" y="280" text-anchor="middle" font-family="'Inter', sans-serif" font-size="36" font-weight="900" fill="#0f172a">${name}</text>
    
    <text x="400" y="340" text-anchor="middle" font-family="'Inter', sans-serif" font-size="13" fill="#334155">Has successfully cleared the VLSI Tcl Challenge across all 3 difficulty tiers,</text>
    <text x="400" y="360" text-anchor="middle" font-family="'Inter', sans-serif" font-size="13" fill="#334155">demonstrating full mastery of Brent Welch Substitution Rules, Physical Layout &amp; STA Sign-Off.</text>
    
    <!-- Gold Rosette Seal -->
    <circle cx="400" cy="440" r="32" fill="#fef3c7" stroke="#b45309" stroke-width="2" />
    <text x="400" y="448" text-anchor="middle" font-family="'Inter', sans-serif" font-size="24" fill="#b45309">★</text>
    
    <!-- Signatures and hash -->
    <text x="140" y="460" font-family="'Inter', sans-serif" font-size="12" font-weight="700" fill="#0f172a">${dateStr}</text>
    <text x="140" y="478" font-family="'Inter', sans-serif" font-size="11" fill="#94a3b8">Date of Award</text>
    
    <text x="660" y="460" text-anchor="end" font-family="monospace" font-size="13" font-weight="700" fill="#0f172a">${hash}</text>
    <text x="660" y="478" text-anchor="end" font-family="'Inter', sans-serif" font-size="11" fill="#94a3b8">Verification Hash</text>
  </svg>`;

  const blob = new Blob([svg], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `Certificate_${name.replace(/\s+/g, '_')}_TCL_VLSI.svg`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function restartChallenge() {
  document.getElementById('quiz-report-screen').style.display = 'none';
  document.getElementById('quiz-start-screen').style.display = 'block';
}

// Keyboard shortcuts (1-4 and A-D)
window.addEventListener('keydown', e => {
  if (document.getElementById('quiz-active-screen').style.display !== 'block') return;
  const key = e.key.toUpperCase();
  if (key === '1' || key === 'A') selectChoice(0);
  else if (key === '2' || key === 'B') selectChoice(1);
  else if (key === '3' || key === 'C') selectChoice(2);
  else if (key === '4' || key === 'D') selectChoice(3);
  else if (key === 'ENTER' && !document.getElementById('btnSubmitAnswer').disabled) {
    submitCurrentAnswer();
  }
});
</script>"""


LEADERBOARD_JS = r"""<script>
const SEED_BENCHMARKS = [
  { candidate: "Dr. Yongfu Li (Research Lead)", mode: "Full Grand Prix", score: 3600, accuracy: 100, time: "3m 42s", cleared: "4/4/4", date: "2026-10-18", certId: "TCL-VLSI-SJTU-YFL001" },
  { candidate: "FanqinZeng (WASM Architect)", mode: "Full Grand Prix", score: 3450, accuracy: 98, time: "4m 15s", cleared: "4/4/4", date: "2026-10-17", certId: "TCL-VLSI-SJTU-FQZ002" },
  { candidate: "Su3037 (Tcl Quest Creator)", mode: "Full Grand Prix", score: 3380, accuracy: 95, time: "4m 38s", cleared: "4/4/4", date: "2026-10-16", certId: "TCL-VLSI-SJTU-SU003" },
  { candidate: "GateUltra (Homework Lead)", mode: "Full Grand Prix", score: 3210, accuracy: 92, time: "5m 02s", cleared: "4/4/4", date: "2026-10-15", certId: "TCL-VLSI-SJTU-GU004" },
  { candidate: "Capeur (DRV-Lite Core)", mode: "Full Grand Prix", score: 3150, accuracy: 90, time: "5m 24s", cleared: "4/4/4", date: "2026-10-14", certId: "TCL-VLSI-SJTU-CAP005" },
  { candidate: "thy031 (Quiz Module)", mode: "Sprint Diagnostic", score: 1840, accuracy: 100, time: "1m 30s", cleared: "2/2/2", date: "2026-10-19", certId: "TCL-VLSI-SJTU-THY006" },
  { candidate: "VLSI_Signoff_Ninja", mode: "Sprint Diagnostic", score: 1720, accuracy: 94, time: "1m 48s", cleared: "2/2/2", date: "2026-10-19", certId: "TCL-VLSI-SJTU-NIN007" }
];

let activeMode = 'all';
let allRows = [];

function initLeaderboard() {
  allRows = [...SEED_BENCHMARKS];
  try {
    const raw = localStorage.getItem('tcl_vlsi_leaderboard');
    if (raw) {
      const localRows = JSON.parse(raw);
      localRows.forEach(lr => {
        allRows.push(lr);
      });
    }
  } catch(e) {}

  // Sort descending by score
  allRows.sort((a, b) => b.score - a.score);
  renderLeaderboard();
}

function setBoardMode(mode) {
  activeMode = mode;
  document.querySelectorAll('.board-mode-btn').forEach(btn => {
    btn.style.background = 'var(--tcl-surface-card)';
    btn.style.color = 'var(--tcl-heading)';
  });
  const activeBtn = document.getElementById(mode === 'all' ? 'btnModeAll' : (mode === 'full' ? 'btnModeFull' : 'btnModeSprint'));
  if (activeBtn) {
    activeBtn.style.background = 'var(--tcl-blue-600)';
    activeBtn.style.color = '#ffffff';
  }
  filterLeaderboard();
}

function filterLeaderboard() {
  const query = document.getElementById('boardSearchInput').value.toLowerCase().trim();
  let filtered = allRows.filter(r => {
    const matchesSearch = r.candidate.toLowerCase().includes(query) || (r.certId && r.certId.toLowerCase().includes(query));
    if (activeMode === 'all') return matchesSearch;
    if (activeMode === 'full') return matchesSearch && r.mode.includes('Full');
    if (activeMode === 'sprint') return matchesSearch && r.mode.includes('Sprint');
    return matchesSearch;
  });
  renderLeaderboard(filtered);
}

function renderLeaderboard(data = allRows) {
  const tbody = document.getElementById('leaderboardTbody');
  if (data.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" style="padding:20px; text-align:center; color:var(--md-default-fg-color--lighter);">No matching records found.</td></tr>`;
    return;
  }

  let html = '';
  data.forEach((row, idx) => {
    let rankBadge = `${idx + 1}`;
    if (idx === 0) rankBadge = '🥇 1';
    else if (idx === 1) rankBadge = '🥈 2';
    else if (idx === 2) rankBadge = '🥉 3';

    html += `
      <tr style="border-bottom:1px solid var(--tcl-border); transition:background 0.15s ease;">
        <td style="padding:10px 14px; font-weight:800; color:${idx < 3 ? 'var(--tcl-blue-600)' : 'var(--tcl-heading)'};">${rankBadge}</td>
        <td style="padding:10px 14px; font-weight:700; color:var(--tcl-heading);">
          ${row.candidate}
          ${row.certId ? `<span style="display:block; font-size:11px; font-family:monospace; color:var(--md-default-fg-color--lighter);">${row.certId}</span>` : ''}
        </td>
        <td style="padding:10px 14px;"><span style="display:inline-block; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600; background:rgba(37,99,235,0.1); color:var(--tcl-blue-600);">${row.mode}</span></td>
        <td style="padding:10px 14px; text-align:right; font-weight:800; color:var(--tcl-heading);">${row.score.toLocaleString()}</td>
        <td style="padding:10px 14px; text-align:right; font-weight:700; color:#10b981;">${row.accuracy}%</td>
        <td style="padding:10px 14px; text-align:right; font-family:monospace;">${row.time}</td>
        <td style="padding:10px 14px; text-align:center; font-family:monospace; font-weight:600;">${row.cleared}</td>
        <td style="padding:10px 14px; text-align:right; font-size:12px; color:var(--md-default-fg-color--lighter);">${row.date}</td>
      </tr>
    `;
  });
  tbody.innerHTML = html;
}

function verifyCertificateHash() {
  const hash = document.getElementById('verifyHashInput').value.trim();
  const box = document.getElementById('verifyResultBox');
  if (!hash) return;
  box.style.display = 'block';

  const match = allRows.find(r => r.certId && r.certId.toUpperCase() === hash.toUpperCase());
  if (match) {
    box.style.background = 'rgba(16, 185, 129, 0.12)';
    box.style.border = '1px solid #10b981';
    box.style.color = '#10b981';
    box.innerHTML = `<strong>✓ VERIFIED AUTHENTIC CERTIFICATE</strong><br>Candidate: <strong>${match.candidate}</strong> | Mode: ${match.mode} | Score: ${match.score} pts | Accuracy: ${match.accuracy}% | Date: ${match.date} | Issuer: SJTU-YONGFU-RESEARCH-GRP.`;
  } else {
    box.style.background = 'rgba(239, 68, 68, 0.12)';
    box.style.border = '1px solid #ef4444';
    box.style.color = '#ef4444';
    box.innerHTML = `<strong>✗ INVALID OR UNRECOGNIZED CERTIFICATE HASH</strong><br>No matching record found in official lab credential registry.`;
  }
}

window.addEventListener('DOMContentLoaded', initLeaderboard);
</script>"""
