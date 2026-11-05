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
        # 160 DPI gives razor-sharp rendering when scaled in LaTeX reports
        png_target = os.path.join(d, f"{base_name}.png")
        fig.savefig(png_target, dpi=160, bbox_inches='tight', facecolor='#FFFFFF', edgecolor='none')
        
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
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.015",
                                 facecolor=bg, edgecolor=border, linewidth=lw, linestyle=ls, hatch=hatch, zorder=zorder)
    ax.add_patch(box)
    return box

# ==========================================
# 17. Figure 3.17: Complete Kali-Nova System Workflow
# ==========================================
def gen_fig3_17():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    phases = [
        ("Phase 1:\nTarget Scope", "Scope validation,\nCIDR verify &\nprofile selection", 0.045, 0.54),
        ("Phase 2:\nPerimeter Recon", "OSINT discovery\nvia Whois &\ntheHarvester", 0.285, 0.54),
        ("Phase 3:\nPort Discovery", "Nmap SYN sweeps,\nservice banner\ngrab (P_crit)", 0.525, 0.54),
        ("Phase 4:\nWeb Fuzzing", "Nikto web audits\n& Gobuster path\nenumeration", 0.765, 0.54),

        ("Phase 8:\nReport Export", "Executive PDF\n& HTML reports\nvia ReportLab", 0.045, 0.08),
        ("Phase 7:\nAudit Store", "Scan history,\nevents & hashes\nin kalinova.db", 0.285, 0.08),
        ("Phase 6:\nAI Remediation", "CVSS scoring &\ncode patches\n(Py/Node/Bash)", 0.525, 0.08),
        ("Phase 5:\nExploit Audit", "SQLMap injection\n& Hydra login\ncredential tests", 0.765, 0.08)
    ]

    for ptitle, pdesc, px, py in phases:
        draw_box(ax, px, py, 0.19, 0.38, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(px + 0.095, py + 0.295, ptitle, color=TEXT_BLACK, fontsize=12.5, fontweight='bold', ha='center', va='center')
        ax.plot([px + 0.02, px + 0.17], [ny := py + 0.22, ny], color=BORDER_BLACK, lw=0.8)
        ax.text(px + 0.095, py + 0.110, pdesc, color=TEXT_MUTED, fontsize=11.2, ha='center', va='center')

    # Top row forward arrows
    ax.annotate("", xy=(0.280, 0.73), xytext=(0.240, 0.73), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.520, 0.73), xytext=(0.480, 0.73), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.760, 0.73), xytext=(0.720, 0.73), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

    # Turn down
    ax.annotate("", xy=(0.86, 0.46), xytext=(0.86, 0.54), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

    # Bottom row reverse arrows
    ax.annotate("", xy=(0.720, 0.27), xytext=(0.760, 0.27), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.480, 0.27), xytext=(0.520, 0.27), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.240, 0.27), xytext=(0.280, 0.27), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

    save_fig(fig, "complete_workflow.png")

# ==========================================
# 18. Figure 3.18: Data Flow Diagram of Kali-Nova
# ==========================================
def gen_fig3_18():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # External Entities
    draw_box(ax, 0.02, 0.77, 0.145, 0.16, bg=FILL_GRAY2, lw=2)
    ax.text(0.0925, 0.850, "Security Analyst\n(Operator)", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')

    draw_box(ax, 0.835, 0.77, 0.145, 0.16, bg=FILL_GRAY2, lw=2)
    ax.text(0.9075, 0.850, "Target Host\n(Remote)", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')

    draw_box(ax, 0.835, 0.08, 0.145, 0.16, bg=FILL_GRAY2, lw=2)
    ax.text(0.9075, 0.160, "AI LLM Provider\n(Groq / Mistral)", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')

    # Processes
    procs = [
        ("1.0 Scope & Config\nValidator", 0.295, 0.77),
        ("2.0 Interactive\nExecutor", 0.575, 0.77),
        ("3.0 Telemetry\nStream Parser", 0.575, 0.43),
        ("4.0 State & Risk\nOrchestrator", 0.22, 0.43),
        ("5.0 Copilot Patch\nSynthesizer", 0.575, 0.08),
        ("6.0 Report Engine\n& Exporter", 0.02, 0.08)
    ]
    for pname, px, py in procs:
        draw_box(ax, px, py, 0.155, 0.16, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(px + 0.0775, py + 0.080, pname, color=TEXT_BLACK, fontsize=11.2, fontweight='bold', ha='center', va='center')

    # Data Stores
    for ds_name, dx, dy in [("[D1] kalinova.db (SQLite)", 0.23, 0.04), ("[D2] Artifacts Dict (State)", 0.23, 0.25)]:
        ax.plot([dx, dx + 0.24], [dy + 0.065, dy + 0.065], color=BORDER_BLACK, lw=2.2)
        ax.plot([dx, dx + 0.24], [dy, dy], color=BORDER_BLACK, lw=2.2)
        ax.text(dx + 0.12, dy + 0.032, ds_name, color=TEXT_BLACK, fontsize=11.2, fontweight='bold', ha='center', va='center')

    # Top horizontal arrows & labels (cleanly in gaps)
    ax.annotate("", xy=(0.290, 0.850), xytext=(0.170, 0.850), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.text(0.230, 0.880, "Target Scope", color=TEXT_BLACK, fontsize=10.5, fontweight='bold', ha='center', va='bottom')

    ax.annotate("", xy=(0.570, 0.850), xytext=(0.455, 0.850), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.text(0.5125, 0.880, "Sanitized CLI", color=TEXT_BLACK, fontsize=10.5, fontweight='bold', ha='center', va='bottom')

    ax.annotate("", xy=(0.830, 0.850), xytext=(0.735, 0.850), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.text(0.7825, 0.880, "Probes", color=TEXT_BLACK, fontsize=10.5, fontweight='bold', ha='center', va='bottom')

    # Vertical arrow from 2.0 to 3.0
    ax.annotate("", xy=(0.6525, 0.595), xytext=(0.6525, 0.765), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.text(0.675, 0.680, "Raw stdout", color=TEXT_BLACK, fontsize=10.5, fontweight='bold', va='center')

    # Extracted Ports arrow cleanly in gap
    ax.annotate("", xy=(0.380, 0.510), xytext=(0.570, 0.510), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.text(0.475, 0.535, "Extracted Ports", color=TEXT_BLACK, fontsize=10.5, fontweight='bold', ha='center', va='bottom')

    # Vertical arrow from 3.0 to 5.0
    ax.annotate("", xy=(0.6525, 0.245), xytext=(0.6525, 0.425), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.text(0.675, 0.335, "Threat Event", color=TEXT_BLACK, fontsize=10.5, fontweight='bold', va='center')

    # Bottom right prompt/resp
    ax.annotate("", xy=(0.830, 0.160), xytext=(0.735, 0.160), arrowprops=dict(arrowstyle="<->", color=BORDER_BLACK, lw=2.2))
    ax.text(0.7825, 0.185, "Prompt / Resp", color=TEXT_BLACK, fontsize=10.5, fontweight='bold', ha='center', va='bottom')

    # Findings arrow from 4.0 to 6.0
    ax.annotate("", xy=(0.11, 0.245), xytext=(0.23, 0.425), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.text(0.135, 0.355, "Findings", color=TEXT_BLACK, fontsize=10.5, fontweight='bold', va='center')

    # Connect processes to data stores
    ax.annotate("", xy=(0.29, 0.320), xytext=(0.29, 0.425), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.0))
    ax.annotate("", xy=(0.29, 0.110), xytext=(0.29, 0.245), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.0))

    save_fig(fig, "data_flow_diagram.png")

# ==========================================
# 19. Figure 3.19: Session Management Module
# ==========================================
def gen_fig3_19():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    tables = [
        ("TABLE: scans", [
            "id: INTEGER PRIMARY KEY",
            "session_uuid: TEXT",
            "tool_name: TEXT (nmap)",
            "target: TEXT (.105)",
            "start_time: TIMESTAMP",
            "end_time: TIMESTAMP",
            "status: TEXT (DONE)",
            "exit_code: INTEGER"
        ], 0.04, 0.34),

        ("TABLE: events", [
            "id: INTEGER PRIMARY KEY",
            "scan_id: INTEGER (FK)",
            "event: TEXT (PORT_FOUND)",
            "severity: TEXT (CRIT)",
            "raw_line: TEXT",
            "timestamp: TIMESTAMP"
        ], 0.36, 0.34),

        ("TABLE: vulnerabilities", [
            "id: INTEGER PRIMARY KEY",
            "scan_id: INTEGER (FK)",
            "cve_id: TEXT (CVE-2011)",
            "cvss_score: REAL (9.8)",
            "remediation_code: TEXT",
            "verified: BOOLEAN"
        ], 0.68, 0.34)
    ]

    for tname, fields, tx, ty in tables:
        draw_box(ax, tx, ty, 0.28, 0.60, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        # Dedicated Header Banner
        rect = patches.Rectangle((tx, ty + 0.51), 0.28, 0.09, facecolor=FILL_GRAY2, edgecolor=BORDER_BLACK, lw=1.2)
        ax.add_patch(rect)
        ax.text(tx + 0.14, ty + 0.555, tname, color=TEXT_BLACK, fontsize=13.0, fontweight='bold', ha='center', va='center')
        for fidx, f in enumerate(fields):
            ax.text(tx + 0.02, ty + 0.455 - fidx * 0.058, f, color=TEXT_BLACK, fontsize=10.5, family='monospace')

    # Connect table headers cleanly in the gap
    ax.annotate("", xy=(0.355, 0.895), xytext=(0.325, 0.895), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.675, 0.895), xytext=(0.645, 0.895), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

    # Bottom Operations Box
    draw_box(ax, 0.05, 0.04, 0.90, 0.26, bg=FILL_WHITE, lw=1.5)
    ax.text(0.07, 0.255, "Session Management Operations", color=TEXT_BLACK, fontsize=13.5, fontweight='bold')
    ax.plot([0.07, 0.40], [0.235, 0.235], color=BORDER_BLACK, lw=1.2)

    ops = [
        ("Session Snapshots", "Captures full AppState\nstate tuple for timeline\nplayback and review", 0.08),
        ("Forensic Traceability", "Immutable logging of\nexecuted CLI commands\nand runtime stdout hashes", 0.38),
        ("Export & Migration", "One-click export to\nSQLite dump or encrypted\nJSON backup archive", 0.68)
    ]
    for otitle, odesc, ox in ops:
        draw_box(ax, ox, 0.055, 0.24, 0.170, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.2)
        ax.text(ox + 0.12, 0.190, otitle, color=TEXT_BLACK, fontsize=12.2, fontweight='bold', ha='center', va='center')
        ax.plot([ox + 0.02, ox + 0.22], [0.168, 0.168], color=BORDER_BLACK, lw=0.8)
        ax.text(ox + 0.12, 0.110, odesc, color=TEXT_MUTED, fontsize=10.2, ha='center', va='center')

    save_fig(fig, "session_management.png")

# ==========================================
# 20. Figure 3.20: Security Report Generation
# ==========================================
def gen_fig3_20():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    stages = [
        ("1. Telemetry\nIngestion", "Queries kalinova.db\nfor ports, CVEs,\nlogs & risk metrics", 0.04),
        ("2. Metric\nNormalization", "Computes composite\nscore R_t, and CVSS\nvector distribution", 0.28),
        ("3. Remediation\nCompilation", "Incorporates AI\nCopilot code patches\n(Py / Node / Bash)", 0.52),
        ("4. ReportLab\nEngine", "Compiles formatted\nPDF with tables,\nheaders & risk charts", 0.76)
    ]
    for stitle, sdesc, sx in stages:
        draw_box(ax, sx, 0.52, 0.20, 0.42, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(sx + 0.10, 0.86, stitle, color=TEXT_BLACK, fontsize=12.5, fontweight='bold', ha='center', va='center')
        ax.plot([sx + 0.02, sx + 0.18], [0.795, 0.795], color=BORDER_BLACK, lw=0.8)
        ax.text(sx + 0.10, 0.645, sdesc, color=TEXT_MUTED, fontsize=10.5, ha='center', va='center')

    for i in range(len(stages) - 1):
        x1 = stages[i][2] + 0.20 + 0.005
        x2 = stages[i+1][2] - 0.005
        ax.annotate("", xy=(x2, 0.76), xytext=(x1, 0.76), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

    draw_box(ax, 0.04, 0.04, 0.44, 0.44, bg=FILL_WHITE, lw=1.5)
    ax.text(0.06, 0.435, "Executive PDF Report Structure", color=TEXT_BLACK, fontsize=13.8, fontweight='bold')
    ax.plot([0.06, 0.44], [0.410, 0.410], color=BORDER_BLACK, lw=1.2)
    ax.text(0.06, 0.35, "- Cover Page: Target FQDN, Date, Lead Auditor", color=TEXT_BLACK, fontsize=11.2)
    ax.text(0.06, 0.28, "- Executive Summary: Composite Risk Score 78.4", color=TEXT_BLACK, fontsize=11.2)
    ax.text(0.06, 0.21, "- Vulnerability Matrix: CVE-2011-2523, SQLi, Ports", color=TEXT_BLACK, fontsize=11.2)
    ax.text(0.06, 0.14, "- Technical Remediation: Code diffs & WAF rules", color=TEXT_BLACK, fontsize=11.2)
    ax.text(0.06, 0.07, "- Forensic Appendix: Command history & hashes", color=TEXT_BLACK, fontsize=11.2)

    draw_box(ax, 0.52, 0.04, 0.44, 0.44, bg=FILL_WHITE, lw=1.5)
    ax.text(0.54, 0.435, "Interactive HTML Dashboard Report", color=TEXT_BLACK, fontsize=13.8, fontweight='bold')
    ax.plot([0.54, 0.92], [0.410, 0.410], color=BORDER_BLACK, lw=1.2)
    ax.text(0.54, 0.35, "- Responsive Bento Grid: Radar plots & severity dials", color=TEXT_BLACK, fontsize=11.0)
    ax.text(0.54, 0.28, "- Filterable Findings: Search by severity or port", color=TEXT_BLACK, fontsize=11.0)
    ax.text(0.54, 0.21, "- Code Snippets: One-click patch copy for developers", color=TEXT_BLACK, fontsize=11.0)
    ax.text(0.54, 0.14, "- Offline Compliant: Zero external CDN dependencies", color=TEXT_BLACK, fontsize=11.0)
    ax.text(0.54, 0.07, "- Portable Output: Self-contained single-file HTML", color=TEXT_BLACK, fontsize=11.0)

    save_fig(fig, "report_generation.png")

# ==========================================
# 21. Figure 3.21: Kali-Nova User Interface Layout
# ==========================================
def gen_fig3_21():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Topbar
    draw_box(ax, 0.02, 0.905, 0.96, 0.065, bg=FILL_GRAY2, lw=2)
    ax.text(0.04, 0.9375, "A. TOPBAR: Target FQDN | Scope CIDR | Risk Index | Profile Mode Switcher", color=TEXT_BLACK, fontsize=12.2, fontweight='bold', va='center')

    # Sidebar with dedicated header
    draw_box(ax, 0.02, 0.04, 0.17, 0.845, bg=FILL_LIGHT, lw=1.5)
    draw_box(ax, 0.03, 0.825, 0.15, 0.048, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1.2)
    ax.text(0.105, 0.849, "B. SIDEBAR", color=TEXT_BLACK, fontsize=12.0, fontweight='bold', ha='center', va='center')
    nav_list = [
        "- Dashboard View",
        "- Recon (Nmap)",
        "- Web Security",
        "- Auth Resilience",
        "- Network Audits",
        "- Reports & DB",
        "- Global Settings"
    ]
    for idx, item in enumerate(nav_list):
        ax.text(0.035, 0.74 - idx * 0.095, item, color=TEXT_BLACK, fontsize=11.0, fontweight='bold')

    # Central Workspace with dedicated header
    draw_box(ax, 0.21, 0.35, 0.55, 0.535, bg=FILL_WHITE, lw=2)
    draw_box(ax, 0.22, 0.825, 0.53, 0.048, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1.2)
    ax.text(0.485, 0.849, "C. PRIMARY CENTRAL WORKSPACE", color=TEXT_BLACK, fontsize=12.5, fontweight='bold', ha='center', va='center')
    ws_features = [
        "- Animated Network Topology Canvas (20 FPS Spatial Radar Sweep)",
        "- Dynamic Threat Score Speedometer Gauge (0 - 100 CVSS Arc)",
        "- Real-Time Discovered Port Matrix with Live Service Banners",
        "- Dynamic Security Tool Configuration & Execution Parameter Forms",
        "- Automated Next-Step Workflow Prescription Cards"
    ]
    for idx, feat in enumerate(ws_features):
        ax.text(0.23, 0.74 - idx * 0.082, feat, color=TEXT_MUTED, fontsize=11.0)

    # Console Dock with dedicated header
    draw_box(ax, 0.21, 0.04, 0.55, 0.29, bg=FILL_LIGHT, lw=1.5)
    draw_box(ax, 0.22, 0.275, 0.53, 0.045, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1.2)
    ax.text(0.485, 0.2975, "D. INTERACTIVE CONSOLE DOCK (Live PTY Stream)", color=TEXT_BLACK, fontsize=12.0, fontweight='bold', ha='center', va='center')
    console_sample = (
        "$ nmap -sV -T4 192.168.1.105 [PTY Stream 100 Hz]\n"
        "[+] Port 80/tcp OPEN (Apache 2.4.41 PHP 7.4.3)\n"
        "[+] Port 3306/tcp OPEN (MariaDB 10.3.38 MySQL)"
    )
    ax.text(0.23, 0.155, console_sample, color=TEXT_BLACK, fontsize=10.5, family='monospace')

    # AI Copilot Drawer with dedicated header
    draw_box(ax, 0.78, 0.04, 0.20, 0.845, bg=FILL_LIGHT, lw=1.5)
    draw_box(ax, 0.79, 0.825, 0.18, 0.048, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1.2)
    ax.text(0.88, 0.849, "E. AI COPILOT", color=TEXT_BLACK, fontsize=12.0, fontweight='bold', ha='center', va='center')
    copilot_items = [
        "- Sliding Drawer UI",
        "- Diagnostics Pane",
        "- CVSS v3.1 Severity",
        "- Parameterized Fixes",
        "  (Python / Node.js)",
        "- 1-Click Code Copy",
        "- Diagnostic Reason"
    ]
    for idx, citem in enumerate(copilot_items):
        ax.text(0.80, 0.74 - idx * 0.085, citem, color=TEXT_BLACK, fontsize=11.0)

    save_fig(fig, "ui_layout.png")

# ==========================================
# 22. Figure 3.22: Testing Methodology
# ==========================================
def gen_fig3_22():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
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
        # Main Tier Box - Uniform 0.88 width ensures zero badge-text collision
        draw_box(ax, 0.06, ty, 0.88, 0.19, bg=tbg, border=BORDER_BLACK, lw=1.5, zorder=3)
        ax.text(0.09, ty + 0.138, ttitle, color=TEXT_BLACK, fontsize=13.5, fontweight='bold', zorder=5)

        # Divider line
        ax.plot([0.09, 0.50], [ty + 0.112, ty + 0.112], color=BORDER_BLACK, lw=1.2, zorder=5)
        ax.text(0.09, ty + 0.052, tdesc, color=TEXT_MUTED, fontsize=11.2, zorder=5)

        # Right Stat Badge Box safely on the right
        draw_box(ax, 0.69, ty + 0.052, 0.22, 0.085, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.2, zorder=5)
        ax.text(0.80, ty + 0.095, tstat, color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center', zorder=6)

    save_fig(fig, "testing_workflow.png")

# ==========================================
# 23. Figure 4.11: CVSS-Based Vulnerability Analysis
# ==========================================
def gen_fig4_11():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax_bar = fig.add_axes([0.23, 0.10, 0.26, 0.82], facecolor=BG_WHITE)
    vulns = ['SQL Injection\n(CWE-89)', 'vsftpd Backdoor\n(CVE-2011-2523)', 'Weak SSH Auth\n(Hydra Crack)', 'Deprecated TLS 1.0\n(SSLyze)', 'Directory Traversal\n(CWE-22)', 'Info Banner Leak\n(Apache)']
    scores = [9.8, 9.8, 8.1, 6.5, 5.3, 2.1]
    grays = [FILL_GRAY3, FILL_GRAY3, FILL_GRAY2, FILL_GRAY1, FILL_LIGHT, FILL_WHITE]

    y_pos = np.arange(len(vulns))
    for i in range(len(vulns)):
        ax_bar.barh(y_pos[i], scores[i], height=0.52, facecolor=grays[i], edgecolor=BORDER_BLACK, lw=1.5)
        ax_bar.text(scores[i] + 0.32, y_pos[i], f"{scores[i]}", color=TEXT_BLACK, va='center', fontweight='bold', fontsize=12.5)

    ax_bar.set_yticks(y_pos)
    ax_bar.set_yticklabels(vulns, color=TEXT_BLACK, fontsize=12.0, fontweight='bold')
    ax_bar.set_xlabel("CVSS v3.1 Base Severity Score", color=TEXT_BLACK, fontsize=13.5, fontweight='bold')
    ax_bar.set_xlim(0, 11.5)
    ax_bar.grid(axis='x', color=FILL_GRAY3, linestyle='--', lw=1.2)
    ax_bar.tick_params(colors=TEXT_BLACK, labelsize=11.5)
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)
    ax_bar.spines['left'].set_color(BORDER_BLACK)
    ax_bar.spines['bottom'].set_color(BORDER_BLACK)

    # Statistics Card
    draw_box(ax, 0.52, 0.08, 0.45, 0.86, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.54, 0.895, "Assessment Statistics & Metrics", color=TEXT_BLACK, fontsize=14.0, fontweight='bold')
    ax.plot([0.54, 0.95], [0.868, 0.868], color=BORDER_BLACK, lw=1.2)

    stats = [
        ("Total Vulnerabilities Detected:", "18 Findings"),
        ("Critical Severity (9.0 - 10.0):", "5 Findings (27.8%)"),
        ("High Severity (7.0 - 8.9):", "6 Findings (33.3%)"),
        ("Medium Severity (4.0 - 6.9):", "5 Findings (27.8%)"),
        ("Low Severity (0.1 - 3.9):", "2 Findings (11.1%)"),
        ("Mean CVSS Base Score:", "7.24 / 10.0"),
        ("Auto Remediation Success:", "96.4% Verified"),
        ("Expert Tester Alignment:", "98.2% Correlation")
    ]
    for sidx, (slbl, sval) in enumerate(stats):
        sy = 0.80 - sidx * 0.085
        ax.text(0.54, sy, slbl, color=TEXT_MUTED, fontsize=11.0)
        ax.text(0.95, sy, sval, color=TEXT_BLACK, fontsize=11.2, fontweight='bold', ha='right')
        sy = 0.80 - sidx * 0.085
        ax.text(0.56, sy, slbl, color=TEXT_MUTED, fontsize=11.8)
        ax.text(0.93, sy, sval, color=TEXT_BLACK, fontsize=12.2, fontweight='bold', ha='right')

    save_fig(fig, "cvss_result.png")

# ==========================================
# 24. Figure 4.15: Integration Testing Workflow
# ==========================================
def gen_fig4_15():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ci_stages = [
        ("1. Code Push\n/ PR", "Developer commits\nto GitHub; triggers\nCI/CD Actions", 0.045, 0.54),
        ("2. Static Code\nLinting", "Flake8, Pyright,\nBlack syntax and\ntyping enforcement", 0.285, 0.54),
        ("3. Subsystem\nUnit Tests", "PyTest suite with\n42+ unit & parser\ntest cases", 0.525, 0.54),
        ("4. Container\nTestbed", "Docker vulnerable\ntarget containers\n(Metasploit/Juice)", 0.765, 0.54),

        ("8. Release\nPackage", "Builds verified\nDebian package\nkalinova_1.3.1_all", 0.045, 0.08),
        ("7. Security\nAudits", "Bandit AST scans\n& CIDR boundary\nscope verification", 0.285, 0.08),
        ("6. Performance\nBench", "Validates < 200MB\nRAM & accelerated\nrecon latency", 0.525, 0.08),
        ("5. End-to-End\nTest", "Simulates Nmap ->\nAppState -> ML\nAdvisor pipeline", 0.765, 0.08)
    ]

    for ctitle, cdesc, cx, cy in ci_stages:
        draw_box(ax, cx, cy, 0.19, 0.38, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(cx + 0.095, cy + 0.295, ctitle, color=TEXT_BLACK, fontsize=12.5, fontweight='bold', ha='center', va='center')
        ax.plot([cx + 0.02, cx + 0.17], [ny := cy + 0.22, ny], color=BORDER_BLACK, lw=0.8)
        ax.text(cx + 0.095, cy + 0.110, cdesc, color=TEXT_MUTED, fontsize=11.2, ha='center', va='center')

    # Top row forward arrows
    ax.annotate("", xy=(0.280, 0.73), xytext=(0.240, 0.73), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.520, 0.73), xytext=(0.480, 0.73), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.760, 0.73), xytext=(0.720, 0.73), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

    # Turn down
    ax.annotate("", xy=(0.86, 0.46), xytext=(0.86, 0.54), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

    # Bottom row reverse arrows
    ax.annotate("", xy=(0.720, 0.27), xytext=(0.760, 0.27), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.480, 0.27), xytext=(0.520, 0.27), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.240, 0.27), xytext=(0.280, 0.27), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

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
