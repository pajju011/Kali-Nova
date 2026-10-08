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

def draw_card(ax, x, y, w, h, title="", bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5, ls='-', hatch=None):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.02",
                                 facecolor=bg, edgecolor=border, linewidth=lw, linestyle=ls, hatch=hatch, zorder=2)
    ax.add_patch(box)
    if title:
        ax.text(x + 0.02*w, y + h - 0.04, title, color=TEXT_BLACK, fontsize=10.5, fontweight='bold', va='top', zorder=4)
    return box

# ==========================================
# 1. Figure 3.1: Overall Architecture of Kali-Nova
# ==========================================
def gen_fig3_1():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "Kali-Nova: Overall System Architecture", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.925, "Decoupled Three-Tier Architecture for Autonomous Threat Modeling & Security Orchestration", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    # Tier 1: Presentation
    draw_card(ax, 0.03, 0.65, 0.94, 0.24, "1. PRESENTATION LAYER (PyQt6 Cyber HUD)", bg=FILL_LIGHT, lw=2)
    p_mods = [
        ("Navigation Sidebar", "Recon, Web, Auth,\nNetwork, Reports", 0.05),
        ("Master Bento Dashboard", "Threat Radar, Risk Gauge,\nPort Matrix, Scan History", 0.235),
        ("Tool Workspaces", "Dynamic Parameter Forms,\nScope CIDR Validation", 0.42),
        ("Interactive Console", "PTY Live Telemetry Stream,\nANSI Highlighting, Stdin", 0.605),
        ("AI Copilot Drawer", "CVSS Diagnostics, Patches\nPython / Node.js Remediation", 0.79)
    ]
    for name, desc, px in p_mods:
        draw_card(ax, px, 0.67, 0.165, 0.155, "", bg=FILL_WHITE, border=BORDER_BLACK, lw=1.2)
        ax.text(px + 0.0825, 0.785, name, color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', zorder=5)
        ax.plot([px + 0.02, px + 0.145], [0.765, 0.765], color=BORDER_BLACK, lw=0.8, zorder=5)
        ax.text(px + 0.0825, 0.725, desc, color=TEXT_MUTED, fontsize=8, ha='center', va='center', zorder=5)

    # Tier 2: Concurrency & State
    draw_card(ax, 0.03, 0.35, 0.94, 0.24, "2. CONCURRENCY & ORCHESTRATION LAYER (Qt Signals & Asynchronous Workers)", bg=FILL_LIGHT, lw=2)
    c_mods = [
        ("AppState Singleton", "State Tuple S_t = <T, P, E, A, H, R_t>\nCentralized Reactive Observer Pattern", 0.07),
        ("InteractiveExecutor", "QThread Worker Pools & POSIX/Win PTY\nNon-Blocking Asynchronous Subprocess Lifecycle", 0.37),
        ("Event & Parsing Engine", "Real-Time Heuristic Regular Expression Engine\nPort, Banner, & CVE Diagnostic Tokenizer", 0.67)
    ]
    for name, desc, cx in c_mods:
        draw_card(ax, cx, 0.37, 0.26, 0.155, "", bg=FILL_WHITE, border=BORDER_BLACK, lw=1.2)
        ax.text(cx + 0.13, 0.485, name, color=TEXT_BLACK, fontsize=10, fontweight='bold', ha='center', zorder=5)
        ax.plot([cx + 0.03, cx + 0.23], [0.465, 0.465], color=BORDER_BLACK, lw=0.8, zorder=5)
        ax.text(cx + 0.13, 0.425, desc, color=TEXT_MUTED, fontsize=8.5, ha='center', va='center', zorder=5)

    # Tier 3: Intelligence & Persistence
    draw_card(ax, 0.03, 0.05, 0.94, 0.24, "3. INTELLIGENCE & PERSISTENCE LAYER (ML, AI, & Database Engines)", bg=FILL_LIGHT, lw=2)
    i_mods = [
        ("ML Scenario Advisor", "Feature Vector x_t -> Softmax\nTop-1 & Top-3 Action Predictions", 0.05),
        ("Dynamic Risk Engine", "Multi-factor CVSS v3.1 Model\nNormalized R_t Formulation (0-100)", 0.235),
        ("Multimodal AI Copilot", "Groq / Ollama / Mistral Engine\nAutomated Secure Code Synthesis", 0.42),
        ("SQLite DB (kalinova.db)", "Persistent Scan Records, Target\nEntities, & Telemetry History", 0.605),
        ("ReportLab Compiler", "Executive PDF Documents &\nInteractive HTML Dashboard", 0.79)
    ]
    for name, desc, ix in i_mods:
        draw_card(ax, ix, 0.07, 0.165, 0.155, "", bg=FILL_WHITE, border=BORDER_BLACK, lw=1.2)
        ax.text(ix + 0.0825, 0.185, name, color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', zorder=5)
        ax.plot([ix + 0.02, ix + 0.145], [0.165, 0.165], color=BORDER_BLACK, lw=0.8, zorder=5)
        ax.text(ix + 0.0825, 0.125, desc, color=TEXT_MUTED, fontsize=8, ha='center', va='center', zorder=5)

    # Clean vertical connector arrows between tiers
    for x_arr in [0.20, 0.50, 0.80]:
        ax.annotate("", xy=(x_arr, 0.65), xytext=(x_arr, 0.59),
                    arrowprops=dict(arrowstyle="<->", color=BORDER_BLACK, lw=2))
        ax.annotate("", xy=(x_arr, 0.35), xytext=(x_arr, 0.29),
                    arrowprops=dict(arrowstyle="<->", color=BORDER_BLACK, lw=2))

    save_fig(fig, "system_architecture.png")

# ==========================================
# 2. Figure 3.2: Kali-Nova Main Dashboard
# ==========================================
def gen_fig3_2():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Topbar
    draw_card(ax, 0.02, 0.91, 0.96, 0.07, "", bg=FILL_GRAY1, border=BORDER_BLACK, lw=1.5)
    ax.text(0.04, 0.945, "KALI-NOVA  v1.3.1  //  DESKTOP CONTROL CENTER", color=TEXT_BLACK, fontsize=12, fontweight='bold', va='center')
    ax.text(0.44, 0.945, "TARGET: 192.168.1.105   |   PROFILE: PROFESSIONAL   |   STATUS: ARMED", color=TEXT_BLACK, fontsize=9.5, va='center')
    ax.text(0.92, 0.945, "[ONLINE]", color=TEXT_BLACK, fontsize=10.5, fontweight='bold', va='center')

    # Left Sidebar
    draw_card(ax, 0.02, 0.04, 0.16, 0.85, "NAVIGATION", bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
    nav_items = ["Dashboard (Active)", "Reconnaissance (Nmap)", "Web Vulnerability (Nikto)", "Auth Resiliency (Hydra)", "Network Audit (SSLyze)", "Database Reports", "Global Settings"]
    for i, item in enumerate(nav_items):
        y_pos = 0.80 - i * 0.09
        bg_col = FILL_GRAY2 if i == 0 else FILL_WHITE
        draw_card(ax, 0.03, y_pos, 0.14, 0.07, "", bg=bg_col, border=BORDER_BLACK, lw=1.2)
        ax.text(0.10, y_pos + 0.035, item, color=TEXT_BLACK, fontsize=8.5, fontweight='bold' if i==0 else 'normal', ha='center', va='center')

    # Top-Left: Threat Gauge
    draw_card(ax, 0.20, 0.50, 0.38, 0.39, "DYNAMIC THREAT RISK GAUGE", bg=FILL_WHITE, lw=1.5)
    theta = np.linspace(np.pi, 0, 100)
    r = 0.08
    cx, cy = 0.39, 0.73
    ax.plot(cx + r*np.cos(theta), cy + r*np.sin(theta), color=FILL_GRAY3, lw=9, zorder=3)
    t_active = np.linspace(np.pi, np.pi * 0.22, 78)
    ax.plot(cx + r*np.cos(t_active), cy + r*np.sin(t_active), color=BORDER_BLACK, lw=9, zorder=4)

    # Dedicated score display box below the arc
    draw_card(ax, 0.32, 0.60, 0.14, 0.08, "", bg=FILL_GRAY1, border=BORDER_BLACK, lw=1)
    ax.text(0.39, 0.655, "78.4 / 100", color=TEXT_BLACK, fontsize=12, fontweight='bold', ha='center')
    ax.text(0.39, 0.615, "CRITICAL EXPOSURE", color=TEXT_BLACK, fontsize=8, fontweight='bold', ha='center')

    # Bottom indicators
    draw_card(ax, 0.22, 0.52, 0.16, 0.065, "", bg=FILL_LIGHT, lw=1)
    ax.text(0.30, 0.552, "Critical Ports: 4 Open\nActive CVEs: 6 Verified", color=TEXT_BLACK, fontsize=7.5, ha='center', va='center')
    draw_card(ax, 0.40, 0.52, 0.16, 0.065, "", bg=FILL_LIGHT, lw=1)
    ax.text(0.48, 0.552, "Exploit Surface: 84.3%\nStatus: Urgent Remediation", color=TEXT_BLACK, fontsize=7.5, ha='center', va='center')

    # Top-Right: Network Radar Topology
    draw_card(ax, 0.60, 0.50, 0.38, 0.39, "NETWORK TOPOLOGY & RADAR SCAN", bg=FILL_WHITE, lw=1.5)
    rcx, rcy = 0.79, 0.69
    for rad in [0.035, 0.075, 0.115]:
        circle = plt.Circle((rcx, rcy), rad, color=BORDER_BLACK, fill=False, lw=1, ls="--", alpha=0.6, zorder=3)
        ax.add_patch(circle)
    nodes = [(0.79, 0.69, "Gateway\n192.168.1.1"),
             (0.85, 0.75, "Target Web\n.105 (Vuln)"),
             (0.73, 0.63, "Database\n.120 (At-Risk)"),
             (0.85, 0.63, "Client Node\n.110 (Active)")]
    for nx, ny, lbl in nodes:
        ax.scatter([nx], [ny], color=BORDER_BLACK, s=100, zorder=5)
        ax.plot([rcx, nx], [rcy, ny], color=BORDER_BLACK, lw=1, ls=":", zorder=4)
        ax.text(nx, ny - 0.038, lbl, color=TEXT_BLACK, fontsize=7.5, ha='center', zorder=6)

    # Bottom-Left: Port Matrix
    draw_card(ax, 0.20, 0.04, 0.38, 0.44, "REAL-TIME OPEN PORT MATRIX", bg=FILL_WHITE, lw=1.5)
    ax.text(0.22, 0.43, "PORT", color=TEXT_BLACK, fontsize=8.5, fontweight='bold')
    ax.text(0.31, 0.43, "SERVICE BANNER", color=TEXT_BLACK, fontsize=8.5, fontweight='bold')
    ax.text(0.47, 0.43, "STATE", color=TEXT_BLACK, fontsize=8.5, fontweight='bold')
    ax.text(0.53, 0.43, "RISK LEVEL", color=TEXT_BLACK, fontsize=8.5, fontweight='bold')
    ax.plot([0.21, 0.57], [0.42, 0.42], color=BORDER_BLACK, lw=1)

    ports_data = [
        ("21/TCP", "vsftpd 2.3.4 (Anon)", "OPEN", "CRITICAL"),
        ("22/TCP", "OpenSSH 8.9p1", "OPEN", "SECURE"),
        ("80/TCP", "Apache 2.4.41", "OPEN", "HIGH"),
        ("443/TCP", "HTTPS (TLS 1.3)", "OPEN", "MODERATE"),
        ("3306/TCP", "MariaDB 10.3", "OPEN", "CRITICAL")
    ]
    for idx, (p, s, st, rk) in enumerate(ports_data):
        py = 0.36 - idx * 0.065
        draw_card(ax, 0.21, py, 0.36, 0.055, "", bg=FILL_GRAY1 if idx%2==0 else FILL_WHITE, border=BORDER_BLACK, lw=0.8)
        ax.text(0.22, py + 0.027, p, color=TEXT_BLACK, fontsize=8, fontweight='bold', va='center')
        ax.text(0.31, py + 0.027, s, color=TEXT_MUTED, fontsize=8, va='center')
        ax.text(0.47, py + 0.027, st, color=TEXT_BLACK, fontsize=7.5, fontweight='bold', va='center')
        ax.text(0.53, py + 0.027, rk, color=TEXT_BLACK, fontsize=7.5, fontweight='bold', va='center')

    # Bottom-Right: AI Copilot & Console
    draw_card(ax, 0.60, 0.04, 0.38, 0.44, "AI COPILOT REMEDIATION & CONSOLE", bg=FILL_WHITE, lw=1.5)
    # AI Summary Box
    draw_card(ax, 0.615, 0.27, 0.35, 0.15, "", bg=FILL_LIGHT, border=BORDER_BLACK, lw=1)
    ax.text(0.625, 0.39, "DIAGNOSTIC FINDING:", color=TEXT_BLACK, fontsize=8.5, fontweight='bold')
    ax.text(0.625, 0.35, "Vulnerability: SQL Injection on parameter 'id' (CVSS 9.8)", color=TEXT_BLACK, fontsize=8)
    ax.text(0.625, 0.315, "Action: Execute SQLMap -> Apply Parameterized Queries", color=TEXT_MUTED, fontsize=8)
    ax.text(0.625, 0.285, "Remediation patch generated in sliding drawer.", color=TEXT_MUTED, fontsize=7.5, style='italic')

    # Console Terminal Box
    draw_card(ax, 0.615, 0.06, 0.35, 0.19, "", bg=FILL_GRAY1, border=BORDER_BLACK, lw=1)
    console_lines = [
        "[*] [18:42:01] Starting Nmap 7.94 scan on 192.168.1.105...",
        "[+] [18:42:03] Discovered 5 open ports on target host.",
        "[!] [18:42:05] WARNING: Anonymous FTP access allowed",
        "[+] [18:42:07] AppState updated. Dynamic Risk Score: 78.4",
        "[*] [18:42:08] Awaiting confirmation for automated audit..."
    ]
    for ci, cline in enumerate(console_lines):
        ax.text(0.625, 0.215 - ci * 0.035, cline, color=TEXT_BLACK, fontsize=7.5, family='monospace', va='center')

    save_fig(fig, "main_dashboard.png")

# ==========================================
# 3. Figure 3.3: Security Tool Integration Workflow
# ==========================================
def gen_fig3_3():
    fig, ax = plt.subplots(figsize=(15, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "Security Tool Integration Workflow", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.91, "End-to-End Execution Pipeline from UI Parameterization to PTY Streaming", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    steps = [
        ("1. Tool Selection", "Analyst chooses module\n(Nmap, Nikto, Hydra,\nSQLMap, SSLyze)", 0.04),
        ("2. Form Generation", "Dynamic GUI generation\nTarget, Port Scope,\nTiming Templates", 0.195),
        ("3. Scope Validation", "Boundary CIDR check\nPrevents out-of-scope\nunauthorized scans", 0.35),
        ("4. Command Synthesis", "Constructs sanitized CLI\nstring with parameters\n& pipeline artifacts", 0.505),
        ("5. Async Dispatch", "Spawns worker thread\nQThread & allocates\nPOSIX/Win PTY channel", 0.66),
        ("6. Stream & State", "Non-blocking stdout\nRegex event parsing\nUpdates AppState & UI", 0.815)
    ]

    for title, desc, sx in steps:
        draw_card(ax, sx, 0.40, 0.145, 0.34, "", bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(sx + 0.0725, 0.70, title, color=TEXT_BLACK, fontsize=10, fontweight='bold', ha='center')
        ax.plot([sx + 0.02, sx + 0.125], [0.67, 0.67], color=BORDER_BLACK, lw=0.8)
        ax.text(sx + 0.0725, 0.55, desc, color=TEXT_MUTED, fontsize=8.5, ha='center', va='center')

    # Clean connecting arrows between cards
    for i in range(len(steps) - 1):
        x1 = steps[i][2] + 0.145
        x2 = steps[i+1][2]
        ax.annotate("", xy=(x2, 0.57), xytext=(x1, 0.57),
                    arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    draw_card(ax, 0.04, 0.08, 0.92, 0.24, "Key Architectural Safeguards & Mechanisms", bg=FILL_WHITE, lw=1.5)
    ax.text(0.06, 0.23, "- Input Sanitization: Strict parameter escaping prevents command injection inside Kali-Nova itself.", color=TEXT_BLACK, fontsize=9.5)
    ax.text(0.06, 0.17, "- Pipeline Artifact Handoff: Discovered open ports (e.g. 80, 443) automatically pre-populate downstream web tools.", color=TEXT_BLACK, fontsize=9.5)
    ax.text(0.06, 0.11, "- Audit Compliance: Full command line, timestamp, user context, and output hash are recorded to kalinova.db.", color=TEXT_BLACK, fontsize=9.5)

    save_fig(fig, "tool_integration.png")

# ==========================================
# 4. Figure 3.4: Asynchronous Command Execution
# ==========================================
def gen_fig3_4():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "Asynchronous Command Execution & Threading Architecture", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.92, "Non-Blocking Telemetry Streaming via QThread Worker Pools & Qt Signal Emission", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    cols = [
        ("Main UI Thread (PyQt6)", 0.14),
        ("Worker Thread (InteractiveExecutor)", 0.50),
        ("OS Subprocess Layer (CLI)", 0.86)
    ]
    for ctitle, cx in cols:
        draw_card(ax, cx - 0.11, 0.80, 0.22, 0.07, "", bg=FILL_GRAY2, border=BORDER_BLACK, lw=1.5)
        ax.text(cx, 0.835, ctitle, color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', va='center')
        ax.plot([cx, cx], [0.10, 0.80], color=BORDER_BLACK, ls="--", lw=1.2, zorder=1)

    seq = [
        (0.72, 0.14, 0.50, "1. User starts scan -> Spawns worker thread"),
        (0.63, 0.50, 0.86, "2. Subprocess.Popen() creates child CLI process"),
        (0.54, 0.86, 0.50, "3. Real-time stdout stream read into buffer chunk"),
        (0.45, 0.50, 0.14, "4. Emit Qt Signal: output_received(chunk)"),
        (0.36, 0.50, 0.50, "5. Regex parser extracts open ports & signatures"),
        (0.27, 0.86, 0.50, "6. Process terminates with exit code"),
        (0.18, 0.50, 0.14, "7. Emit Qt Signal: finished() -> Unlock UI")
    ]

    for y, x_from, x_to, msg in seq:
        if x_from != x_to:
            ax.annotate("", xy=(x_to, y), xytext=(x_from, y),
                        arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
            mid_x = (x_from + x_to) / 2
            ax.text(mid_x, y + 0.02, msg, color=TEXT_BLACK, fontsize=8.5, ha='center', zorder=5)
        else:
            arc = patches.Arc((x_from + 0.02, y), 0.04, 0.035, angle=0, theta1=-90, theta2=90, color=BORDER_BLACK, lw=1.5)
            ax.add_patch(arc)
            ax.text(x_from + 0.05, y, msg, color=TEXT_BLACK, fontsize=8.5, va='center', zorder=5)

    save_fig(fig, "async_execution.png")

# ==========================================
# 5. Figure 3.5: Global State Management
# ==========================================
def gen_fig3_5():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "Global State Management Architecture", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.92, "Reactive Singleton AppState Coordinating Assessment Entities and Subsystems", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    # Center Card
    draw_card(ax, 0.31, 0.28, 0.38, 0.50, "SINGLETON AppState (State Engine)", bg=FILL_LIGHT, border=BORDER_BLACK, lw=2)
    ax.text(0.50, 0.725, r"$\mathcal{S}_t = \langle \mathcal{T}, \mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{H}, R_t \rangle$", color=TEXT_BLACK, fontsize=11, ha='center', va='center')
    ax.plot([0.33, 0.67], [0.70, 0.70], color=BORDER_BLACK, lw=1)

    state_elements = [
        (r"T (Scope)", "Target IP addresses & CIDR boundary masks"),
        (r"P (Ports)", "Open port set: {21, 22, 80, 443, 3306}"),
        (r"E (Events)", "Detected threat events & banner vulnerabilities"),
        (r"A (Artifacts)", "Web endpoints, parameters, & hashes"),
        (r"H (History)", "Chronological tool log & timestamp trace"),
        (r"R_t (Risk)", "Normalized dynamic composite risk score (0-100)")
    ]
    for idx, (el, sub) in enumerate(state_elements):
        ey = 0.66 - idx * 0.058
        ax.text(0.33, ey, f"- {el}:", color=TEXT_BLACK, fontsize=9, fontweight='bold')
        ax.text(0.44, ey, sub, color=TEXT_MUTED, fontsize=8)

    # 4 Satellites
    satellites = [
        ("Execution Engine", "Dispatches stdout chunks\n& process exit signals", 0.05, 0.58),
        ("Parsing Engine", "Injects discovered ports\n& vulnerability findings", 0.05, 0.24),
        ("Dynamic Risk Engine", "Queries P & E to compute\ncomposite threat index R_t", 0.73, 0.58),
        ("UI View Subscribers", "Subscribes to state updates\n(Dashboard, Port Matrix, HUD)", 0.73, 0.24),
        ("SQLite Database", "Commits state snapshots\nto kalinova.db persistent storage", 0.37, 0.05)
    ]
    for s_title, s_desc, sx, sy in satellites[:4]:
        draw_card(ax, sx, sy, 0.22, 0.20, "", bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5)
        ax.text(sx + 0.11, sy + 0.15, s_title, color=TEXT_BLACK, fontsize=10, fontweight='bold', ha='center')
        ax.plot([sx + 0.03, sx + 0.19], [0.13 + sy, 0.13 + sy], color=BORDER_BLACK, lw=0.8)
        ax.text(sx + 0.11, sy + 0.07, s_desc, color=TEXT_MUTED, fontsize=8.5, ha='center', va='center')

    # Bottom DB Card
    draw_card(ax, 0.36, 0.05, 0.28, 0.15, "", bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5)
    ax.text(0.50, 0.15, "SQLite Persistence", color=TEXT_BLACK, fontsize=10, fontweight='bold', ha='center')
    ax.text(0.50, 0.09, "Commits state snapshot to kalinova.db", color=TEXT_MUTED, fontsize=8.5, ha='center')

    # Connecting arrows
    ax.annotate("", xy=(0.31, 0.64), xytext=(0.27, 0.64), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.31, 0.38), xytext=(0.27, 0.38), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.73, 0.64), xytext=(0.69, 0.64), arrowprops=dict(arrowstyle="<-", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.73, 0.38), xytext=(0.69, 0.38), arrowprops=dict(arrowstyle="<-", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.50, 0.20), xytext=(0.50, 0.28), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))

    save_fig(fig, "global_state.png")

# ==========================================
# 6. Figure 3.6: Event and Port Parsing Process
# ==========================================
def gen_fig3_6():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "Event and Port Parsing Pipeline", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.92, "Heuristic Regular Expression Tokenizer & Entity Normalization Engine", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    # Left: Raw Output Stream
    draw_card(ax, 0.04, 0.44, 0.24, 0.42, "1. Raw Output Stream", bg=FILL_LIGHT, lw=1.5)
    raw_text = (
        "80/tcp open http Apache/2.4.41\n\n"
        "[+] Vuln: SQL Injection detected\n"
        "    in /search.php?q=admin\n\n"
        "3306/tcp open mysql MariaDB\n\n"
        "Discovered Subdomain: api.host\n"
        "MD5: 5d41402abc4b2a76b9719d911017c592"
    )
    ax.text(0.06, 0.77, raw_text, color=TEXT_BLACK, fontsize=8, family='monospace', va='top', zorder=5)

    # Center: Regex Engine
    draw_card(ax, 0.33, 0.44, 0.34, 0.42, "2. Regex Rules Engine", bg=FILL_LIGHT, lw=1.5)
    regexes = [
        ("Port Pattern:", r"(\d+)/(tcp|udp)\s+(\w+)\s+(.+)"),
        ("SQLi Event:", r"(SQL injection|syntax error)"),
        ("Web Endpoint:", r"(https?://[^\s]+|/[a-zA-Z0-9_\-\./]+)"),
        ("Hash String:", r"([a-fA-F0-9]{32,64})")
    ]
    for idx, (lbl, reg) in enumerate(regexes):
        ry = 0.76 - idx * 0.08
        ax.text(0.35, ry, lbl, color=TEXT_BLACK, fontsize=9, fontweight='bold')
        ax.text(0.35, ry - 0.03, reg, color=TEXT_MUTED, fontsize=8, family='monospace')

    # Right: Extracted Entities
    draw_card(ax, 0.72, 0.44, 0.24, 0.42, "3. Extracted Entities", bg=FILL_LIGHT, lw=1.5)
    extracted = [
        "- Port: 80/TCP (HTTP)",
        "- Port: 3306/TCP (MySQL)",
        "- Event: SQL_INJECTION",
        "- Endpoint: /search.php",
        "- Artifact: api.host",
        "- Credential Hash Extracted"
    ]
    for idx, item in enumerate(extracted):
        ax.text(0.74, 0.76 - idx * 0.055, item, color=TEXT_BLACK, fontsize=8.5, zorder=5)

    # Inter-stage arrows
    ax.annotate("", xy=(0.33, 0.65), xytext=(0.28, 0.65), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.annotate("", xy=(0.72, 0.65), xytext=(0.67, 0.65), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    # Downstream consumers
    draw_card(ax, 0.04, 0.08, 0.92, 0.28, "Downstream Event Consumers & Dispatched Signals", bg=FILL_WHITE, lw=1.5)
    downstream = [
        ("AppState Update", "Registers open ports in P,\nupdates entity dictionary A", 0.07),
        ("Dynamic Risk Engine", "Computes updated CVSS score\nand threat severity gauge", 0.38),
        ("AI Copilot Trigger", "Generates contextual patch\n(Python/Node.js remediation)", 0.69)
    ]
    for dtitle, ddesc, dx in downstream:
        draw_card(ax, dx, 0.11, 0.24, 0.20, "", bg=FILL_GRAY1, border=BORDER_BLACK, lw=1.2)
        ax.text(dx + 0.12, 0.24, dtitle, color=TEXT_BLACK, fontsize=10, fontweight='bold', ha='center')
        ax.plot([dx + 0.03, dx + 0.21], [0.22, 0.22], color=BORDER_BLACK, lw=0.8)
        ax.text(dx + 0.12, 0.16, ddesc, color=TEXT_MUTED, fontsize=8.5, ha='center', va='center')

    save_fig(fig, "parsing_engine.png")

# ==========================================
# 7. Figure 3.7: Port Detection Flowchart
# ==========================================
def gen_fig3_7():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "Port Detection & Classification Flowchart", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.92, "Algorithmic Decision Tree for Live Port Stream Processing", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    draw_card(ax, 0.40, 0.84, 0.20, 0.06, "START", bg=FILL_GRAY2, lw=1.5)
    draw_card(ax, 0.35, 0.72, 0.30, 0.07, "Read Stdout Stream Chunk", bg=FILL_WHITE, lw=1.5)

    # Diamond 1
    d1 = patches.Polygon([[0.50, 0.67], [0.66, 0.60], [0.50, 0.53], [0.34, 0.60]], closed=True,
                         facecolor=FILL_LIGHT, edgecolor=BORDER_BLACK, lw=1.5, zorder=2)
    ax.add_patch(d1)
    ax.text(0.50, 0.60, "Matches Port Pattern\n(Regex Test)?", color=TEXT_BLACK, fontsize=9, fontweight='bold', ha='center', va='center', zorder=5)

    # Diamond 2
    d2 = patches.Polygon([[0.50, 0.44], [0.66, 0.37], [0.50, 0.30], [0.34, 0.37]], closed=True,
                         facecolor=FILL_LIGHT, edgecolor=BORDER_BLACK, lw=1.5, zorder=2)
    ax.add_patch(d2)
    ax.text(0.50, 0.37, "Is Port Critical\n(in P_crit)?", color=TEXT_BLACK, fontsize=9, fontweight='bold', ha='center', va='center', zorder=5)

    draw_card(ax, 0.06, 0.33, 0.22, 0.08, "Assign High Risk Weight", bg=FILL_WHITE, lw=1.5)
    ax.text(0.17, 0.355, "Trigger Critical Alert", color=TEXT_MUTED, fontsize=8, ha='center')
    draw_card(ax, 0.72, 0.33, 0.22, 0.08, "Assign Standard Weight", bg=FILL_WHITE, lw=1.5)
    ax.text(0.83, 0.355, "Standard Registry Entry", color=TEXT_MUTED, fontsize=8, ha='center')

    draw_card(ax, 0.33, 0.16, 0.34, 0.08, "Update AppState & Port Matrix", bg=FILL_GRAY1, lw=1.5)
    ax.text(0.50, 0.185, "Emit Signals to UI & Recalculate Risk", color=TEXT_MUTED, fontsize=8, ha='center')

    draw_card(ax, 0.42, 0.03, 0.16, 0.06, "END", bg=FILL_GRAY2, lw=1.5)

    # Connections
    ax.annotate("", xy=(0.50, 0.79), xytext=(0.50, 0.84), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.50, 0.67), xytext=(0.50, 0.72), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.annotate("", xy=(0.50, 0.44), xytext=(0.50, 0.53), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.text(0.52, 0.485, "Yes", color=TEXT_BLACK, fontsize=9, fontweight='bold')

    # No from D1 routes left and down
    ax.plot([0.34, 0.25, 0.25], [0.60, 0.60, 0.06], color=BORDER_BLACK, lw=1.5, ls="--")
    ax.annotate("", xy=(0.42, 0.06), xytext=(0.25, 0.06), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.5))
    ax.text(0.28, 0.61, "No", color=TEXT_BLACK, fontsize=8.5, fontweight='bold')

    # Branches from D2
    ax.annotate("", xy=(0.28, 0.37), xytext=(0.34, 0.37), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.text(0.30, 0.39, "Yes", color=TEXT_BLACK, fontsize=8.5, fontweight='bold')

    ax.annotate("", xy=(0.72, 0.37), xytext=(0.66, 0.37), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.text(0.68, 0.39, "No", color=TEXT_BLACK, fontsize=8.5, fontweight='bold')

    # Convergence
    ax.plot([0.17, 0.17, 0.33], [0.33, 0.20, 0.20], color=BORDER_BLACK, lw=1.5)
    ax.plot([0.83, 0.83, 0.67], [0.33, 0.20, 0.20], color=BORDER_BLACK, lw=1.5)
    ax.annotate("", xy=(0.50, 0.09), xytext=(0.50, 0.16), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))

    save_fig(fig, "port_detection_flowchart.png")

# ==========================================
# 8. Figure 3.8: Dynamic Threat Risk Assessment
# ==========================================
def gen_fig3_8():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "Dynamic Threat Risk Assessment Engine", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.92, "Multi-Factor Weighted Quantification of Attack Surface and CVSS Metrics", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    # Equation Banner
    draw_card(ax, 0.12, 0.78, 0.76, 0.11, "", bg=FILL_GRAY1, border=BORDER_BLACK, lw=2)
    ax.text(0.50, 0.835, r"$R_t = \min\left(100, \; \sum_{v \in \mathcal{V}_t} w_v \cdot \mathrm{CVSS}(v) + \alpha |\mathcal{P}_{\mathrm{crit}}| + \beta \log_2(1 + |\mathcal{E}|)\right)$",
            color=TEXT_BLACK, fontsize=12.5, ha='center', va='center')

    # 3 Inputs
    inputs = [
        ("Verified Vulnerabilities", "Sum of CVSS Base Scores (0-10)\nweighted by exposure coefficient w_v", 0.05),
        ("Critical Exposed Ports", "Count of high-impact ports exposed:\n{21, 22, 80, 443, 3306, 8080} * alpha", 0.38),
        ("Discovered Threat Signals", "Anomaly indicators & banner warnings:\nLogarithmic scaling factor beta", 0.71)
    ]
    for ititle, idesc, ix in inputs:
        draw_card(ax, ix, 0.46, 0.24, 0.24, "", bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5)
        ax.text(ix + 0.12, 0.64, ititle, color=TEXT_BLACK, fontsize=10.5, fontweight='bold', ha='center')
        ax.plot([ix + 0.02, ix + 0.22], [0.61, 0.61], color=BORDER_BLACK, lw=0.8)
        ax.text(ix + 0.12, 0.54, idesc, color=TEXT_MUTED, fontsize=8.5, ha='center', va='center')
        ax.annotate("", xy=(ix + 0.12, 0.78), xytext=(ix + 0.12, 0.70), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))

    # Tiers at bottom
    draw_card(ax, 0.05, 0.08, 0.90, 0.30, "Composite Threat Index Tier Mapping (R_t in [0, 100])", bg=FILL_LIGHT, lw=1.5)
    tiers = [
        ("LOW (0.0 - 24.9)", "Standard perimeter services,\nno verified CVEs.", 0.07, FILL_WHITE, None),
        ("MODERATE (25.0 - 49.9)", "Informational disclosures,\nnon-critical ports open.", 0.295, FILL_GRAY1, "//"),
        ("HIGH (50.0 - 74.9)", "Vulnerable software versions,\nunencrypted auth protocols.", 0.52, FILL_GRAY2, "\\\\"),
        ("CRITICAL (75.0 - 100)", "Verified RCE, SQLi, root exposure,\nimmediate patching required.", 0.745, FILL_GRAY3, "xx")
    ]
    for tt, td, tx, tbg, th in tiers:
        draw_card(ax, tx, 0.11, 0.20, 0.20, "", bg=tbg, border=BORDER_BLACK, lw=1.5, hatch=th)
        ax.text(tx + 0.10, 0.25, tt, color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center')
        ax.plot([tx + 0.02, tx + 0.18], [0.22, 0.22], color=BORDER_BLACK, lw=0.8)
        ax.text(tx + 0.10, 0.165, td, color=TEXT_MUTED, fontsize=8, ha='center', va='center')

    save_fig(fig, "risk_engine.png")

if __name__ == "__main__":
    print("Generating Clean B&W Figures 3.1 to 3.8...")
    gen_fig3_1()
    gen_fig3_2()
    gen_fig3_3()
    gen_fig3_4()
    gen_fig3_5()
    gen_fig3_6()
    gen_fig3_7()
    gen_fig3_8()
    print("Part 1 finished!")
