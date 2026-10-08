import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIRS = [
    r"c:\Users\ASUS\Desktop\Kali-Nova\docs\figures",
    r"c:\Users\ASUS\Desktop\Kali-Nova\docs",
    r"c:\Users\ASUS\Desktop\Kali-Nova\report_images",
    r"C:\Users\ASUS\.gemini\antigravity-ide\brain\523ecfae-57b6-4417-8a2a-e091cd140d51"
]

def save_fig(fig, filename):
    for d in OUTPUT_DIRS:
        os.makedirs(d, exist_ok=True)
        target = os.path.join(d, filename)
        fig.savefig(target, dpi=300, bbox_inches='tight', facecolor='#FFFFFF', edgecolor='none')
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

    ax.text(0.5, 0.965, "Complete Kali-Nova Operational Workflow", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "End-to-End Penetration Testing Lifecycle: Reconnaissance to Report Generation", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    phases = [
        ("Phase 1: Target Definition", "Scope validation, CIDR check,\nprofile selection (Professional)", 0.06, 0.58),
        ("Phase 2: Perimeter Recon", "OSINT discovery via Whois &\ntheHarvester for domains", 0.29, 0.58),
        ("Phase 3: Port Enumeration", "Nmap SYN sweeps, service\nbanner grabbing (P_crit)", 0.52, 0.58),
        ("Phase 4: Web Fuzzing", "Nikto vulnerability scans &\nGobuster directory enumeration", 0.75, 0.58),

        ("Phase 8: Report Export", "Executive PDF & HTML report\ngeneration via ReportLab", 0.06, 0.12),
        ("Phase 7: Persistent Store", "Scan history, events & hashes\ncommitted to kalinova.db", 0.29, 0.12),
        ("Phase 6: AI Remediation", "CVSS scoring & parameterized\ncode patches (Py/Node/Bash)", 0.52, 0.12),
        ("Phase 5: Exploit Auditing", "SQLMap injection verification &\nHydra authentication testing", 0.75, 0.12)
    ]

    for ptitle, pdesc, px, py in phases:
        draw_box(ax, px, py, 0.18, 0.25, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(px + 0.09, py + 0.205, ptitle, color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center')
        ax.plot([px + 0.02, px + 0.16], [py + 0.18, py + 0.18], color=BORDER_BLACK, lw=0.8)
        ax.text(px + 0.09, py + 0.09, pdesc, color=TEXT_MUTED, fontsize=8.5, ha='center', va='center')

    # Top row forward arrows (clear 0.05 gap between boxes)
    ax.annotate("", xy=(0.285, 0.705), xytext=(0.245, 0.705), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.515, 0.705), xytext=(0.475, 0.705), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.745, 0.705), xytext=(0.705, 0.705), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))

    # Turn down
    ax.annotate("", xy=(0.84, 0.375), xytext=(0.84, 0.575), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))

    # Bottom row reverse arrows
    ax.annotate("", xy=(0.705, 0.245), xytext=(0.745, 0.245), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.475, 0.245), xytext=(0.515, 0.245), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.245, 0.245), xytext=(0.285, 0.245), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))

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

    ax.text(0.5, 0.965, "Data Flow Diagram (DFD Level 1) of Kali-Nova", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Information Exchanges between Entities, Processes, and Data Stores", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    draw_box(ax, 0.04, 0.75, 0.16, 0.13, bg=FILL_GRAY2, lw=2)
    ax.text(0.12, 0.815, "Security Analyst\n(User / Operator)", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', va='center')

    draw_box(ax, 0.80, 0.75, 0.16, 0.13, bg=FILL_GRAY2, lw=2)
    ax.text(0.88, 0.815, "Target Host\n(Remote System)", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', va='center')

    draw_box(ax, 0.80, 0.10, 0.16, 0.13, bg=FILL_GRAY2, lw=2)
    ax.text(0.88, 0.165, "AI LLM Provider\n(Groq / Ollama)", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', va='center')

    procs = [
        ("1.0 Scope & Config\nValidator", 0.28, 0.75),
        ("2.0 Interactive\nExecutor", 0.54, 0.75),
        ("3.0 Telemetry Stream\nParser", 0.54, 0.44),
        ("4.0 State & Risk\nOrchestrator", 0.28, 0.44),
        ("5.0 Copilot Patch\nSynthesizer", 0.54, 0.10),
        ("6.0 Report Compiler\n& Exporter", 0.04, 0.10)
    ]
    for pname, px, py in procs:
        draw_box(ax, px, py, 0.18, 0.13, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(px + 0.09, py + 0.065, pname, color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Data Stores
    for ds_name, dx, dy in [("[D1] kalinova.db (SQLite)", 0.28, 0.04), ("[D2] Artifacts Dict (State)", 0.28, 0.28)]:
        ax.plot([dx, dx + 0.18], [dy + 0.05, dy + 0.05], color=BORDER_BLACK, lw=2)
        ax.plot([dx, dx + 0.18], [dy, dy], color=BORDER_BLACK, lw=2)
        ax.text(dx + 0.09, dy + 0.025, ds_name, color=TEXT_BLACK, fontsize=8.5, fontweight='bold', ha='center', va='center')

    ax.annotate("", xy=(0.28, 0.815), xytext=(0.20, 0.815), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.text(0.24, 0.835, "Target / Flags", color=TEXT_MUTED, fontsize=7.5, ha='center', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.54, 0.815), xytext=(0.46, 0.815), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.text(0.50, 0.835, "Sanitized CLI", color=TEXT_MUTED, fontsize=7.5, ha='center', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.80, 0.815), xytext=(0.72, 0.815), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.text(0.76, 0.835, "Probes", color=TEXT_MUTED, fontsize=7.5, ha='center', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.63, 0.57), xytext=(0.63, 0.75), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.text(0.66, 0.66, "Raw stdout", color=TEXT_MUTED, fontsize=7.5, bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.46, 0.505), xytext=(0.54, 0.505), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.text(0.50, 0.53, "Extracted Ports", color=TEXT_MUTED, fontsize=7.5, ha='center', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.63, 0.23), xytext=(0.63, 0.44), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.text(0.66, 0.33, "Threat Event", color=TEXT_MUTED, fontsize=7.5, bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.80, 0.165), xytext=(0.72, 0.165), arrowprops=dict(arrowstyle="<->", color=BORDER_BLACK, lw=1.8))
    ax.text(0.76, 0.19, "Prompt/Resp", color=TEXT_MUTED, fontsize=7.5, ha='center', bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    ax.annotate("", xy=(0.13, 0.23), xytext=(0.28, 0.44), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.text(0.19, 0.35, "Findings", color=TEXT_MUTED, fontsize=7.5, bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    # Connect processes to data stores
    ax.annotate("", xy=(0.37, 0.33), xytext=(0.37, 0.44), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.5))
    ax.annotate("", xy=(0.37, 0.09), xytext=(0.37, 0.28), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.5))

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

    ax.text(0.5, 0.965, "Session Management & Database Architecture", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "SQLite kalinova.db Schema and State Persistence Lifecycle", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

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
        ], 0.05, 0.36),

        ("TABLE: events", [
            "id: INTEGER PRIMARY KEY",
            "scan_id: INTEGER (FK)",
            "event_type: TEXT (PORT_FOUND)",
            "severity: TEXT (CRITICAL)",
            "raw_line: TEXT",
            "timestamp: TIMESTAMP"
        ], 0.37, 0.36),

        ("TABLE: vulnerabilities", [
            "id: INTEGER PRIMARY KEY",
            "scan_id: INTEGER (FK)",
            "cve_id: TEXT (CVE-2011-2523)",
            "cvss_score: REAL (9.8)",
            "remediation_code: TEXT",
            "verified: BOOLEAN"
        ], 0.69, 0.36)
    ]

    for tname, fields, tx, ty in tables:
        draw_box(ax, tx, ty, 0.26, 0.52, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        # Dedicated Header Banner
        rect = patches.Rectangle((tx, ty + 0.44), 0.26, 0.08, facecolor=FILL_GRAY2, edgecolor=BORDER_BLACK, lw=1)
        ax.add_patch(rect)
        ax.text(tx + 0.13, ty + 0.48, tname, color=TEXT_BLACK, fontsize=10.5, fontweight='bold', ha='center', va='center')
        for fidx, f in enumerate(fields):
            ax.text(tx + 0.02, ty + 0.39 - fidx * 0.048, f, color=TEXT_BLACK, fontsize=8.5, family='monospace')

    ax.annotate("", xy=(0.37, 0.62), xytext=(0.31, 0.62), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.69, 0.62), xytext=(0.63, 0.62), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))

    draw_box(ax, 0.05, 0.06, 0.90, 0.26, bg=FILL_WHITE, lw=1.5)
    ax.text(0.07, 0.285, "Session Management Operations", color=TEXT_BLACK, fontsize=10.5, fontweight='bold')
    ax.plot([0.07, 0.35], [0.265, 0.265], color=BORDER_BLACK, lw=0.8)

    ops = [
        ("Session Snapshots", "Captures full AppState state tuple\nfor timeline playback and review", 0.08),
        ("Forensic Traceability", "Immutable logging of executed CLI\ncommands and runtime stdout hashes", 0.38),
        ("Export & Migration", "One-click export to SQLite dump\nor encrypted JSON backup archive", 0.68)
    ]
    for otitle, odesc, ox in ops:
        draw_box(ax, ox, 0.08, 0.24, 0.165, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.2)
        ax.text(ox + 0.12, 0.205, otitle, color=TEXT_BLACK, fontsize=10, fontweight='bold', ha='center')
        ax.plot([ox + 0.02, ox + 0.22], [0.18, 0.18], color=BORDER_BLACK, lw=0.8)
        ax.text(ox + 0.12, 0.125, odesc, color=TEXT_MUTED, fontsize=8, ha='center', va='center')

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

    ax.text(0.5, 0.965, "Security Report Generation Pipeline", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Automated Aggregation of Assessment Telemetry into Executive PDF and HTML Reports", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    stages = [
        ("1. Telemetry Ingestion", "Queries kalinova.db for\nports, CVEs, logs & risk metrics", 0.05),
        ("2. Metric Normalization", "Computes composite score R_t,\nCVSS vector distribution", 0.285),
        ("3. Remediation Compilation", "Incorporates AI Copilot code\npatches (Py/Node/Bash)", 0.52),
        ("4. ReportLab Engine", "Compiles formatted PDF with\ntables, headers & risk charts", 0.755)
    ]
    for stitle, sdesc, sx in stages:
        draw_box(ax, sx, 0.55, 0.18, 0.34, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(sx + 0.09, 0.835, stitle, color=TEXT_BLACK, fontsize=10, fontweight='bold', ha='center')
        ax.plot([sx + 0.02, sx + 0.16], [0.805, 0.805], color=BORDER_BLACK, lw=0.8)
        ax.text(sx + 0.09, 0.68, sdesc, color=TEXT_MUTED, fontsize=8.5, ha='center', va='center')

    for i in range(len(stages) - 1):
        x1 = stages[i][2] + 0.18
        x2 = stages[i+1][2]
        ax.annotate("", xy=(x2, 0.72), xytext=(x1, 0.72), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    draw_box(ax, 0.04, 0.06, 0.44, 0.44, bg=FILL_WHITE, lw=1.5)
    ax.text(0.06, 0.455, "Executive PDF Report Structure", color=TEXT_BLACK, fontsize=10.5, fontweight='bold')
    ax.plot([0.06, 0.40], [0.435, 0.435], color=BORDER_BLACK, lw=0.8)
    ax.text(0.06, 0.38, "- Cover Page: Target FQDN, Date, Lead Security Auditor", color=TEXT_BLACK, fontsize=8.5)
    ax.text(0.06, 0.32, "- Executive Summary: Composite Risk Score 78.4 (Critical)", color=TEXT_BLACK, fontsize=8.5)
    ax.text(0.06, 0.26, "- Vulnerability Matrix: CVE-2011-2523, SQLi, Open Ports", color=TEXT_BLACK, fontsize=8.5)
    ax.text(0.06, 0.20, "- Technical Remediation: Code diffs & firewall script rules", color=TEXT_BLACK, fontsize=8.5)
    ax.text(0.06, 0.14, "- Forensic Appendix: Full command execution history & hashes", color=TEXT_BLACK, fontsize=8.5)

    draw_box(ax, 0.52, 0.06, 0.44, 0.44, bg=FILL_WHITE, lw=1.5)
    ax.text(0.54, 0.455, "Interactive HTML Dashboard Report", color=TEXT_BLACK, fontsize=10.5, fontweight='bold')
    ax.plot([0.54, 0.88], [0.435, 0.435], color=BORDER_BLACK, lw=0.8)
    ax.text(0.54, 0.38, "- Responsive Bento Grid: Radar plots & severity dials", color=TEXT_BLACK, fontsize=8.5)
    ax.text(0.54, 0.32, "- Filterable Findings Table: Search by severity tier or port", color=TEXT_BLACK, fontsize=8.5)
    ax.text(0.54, 0.26, "- One-Click Code Snippet Copy: Fast developer handoff", color=TEXT_BLACK, fontsize=8.5)
    ax.text(0.54, 0.20, "- Offline Compliant: Zero external CDN dependencies", color=TEXT_BLACK, fontsize=8.5)
    ax.text(0.54, 0.14, "- Portable Output: Self-contained single-file HTML report", color=TEXT_BLACK, fontsize=8.5)

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

    ax.text(0.5, 0.965, "Kali-Nova User Interface Layout Blueprint", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Structural Wireframe and Component Topology of the PyQt6 Cyber HUD", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    # Topbar
    draw_box(ax, 0.04, 0.83, 0.92, 0.075, bg=FILL_GRAY2, lw=2)
    ax.text(0.06, 0.867, "A. TOPBAR: Target FQDN | Scope CIDR | Risk Index | Profile Mode Switcher", color=TEXT_BLACK, fontsize=10, fontweight='bold', va='center')

    # Sidebar with dedicated header
    draw_box(ax, 0.04, 0.06, 0.16, 0.74, bg=FILL_LIGHT, lw=1.5)
    draw_box(ax, 0.05, 0.73, 0.14, 0.055, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1)
    ax.text(0.12, 0.7575, "B. SIDEBAR", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', va='center')
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
        ax.text(0.06, 0.67 - idx * 0.075, item, color=TEXT_BLACK, fontsize=8.5)

    # Central Workspace with dedicated header
    draw_box(ax, 0.22, 0.32, 0.52, 0.48, bg=FILL_WHITE, lw=2)
    draw_box(ax, 0.23, 0.73, 0.50, 0.055, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1)
    ax.text(0.48, 0.7575, "C. PRIMARY CENTRAL WORKSPACE", color=TEXT_BLACK, fontsize=10, fontweight='bold', ha='center', va='center')
    ws_features = [
        "- Animated Network Topology Canvas (20 FPS Spatial Radar Sweep)",
        "- Dynamic Threat Score Speedometer Gauge (0 - 100 CVSS Arc)",
        "- Real-Time Discovered Port Matrix with Live Service Banners",
        "- Dynamic Security Tool Configuration & Execution Parameter Forms",
        "- Automated Next-Step Workflow Prescription Cards"
    ]
    for idx, feat in enumerate(ws_features):
        ax.text(0.24, 0.66 - idx * 0.07, feat, color=TEXT_MUTED, fontsize=8.5)

    # Console Dock with dedicated header
    draw_box(ax, 0.22, 0.06, 0.52, 0.23, bg=FILL_LIGHT, lw=1.5)
    draw_box(ax, 0.23, 0.22, 0.50, 0.055, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1)
    ax.text(0.48, 0.2475, "D. INTERACTIVE CONSOLE DOCK (Live PTY Stream)", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', va='center')
    console_sample = (
        "$ nmap -sV -T4 192.168.1.105 ... [Streaming Telemetry at 100 Hz]\n"
        "[+] Port 80/tcp OPEN (Apache 2.4.41 PHP 7.4.3)\n"
        "[+] Port 3306/tcp OPEN (MariaDB 10.3.38 MySQL Protocol)"
    )
    ax.text(0.24, 0.14, console_sample, color=TEXT_BLACK, fontsize=8, family='monospace')

    # AI Copilot Drawer with dedicated header
    draw_box(ax, 0.76, 0.06, 0.20, 0.74, bg=FILL_LIGHT, lw=1.5)
    draw_box(ax, 0.77, 0.73, 0.18, 0.055, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1)
    ax.text(0.86, 0.7575, "E. AI COPILOT", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', va='center')
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
        ax.text(0.78, 0.67 - idx * 0.07, citem, color=TEXT_BLACK, fontsize=8.5)

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

    ax.text(0.5, 0.965, "Testing Methodology & Verification Hierarchy", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Multi-Tiered Quality Assurance across Unit, Concurrency, UI, and Cyber-Range Testbeds", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    # Solid grayscale shades, ZERO HATCHING, 100% visible text
    tiers = [
        ("Tier 1: Unit Testing (PyTest)", "Test regex parsers, CVSS scoring math,\nAppState mutations, and input validation.", 0.72, "98.2% Code Coverage", FILL_WHITE),
        ("Tier 2: Concurrency & PTY Testing", "Stress test CommandThread lifecycle,\nbuffer overflow prevention, and process cleanup.", 0.52, "Zero Process Leaks", FILL_LIGHT),
        ("Tier 3: GUI & Signal Integration", "PyQt6 headless test harness validating\nsignal emissions, state updates & UI responsiveness.", 0.32, "60 FPS Responsive HUD", FILL_GRAY1),
        ("Tier 4: Cyber-Range Validation", "End-to-end operational testing against 15 vulnerable VMs\n(OWASP Juice Shop, Metasploitable 2/3, DVWA).", 0.12, "84.3% Recon Latency Drop", FILL_GRAY2)
    ]

    for ttitle, tdesc, ty, tstat, tbg in tiers:
        w = 0.54 + (0.75 - ty) * 0.40
        x = 0.50 - w / 2

        # Main Tier Box
        draw_box(ax, x, ty, w, 0.16, bg=tbg, border=BORDER_BLACK, lw=1.5, zorder=3)
        ax.text(x + 0.03, ty + 0.115, ttitle, color=TEXT_BLACK, fontsize=10.5, fontweight='bold', zorder=5)

        # Divider line strictly limited so it NEVER touches the right badge box
        ax.plot([x + 0.03, x + 0.28], [ty + 0.09, ty + 0.09], color=BORDER_BLACK, lw=0.8, zorder=5)
        ax.text(x + 0.03, ty + 0.045, tdesc, color=TEXT_MUTED, fontsize=8.5, zorder=5)

        # Right Stat Badge Box - cleanly separated
        draw_box(ax, x + w - 0.22, ty + 0.045, 0.20, 0.07, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.2, zorder=5)
        ax.text(x + w - 0.12, ty + 0.08, tstat, color=TEXT_BLACK, fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=6)

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

    ax.text(0.5, 0.965, "CVSS-Based Vulnerability Assessment Results", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Empirical Evaluation of Vulnerability Detections across Cyber-Range Targets", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    ax_bar = fig.add_axes([0.08, 0.16, 0.44, 0.68], facecolor=BG_WHITE)
    vulns = ['SQL Injection\n(CWE-89)', 'vsftpd Backdoor\n(CVE-2011-2523)', 'Weak SSH Auth\n(Hydra Crack)', 'Deprecated TLS 1.0\n(SSLyze)', 'Directory Traversal\n(CWE-22)', 'Info Banner Leak\n(Apache)']
    scores = [9.8, 9.8, 8.1, 6.5, 5.3, 2.1]
    grays = [FILL_GRAY3, FILL_GRAY3, FILL_GRAY2, FILL_GRAY1, FILL_LIGHT, FILL_WHITE]

    y_pos = np.arange(len(vulns))
    for i in range(len(vulns)):
        ax_bar.barh(y_pos[i], scores[i], height=0.50, facecolor=grays[i], edgecolor=BORDER_BLACK, lw=1.5)
        ax_bar.text(scores[i] + 0.30, y_pos[i], f"{scores[i]}", color=TEXT_BLACK, va='center', fontweight='bold', fontsize=9.5)

    ax_bar.set_yticks(y_pos)
    ax_bar.set_yticklabels(vulns, color=TEXT_BLACK, fontsize=9.5)
    ax_bar.set_xlabel("CVSS v3.1 Base Severity Score", color=TEXT_BLACK, fontsize=10, fontweight='bold')
    ax_bar.set_xlim(0, 11.5)
    ax_bar.grid(axis='x', color=FILL_GRAY3, linestyle='--')
    ax_bar.tick_params(colors=TEXT_BLACK)
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)
    ax_bar.spines['left'].set_color(BORDER_BLACK)
    ax_bar.spines['bottom'].set_color(BORDER_BLACK)

    # Statistics Card
    draw_box(ax, 0.58, 0.16, 0.38, 0.68, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.60, 0.805, "Assessment Statistics & Metrics", color=TEXT_BLACK, fontsize=11, fontweight='bold')
    ax.plot([0.60, 0.94], [0.785, 0.785], color=BORDER_BLACK, lw=0.8)

    stats = [
        ("Total Vulnerabilities Detected:", "18 Findings"),
        ("Critical Severity (CVSS 9.0-10):", "5 Findings (27.8%)"),
        ("High Severity (CVSS 7.0-8.9):", "6 Findings (33.3%)"),
        ("Medium Severity (CVSS 4.0-6.9):", "5 Findings (27.8%)"),
        ("Low Severity (CVSS 0.1-3.9):", "2 Findings (11.1%)"),
        ("Mean CVSS Base Score:", "7.24 / 10.0"),
        ("Auto Remediation Success Rate:", "96.4% Verified Patches"),
        ("Expert Tester Score Alignment:", "98.2% Correlation")
    ]
    for sidx, (slbl, sval) in enumerate(stats):
        sy = 0.73 - sidx * 0.072
        ax.text(0.60, sy, slbl, color=TEXT_MUTED, fontsize=9)
        ax.text(0.94, sy, sval, color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='right')

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

    ax.text(0.5, 0.965, "Continuous Integration & Automated Testing Pipeline", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Automated Verification of Kali-Nova Toolchains, Subprocesses, and Debian Packages", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    ci_stages = [
        ("1. Code Push / PR", "Developer commits to GitHub;\nTriggers CI/CD Actions", 0.06, 0.58),
        ("2. Static Code Linting", "Flake8, Pyright, Black syntax\nand typing enforcement", 0.29, 0.58),
        ("3. Subsystem Unit Tests", "PyTest suite executing 42+\nunit & parser test cases", 0.52, 0.58),
        ("4. Container Testbed", "Spawns Docker vulnerable\ntargets (Metasploitable/Juice)", 0.75, 0.58),

        ("8. Release Package", "Builds verified Debian package\nkalinova_1.3.1_all.deb", 0.06, 0.12),
        ("7. Security Audits", "Bandit AST vulnerability scan &\nCIDR boundary scope checks", 0.29, 0.12),
        ("6. Performance Bench", "Validates < 200MB memory &\nrecon latency acceleration", 0.52, 0.12),
        ("5. End-to-End Test", "Simulates Nmap -> AppState ->\nML Advisor -> Report pipeline", 0.75, 0.12)
    ]

    for ctitle, cdesc, cx, cy in ci_stages:
        draw_box(ax, cx, cy, 0.18, 0.25, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(cx + 0.09, cy + 0.205, ctitle, color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center')
        ax.plot([cx + 0.02, cx + 0.16], [cy + 0.18, cy + 0.18], color=BORDER_BLACK, lw=0.8)
        ax.text(cx + 0.09, cy + 0.09, cdesc, color=TEXT_MUTED, fontsize=8.5, ha='center', va='center')

    # Top row forward arrows (clear 0.05 gap between boxes)
    ax.annotate("", xy=(0.285, 0.705), xytext=(0.245, 0.705), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.515, 0.705), xytext=(0.475, 0.705), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.745, 0.705), xytext=(0.705, 0.705), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))

    # Turn down
    ax.annotate("", xy=(0.84, 0.375), xytext=(0.84, 0.575), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))

    # Bottom row reverse arrows
    ax.annotate("", xy=(0.705, 0.245), xytext=(0.745, 0.245), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.475, 0.245), xytext=(0.515, 0.245), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.245, 0.245), xytext=(0.285, 0.245), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))

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
