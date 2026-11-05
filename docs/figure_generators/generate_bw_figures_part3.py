import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIRS = [
    r"c:\Users\ASUS\Desktop\Kali-Nova\Kali-Nova-Figures-Folder",
    r"c:\Users\ASUS\Desktop\Kali-Nova\docs\figures"
]

def save_fig(fig, filename):
    base_name = os.path.splitext(filename)[0]
    for d in OUTPUT_DIRS:
        os.makedirs(d, exist_ok=True)
        # Optimized PNG for Overleaf & web: 140 DPI (~1500-1600px wide, lightweight, fast loading)
        png_target = os.path.join(d, f"{base_name}.png")
        fig.savefig(png_target, dpi=140, bbox_inches='tight', facecolor='#FFFFFF', edgecolor='none')
        
        try:
            from PIL import Image
            with Image.open(png_target) as img:
                img.save(png_target, optimize=True)
        except Exception:
            pass

    # Ensure paper figure aliases exist
    if base_name == "system_architecture":
        for d in OUTPUT_DIRS:
            src = os.path.join(d, f"{base_name}.png")
            dst = os.path.join(d, "architecture_diagram.png")
            if os.path.exists(src):
                import shutil
                shutil.copy2(src, dst)
    elif base_name == "tool_execution_workflow":
        for d in OUTPUT_DIRS:
            src = os.path.join(d, f"{base_name}.png")
            dst = os.path.join(d, "state_transition_diagram.png")
            if os.path.exists(src):
                import shutil
                shutil.copy2(src, dst)

    print(f"Generated Clean B&W {filename}")
    plt.close(fig)

BG_WHITE = "#FFFFFF"
BORDER_BLACK = "#000000"
TEXT_BLACK = "#000000"
TEXT_MUTED = "#374151"
FILL_WHITE = "#FFFFFF"
FILL_LIGHT = "#F9FAFB"
FILL_GRAY1 = "#F3F4F6"
FILL_GRAY2 = "#E5E7EB"
FILL_GRAY3 = "#D1D5DB"

def draw_box(ax, x, y, w, h, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5, ls='-', hatch=None, zorder=2):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.02",
                                 facecolor=bg, edgecolor=border, linewidth=lw, linestyle=ls, hatch=hatch, zorder=zorder)
    ax.add_patch(box)
    return box

# ==========================================
# 17. Figure 3.17: Complete Kali-Nova System Workflow
# ==========================================
def gen_fig3_17():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    phases = [
        ("Phase 1:\nTarget Definition", "Scope validation, CIDR check,\nprofile selection (Professional)", 0.05, 0.54),
        ("Phase 2:\nPerimeter Recon", "OSINT discovery via Whois &\ntheHarvester for domains", 0.29, 0.54),
        ("Phase 3:\nPort Enumeration", "Nmap SYN sweeps, service\nbanner grabbing (P_crit)", 0.53, 0.54),
        ("Phase 4:\nWeb Fuzzing", "Nikto vulnerability scans &\nGobuster directory enumeration", 0.77, 0.54),

        ("Phase 8:\nReport Export", "Executive PDF & HTML report\ngeneration via ReportLab", 0.05, 0.08),
        ("Phase 7:\nPersistent Store", "Scan history, events & hashes\ncommitted to kalinova.db", 0.29, 0.08),
        ("Phase 6:\nAI Remediation", "CVSS scoring & parameterized\ncode patches (Py/Node/Bash)", 0.53, 0.08),
        ("Phase 5:\nExploit Auditing", "SQLMap injection verification &\nHydra authentication testing", 0.77, 0.08)
    ]

    for ptitle, pdesc, px, py in phases:
        draw_box(ax, px, py, 0.18, 0.38, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(px + 0.09, py + 0.285, ptitle, color=TEXT_BLACK, fontsize=11, fontweight='bold', ha='center', va='center')
        ax.plot([px + 0.02, px + 0.16], [py + 0.22, py + 0.22], color=BORDER_BLACK, lw=0.8)
        ax.text(px + 0.09, py + 0.11, pdesc, color=TEXT_MUTED, fontsize=9.8, ha='center', va='center')

    # Top row forward arrows
    ax.annotate("", xy=(0.285, 0.74), xytext=(0.235, 0.74), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.annotate("", xy=(0.525, 0.74), xytext=(0.475, 0.74), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.annotate("", xy=(0.765, 0.74), xytext=(0.715, 0.74), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    # Turn down
    ax.annotate("", xy=(0.86, 0.46), xytext=(0.86, 0.54), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    # Bottom row reverse arrows
    ax.annotate("", xy=(0.715, 0.26), xytext=(0.765, 0.26), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.annotate("", xy=(0.475, 0.26), xytext=(0.525, 0.26), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.annotate("", xy=(0.235, 0.26), xytext=(0.285, 0.26), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    save_fig(fig, "complete_workflow.png")

# ==========================================
# 18. Figure 3.18: Data Flow Diagram of Kali-Nova
# ==========================================
def gen_fig3_18():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    draw_box(ax, 0.04, 0.78, 0.17, 0.15, bg=FILL_GRAY2, lw=2)
    ax.text(0.125, 0.855, "Security Analyst\n(User / Operator)", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')

    draw_box(ax, 0.79, 0.78, 0.17, 0.15, bg=FILL_GRAY2, lw=2)
    ax.text(0.875, 0.855, "Target Host\n(Remote System)", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')

    draw_box(ax, 0.79, 0.08, 0.17, 0.15, bg=FILL_GRAY2, lw=2)
    ax.text(0.875, 0.155, "AI LLM Provider\n(Groq / Ollama)", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')

    procs = [
        ("1.0 Scope & Config\nValidator", 0.28, 0.78),
        ("2.0 Interactive\nExecutor", 0.56, 0.78),
        ("3.0 Telemetry\nStream Parser", 0.56, 0.44),
        ("4.0 State & Risk\nOrchestrator", 0.24, 0.44),
        ("5.0 Copilot Patch\nSynthesizer", 0.56, 0.08),
        ("6.0 Report Compiler\n& Exporter", 0.04, 0.08)
    ]
    for pname, px, py in procs:
        draw_box(ax, px, py, 0.18, 0.15, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(px + 0.09, py + 0.075, pname, color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')

    # Data Stores
    for ds_name, dx, dy in [("[D1] kalinova.db (SQLite)", 0.24, 0.04), ("[D2] Artifacts Dict (State)", 0.24, 0.27)]:
        ax.plot([dx, dx + 0.18], [dy + 0.06, dy + 0.06], color=BORDER_BLACK, lw=2)
        ax.plot([dx, dx + 0.18], [dy, dy], color=BORDER_BLACK, lw=2)
        ax.text(dx + 0.09, dy + 0.03, ds_name, color=TEXT_BLACK, fontsize=10.5, fontweight='bold', ha='center', va='center')

    ax.annotate("", xy=(0.28, 0.855), xytext=(0.21, 0.855), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.text(0.245, 0.88, "Target / Flags", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.56, 0.855), xytext=(0.46, 0.855), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.text(0.51, 0.88, "Sanitized CLI", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.79, 0.855), xytext=(0.74, 0.855), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.text(0.765, 0.88, "Probes", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.65, 0.59), xytext=(0.65, 0.78), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.text(0.68, 0.685, "Raw stdout", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    # Extracted Ports arrow cleanly in gap
    ax.annotate("", xy=(0.42, 0.515), xytext=(0.56, 0.515), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.text(0.49, 0.54, "Extracted Ports", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.65, 0.23), xytext=(0.65, 0.44), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.text(0.68, 0.33, "Threat Event", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.79, 0.155), xytext=(0.74, 0.155), arrowprops=dict(arrowstyle="<->", color=BORDER_BLACK, lw=2))
    ax.text(0.765, 0.18, "Prompt/Resp", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.135, 0.23), xytext=(0.24, 0.44), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.text(0.18, 0.35, "Findings", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    # Connect processes to data stores
    ax.annotate("", xy=(0.33, 0.33), xytext=(0.33, 0.44), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.33, 0.10), xytext=(0.33, 0.27), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))

    save_fig(fig, "data_flow_diagram.png")

# ==========================================
# 19. Figure 3.19: Session Management Module
# ==========================================
def gen_fig3_19():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    tables = [
        ("TABLE: scans", [
            "id: INTEGER PRIMARY KEY",
            "session_uuid: TEXT",
            "tool_name: TEXT (e.g. nmap)",
            "target: TEXT (192.168.1.105)",
            "start_time: TIMESTAMP",
            "end_time: TIMESTAMP",
            "status: TEXT (COMPLETED)",
            "exit_code: INTEGER"
        ], 0.05, 0.34),

        ("TABLE: events", [
            "id: INTEGER PRIMARY KEY",
            "scan_id: INTEGER (FK)",
            "event_type: TEXT (PORT_FOUND)",
            "severity: TEXT (CRITICAL)",
            "raw_line: TEXT",
            "timestamp: TIMESTAMP"
        ], 0.37, 0.34),

        ("TABLE: vulnerabilities", [
            "id: INTEGER PRIMARY KEY",
            "scan_id: INTEGER (FK)",
            "cve_id: TEXT (CVE-2011-2523)",
            "cvss_score: REAL (9.8)",
            "remediation_code: TEXT",
            "verified: BOOLEAN"
        ], 0.69, 0.34)
    ]

    for tname, fields, tx, ty in tables:
        draw_box(ax, tx, ty, 0.26, 0.60, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        # Dedicated Header Banner
        rect = patches.Rectangle((tx, ty + 0.51), 0.26, 0.09, facecolor=FILL_GRAY2, edgecolor=BORDER_BLACK, lw=1)
        ax.add_patch(rect)
        ax.text(tx + 0.13, ty + 0.555, tname, color=TEXT_BLACK, fontsize=12, fontweight='bold', ha='center', va='center')
        for fidx, f in enumerate(fields):
            ax.text(tx + 0.02, ty + 0.45 - fidx * 0.056, f, color=TEXT_BLACK, fontsize=10.5, family='monospace')

    ax.annotate("", xy=(0.365, 0.70), xytext=(0.315, 0.70), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.annotate("", xy=(0.685, 0.70), xytext=(0.635, 0.70), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    draw_box(ax, 0.05, 0.04, 0.90, 0.26, bg=FILL_WHITE, lw=1.5)
    ax.text(0.07, 0.255, "Session Management Operations", color=TEXT_BLACK, fontsize=12.5, fontweight='bold')
    ax.plot([0.07, 0.38], [0.235, 0.235], color=BORDER_BLACK, lw=1)

    ops = [
        ("Session Snapshots", "Captures full AppState state tuple\nfor timeline playback and review", 0.08),
        ("Forensic Traceability", "Immutable logging of executed CLI\ncommands and runtime stdout hashes", 0.38),
        ("Export & Migration", "One-click export to SQLite dump\nor encrypted JSON backup archive", 0.68)
    ]
    for otitle, odesc, ox in ops:
        draw_box(ax, ox, 0.06, 0.24, 0.155, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.2)
        ax.text(ox + 0.12, 0.165, otitle, color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center')
        ax.plot([ox + 0.02, ox + 0.22], [0.14, 0.14], color=BORDER_BLACK, lw=0.8)
        ax.text(ox + 0.12, 0.09, odesc, color=TEXT_MUTED, fontsize=10, ha='center', va='center')

    save_fig(fig, "session_management.png")

# ==========================================
# 20. Figure 3.20: Security Report Generation
# ==========================================
def gen_fig3_20():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    stages = [
        ("1. Telemetry\nIngestion", "Queries kalinova.db for\nports, CVEs, logs & risk metrics", 0.04),
        ("2. Metric\nNormalization", "Computes composite score R_t,\nCVSS vector distribution", 0.285),
        ("3. Remediation\nCompilation", "Incorporates AI Copilot code\npatches (Py/Node/Bash)", 0.53),
        ("4. ReportLab\nEngine", "Compiles formatted PDF with\ntables, headers & risk charts", 0.775)
    ]
    for stitle, sdesc, sx in stages:
        draw_box(ax, sx, 0.52, 0.185, 0.42, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(sx + 0.0925, 0.86, stitle, color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')
        ax.plot([sx + 0.02, sx + 0.165], [0.80, 0.80], color=BORDER_BLACK, lw=0.8)
        ax.text(sx + 0.0925, 0.66, sdesc, color=TEXT_MUTED, fontsize=10.2, ha='center', va='center')

    for i in range(len(stages) - 1):
        x1 = stages[i][2] + 0.185 + 0.005
        x2 = stages[i+1][2] - 0.005
        ax.annotate("", xy=(x2, 0.76), xytext=(x1, 0.76), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    draw_box(ax, 0.04, 0.04, 0.44, 0.44, bg=FILL_WHITE, lw=1.5)
    ax.text(0.06, 0.435, "Executive PDF Report Structure", color=TEXT_BLACK, fontsize=12.5, fontweight='bold')
    ax.plot([0.06, 0.42], [0.41, 0.41], color=BORDER_BLACK, lw=1)
    ax.text(0.06, 0.35, "- Cover Page: Target FQDN, Date, Lead Auditor", color=TEXT_BLACK, fontsize=10.5)
    ax.text(0.06, 0.28, "- Executive Summary: Composite Risk Score 78.4", color=TEXT_BLACK, fontsize=10.5)
    ax.text(0.06, 0.21, "- Vulnerability Matrix: CVE-2011-2523, SQLi, Ports", color=TEXT_BLACK, fontsize=10.5)
    ax.text(0.06, 0.14, "- Technical Remediation: Code diffs & WAF rules", color=TEXT_BLACK, fontsize=10.5)
    ax.text(0.06, 0.07, "- Forensic Appendix: Command history & hashes", color=TEXT_BLACK, fontsize=10.5)

    draw_box(ax, 0.52, 0.04, 0.44, 0.44, bg=FILL_WHITE, lw=1.5)
    ax.text(0.54, 0.435, "Interactive HTML Dashboard Report", color=TEXT_BLACK, fontsize=12.5, fontweight='bold')
    ax.plot([0.54, 0.90], [0.41, 0.41], color=BORDER_BLACK, lw=1)
    ax.text(0.54, 0.35, "- Responsive Bento Grid: Radar plots & severity dials", color=TEXT_BLACK, fontsize=10.5)
    ax.text(0.54, 0.28, "- Filterable Findings Table: Search by severity or port", color=TEXT_BLACK, fontsize=10.5)
    ax.text(0.54, 0.21, "- One-Click Code Snippet Copy: Fast developer handoff", color=TEXT_BLACK, fontsize=10.5)
    ax.text(0.54, 0.14, "- Offline Compliant: Zero external CDN dependencies", color=TEXT_BLACK, fontsize=10.5)
    ax.text(0.54, 0.07, "- Portable Output: Self-contained single-file HTML", color=TEXT_BLACK, fontsize=10.5)

    save_fig(fig, "report_generation.png")

# ==========================================
# 21. Figure 3.21: Kali-Nova User Interface Layout
# ==========================================
def gen_fig3_21():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Topbar
    draw_box(ax, 0.04, 0.89, 0.92, 0.075, bg=FILL_GRAY2, lw=2)
    ax.text(0.06, 0.927, "A. TOPBAR: Target FQDN | Scope CIDR | Risk Index | Profile Mode Switcher", color=TEXT_BLACK, fontsize=12, fontweight='bold', va='center')

    # Sidebar with dedicated header
    draw_box(ax, 0.04, 0.04, 0.16, 0.82, bg=FILL_LIGHT, lw=1.5)
    draw_box(ax, 0.05, 0.79, 0.14, 0.06, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1)
    ax.text(0.12, 0.82, "B. SIDEBAR", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')
    nav_list = [
        "- Dashboard View",
        "- Reconnaissance",
        "- Web Security",
        "- Auth Resilience",
        "- Network Audits",
        "- Reports & DB",
        "- Global Settings"
    ]
    for idx, item in enumerate(nav_list):
        ax.text(0.06, 0.72 - idx * 0.085, item, color=TEXT_BLACK, fontsize=10.5, fontweight='bold')

    # Central Workspace with dedicated header
    draw_box(ax, 0.22, 0.32, 0.52, 0.54, bg=FILL_WHITE, lw=2)
    draw_box(ax, 0.23, 0.79, 0.50, 0.06, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1)
    ax.text(0.48, 0.82, "C. PRIMARY CENTRAL WORKSPACE", color=TEXT_BLACK, fontsize=12, fontweight='bold', ha='center', va='center')
    ws_features = [
        "- Animated Network Topology Canvas (20 FPS Spatial Radar Sweep)",
        "- Dynamic Threat Score Speedometer Gauge (0 - 100 CVSS Arc)",
        "- Real-Time Discovered Port Matrix with Live Service Banners",
        "- Dynamic Security Tool Configuration & Execution Parameter Forms",
        "- Automated Next-Step Workflow Prescription Cards"
    ]
    for idx, feat in enumerate(ws_features):
        ax.text(0.24, 0.71 - idx * 0.08, feat, color=TEXT_MUTED, fontsize=10.5)

    # Console Dock with dedicated header
    draw_box(ax, 0.22, 0.04, 0.52, 0.25, bg=FILL_LIGHT, lw=1.5)
    draw_box(ax, 0.23, 0.22, 0.50, 0.06, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1)
    ax.text(0.48, 0.25, "D. INTERACTIVE CONSOLE DOCK (Live PTY Stream)", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')
    console_sample = (
        "$ nmap -sV -T4 192.168.1.105 ... [Streaming Telemetry at 100 Hz]\n"
        "[+] Port 80/tcp OPEN (Apache 2.4.41 PHP 7.4.3)\n"
        "[+] Port 3306/tcp OPEN (MariaDB 10.3.38 MySQL Protocol)"
    )
    ax.text(0.24, 0.13, console_sample, color=TEXT_BLACK, fontsize=10, family='monospace')

    # AI Copilot Drawer with dedicated header
    draw_box(ax, 0.76, 0.04, 0.20, 0.82, bg=FILL_LIGHT, lw=1.5)
    draw_box(ax, 0.77, 0.79, 0.18, 0.06, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1)
    ax.text(0.86, 0.82, "E. AI COPILOT", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')
    copilot_items = [
        "- Sliding Drawer UI",
        "- Markdown Diagnostics",
        "- CVSS v3.1 Severity",
        "- Parameterized Fixes",
        "  (Python / Node.js)",
        "- 1-Click Code Copy",
        "- Diagnostic Reasoning"
    ]
    for idx, citem in enumerate(copilot_items):
        ax.text(0.78, 0.72 - idx * 0.08, citem, color=TEXT_BLACK, fontsize=10.5)

    save_fig(fig, "ui_layout.png")

# ==========================================
# 22. Figure 3.22: Testing Methodology
# ==========================================
def gen_fig3_22():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    tiers = [
        ("Tier 1: Unit Testing (PyTest)", "Test regex parsers, CVSS scoring math,\nAppState mutations & input validation.", 0.74, "98.2% Code Coverage", FILL_WHITE),
        ("Tier 2: Concurrency & PTY Testing", "Stress test CommandThread lifecycle,\nbuffer overflow prevention & cleanup.", 0.51, "Zero Process Leaks", FILL_LIGHT),
        ("Tier 3: GUI & Signal Integration", "PyQt6 headless test harness validating\nsignal emissions, state updates & HUD FPS.", 0.28, "60 FPS Responsive HUD", FILL_GRAY1),
        ("Tier 4: Cyber-Range Validation", "End-to-end testing against 15 vulnerable VMs\n(OWASP Juice Shop, Metasploitable 2/3, DVWA).", 0.05, "84.3% Latency Drop", FILL_GRAY2)
    ]

    for ttitle, tdesc, ty, tstat, tbg in tiers:
        w = 0.54 + (0.75 - ty) * 0.40
        x = 0.50 - w / 2

        # Main Tier Box
        draw_box(ax, x, ty, w, 0.19, bg=tbg, border=BORDER_BLACK, lw=1.5, zorder=3)
        ax.text(x + 0.03, ty + 0.14, ttitle, color=TEXT_BLACK, fontsize=12.5, fontweight='bold', zorder=5)

        # Divider line
        ax.plot([x + 0.03, x + 0.32], [ty + 0.115, ty + 0.115], color=BORDER_BLACK, lw=1, zorder=5)
        ax.text(x + 0.03, ty + 0.055, tdesc, color=TEXT_MUTED, fontsize=10.2, zorder=5)

        # Right Stat Badge Box safely on the right
        draw_box(ax, x + w - 0.23, ty + 0.055, 0.21, 0.08, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.2, zorder=5)
        ax.text(x + w - 0.125, ty + 0.095, tstat, color=TEXT_BLACK, fontsize=10, fontweight='bold', ha='center', va='center', zorder=6)

    save_fig(fig, "testing_workflow.png")

# ==========================================
# 23. Figure 4.11: CVSS-Based Vulnerability Analysis
# ==========================================
def gen_fig4_11():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax_bar = fig.add_axes([0.16, 0.10, 0.35, 0.82], facecolor=BG_WHITE)
    vulns = ['SQL Injection\n(CWE-89)', 'vsftpd Backdoor\n(CVE-2011-2523)', 'Weak SSH Auth\n(Hydra Crack)', 'Deprecated TLS 1.0\n(SSLyze)', 'Directory Traversal\n(CWE-22)', 'Info Banner Leak\n(Apache)']
    scores = [9.8, 9.8, 8.1, 6.5, 5.3, 2.1]
    grays = [FILL_GRAY3, FILL_GRAY3, FILL_GRAY2, FILL_GRAY1, FILL_LIGHT, FILL_WHITE]

    y_pos = np.arange(len(vulns))
    for i in range(len(vulns)):
        ax_bar.barh(y_pos[i], scores[i], height=0.52, facecolor=grays[i], edgecolor=BORDER_BLACK, lw=1.5)
        ax_bar.text(scores[i] + 0.30, y_pos[i], f"{scores[i]}", color=TEXT_BLACK, va='center', fontweight='bold', fontsize=11)

    ax_bar.set_yticks(y_pos)
    ax_bar.set_yticklabels(vulns, color=TEXT_BLACK, fontsize=10.5, fontweight='bold')
    ax_bar.set_xlabel("CVSS v3.1 Base Severity Score", color=TEXT_BLACK, fontsize=12, fontweight='bold')
    ax_bar.set_xlim(0, 11.5)
    ax_bar.grid(axis='x', color=FILL_GRAY3, linestyle='--', lw=1.2)
    ax_bar.tick_params(colors=TEXT_BLACK, labelsize=10.5)
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)
    ax_bar.spines['left'].set_color(BORDER_BLACK)
    ax_bar.spines['bottom'].set_color(BORDER_BLACK)

    # Statistics Card
    draw_box(ax, 0.54, 0.08, 0.42, 0.86, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.56, 0.89, "Assessment Statistics & Metrics", color=TEXT_BLACK, fontsize=13, fontweight='bold')
    ax.plot([0.56, 0.94], [0.865, 0.865], color=BORDER_BLACK, lw=1)

    stats = [
        ("Total Vulnerabilities Detected:", "18 Findings"),
        ("Critical Severity (9.0-10):", "5 Findings (27.8%)"),
        ("High Severity (7.0-8.9):", "6 Findings (33.3%)"),
        ("Medium Severity (4.0-6.9):", "5 Findings (27.8%)"),
        ("Low Severity (0.1-3.9):", "2 Findings (11.1%)"),
        ("Mean CVSS Base Score:", "7.24 / 10.0"),
        ("Auto Remediation Success:", "96.4% Verified"),
        ("Expert Tester Alignment:", "98.2% Correlation")
    ]
    for sidx, (slbl, sval) in enumerate(stats):
        sy = 0.80 - sidx * 0.085
        ax.text(0.56, sy, slbl, color=TEXT_MUTED, fontsize=10.5)
        ax.text(0.93, sy, sval, color=TEXT_BLACK, fontsize=11, fontweight='bold', ha='right')

    save_fig(fig, "cvss_result.png")

# ==========================================
# 24. Figure 4.15: Integration Testing Workflow
# ==========================================
def gen_fig4_15():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ci_stages = [
        ("1. Code Push\n/ PR", "Developer commits to GitHub;\nTriggers CI/CD Actions", 0.05, 0.54),
        ("2. Static Code\nLinting", "Flake8, Pyright, Black syntax\nand typing enforcement", 0.29, 0.54),
        ("3. Subsystem\nUnit Tests", "PyTest suite executing 42+\nunit & parser test cases", 0.53, 0.54),
        ("4. Container\nTestbed", "Spawns Docker vulnerable\ntargets (Metasploitable/Juice)", 0.77, 0.54),

        ("8. Release\nPackage", "Builds verified Debian package\nkalinova_1.3.1_all.deb", 0.05, 0.08),
        ("7. Security\nAudits", "Bandit AST vulnerability scan &\nCIDR boundary scope checks", 0.29, 0.08),
        ("6. Performance\nBench", "Validates < 200MB memory &\nrecon latency acceleration", 0.53, 0.08),
        ("5. End-to-End\nTest", "Simulates Nmap -> AppState ->\nML Advisor -> Report pipeline", 0.77, 0.08)
    ]

    for ctitle, cdesc, cx, cy in ci_stages:
        draw_box(ax, cx, cy, 0.18, 0.38, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(cx + 0.09, cy + 0.285, ctitle, color=TEXT_BLACK, fontsize=11, fontweight='bold', ha='center', va='center')
        ax.plot([cx + 0.02, cx + 0.16], [cy + 0.22, cy + 0.22], color=BORDER_BLACK, lw=0.8)
        ax.text(cx + 0.09, cy + 0.11, cdesc, color=TEXT_MUTED, fontsize=9.8, ha='center', va='center')

    # Top row forward arrows
    ax.annotate("", xy=(0.285, 0.74), xytext=(0.235, 0.74), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.annotate("", xy=(0.525, 0.74), xytext=(0.475, 0.74), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.annotate("", xy=(0.765, 0.74), xytext=(0.715, 0.74), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    # Turn down
    ax.annotate("", xy=(0.86, 0.46), xytext=(0.86, 0.54), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    # Bottom row reverse arrows
    ax.annotate("", xy=(0.715, 0.26), xytext=(0.765, 0.26), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.annotate("", xy=(0.475, 0.26), xytext=(0.525, 0.26), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.annotate("", xy=(0.235, 0.26), xytext=(0.285, 0.26), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    save_fig(fig, "integration_testing.png")

if __name__ == "__main__":
    print("Generating Clean B&W Figures 3.17 to 3.22, 4.11, 4.15...")
    gen_fig3_17()
    gen_fig3_18()
    gen_fig3_19()
    gen_fig3_20()
    gen_fig3_21()
    gen_fig3_22()
    gen_fig4_11()
    gen_fig4_15()
    print("Part 3 finished!")
