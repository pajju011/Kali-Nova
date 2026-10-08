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
        fig.savefig(target, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"Generated {filename}")
    plt.close(fig)

# Color Palette Constants
BG_COLOR = "#0A0E17"
CARD_BG = "#111827"
CARD_BORDER = "#1F2937"
ACCENT_CYAN = "#00F0FF"
ACCENT_GREEN = "#10B981"
ACCENT_PURPLE = "#8B5CF6"
ACCENT_AMBER = "#F59E0B"
ACCENT_RED = "#EF4444"
ACCENT_BLUE = "#3B82F6"
TEXT_WHITE = "#F9FAFB"
TEXT_MUTED = "#9CA3AF"

def draw_card(ax, x, y, w, h, title="", subtitle="", bg=CARD_BG, border=CARD_BORDER, border_width=1.5, title_color=TEXT_WHITE):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.03",
                                 facecolor=bg, edgecolor=border, linewidth=border_width, zorder=2)
    ax.add_patch(box)
    if title:
        ax.text(x + 0.02*w, y + h - 0.12*h, title, color=title_color, fontsize=11, fontweight='bold', zorder=4)
    if subtitle:
        ax.text(x + 0.02*w, y + h - 0.22*h, subtitle, color=TEXT_MUTED, fontsize=8.5, zorder=4)
    return box

# ==========================================
# 1. Figure 3.1: Overall Architecture of Kali-Nova
# ==========================================
def gen_fig3_1():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.95, "Kali-Nova: Overall System Architecture", color=TEXT_WHITE, fontsize=19, fontweight='bold', ha='center')
    ax.text(0.5, 0.92, "Decoupled Three-Tier Architecture for Autonomous Threat Modeling & Security Orchestration", color=ACCENT_CYAN, fontsize=11, ha='center')

    # Tier 1: Presentation Layer
    draw_card(ax, 0.04, 0.65, 0.92, 0.23, "1. PRESENTATION LAYER (PyQt6 Cyber HUD)", "Reactive user interface with asynchronous non-blocking event loops", border=ACCENT_CYAN, title_color=ACCENT_CYAN)
    p_mods = [
        ("Navigation Sidebar", "Recon, Web, Auth,\nNetwork, Reports", 0.06),
        ("Master Bento Dashboard", "Threat Radar, Risk Gauge,\nPort Matrix, Scan History", 0.245),
        ("Tool Workspaces", "Dynamic Parameter Forms,\nScope CIDR Validation", 0.44),
        ("Interactive Console", "PTY Live Telemetry Stream,\nANSI Highlighting, Stdin", 0.625),
        ("AI Copilot Drawer", "CVSS Diagnostics, Remediation\nPython / Node.js Patches", 0.805)
    ]
    for name, desc, px in p_mods:
        draw_card(ax, px, 0.67, 0.155, 0.13, name, "", bg="#1E293B", border=CARD_BORDER)
        ax.text(px + 0.077, 0.75, name, color=TEXT_WHITE, fontsize=9.5, fontweight='bold', ha='center', zorder=5)
        ax.text(px + 0.077, 0.70, desc, color=TEXT_MUTED, fontsize=7.5, ha='center', zorder=5)

    # Tier 2: Concurrency & State Management
    draw_card(ax, 0.04, 0.35, 0.92, 0.23, "2. CONCURRENCY & ORCHESTRATION LAYER (Qt Signals & Asynchronous Workers)", "Thread management, continuous process monitoring, and centralized state storage", border=ACCENT_PURPLE, title_color=ACCENT_PURPLE)
    c_mods = [
        ("AppState Singleton", "Tuple S_t = <T, P, E, A, H, R_t>\nCentralized Observer Pattern", 0.08, ACCENT_CYAN),
        ("InteractiveExecutor", "QThread Worker Pools\nSubprocess PTY Channels", 0.38, ACCENT_PURPLE),
        ("Event & Parsing Engine", "Real-time Heuristic Regex\nPort & CVE Tokenizer", 0.68, ACCENT_GREEN)
    ]
    for name, desc, cx, color in c_mods:
        draw_card(ax, cx, 0.37, 0.24, 0.13, name, "", bg="#1E293B", border=color)
        ax.text(cx + 0.12, 0.45, name, color=TEXT_WHITE, fontsize=10.5, fontweight='bold', ha='center', zorder=5)
        ax.text(cx + 0.12, 0.40, desc, color=TEXT_MUTED, fontsize=8.5, ha='center', zorder=5)

    # Tier 3: Intelligence & Data Persistence
    draw_card(ax, 0.04, 0.05, 0.92, 0.23, "3. INTELLIGENCE & PERSISTENCE LAYER (ML, AI, & Database Engines)", "Dynamic risk calculation, multi-class transition advisor, and structured storage", border=ACCENT_GREEN, title_color=ACCENT_GREEN)
    i_mods = [
        ("ML Scenario Advisor", "Feature Vector x_t -> Softmax\nTop-1 & Top-3 Tool Actions", 0.06),
        ("Dynamic Risk Engine", "Multi-factor CVSS v3.1 Index\nR_t Formulation (0-100)", 0.245),
        ("Multimodal AI Copilot", "Groq / Ollama / Rule Engine\nAutomated Secure Code Fixes", 0.44),
        ("SQLite Database (kalinova.db)", "Persistent Scan Records, Target\nEntities, & Telemetry Logs", 0.625),
        ("ReportLab Compiler", "Executive PDF Document &\nInteractive HTML Exports", 0.805)
    ]
    for name, desc, ix in i_mods:
        draw_card(ax, ix, 0.07, 0.155, 0.13, name, "", bg="#1E293B", border=CARD_BORDER)
        ax.text(ix + 0.077, 0.15, name, color=TEXT_WHITE, fontsize=9.5, fontweight='bold', ha='center', zorder=5)
        ax.text(ix + 0.077, 0.10, desc, color=TEXT_MUTED, fontsize=7.5, ha='center', zorder=5)

    # Connecting Arrows
    for x_arr in [0.2, 0.5, 0.8]:
        ax.annotate("", xy=(x_arr, 0.65), xytext=(x_arr, 0.58),
                    arrowprops=dict(arrowstyle="<->", color=ACCENT_CYAN, lw=2.5))
        ax.annotate("", xy=(x_arr, 0.35), xytext=(x_arr, 0.28),
                    arrowprops=dict(arrowstyle="<->", color=ACCENT_GREEN, lw=2.5))

    save_fig(fig, "system_architecture.png")

# ==========================================
# 2. Figure 3.2: Kali-Nova Main Dashboard
# ==========================================
def gen_fig3_2():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Topbar
    draw_card(ax, 0.02, 0.90, 0.96, 0.08, bg="#131B2E", border=ACCENT_CYAN, border_width=1.5)
    ax.text(0.04, 0.945, "KALI-NOVA  v1.3.1  //  CONTROL CENTER", color=ACCENT_CYAN, fontsize=13, fontweight='bold')
    ax.text(0.40, 0.945, "TARGET: 192.168.1.105 (internal-prod.local)   |   PROFILE: PROFESSIONAL   |   STATUS: ARMED", color=TEXT_WHITE, fontsize=10)
    ax.text(0.92, 0.945, "ONLINE", color=ACCENT_GREEN, fontsize=11, fontweight='bold')

    # Left Sidebar
    draw_card(ax, 0.02, 0.04, 0.16, 0.84, "NAVIGATION", "", bg="#111827", border=CARD_BORDER)
    nav_items = ["Dashboard (Active)", "Reconnaissance (Nmap)", "Web Vulnerability (Nikto)", "Auth Resiliency (Hydra)", "Network Audit (SSLyze)", "Database Reports", "Global Settings"]
    for i, item in enumerate(nav_items):
        y_pos = 0.80 - i * 0.085
        col = ACCENT_CYAN if i == 0 else TEXT_MUTED
        bg_col = "#1E293B" if i == 0 else "#151E2E"
        draw_card(ax, 0.03, y_pos, 0.14, 0.065, item, "", bg=bg_col, border=col, title_color=col)

    # Main Center - Top Left: Threat Risk Gauge
    draw_card(ax, 0.20, 0.50, 0.38, 0.38, "DYNAMIC THREAT RISK GAUGE", "Multi-factor CVSS v3.1 Risk Quantification", border=ACCENT_RED, title_color=ACCENT_RED)
    # Draw Gauge Arc
    theta = np.linspace(np.pi, 0, 100)
    r = 0.10
    cx, cy = 0.39, 0.65
    ax.plot(cx + r*np.cos(theta), cy + r*np.sin(theta), color="#374151", lw=12, zorder=3)
    # Active threat level (78%)
    t_active = np.linspace(np.pi, np.pi * 0.22, 78)
    ax.plot(cx + r*np.cos(t_active), cy + r*np.sin(t_active), color=ACCENT_RED, lw=12, zorder=4)
    ax.text(cx, cy + 0.03, "78.4", color=TEXT_WHITE, fontsize=24, fontweight='bold', ha='center', zorder=5)
    ax.text(cx, cy - 0.02, "CRITICAL RISK EXPOSURE", color=ACCENT_RED, fontsize=9.5, fontweight='bold', ha='center', zorder=5)
    ax.text(0.22, 0.54, "Critical Ports: 4 Exposed\nVerified CVEs: 6 Active", color=TEXT_MUTED, fontsize=8.5)
    ax.text(0.44, 0.54, "Exploit Surface: 84.3%\nRecommendation: Patch Urgently", color=TEXT_MUTED, fontsize=8.5)

    # Main Center - Top Right: Network Radar Topology
    draw_card(ax, 0.60, 0.50, 0.38, 0.38, "NETWORK TOPOLOGY & RADAR SCAN", "Animated 20 FPS Spatial Telemetry Canvas", border=ACCENT_CYAN, title_color=ACCENT_CYAN)
    rcx, rcy = 0.79, 0.68
    for rad in [0.03, 0.07, 0.11]:
        circle = plt.Circle((rcx, rcy), rad, color=ACCENT_CYAN, fill=False, lw=1.2, ls="--", alpha=0.6, zorder=3)
        ax.add_patch(circle)
    # Nodes
    nodes = [(0.79, 0.68, "Gateway\n192.168.1.1", ACCENT_GREEN),
             (0.84, 0.73, "Target Host\n.105 (Vulnerable)", ACCENT_RED),
             (0.74, 0.63, "Database\n.120 (At-Risk)", ACCENT_AMBER),
             (0.85, 0.62, "Workstation\n.110 (Active)", ACCENT_CYAN)]
    for nx, ny, lbl, ncol in nodes:
        ax.scatter([nx], [ny], color=ncol, s=120, zorder=5, edgecolor=TEXT_WHITE)
        ax.plot([rcx, nx], [rcy, ny], color=ncol, lw=1, alpha=0.5, zorder=4)
        ax.text(nx, ny - 0.03, lbl, color=TEXT_WHITE, fontsize=7.5, ha='center', zorder=6)

    # Main Center - Bottom Left: Port Matrix
    draw_card(ax, 0.20, 0.04, 0.38, 0.44, "REAL-TIME OPEN PORT MATRIX", "Discovered Services & Vulnerability Status", border=ACCENT_AMBER, title_color=ACCENT_AMBER)
    ports_data = [
        ("PORT 21/TCP", "FTP (vsftpd 2.3.4)", "CRITICAL (Backdoor)", ACCENT_RED),
        ("PORT 22/TCP", "SSH (OpenSSH 8.9p1)", "SECURE / AUTH REQ", ACCENT_GREEN),
        ("PORT 80/TCP", "HTTP (Apache 2.4.41)", "HIGH (SQLi Vector)", ACCENT_RED),
        ("PORT 443/TCP", "HTTPS (TLS 1.3)", "MODERATE (Cert Expired)", ACCENT_AMBER),
        ("PORT 3306/TCP", "MySQL (MariaDB 10.3)", "CRITICAL (Remote Root)", ACCENT_RED)
    ]
    for idx, (p, s, st, c) in enumerate(ports_data):
        py = 0.38 - idx * 0.07
        draw_card(ax, 0.21, py, 0.36, 0.06, "", "", bg="#1E293B", border=c, border_width=1)
        ax.text(0.22, py + 0.02, p, color=TEXT_WHITE, fontsize=9, fontweight='bold', zorder=5)
        ax.text(0.31, py + 0.02, s, color=TEXT_MUTED, fontsize=8.5, zorder=5)
        ax.text(0.50, py + 0.02, st, color=c, fontsize=8, fontweight='bold', zorder=5)

    # Main Center - Bottom Right: AI Copilot & Live Terminal
    draw_card(ax, 0.60, 0.04, 0.38, 0.44, "AI COPILOT REMEDIATION & LIVE CONSOLE", "Autonomous Intelligence & PTY Stream", border=ACCENT_PURPLE, title_color=ACCENT_PURPLE)
    ax.text(0.615, 0.40, "[AI Copilot Analysis]:", color=ACCENT_CYAN, fontsize=9.5, fontweight='bold')
    ax.text(0.615, 0.34, "High probability of SQL Injection on parameter 'id'.\nSuggested tool transition: Execute SQLMap -> Nikto.\nRemediation code ready in Copilot drawer.", color=TEXT_WHITE, fontsize=8.5)
    # Console terminal box inside
    draw_card(ax, 0.615, 0.06, 0.35, 0.25, "", "", bg="#050811", border="#374151")
    console_lines = [
        "[*] [18:42:01] Starting Nmap 7.94 scan on 192.168.1.105...",
        "[+] [18:42:03] Discovered 5 open ports on target host.",
        "[!] [18:42:05] WARNING: Anonymous FTP access allowed (CVE-2011-2523)",
        "[+] [18:42:07] Dispatched signal to AppState. Risk Score updated to 78.4",
        "[*] [18:42:08] Awaiting analyst confirmation for automated exploit audit..."
    ]
    for ci, cline in enumerate(console_lines):
        ax.text(0.625, 0.27 - ci * 0.045, cline, color="#34D399" if "[+]" in cline else ("#F87171" if "[!]" in cline else TEXT_MUTED), fontsize=7.5, family='monospace', zorder=5)

    save_fig(fig, "main_dashboard.png")

# ==========================================
# 3. Figure 3.3: Security Tool Integration Workflow
# ==========================================
def gen_fig3_3():
    fig, ax = plt.subplots(figsize=(15, 8.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.94, "Security Tool Integration Workflow", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.90, "End-to-End Execution Pipeline from UI Parameterization to PTY Streaming", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    steps = [
        ("1. Tool Selection", "Analyst chooses module\n(Nmap, Nikto, Hydra,\nSQLMap, SSLyze)", 0.05, ACCENT_BLUE),
        ("2. Form Generation", "Dynamic GUI generation\nTarget, Port Scope,\nTiming Templates", 0.21, ACCENT_CYAN),
        ("3. Scope Validation", "Boundary CIDR check\nPrevents out-of-scope\nunauthorized scans", 0.37, ACCENT_AMBER),
        ("4. Command Synthesis", "Constructs sanitized CLI\nstring with parameters\n& pipeline artifacts", 0.53, ACCENT_PURPLE),
        ("5. Async Dispatch", "Spawns worker thread\nQThread & allocates\nPOSIX/Win PTY channel", 0.69, ACCENT_GREEN),
        ("6. Stream & State", "Non-blocking stdout\nRegex event parsing\nUpdates AppState & UI", 0.85, ACCENT_RED)
    ]

    for title, desc, sx, col in steps:
        draw_card(ax, sx, 0.38, 0.12, 0.32, title, "", bg="#131B2E", border=col, border_width=1.8)
        ax.text(sx + 0.06, 0.64, title, color=col, fontsize=10.5, fontweight='bold', ha='center', zorder=5)
        ax.text(sx + 0.06, 0.52, desc, color=TEXT_WHITE, fontsize=8.5, ha='center', zorder=5)

    for i in range(len(steps) - 1):
        x1 = steps[i][2] + 0.12
        x2 = steps[i+1][2]
        ax.annotate("", xy=(x2, 0.54), xytext=(x1, 0.54),
                    arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=2.5))

    # Detailed specifications below
    draw_card(ax, 0.05, 0.08, 0.92, 0.22, "Key Architectural Safeguards & Mechanisms", "", bg="#111827", border=CARD_BORDER)
    ax.text(0.07, 0.22, "- Input Sanitization: Strict parameter escaping prevents command injection inside Kali-Nova itself.", color=TEXT_WHITE, fontsize=9.5)
    ax.text(0.07, 0.17, "- Pipeline Artifact Handoff: Discovered open ports (e.g. 80, 443) automatically pre-populate downstream web tools.", color=TEXT_WHITE, fontsize=9.5)
    ax.text(0.07, 0.12, "- Audit Compliance: Full command line, timestamp, user context, and output hash are recorded to kalinova.db.", color=TEXT_WHITE, fontsize=9.5)

    save_fig(fig, "tool_integration.png")

# ==========================================
# 4. Figure 3.4: Asynchronous Command Execution
# ==========================================
def gen_fig3_4():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "Asynchronous Command Execution & Threading Architecture", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.91, "Non-Blocking Telemetry Streaming via QThread Worker Pools & Qt Signal Emission", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    # Columns
    cols = [
        ("Main UI Thread (PyQt6)", 0.08, ACCENT_CYAN),
        ("Worker Thread (CommandThread)", 0.42, ACCENT_PURPLE),
        ("OS Subprocess Layer (CLI)", 0.76, ACCENT_GREEN)
    ]
    for ctitle, cx, ccol in cols:
        draw_card(ax, cx, 0.78, 0.20, 0.08, ctitle, "", bg="#1E293B", border=ccol)
        ax.text(cx + 0.10, 0.82, ctitle, color=ccol, fontsize=10.5, fontweight='bold', ha='center', zorder=5)
        # Lifeline
        ax.plot([cx + 0.10, cx + 0.10], [0.15, 0.78], color="#374151", ls="--", lw=1.5, zorder=1)

    # Sequence Arrows & Actions
    seq = [
        (0.72, 0.18, 0.52, "1. User initiates scan (e.g., Nmap) -> Instantiate CommandThread", ACCENT_CYAN),
        (0.64, 0.52, 0.86, "2. Subprocess.Popen() spawns child process with PTY pipe", ACCENT_PURPLE),
        (0.56, 0.86, 0.86, "3. OS executes raw security binary (nmap -sV ...)", ACCENT_GREEN),
        (0.48, 0.86, 0.52, "4. Real-time stdout chunk streaming via buffered channel", ACCENT_GREEN),
        (0.40, 0.52, 0.18, "5. Emit Qt Signal: output_received(str) -> Console Widget updates", ACCENT_CYAN),
        (0.32, 0.52, 0.52, "6. Internal Regex Parser evaluates output for ports & threats", ACCENT_AMBER),
        (0.24, 0.86, 0.52, "7. Process terminates with exit status code (0 = success)", ACCENT_GREEN),
        (0.16, 0.52, 0.18, "8. Emit Qt Signal: finished() -> Unlock UI & trigger ML Advisor", ACCENT_PURPLE)
    ]

    for y, x_from, x_to, msg, col in seq:
        if x_from != x_to:
            ax.annotate("", xy=(x_to, y), xytext=(x_from, y),
                        arrowprops=dict(arrowstyle="->", color=col, lw=2.0))
            mid_x = (x_from + x_to) / 2
            ax.text(mid_x, y + 0.015, msg, color=TEXT_WHITE, fontsize=8.5, ha='center', zorder=5)
        else:
            # Self loop
            arc = patches.Arc((x_from + 0.03, y), 0.05, 0.04, angle=0, theta1=-90, theta2=90, color=col, lw=2)
            ax.add_patch(arc)
            ax.text(x_from + 0.06, y, msg, color=TEXT_WHITE, fontsize=8.5, zorder=5)

    save_fig(fig, "async_execution.png")

# ==========================================
# 5. Figure 3.5: Global State Management
# ==========================================
def gen_fig3_5():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "Global State Management Architecture", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.91, "Reactive Singleton AppState Coordinating Assessment Entities and Subsystems", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    # Central Hub
    draw_card(ax, 0.33, 0.32, 0.34, 0.45, "SINGLETON AppState", "Central Assessment State Tuple: S_t = <T, P, E, A, H, R_t>", bg="#1E293B", border=ACCENT_CYAN, border_width=2.5, title_color=ACCENT_CYAN)
    state_elements = [
        ("T (Target Scope)", "FQDNs, IP Ranges, Target CIDR boundaries"),
        ("P (Open Ports)", "Discovered port set: {21, 22, 80, 443, 3306}"),
        ("E (Signatures)", "Detected threat events, banner vulnerabilities"),
        ("A (Artifacts)", "Web endpoints, subdomains, credential hashes"),
        ("H (Execution Trace)", "Historical tool log sequence & timestamp trace"),
        ("R_t (Risk Score)", "Composite dynamic threat index (0 - 100)")
    ]
    for idx, (el, sub) in enumerate(state_elements):
        ey = 0.67 - idx * 0.058
        ax.text(0.35, ey, f"- {el}:", color=ACCENT_GREEN, fontsize=9.5, fontweight='bold', zorder=5)
        ax.text(0.49, ey, sub, color=TEXT_WHITE, fontsize=8.5, zorder=5)

    # Surrounding Subsystems
    satellites = [
        ("Execution Engine", "Dispatches stdout chunks\n& exit signals", 0.06, 0.65, ACCENT_PURPLE),
        ("Parsing Engine", "Injects open ports\n& vulnerability findings", 0.06, 0.25, ACCENT_GREEN),
        ("Dynamic Risk Engine", "Queries P & E to compute\ncomposite threat index R_t", 0.74, 0.65, ACCENT_RED),
        ("UI View Subscribers", "Subscribes to state updates\n(Dashboard, Port Matrix, HUD)", 0.74, 0.25, ACCENT_AMBER),
        ("SQLite Persistence", "Commits state snapshot\nto kalinova.db database", 0.40, 0.06, ACCENT_BLUE)
    ]

    for s_title, s_desc, sx, sy, scol in satellites:
        draw_card(ax, sx, sy, 0.20, 0.18, s_title, "", bg="#131B2E", border=scol, border_width=1.8)
        ax.text(sx + 0.10, sy + 0.13, s_title, color=scol, fontsize=10.5, fontweight='bold', ha='center', zorder=5)
        ax.text(sx + 0.10, sy + 0.06, s_desc, color=TEXT_MUTED, fontsize=8.5, ha='center', zorder=5)

    # Connections to Center
    ax.annotate("", xy=(0.33, 0.60), xytext=(0.26, 0.70), arrowprops=dict(arrowstyle="->", color=ACCENT_PURPLE, lw=2))
    ax.annotate("", xy=(0.33, 0.45), xytext=(0.26, 0.35), arrowprops=dict(arrowstyle="->", color=ACCENT_GREEN, lw=2))
    ax.annotate("", xy=(0.74, 0.70), xytext=(0.67, 0.60), arrowprops=dict(arrowstyle="<-", color=ACCENT_RED, lw=2))
    ax.annotate("", xy=(0.74, 0.35), xytext=(0.67, 0.45), arrowprops=dict(arrowstyle="<-", color=ACCENT_AMBER, lw=2))
    ax.annotate("", xy=(0.50, 0.24), xytext=(0.50, 0.32), arrowprops=dict(arrowstyle="->", color=ACCENT_BLUE, lw=2))

    save_fig(fig, "global_state.png")

# ==========================================
# 6. Figure 3.6: Event and Port Parsing Process
# ==========================================
def gen_fig3_6():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "Event and Port Parsing Pipeline", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.91, "Heuristic Regular Expression Tokenizer & Entity Normalization Engine", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    # Stages
    draw_card(ax, 0.05, 0.48, 0.20, 0.35, "Raw Output Stream", "Standard I/O stream from CLI", border=ACCENT_CYAN)
    ax.text(0.065, 0.70, "80/tcp open http Apache/2.4.41\n\n[+] Vulnerability found: SQLi\nin /search.php?q=admin\n\n3306/tcp open mysql MariaDB\n\nDiscovered Subdomain: api.host", color=TEXT_MUTED, fontsize=8, family='monospace', zorder=5)

    draw_card(ax, 0.32, 0.48, 0.36, 0.35, "Heuristic Regex Rules Engine", "Pattern matchers and entity filters", border=ACCENT_PURPLE)
    regexes = [
        ("Port Pattern:", r"(\d+)/(tcp|udp)\s+(\w+)\s+(.+)", ACCENT_CYAN),
        ("SQLi Event:", r"(SQL injection|syntax error|union select)", ACCENT_RED),
        ("Web Endpoint:", r"(https?://[^\s]+|/[a-zA-Z0-9_\-\./]+)", ACCENT_GREEN),
        ("Credential Hash:", r"([a-fA-F0-9]{32,64})", ACCENT_AMBER)
    ]
    for idx, (lbl, reg, rcol) in enumerate(regexes):
        ry = 0.73 - idx * 0.06
        ax.text(0.335, ry, lbl, color=rcol, fontsize=9.5, fontweight='bold', zorder=5)
        ax.text(0.445, ry, reg, color=TEXT_WHITE, fontsize=8.5, family='monospace', zorder=5)

    draw_card(ax, 0.75, 0.48, 0.20, 0.35, "Extracted Entities", "Normalized state objects", border=ACCENT_GREEN)
    ax.text(0.765, 0.72, "- Port 80 (HTTP)\n- Port 3306 (MySQL)\n- Event: SQL_INJECTION\n- URI: /search.php\n- Artifact: Subdomain api", color=TEXT_WHITE, fontsize=8.5, zorder=5)

    ax.annotate("", xy=(0.32, 0.65), xytext=(0.25, 0.65), arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=2.5))
    ax.annotate("", xy=(0.75, 0.65), xytext=(0.68, 0.65), arrowprops=dict(arrowstyle="->", color=ACCENT_GREEN, lw=2.5))

    # Downstream consumers
    draw_card(ax, 0.05, 0.08, 0.90, 0.32, "Downstream Event Consumers & Dispatched Signals", "", border=CARD_BORDER)
    downstream = [
        ("AppState Update", "Registers open ports in P,\nupdates active entity map", 0.08, ACCENT_CYAN),
        ("Dynamic Risk Engine", "Computes updated CVSS score\nand threat severity gauge", 0.38, ACCENT_RED),
        ("AI Copilot Trigger", "Generates contextual patch\n(Python/Node.js remediation)", 0.68, ACCENT_PURPLE)
    ]
    for dtitle, ddesc, dx, dcol in downstream:
        draw_card(ax, dx, 0.11, 0.24, 0.22, dtitle, "", bg="#1E293B", border=dcol)
        ax.text(dx + 0.12, 0.26, dtitle, color=dcol, fontsize=10.5, fontweight='bold', ha='center', zorder=5)
        ax.text(dx + 0.12, 0.18, ddesc, color=TEXT_WHITE, fontsize=8.5, ha='center', zorder=5)

    save_fig(fig, "parsing_engine.png")

# ==========================================
# 7. Figure 3.7: Port Detection Flowchart
# ==========================================
def gen_fig3_7():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "Port Detection & Classification Flowchart", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.92, "Algorithmic Decision Tree for Live Port Stream Processing", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    # Flowchart Blocks
    draw_card(ax, 0.40, 0.83, 0.20, 0.065, "START", "Initiate Recon Scan", bg="#1E293B", border=ACCENT_GREEN, title_color=ACCENT_GREEN)
    draw_card(ax, 0.36, 0.72, 0.28, 0.07, "Read Next Stdout Line", "Buffered non-blocking line read", bg="#131B2E", border=CARD_BORDER)

    # Decision Diamond 1: Matches Port Regex?
    d1 = patches.Polygon([[0.50, 0.67], [0.65, 0.60], [0.50, 0.53], [0.35, 0.60]], closed=True,
                         facecolor="#1E293B", edgecolor=ACCENT_PURPLE, lw=2, zorder=2)
    ax.add_patch(d1)
    ax.text(0.50, 0.60, "Matches Port\nRegex Pattern?", color=TEXT_WHITE, fontsize=9.5, fontweight='bold', ha='center', va='center', zorder=5)

    # Decision Diamond 2: Critical Port?
    d2 = patches.Polygon([[0.50, 0.44], [0.65, 0.37], [0.50, 0.30], [0.35, 0.37]], closed=True,
                         facecolor="#1E293B", edgecolor=ACCENT_AMBER, lw=2, zorder=2)
    ax.add_patch(d2)
    ax.text(0.50, 0.37, "Is Port in\nCritical Set P_crit?", color=TEXT_WHITE, fontsize=9.5, fontweight='bold', ha='center', va='center', zorder=5)

    # Side boxes
    draw_card(ax, 0.05, 0.33, 0.22, 0.08, "Assign High Risk Weight", "Trigger Critical HUD Warning", bg="#131B2E", border=ACCENT_RED, title_color=ACCENT_RED)
    draw_card(ax, 0.73, 0.33, 0.22, 0.08, "Assign Standard Weight", "Add to standard port registry", bg="#131B2E", border=ACCENT_CYAN, title_color=ACCENT_CYAN)

    draw_card(ax, 0.35, 0.16, 0.30, 0.08, "Update AppState & Port Matrix", "Emit Signals to Dashboard & ML Advisor", bg="#1E293B", border=ACCENT_CYAN)
    draw_card(ax, 0.42, 0.03, 0.16, 0.065, "END", "Port Sweep Finalized", bg="#1E293B", border=ACCENT_GREEN, title_color=ACCENT_GREEN)

    # Connecting Arrows
    ax.annotate("", xy=(0.50, 0.79), xytext=(0.50, 0.83), arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=2))
    ax.annotate("", xy=(0.50, 0.67), xytext=(0.50, 0.72), arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=2))
    ax.annotate("", xy=(0.50, 0.44), xytext=(0.50, 0.53), arrowprops=dict(arrowstyle="->", color=ACCENT_GREEN, lw=2))
    ax.text(0.52, 0.48, "Yes", color=ACCENT_GREEN, fontsize=9, fontweight='bold')

    # No from D1 loops back or exits
    ax.annotate("", xy=(0.20, 0.60), xytext=(0.35, 0.60), arrowprops=dict(arrowstyle="->", color=TEXT_MUTED, lw=2))
    ax.text(0.26, 0.61, "No (Skip line)", color=TEXT_MUTED, fontsize=8.5)

    # Branches from D2
    ax.annotate("", xy=(0.27, 0.37), xytext=(0.35, 0.37), arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=2))
    ax.text(0.30, 0.39, "Yes", color=ACCENT_RED, fontsize=9, fontweight='bold')

    ax.annotate("", xy=(0.73, 0.37), xytext=(0.65, 0.37), arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=2))
    ax.text(0.68, 0.39, "No", color=ACCENT_CYAN, fontsize=9, fontweight='bold')

    # Both lead to update
    ax.annotate("", xy=(0.40, 0.24), xytext=(0.16, 0.33), arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=2))
    ax.annotate("", xy=(0.60, 0.24), xytext=(0.84, 0.33), arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=2))
    ax.annotate("", xy=(0.50, 0.095), xytext=(0.50, 0.16), arrowprops=dict(arrowstyle="->", color=ACCENT_GREEN, lw=2))

    save_fig(fig, "port_detection_flowchart.png")

# ==========================================
# 8. Figure 3.8: Dynamic Threat Risk Assessment
# ==========================================
def gen_fig3_8():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "Dynamic Threat Risk Assessment Engine", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.91, "Multi-Factor Weighted Quantification of Attack Surface and CVSS Metrics", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    # Mathematical Equation Banner
    draw_card(ax, 0.15, 0.77, 0.70, 0.10, "", "", bg="#1E293B", border=ACCENT_CYAN, border_width=2)
    ax.text(0.50, 0.82, r"$R_t = \min\left(100, \; \sum_{v \in \mathcal{V}_t} w_v \cdot \mathrm{CVSS}(v) + \alpha |\mathcal{P}_{\mathrm{crit}}| + \beta \log_2(1 + |\mathcal{E}|)\right)$",
            color=TEXT_WHITE, fontsize=13, ha='center', va='center', zorder=5)

    # 3 Inputs Cards
    inputs = [
        ("Verified Vulnerabilities", "Sum of CVSS Base Scores (0-10)\nweighted by exposure coefficient w_v", 0.06, ACCENT_RED),
        ("Critical Exposed Ports", "Count of high-impact ports exposed:\n{21, 22, 80, 443, 3306, 8080} * alpha", 0.38, ACCENT_AMBER),
        ("Discovered Threat Signals", "Anomaly indicators & banner warnings:\nLogarithmic scaling factor beta", 0.70, ACCENT_PURPLE)
    ]
    for ititle, idesc, ix, icol in inputs:
        draw_card(ax, ix, 0.44, 0.24, 0.26, ititle, "", bg="#131B2E", border=icol)
        ax.text(ix + 0.12, 0.63, ititle, color=icol, fontsize=11, fontweight='bold', ha='center', zorder=5)
        ax.text(ix + 0.12, 0.52, idesc, color=TEXT_WHITE, fontsize=8.5, ha='center', zorder=5)
        ax.annotate("", xy=(0.50, 0.77), xytext=(ix + 0.12, 0.70), arrowprops=dict(arrowstyle="->", color=icol, lw=2))

    # Severity Tier Scales
    draw_card(ax, 0.06, 0.08, 0.88, 0.28, "Composite Threat Index Tier Mapping (R_t in [0, 100])", "", border=CARD_BORDER)
    tiers = [
        ("LOW THREAT (0.0 - 24.9)", "Standard perimeter services, no CVEs,\nrestricted ingress filtering.", 0.08, ACCENT_GREEN),
        ("MODERATE (25.0 - 49.9)", "Informational disclosures, non-critical\nports open, outdated headers.", 0.30, ACCENT_CYAN),
        ("HIGH THREAT (50.0 - 74.9)", "Vulnerable software versions, unencrypted\nauth protocols, CVE > 6.0.", 0.52, ACCENT_AMBER),
        ("CRITICAL (75.0 - 100.0)", "Verified RCE, SQLi, root exposure,\nimmediate automated remediation required.", 0.74, ACCENT_RED)
    ]
    for tt, td, tx, tc in tiers:
        draw_card(ax, tx, 0.11, 0.20, 0.18, tt, "", bg="#1E293B", border=tc)
        ax.text(tx + 0.10, 0.23, tt, color=tc, fontsize=9.5, fontweight='bold', ha='center', zorder=5)
        ax.text(tx + 0.10, 0.16, td, color=TEXT_WHITE, fontsize=7.5, ha='center', zorder=5)

    save_fig(fig, "risk_engine.png")

if __name__ == "__main__":
    print("Generating Figures 3.1 to 3.8...")
    gen_fig3_1()
    gen_fig3_2()
    gen_fig3_3()
    gen_fig3_4()
    gen_fig3_5()
    gen_fig3_6()
    gen_fig3_7()
    gen_fig3_8()
    print("Part 1 finished!")
