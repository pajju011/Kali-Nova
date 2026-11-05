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
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.02",
                                 facecolor=bg, edgecolor=border, linewidth=lw, linestyle=ls, hatch=hatch, zorder=zorder)
    ax.add_patch(box)
    return box

# ==========================================
# 1. Figure 3.1: Overall Architecture of Kali-Nova
# ==========================================
def gen_fig3_1():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Tier 1 (Presentation Layer)
    draw_box(ax, 0.03, 0.68, 0.94, 0.28, bg=FILL_LIGHT, lw=2)
    ax.text(0.05, 0.925, "1. PRESENTATION LAYER (PyQt6 Cyber HUD)", color=TEXT_BLACK, fontsize=14, fontweight='bold')
    p_mods = [
        ("Navigation\nSidebar", "Recon, Web, Auth,\nNetwork, Reports", 0.05),
        ("Master Bento\nDashboard", "Threat Radar & Gauge\nPort Matrix, History", 0.235),
        ("Tool\nWorkspaces", "Dynamic Forms &\nScope Validation", 0.42),
        ("Interactive\nConsole", "Live PTY Telemetry,\nANSI & Stdin Stream", 0.605),
        ("AI Copilot\nDrawer", "CVSS Diagnostics,\nCode Remediation", 0.79)
    ]
    for name, desc, px in p_mods:
        draw_box(ax, px, 0.70, 0.165, 0.20, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.3)
        ax.text(px + 0.0825, 0.852, name, color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')
        ax.plot([px + 0.02, px + 0.145], [0.805, 0.805], color=BORDER_BLACK, lw=0.8)
        ax.text(px + 0.0825, 0.752, desc, color=TEXT_MUTED, fontsize=10.2, ha='center', va='center')

    # Tier 2 (Concurrency & Orchestration)
    draw_box(ax, 0.03, 0.36, 0.94, 0.275, bg=FILL_LIGHT, lw=2)
    ax.text(0.05, 0.605, "2. CONCURRENCY & ORCHESTRATION LAYER (Qt Signals & Workers)", color=TEXT_BLACK, fontsize=14, fontweight='bold')
    c_mods = [
        ("AppState Singleton", "State Tuple S_t = <T,P,E,A,H,R_t>\nCentralized Reactive State Engine", 0.07),
        ("InteractiveExecutor", "QThread Workers & POSIX PTY\nNon-Blocking Async Subprocess Control", 0.37),
        ("Event & Parsing Engine", "Real-Time Heuristic Regex Engine\nPort, Banner & CVE Diagnostic Tokens", 0.67)
    ]
    for name, desc, cx in c_mods:
        draw_box(ax, cx, 0.38, 0.26, 0.20, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.3)
        ax.text(cx + 0.13, 0.535, name, color=TEXT_BLACK, fontsize=12.2, fontweight='bold', ha='center')
        ax.plot([cx + 0.03, cx + 0.23], [0.510, 0.510], color=BORDER_BLACK, lw=0.8)
        ax.text(cx + 0.13, 0.445, desc, color=TEXT_MUTED, fontsize=10.5, ha='center', va='center')

    # Tier 3 (Intelligence & Persistence)
    draw_box(ax, 0.03, 0.04, 0.94, 0.275, bg=FILL_LIGHT, lw=2)
    ax.text(0.05, 0.285, "3. INTELLIGENCE & PERSISTENCE LAYER (ML, AI, & Database)", color=TEXT_BLACK, fontsize=14, fontweight='bold')
    i_mods = [
        ("ML Scenario\nAdvisor", "Feature Vector x_t\nTop-1 / Top-3 Next Actions", 0.05),
        ("Dynamic Risk\nEngine", "Multi-Factor CVSS Model\nRisk Index R_t in [0, 100]", 0.235),
        ("Multimodal\nAI Copilot", "Groq / Ollama / Mistral\nAutomated Code Patches", 0.42),
        ("SQLite DB\n(kalinova.db)", "Persistent Scan Records,\nTarget Entities & Ledger", 0.605),
        ("ReportLab\nCompiler", "Executive PDF Reports &\nInteractive HTML Dash", 0.79)
    ]
    for name, desc, ix in i_mods:
        draw_box(ax, ix, 0.06, 0.165, 0.20, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.3)
        ax.text(ix + 0.0825, 0.212, name, color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')
        ax.plot([ix + 0.02, ix + 0.145], [0.165, 0.165], color=BORDER_BLACK, lw=0.8)
        ax.text(ix + 0.0825, 0.115, desc, color=TEXT_MUTED, fontsize=10.2, ha='center', va='center')

    # Connecting Arrows between Tiers
    for x_arr in [0.20, 0.50, 0.80]:
        ax.annotate("", xy=(x_arr, 0.68), xytext=(x_arr, 0.635),
                    arrowprops=dict(arrowstyle="<->", color=BORDER_BLACK, lw=2.2))
        ax.annotate("", xy=(x_arr, 0.36), xytext=(x_arr, 0.315),
                    arrowprops=dict(arrowstyle="<->", color=BORDER_BLACK, lw=2.2))

    save_fig(fig, "system_architecture.png")

# ==========================================
# 2. Figure 3.2: Kali-Nova Main Dashboard
# ==========================================
def gen_fig3_2():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Topbar Header Bar
    draw_box(ax, 0.02, 0.915, 0.96, 0.065, bg=FILL_GRAY1, border=BORDER_BLACK, lw=1.5)
    ax.text(0.04, 0.9475, "KALI-NOVA  v1.3.1", color=TEXT_BLACK, fontsize=13, fontweight='bold', va='center')
    ax.text(0.50, 0.9475, "TARGET: 192.168.1.105   |   PROFILE: EXPERT   |   STATUS: ARMED", color=TEXT_BLACK, fontsize=10.5, fontweight='bold', ha='center', va='center')
    ax.text(0.96, 0.9475, "[ONLINE]", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='right', va='center')

    # Left Sidebar
    draw_box(ax, 0.02, 0.04, 0.17, 0.855, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
    draw_box(ax, 0.03, 0.825, 0.15, 0.055, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1)
    ax.text(0.105, 0.8525, "NAVIGATION", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')

    nav_items = ["Dashboard (Active)", "Reconnaissance (Nmap)", "Web Security (Nikto)", "Auth Resiliency (Hydra)", "Network Audit (SSLyze)", "Database Reports", "Global Settings"]
    for i, item in enumerate(nav_items):
        y_pos = 0.735 - i * 0.098
        bg_col = FILL_GRAY1 if i == 0 else FILL_WHITE
        draw_box(ax, 0.03, y_pos, 0.15, 0.078, bg=bg_col, border=BORDER_BLACK, lw=1.2)
        ax.text(0.105, y_pos + 0.039, item, color=TEXT_BLACK, fontsize=10.2, fontweight='bold' if i==0 else 'normal', ha='center', va='center')

    # Top-Left: Threat Gauge
    draw_box(ax, 0.21, 0.50, 0.38, 0.395, bg=FILL_WHITE, lw=1.5)
    ax.text(0.23, 0.86, "DYNAMIC THREAT RISK GAUGE", color=TEXT_BLACK, fontsize=12.5, fontweight='bold')
    ax.plot([0.23, 0.57], [0.845, 0.845], color=BORDER_BLACK, lw=0.8)

    # Arc Gauge
    theta = np.linspace(np.pi, 0, 100)
    r = 0.075
    cx, cy = 0.40, 0.74
    ax.plot(cx + r*np.cos(theta), cy + r*np.sin(theta), color=FILL_GRAY3, lw=9, zorder=3)
    t_active = np.linspace(np.pi, np.pi * 0.22, 78)
    ax.plot(cx + r*np.cos(t_active), cy + r*np.sin(t_active), color=BORDER_BLACK, lw=9, zorder=4)

    # Dedicated score box safely below arc
    draw_box(ax, 0.32, 0.595, 0.16, 0.085, bg=FILL_GRAY1, border=BORDER_BLACK, lw=1)
    ax.text(0.40, 0.65, "78.4 / 100", color=TEXT_BLACK, fontsize=14, fontweight='bold', ha='center')
    ax.text(0.40, 0.612, "CRITICAL EXPOSURE", color=TEXT_BLACK, fontsize=9.8, fontweight='bold', ha='center')

    # Metric summary boxes
    draw_box(ax, 0.23, 0.515, 0.16, 0.068, bg=FILL_LIGHT, lw=1)
    ax.text(0.31, 0.549, "Critical Ports: 4 Open\nActive CVEs: 6 Verified", color=TEXT_BLACK, fontsize=9.2, fontweight='bold', ha='center', va='center')
    draw_box(ax, 0.41, 0.515, 0.16, 0.068, bg=FILL_LIGHT, lw=1)
    ax.text(0.49, 0.549, "Exploit Surface: 84.3%\nStatus: Urgent Action", color=TEXT_BLACK, fontsize=9.2, fontweight='bold', ha='center', va='center')

    # Top-Right: Network Radar Topology
    draw_box(ax, 0.61, 0.50, 0.37, 0.395, bg=FILL_WHITE, lw=1.5)
    ax.text(0.63, 0.86, "NETWORK TOPOLOGY & RADAR SCAN", color=TEXT_BLACK, fontsize=12.5, fontweight='bold')
    ax.plot([0.63, 0.96], [0.845, 0.845], color=BORDER_BLACK, lw=0.8)

    rcx, rcy = 0.80, 0.685
    for rad in [0.035, 0.075, 0.115]:
        circle = plt.Circle((rcx, rcy), rad, color=BORDER_BLACK, fill=False, lw=1, ls="--", alpha=0.6, zorder=3)
        ax.add_patch(circle)
    nodes = [(0.80, 0.685, "Gateway\n192.168.1.1"),
             (0.86, 0.745, "Target Web\n.105 (Vuln)"),
             (0.74, 0.625, "Database\n.120 (At-Risk)"),
             (0.86, 0.625, "Client Node\n.110 (Active)")]
    for nx, ny, lbl in nodes:
        ax.scatter([nx], [ny], color=BORDER_BLACK, s=115, zorder=5)
        ax.plot([rcx, nx], [rcy, ny], color=BORDER_BLACK, lw=1, ls=":", zorder=4)
        ax.text(nx, ny - 0.040, lbl, color=TEXT_BLACK, fontsize=9.2, fontweight='bold', ha='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))

    # Bottom-Left: Port Matrix
    draw_box(ax, 0.21, 0.04, 0.38, 0.44, bg=FILL_WHITE, lw=1.5)
    ax.text(0.23, 0.445, "REAL-TIME OPEN PORT MATRIX", color=TEXT_BLACK, fontsize=12.5, fontweight='bold')
    ax.plot([0.23, 0.57], [0.43, 0.43], color=BORDER_BLACK, lw=0.8)

    # Table Header Row
    ax.text(0.23, 0.405, "PORT", color=TEXT_BLACK, fontsize=10, fontweight='bold')
    ax.text(0.31, 0.405, "SERVICE BANNER", color=TEXT_BLACK, fontsize=10, fontweight='bold')
    ax.text(0.45, 0.405, "STATE", color=TEXT_BLACK, fontsize=10, fontweight='bold')
    ax.text(0.515, 0.405, "RISK", color=TEXT_BLACK, fontsize=10, fontweight='bold')
    ax.plot([0.22, 0.58], [0.395, 0.395], color=BORDER_BLACK, lw=1)

    ports_data = [
        ("21/TCP", "vsftpd 2.3.4 (Anon)", "OPEN", "CRITICAL"),
        ("22/TCP", "OpenSSH 8.9p1", "OPEN", "SECURE"),
        ("80/TCP", "Apache 2.4.41", "OPEN", "HIGH"),
        ("443/TCP", "HTTPS (TLS 1.3)", "OPEN", "MODERATE"),
        ("3306/TCP", "MariaDB 10.3", "OPEN", "CRITICAL")
    ]
    for idx, (p, s, st, rk) in enumerate(ports_data):
        py = 0.332 - idx * 0.065
        draw_box(ax, 0.22, py, 0.36, 0.055, bg=FILL_GRAY1 if idx%2==0 else FILL_WHITE, border=BORDER_BLACK, lw=0.8)
        ax.text(0.23, py + 0.027, p, color=TEXT_BLACK, fontsize=9.8, fontweight='bold', va='center')
        ax.text(0.31, py + 0.027, s, color=TEXT_MUTED, fontsize=9.5, va='center')
        ax.text(0.45, py + 0.027, st, color=TEXT_BLACK, fontsize=9.5, fontweight='bold', va='center')
        ax.text(0.515, py + 0.027, rk, color=TEXT_BLACK, fontsize=9.2, fontweight='bold', va='center')

    # Bottom-Right: AI Copilot & Console
    draw_box(ax, 0.61, 0.04, 0.37, 0.44, bg=FILL_WHITE, lw=1.5)
    ax.text(0.63, 0.445, "AI COPILOT REMEDIATION & CONSOLE", color=TEXT_BLACK, fontsize=12.5, fontweight='bold')
    ax.plot([0.63, 0.96], [0.43, 0.43], color=BORDER_BLACK, lw=0.8)

    # AI Summary Box
    draw_box(ax, 0.625, 0.255, 0.34, 0.165, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1)
    ax.text(0.635, 0.385, "DIAGNOSTIC FINDING:", color=TEXT_BLACK, fontsize=11, fontweight='bold')
    ax.text(0.635, 0.345, "Vuln: SQLi on parameter 'id' (CVSS 9.8)", color=TEXT_BLACK, fontsize=10, fontweight='bold')
    ax.text(0.635, 0.310, "Action: Execute SQLMap -> Bound Parameters", color=TEXT_MUTED, fontsize=10)
    ax.text(0.635, 0.275, "Remediation patch ready in sliding drawer.", color=TEXT_MUTED, fontsize=9.5, style='italic')

    # Console Terminal Box
    draw_box(ax, 0.625, 0.055, 0.34, 0.185, bg=FILL_GRAY1, border=BORDER_BLACK, lw=1)
    console_lines = [
        "[*] [18:42:01] Starting Nmap 7.94 scan on .105...",
        "[+] [18:42:03] Discovered 5 open ports on host.",
        "[!] [18:42:05] WARNING: Anonymous FTP allowed",
        "[+] [18:42:07] AppState updated. Risk Score: 78.4",
        "[*] [18:42:08] Awaiting automated audit approval..."
    ]
    for ci, cline in enumerate(console_lines):
        ax.text(0.635, 0.205 - ci * 0.034, cline[:42], color=TEXT_BLACK, fontsize=9.0, family='monospace', va='center')

    save_fig(fig, "main_dashboard.png")

# ==========================================
# 3. Figure 3.3: Security Tool Integration Workflow
# ==========================================
def gen_fig3_3():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    steps = [
        ("1. Tool\nSelection", "Analyst selects\nmodule (Nmap,\nNikto, Hydra)"),
        ("2. Form\nGeneration", "Dynamic GUI:\ntarget, ports,\ntiming profiles"),
        ("3. Scope\nValidation", "CIDR validation\nenforces ethical\naudit boundary"),
        ("4. Command\nSynthesis", "Builds escaped\nCLI parameters\n& artifacts"),
        ("5. Async\nDispatch", "Spawns worker\nQThread & live\nPTY subprocess"),
        ("6. Stream\n& State", "Parses stdout,\nextracts events,\nupdates state")
    ]

    for i, (title, desc) in enumerate(steps):
        sx = 0.04 + i * 0.158
        draw_box(ax, sx, 0.44, 0.126, 0.50, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(sx + 0.063, 0.855, title, color=TEXT_BLACK, fontsize=12, fontweight='bold', ha='center', va='center')
        ax.plot([sx + 0.015, sx + 0.111], [0.785, 0.785], color=BORDER_BLACK, lw=0.8)
        ax.text(sx + 0.063, 0.58, desc, color=TEXT_MUTED, fontsize=10.5, ha='center', va='center')

    for i in range(len(steps) - 1):
        x1 = 0.04 + i * 0.158 + 0.126 + 0.006
        x2 = 0.04 + (i + 1) * 0.158 - 0.006
        ax.annotate("", xy=(x2, 0.785), xytext=(x1, 0.785),
                    arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))

    draw_box(ax, 0.04, 0.06, 0.92, 0.32, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5)
    ax.text(0.06, 0.32, "Key Architectural Safeguards & Mechanisms", color=TEXT_BLACK, fontsize=13.5, fontweight='bold')
    ax.plot([0.06, 0.44], [0.295, 0.295], color=BORDER_BLACK, lw=1)
    ax.text(0.06, 0.23, "- Input Sanitization: Strict parameter escaping prevents command injection inside Kali-Nova itself.", color=TEXT_BLACK, fontsize=11.5)
    ax.text(0.06, 0.15, "- Pipeline Artifact Handoff: Discovered open ports (e.g. 80, 443) automatically pre-populate downstream web tools.", color=TEXT_BLACK, fontsize=11.5)
    ax.text(0.06, 0.07, "- Audit Compliance: Full command line, timestamp, user context, and output hash are recorded to kalinova.db.", color=TEXT_BLACK, fontsize=11.5)

    save_fig(fig, "tool_integration.png")

# ==========================================
# 4. Figure 3.4: Asynchronous Command Execution
# ==========================================
def gen_fig3_4():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    cols = [
        ("Main UI Thread\n(PyQt6)", 0.14),
        ("Worker Thread\n(InteractiveExecutor)", 0.50),
        ("OS Subprocess Layer\n(CLI)", 0.86)
    ]
    for ctitle, cx in cols:
        draw_box(ax, cx - 0.13, 0.84, 0.26, 0.11, bg=FILL_GRAY2, border=BORDER_BLACK, lw=1.5)
        ax.text(cx, 0.895, ctitle, color=TEXT_BLACK, fontsize=12.5, fontweight='bold', ha='center', va='center')
        ax.plot([cx, cx], [0.06, 0.84], color=BORDER_BLACK, ls="--", lw=1.2, zorder=1)

    seq = [
        (0.75, 0.14, 0.50, "1. User starts scan -> Spawns worker"),
        (0.65, 0.50, 0.86, "2. Subprocess.Popen() creates child CLI"),
        (0.55, 0.86, 0.50, "3. Streaming stdout read into buffer chunk"),
        (0.45, 0.50, 0.14, "4. Emit Qt Signal: output_received()"),
        (0.35, 0.50, 0.50, "5. Regex extracts ports & signatures"),
        (0.25, 0.86, 0.50, "6. Process terminates with exit code"),
        (0.15, 0.50, 0.14, "7. Emit Qt Signal: finished() -> Unlock UI")
    ]

    for y, x_from, x_to, msg in seq:
        if x_from != x_to:
            ax.annotate("", xy=(x_to, y), xytext=(x_from, y),
                        arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
            mid_x = (x_from + x_to) / 2
            ax.text(mid_x, y + 0.025, msg, color=TEXT_BLACK, fontsize=11, fontweight='bold', ha='center', zorder=5,
                    bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))
        else:
            arc = patches.Arc((x_from + 0.02, y), 0.04, 0.04, angle=0, theta1=-90, theta2=90, color=BORDER_BLACK, lw=1.5)
            ax.add_patch(arc)
            ax.text(x_from + 0.05, y, msg, color=TEXT_BLACK, fontsize=11, fontweight='bold', va='center', zorder=5,
                    bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))

    save_fig(fig, "async_execution.png")

# ==========================================
# 5. Figure 3.5: Global State Management
# ==========================================
def gen_fig3_5():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Center Card
    draw_box(ax, 0.31, 0.19, 0.38, 0.75, bg=FILL_LIGHT, border=BORDER_BLACK, lw=2)
    ax.text(0.50, 0.895, "SINGLETON AppState (State Engine)", color=TEXT_BLACK, fontsize=13.5, fontweight='bold', ha='center')
    ax.text(0.50, 0.845, r"$\mathcal{S}_t = \langle \mathcal{T}, \mathcal{P}, \mathcal{E}, \mathcal{A}, \mathcal{H}, R_t \rangle$", color=TEXT_BLACK, fontsize=13.5, ha='center')
    ax.plot([0.33, 0.67], [0.815, 0.815], color=BORDER_BLACK, lw=1)

    state_elements = [
        (r"- T (Scope):", "Target IP addresses & CIDR boundary masks"),
        (r"- P (Ports):", "Open port set: {21, 22, 80, 443, 3306}"),
        (r"- E (Events):", "Detected threat events & banner vulnerabilities"),
        (r"- A (Artifacts):", "Web endpoints, parameters, & hashes"),
        (r"- H (History):", "Chronological tool log & timestamp trace"),
        (r"- R_t (Risk):", "Normalized dynamic composite risk score (0-100)")
    ]
    for idx, (el, sub) in enumerate(state_elements):
        ey = 0.745 - idx * 0.088
        ax.text(0.33, ey, el, color=TEXT_BLACK, fontsize=11.5, fontweight='bold')
        ax.text(0.33, ey - 0.038, sub, color=TEXT_MUTED, fontsize=10.2)

    # 4 Satellites
    satellites = [
        ("Execution Engine", "Dispatches stdout chunks\n& process exit signals", 0.04, 0.58),
        ("Parsing Engine", "Injects discovered ports\n& vulnerability findings", 0.04, 0.19),
        ("Dynamic Risk Engine", "Queries P & E to compute\ncomposite threat index R_t", 0.74, 0.58),
        ("UI View Subscribers", "Subscribes to state updates\n(Dashboard, Port Matrix, HUD)", 0.74, 0.19)
    ]
    for s_title, s_desc, sx, sy in satellites:
        draw_box(ax, sx, sy, 0.22, 0.29, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5)
        ax.text(sx + 0.11, sy + 0.225, s_title, color=TEXT_BLACK, fontsize=12.5, fontweight='bold', ha='center')
        ax.plot([sx + 0.03, sx + 0.19], [sy + 0.195, sy + 0.195], color=BORDER_BLACK, lw=0.8)
        ax.text(sx + 0.11, sy + 0.10, s_desc, color=TEXT_MUTED, fontsize=10.8, ha='center', va='center')

    # Bottom DB Card
    draw_box(ax, 0.31, 0.04, 0.38, 0.12, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5)
    ax.text(0.50, 0.115, "SQLite Persistence Engine", color=TEXT_BLACK, fontsize=12, fontweight='bold', ha='center')
    ax.plot([0.35, 0.65], [0.095, 0.095], color=BORDER_BLACK, lw=0.8)
    ax.text(0.50, 0.065, "Commits persistent state snapshot to kalinova.db", color=TEXT_MUTED, fontsize=10.5, ha='center')

    # Connecting arrows
    ax.annotate("", xy=(0.305, 0.72), xytext=(0.265, 0.72), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.annotate("", xy=(0.305, 0.33), xytext=(0.265, 0.33), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.annotate("", xy=(0.735, 0.72), xytext=(0.695, 0.72), arrowprops=dict(arrowstyle="<-", color=BORDER_BLACK, lw=2.2))
    ax.annotate("", xy=(0.735, 0.33), xytext=(0.695, 0.33), arrowprops=dict(arrowstyle="<-", color=BORDER_BLACK, lw=2.2))
    ax.annotate("", xy=(0.50, 0.165), xytext=(0.50, 0.190), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))

    save_fig(fig, "global_state.png")

# ==========================================
# 6. Figure 3.6: Event and Port Parsing Process
# ==========================================
def gen_fig3_6():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Left: Raw Output Stream
    draw_box(ax, 0.04, 0.40, 0.26, 0.56, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.06, 0.91, "1. Raw Output Stream", color=TEXT_BLACK, fontsize=12.5, fontweight='bold')
    ax.plot([0.06, 0.28], [0.89, 0.89], color=BORDER_BLACK, lw=0.8)
    raw_text = (
        "80/tcp open http Apache/2.4.41\n\n"
        "[+] Vuln: SQL Injection detected\n"
        "    in /search.php?q=admin\n\n"
        "3306/tcp open mysql MariaDB\n\n"
        "Discovered Subdomain: api.host\n"
        "MD5: 5d41402abc4b2a76b9719d"
    )
    ax.text(0.06, 0.835, raw_text, color=TEXT_BLACK, fontsize=9.8, family='monospace', va='top')

    # Center: Regex Engine
    draw_box(ax, 0.34, 0.40, 0.34, 0.56, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.36, 0.91, "2. Regex Rules Engine", color=TEXT_BLACK, fontsize=12.5, fontweight='bold')
    ax.plot([0.36, 0.66], [0.89, 0.89], color=BORDER_BLACK, lw=0.8)
    regexes = [
        ("Port Pattern:", r"(\d+)/(tcp|udp)\s+(\w+)\s+(.+)"),
        ("SQLi Event:", r"(SQL injection|syntax error)"),
        ("Web Endpoint:", r"(https?://[^\s]+|/[a-zA-Z0-9_\-\./]+)"),
        ("Hash String:", r"([a-fA-F0-9]{32,64})")
    ]
    for idx, (lbl, reg) in enumerate(regexes):
        ry = 0.83 - idx * 0.105
        ax.text(0.36, ry, lbl, color=TEXT_BLACK, fontsize=11.5, fontweight='bold')
        ax.text(0.36, ry - 0.04, reg, color=TEXT_MUTED, fontsize=10.2, family='monospace')

    # Right: Extracted Entities
    draw_box(ax, 0.72, 0.40, 0.24, 0.56, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.74, 0.91, "3. Extracted Entities", color=TEXT_BLACK, fontsize=12.5, fontweight='bold')
    ax.plot([0.74, 0.94], [0.89, 0.89], color=BORDER_BLACK, lw=0.8)
    extracted = [
        "- Port: 80/TCP (HTTP)",
        "- Port: 3306/TCP (MySQL)",
        "- Event: SQL_INJECTION",
        "- Endpoint: /search.php",
        "- Artifact: api.host",
        "- Credential Hash Extracted"
    ]
    for idx, item in enumerate(extracted):
        ax.text(0.74, 0.83 - idx * 0.075, item, color=TEXT_BLACK, fontsize=11, fontweight='bold')

    # Inter-stage arrows
    ax.annotate("", xy=(0.335, 0.62), xytext=(0.305, 0.62), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.annotate("", xy=(0.715, 0.62), xytext=(0.685, 0.62), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))

    # Downstream consumers
    draw_box(ax, 0.04, 0.05, 0.92, 0.30, bg=FILL_WHITE, lw=1.5)
    ax.text(0.06, 0.305, "Downstream Event Consumers & Dispatched Signals", color=TEXT_BLACK, fontsize=13.5, fontweight='bold')
    ax.plot([0.06, 0.48], [0.285, 0.285], color=BORDER_BLACK, lw=1)

    downstream = [
        ("AppState Update", "Registers open ports in P,\nupdates entity dictionary A", 0.07),
        ("Dynamic Risk Engine", "Computes updated CVSS score\nand threat severity gauge", 0.38),
        ("AI Copilot Trigger", "Generates contextual patch\n(Python/Node.js remediation)", 0.69)
    ]
    for dtitle, ddesc, dx in downstream:
        draw_box(ax, dx, 0.08, 0.24, 0.18, bg=FILL_GRAY1, border=BORDER_BLACK, lw=1.2)
        ax.text(dx + 0.12, 0.21, dtitle, color=TEXT_BLACK, fontsize=12, fontweight='bold', ha='center')
        ax.plot([dx + 0.03, dx + 0.21], [0.185, 0.185], color=BORDER_BLACK, lw=0.8)
        ax.text(dx + 0.12, 0.13, ddesc, color=TEXT_MUTED, fontsize=10.5, ha='center', va='center')

    save_fig(fig, "parsing_engine.png")

# ==========================================
# 7. Figure 3.7: Port Detection Flowchart
# ==========================================
def gen_fig3_7():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Top: START box
    draw_box(ax, 0.40, 0.90, 0.20, 0.065, bg=FILL_GRAY2, lw=1.5)
    ax.text(0.50, 0.9325, "START", color=TEXT_BLACK, fontsize=13, fontweight='bold', ha='center', va='center')

    # Read Stdout box
    draw_box(ax, 0.34, 0.77, 0.32, 0.075, bg=FILL_WHITE, lw=1.5)
    ax.text(0.50, 0.8075, "Read Stdout Stream Chunk", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center', va='center')

    # Diamond 1: Matches Port Pattern?
    d1 = patches.Polygon([[0.50, 0.72], [0.67, 0.64], [0.50, 0.56], [0.33, 0.64]], closed=True,
                         facecolor=FILL_LIGHT, edgecolor=BORDER_BLACK, lw=1.5, zorder=2)
    ax.add_patch(d1)
    ax.text(0.50, 0.64, "Matches Port Pattern\n(Regex Test)?", color=TEXT_BLACK, fontsize=11, fontweight='bold', ha='center', va='center', zorder=5)

    # Diamond 2: Is Port Critical?
    d2 = patches.Polygon([[0.50, 0.46], [0.67, 0.38], [0.50, 0.30], [0.33, 0.38]], closed=True,
                         facecolor=FILL_LIGHT, edgecolor=BORDER_BLACK, lw=1.5, zorder=2)
    ax.add_patch(d2)
    ax.text(0.50, 0.38, "Is Port Critical\n(in P_crit)?", color=TEXT_BLACK, fontsize=11, fontweight='bold', ha='center', va='center', zorder=5)

    # Left: High Risk Weight
    draw_box(ax, 0.06, 0.33, 0.23, 0.10, bg=FILL_WHITE, lw=1.5)
    ax.text(0.175, 0.395, "Assign High Risk Weight", color=TEXT_BLACK, fontsize=11, fontweight='bold', ha='center')
    ax.text(0.175, 0.355, "Trigger Critical Alert", color=TEXT_MUTED, fontsize=10, ha='center')

    # Right: Standard Weight
    draw_box(ax, 0.71, 0.33, 0.23, 0.10, bg=FILL_WHITE, lw=1.5)
    ax.text(0.825, 0.395, "Assign Standard Weight", color=TEXT_BLACK, fontsize=11, fontweight='bold', ha='center')
    ax.text(0.825, 0.355, "Standard Registry Entry", color=TEXT_MUTED, fontsize=10, ha='center')

    # Update AppState box
    draw_box(ax, 0.32, 0.16, 0.36, 0.085, bg=FILL_GRAY1, lw=1.5)
    ax.text(0.50, 0.215, "Update AppState & Port Matrix", color=TEXT_BLACK, fontsize=12, fontweight='bold', ha='center')
    ax.text(0.50, 0.18, "Emit Signals to UI & Recalculate Risk", color=TEXT_MUTED, fontsize=10.5, ha='center')

    # END box
    draw_box(ax, 0.42, 0.035, 0.16, 0.065, bg=FILL_GRAY2, lw=1.5)
    ax.text(0.50, 0.0675, "END", color=TEXT_BLACK, fontsize=13, fontweight='bold', ha='center', va='center')

    # Connections
    ax.annotate("", xy=(0.50, 0.845), xytext=(0.50, 0.90), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.annotate("", xy=(0.50, 0.72), xytext=(0.50, 0.77), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.annotate("", xy=(0.50, 0.46), xytext=(0.50, 0.56), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.text(0.53, 0.51, "Yes", color=TEXT_BLACK, fontsize=11, fontweight='bold')

    ax.plot([0.33, 0.02, 0.02], [0.64, 0.64, 0.0675], color=BORDER_BLACK, lw=1.8, ls="--")
    ax.annotate("", xy=(0.415, 0.0675), xytext=(0.02, 0.0675), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=1.8))
    ax.text(0.28, 0.655, "No", color=TEXT_BLACK, fontsize=10.5, fontweight='bold')

    ax.annotate("", xy=(0.295, 0.38), xytext=(0.33, 0.38), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.text(0.305, 0.41, "Yes", color=TEXT_BLACK, fontsize=10.5, fontweight='bold')

    ax.annotate("", xy=(0.705, 0.38), xytext=(0.67, 0.38), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))
    ax.text(0.675, 0.41, "No", color=TEXT_BLACK, fontsize=10.5, fontweight='bold')

    ax.plot([0.175, 0.175, 0.32], [0.33, 0.2025, 0.2025], color=BORDER_BLACK, lw=1.8)
    ax.plot([0.825, 0.825, 0.68], [0.33, 0.2025, 0.2025], color=BORDER_BLACK, lw=1.8)
    ax.annotate("", xy=(0.50, 0.105), xytext=(0.50, 0.16), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))

    save_fig(fig, "port_detection_flowchart.png")

# ==========================================
# 8. Figure 3.8: Dynamic Threat Risk Assessment
# ==========================================
def gen_fig3_8():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Equation Banner
    draw_box(ax, 0.08, 0.81, 0.84, 0.14, bg=FILL_GRAY1, border=BORDER_BLACK, lw=2)
    ax.text(0.50, 0.88, r"$R_t = \min\left(100, \; \sum_{v \in \mathcal{V}_t} w_v \cdot \mathrm{CVSS}(v) + \alpha |\mathcal{P}_{\mathrm{crit}}| + \beta \log_2(1 + |\mathcal{E}|)\right)$",
            color=TEXT_BLACK, fontsize=14.5, ha='center', va='center')

    # 3 Inputs
    inputs = [
        ("Verified Vulnerabilities", "Sum of CVSS Base Scores\nweighted by exposure\ncoefficient w_v", 0.05),
        ("Critical Exposed Ports", "High-impact ports exposed:\n{21, 22, 80, 443, 3306}\nscaled by alpha", 0.38),
        ("Discovered Threat Signals", "Anomaly indicators and\nwarnings scaled by\nfactor beta", 0.71)
    ]
    for ititle, idesc, ix in inputs:
        draw_box(ax, ix, 0.44, 0.24, 0.31, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5)
        ax.text(ix + 0.12, 0.68, ititle, color=TEXT_BLACK, fontsize=12.2, fontweight='bold', ha='center')
        ax.plot([ix + 0.02, ix + 0.22], [0.655, 0.655], color=BORDER_BLACK, lw=0.8)
        ax.text(ix + 0.12, 0.54, idesc, color=TEXT_MUTED, fontsize=10.5, ha='center', va='center')
        ax.annotate("", xy=(ix + 0.12, 0.805), xytext=(ix + 0.12, 0.755), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.2))

    # Tiers at bottom
    draw_box(ax, 0.05, 0.05, 0.90, 0.34, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.07, 0.345, "Composite Threat Index Tier Mapping (R_t in [0, 100])", color=TEXT_BLACK, fontsize=13.5, fontweight='bold')
    ax.plot([0.07, 0.47], [0.325, 0.325], color=BORDER_BLACK, lw=1)

    tiers = [
        ("LOW (0.0 - 24.9)", "Standard perimeter\nservices; zero\nverified CVEs.", 0.07, FILL_WHITE),
        ("MODERATE (25.0 - 49.9)", "Informational leaks;\nnon-critical open\nports identified.", 0.29, FILL_LIGHT),
        ("HIGH (50.0 - 74.9)", "Vulnerable software;\nunencrypted login\nprotocols active.", 0.51, FILL_GRAY1),
        ("CRITICAL (75.0 - 100)", "Verified RCE, SQLi,\nroot exposure;\npatching required.", 0.73, FILL_GRAY2)
    ]
    for tt, td, tx, tbg in tiers:
        draw_box(ax, tx, 0.08, 0.19, 0.22, bg=tbg, border=BORDER_BLACK, lw=1.5)
        ax.text(tx + 0.095, 0.245, tt, color=TEXT_BLACK, fontsize=11, fontweight='bold', ha='center')
        ax.plot([tx + 0.02, tx + 0.17], [0.22, 0.22], color=BORDER_BLACK, lw=0.8)
        ax.text(tx + 0.095, 0.145, td, color=TEXT_BLACK, fontsize=10.2, ha='center', va='center')

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
