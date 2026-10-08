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
# 9. Figure 3.9: Machine Learning Scenario Advisor
# ==========================================
def gen_fig3_9():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "Machine Learning Scenario Advisor Architecture", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.91, "State Vector Featurization and Probabilistic Next-Action Tool Recommendation", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    # Box 1: Feature Vector
    draw_card(ax, 0.04, 0.35, 0.24, 0.48, "State Feature Vector phi(S_t)", "Multidimensional encoding x_t in R^d", border=ACCENT_CYAN)
    features = [
        "x_1: Discovered Ports Bitmask",
        "x_2: Web Protocol Detected (80/443)",
        "x_3: Database Port Active (3306/5432)",
        "x_4: Auth Service Present (21/22)",
        "x_5: Web Parameter Vulnerability",
        "x_6: Execution History Length |H|",
        "x_7: Current Composite Risk R_t"
    ]
    for idx, f in enumerate(features):
        ax.text(0.06, 0.70 - idx * 0.05, f, color=TEXT_WHITE, fontsize=8.5, zorder=5)

    # Box 2: ML Model
    draw_card(ax, 0.34, 0.35, 0.30, 0.48, "Multi-Class Classifier", "Ensemble & Deep Categorical Classifier", border=ACCENT_PURPLE)
    ax.text(0.49, 0.74, "Supervised Scenario Model", color=ACCENT_PURPLE, fontsize=11, fontweight='bold', ha='center', zorder=5)
    ax.text(0.49, 0.68, "P(A = a | x_t) = Softmax(W * x_t + b)", color=TEXT_WHITE, fontsize=9.5, family='monospace', ha='center', zorder=5)
    ax.text(0.49, 0.60, "- 500+ Trained Cyber Operational Scenarios\n- Transition Constraint Rule Filter\n- Prevents Out-of-Sequence Exploitation\n- Top-1 Accuracy: 96.2% | Top-3: 99.3%", color=TEXT_MUTED, fontsize=8.5, ha='center', zorder=5)

    # Box 3: Output Recommendations
    draw_card(ax, 0.70, 0.35, 0.26, 0.48, "Tool Action Probabilities", "Ranked Recommendation Output", border=ACCENT_GREEN)
    actions = [
        ("SQLMap (Exploit Audit)", "94.2%", ACCENT_GREEN, 0.942),
        ("Nikto (Web Vuln Scan)", "88.5%", ACCENT_CYAN, 0.885),
        ("Gobuster (Dir Brute)", "72.1%", ACCENT_BLUE, 0.721),
        ("Hydra (Auth Resiliency)", "45.0%", ACCENT_AMBER, 0.450),
        ("SSLyze (TLS Inspection)", "18.3%", TEXT_MUTED, 0.183)
    ]
    for idx, (tname, tprob, tcol, barw) in enumerate(actions):
        ay = 0.70 - idx * 0.075
        ax.text(0.72, ay, tname, color=TEXT_WHITE, fontsize=8.5, fontweight='bold', zorder=5)
        ax.text(0.92, ay, tprob, color=tcol, fontsize=8.5, fontweight='bold', zorder=5)
        # Bar
        ax.plot([0.72, 0.72 + barw * 0.22], [ay - 0.02, ay - 0.02], color=tcol, lw=4, zorder=5)

    # Arrows
    ax.annotate("", xy=(0.34, 0.59), xytext=(0.28, 0.59), arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=2.5))
    ax.annotate("", xy=(0.70, 0.59), xytext=(0.64, 0.59), arrowprops=dict(arrowstyle="->", color=ACCENT_GREEN, lw=2.5))

    # Bottom summary
    draw_card(ax, 0.04, 0.08, 0.92, 0.20, "Decision Rule Integration & Safety Guardrails", "", border=CARD_BORDER)
    ax.text(0.06, 0.19, "- Logical Preconditions: SQL injection audits are suppressed until active HTTP/HTTPS endpoints are verified.", color=TEXT_WHITE, fontsize=9.5)
    ax.text(0.06, 0.14, "- Autonomous Guidance: Replaces trial-and-error CLI workflows with automated, evidence-backed next actions.", color=TEXT_WHITE, fontsize=9.5)

    save_fig(fig, "ml_advisor.png")

# ==========================================
# 10. Figure 3.10: AI Copilot Diagnostic Workflow
# ==========================================
def gen_fig3_10():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "AI Copilot Diagnostic & Remediation Workflow", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.91, "Real-Time Vulnerability Analysis, CVSS Scoring, and Automated Code Patch Synthesis", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    steps = [
        ("1. Vulnerability Trigger", "Parsing engine flags threat:\nSQLi on /search.php?id=1\nCVSS Indicator Triggered", 0.05, ACCENT_RED),
        ("2. Context Assembly", "Aggregates banner info,\nendpoint URI, payload,\nand target tech stack", 0.285, ACCENT_AMBER),
        ("3. AI Copilot Engine", "Hybrid Rule + LLM model\n(Groq Llama-3 / Mistral)\nReasoning & Verification", 0.52, ACCENT_PURPLE),
        ("4. Code Synthesis", "Generates production patch:\n- Parameterized SQL (Py)\n- Node.js PG Prepared Stmts\n- Iptables / WAF Rule (Bash)", 0.755, ACCENT_GREEN)
    ]

    for stitle, sdesc, sx, scol in steps:
        draw_card(ax, sx, 0.48, 0.20, 0.35, stitle, "", bg="#131B2E", border=scol, border_width=2)
        ax.text(sx + 0.10, 0.75, stitle, color=scol, fontsize=11, fontweight='bold', ha='center', zorder=5)
        ax.text(sx + 0.10, 0.62, sdesc, color=TEXT_WHITE, fontsize=9, ha='center', zorder=5)

    for i in range(len(steps) - 1):
        x1 = steps[i][2] + 0.20
        x2 = steps[i+1][2]
        ax.annotate("", xy=(x2, 0.65), xytext=(x1, 0.65), arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=2.5))

    # Bottom Sample Code Output Display
    draw_card(ax, 0.05, 0.06, 0.90, 0.35, "Generated Remediation Code Artifact (Embedded in Sliding Drawer)", "", bg="#050811", border=ACCENT_GREEN)
    code_text = (
        "# [Vulnerability Remediation: CWE-89 SQL Injection in Python / SQLite]\n"
        "# VULNERABLE CODE: cursor.execute(f\"SELECT * FROM users WHERE id = '{user_id}'\")\n"
        "# SECURE PATCH (Synthesized by Kali-Nova Copilot):\n"
        "def get_user_secure(cursor, user_id: str):\n"
        "    query = 'SELECT id, username, role FROM users WHERE id = ?'\n"
        "    cursor.execute(query, (user_id,))   # Bound parameterized query eliminates SQLi\n"
        "    return cursor.fetchone()\n"
        "# WAF Rule (Bash): iptables -A INPUT -p tcp --dport 80 -m string --string \"UNION SELECT\" --algo bm -j DROP"
    )
    ax.text(0.07, 0.24, code_text, color="#34D399", fontsize=8.5, family='monospace', zorder=5)

    save_fig(fig, "ai_copilot.png")

# ==========================================
# 11. Figure 3.11: CVSS-Based Vulnerability Assessment
# ==========================================
def gen_fig3_11():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "CVSS v3.1 Vulnerability Assessment Framework", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.91, "Multi-Vector Metric Quantification and Base Score Computation", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    # Radar/Spider Chart on Left
    ax_sub = fig.add_axes([0.08, 0.20, 0.40, 0.60], polar=True, facecolor="#111827")
    metrics = ['Attack Vector\n(AV: 0.85)', 'Attack Comp.\n(AC: 0.77)', 'Priv. Req.\n(PR: 0.85)',
               'User Interact.\n(UI: 0.85)', 'Scope\n(S: 1.0)', 'Confidentiality\n(C: 0.56)',
               'Integrity\n(I: 0.56)', 'Availability\n(A: 0.56)']
    values = [0.85, 0.77, 0.85, 0.85, 1.0, 0.56, 0.56, 0.56]
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    ax_sub.plot(angles, values, color=ACCENT_RED, linewidth=2.5, linestyle='solid')
    ax_sub.fill(angles, values, color=ACCENT_RED, alpha=0.35)
    ax_sub.set_xticks(angles[:-1])
    ax_sub.set_xticklabels(metrics, color=TEXT_WHITE, fontsize=8.5)
    ax_sub.set_yticklabels([])
    ax_sub.grid(color="#374151")
    ax_sub.spines['polar'].set_color(CARD_BORDER)

    # Details on Right
    draw_card(ax, 0.54, 0.18, 0.42, 0.66, "CVSS v3.1 Metric Breakdown & Vector String", "", bg="#131B2E", border=ACCENT_RED)
    ax.text(0.56, 0.77, "VECTOR: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", color=ACCENT_CYAN, fontsize=9, family='monospace', fontweight='bold', zorder=5)
    ax.text(0.56, 0.69, "BASE SCORE: 9.8  //  SEVERITY: CRITICAL", color=ACCENT_RED, fontsize=15, fontweight='bold', zorder=5)

    specs = [
        ("Attack Vector (AV: Network)", "Exploitable remotely across internet/LAN"),
        ("Attack Complexity (AC: Low)", "No specialized conditions or race conditions"),
        ("Privileges Required (PR: None)", "Unauthenticated attacker can trigger exploit"),
        ("User Interaction (UI: None)", "Zero user action required to compromise"),
        ("Scope (S: Unchanged)", "Impacts targeted component directly"),
        ("Impact Metrics (C:H, I:H, A:H)", "Total loss of confidentiality, integrity & availability")
    ]
    for idx, (head, desc) in enumerate(specs):
        sy = 0.60 - idx * 0.065
        ax.text(0.56, sy, head, color=ACCENT_AMBER, fontsize=9.5, fontweight='bold', zorder=5)
        ax.text(0.56, sy - 0.025, desc, color=TEXT_WHITE, fontsize=8, zorder=5)

    save_fig(fig, "cvss_analysis.png")

# ==========================================
# 12. Figure 3.12: Network Visualization Interface
# ==========================================
def gen_fig3_12():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "Network Topology Visualization Interface", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.92, "Spatial Network Mapping with Node Vulnerability Indicators and Live Traffic Links", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    # Main Canvas Card
    draw_card(ax, 0.05, 0.06, 0.90, 0.83, "", "", bg="#0B132B", border=ACCENT_CYAN, border_width=2)

    # Subnet Clusters
    # Center Router
    ax.scatter([0.50], [0.50], color=ACCENT_CYAN, s=550, zorder=5, edgecolor=TEXT_WHITE, lw=2)
    ax.text(0.50, 0.44, "Core Gateway / Firewall\n192.168.1.1 (FortiGate)", color=TEXT_WHITE, fontsize=9, fontweight='bold', ha='center', zorder=6)

    # Subnet Nodes
    net_nodes = [
        (0.25, 0.70, "Target Web App\n.105 (Apache/PHP)\nSTATUS: VULNERABLE", ACCENT_RED, [80, 443]),
        (0.75, 0.70, "Database Cluster\n.120 (MySQL 8.0)\nSTATUS: AT-RISK", ACCENT_AMBER, [3306]),
        (0.25, 0.30, "Auth Gateway\n.115 (OpenSSH/PAM)\nSTATUS: AUDITED", ACCENT_GREEN, [22]),
        (0.75, 0.30, "Internal File Server\n.130 (vsftpd 2.3.4)\nSTATUS: COMPROMISED", ACCENT_RED, [21]),
        (0.50, 0.78, "DNS / AD Controller\n.100 (Windows Server)\nSTATUS: FILTERED", ACCENT_BLUE, [53, 389])
    ]

    for nx, ny, nlbl, ncol, nports in net_nodes:
        # Link to router
        ax.plot([0.50, nx], [0.50, ny], color=ncol, lw=2, alpha=0.7, zorder=3)
        # Node
        ax.scatter([nx], [ny], color=ncol, s=400, zorder=5, edgecolor=TEXT_WHITE, lw=1.5)
        ax.text(nx, ny - 0.08, nlbl, color=TEXT_WHITE, fontsize=8.5, ha='center', zorder=6)
        # Port Badges
        p_str = "Ports: " + ", ".join(map(str, nports))
        ax.text(nx, ny + 0.05, p_str, color=ncol, fontsize=8, fontweight='bold', ha='center', zorder=6)

    # Cross connections
    ax.plot([0.25, 0.75], [0.70, 0.70], color="#6B7280", lw=1.2, ls=":", zorder=2)
    ax.text(0.50, 0.71, "Internal SQL Query Traffic (Port 3306)", color=TEXT_MUTED, fontsize=7.5, ha='center')

    # Legend in corner
    draw_card(ax, 0.07, 0.08, 0.35, 0.16, "Status Legend", "", bg="#111827", border=CARD_BORDER)
    ax.scatter([0.09], [0.17], color=ACCENT_RED, s=80)
    ax.text(0.12, 0.165, "Critical Vulnerability Discovered", color=TEXT_WHITE, fontsize=8)
    ax.scatter([0.09], [0.13], color=ACCENT_AMBER, s=80)
    ax.text(0.12, 0.125, "At-Risk / Elevated Exposure", color=TEXT_WHITE, fontsize=8)
    ax.scatter([0.09], [0.09], color=ACCENT_GREEN, s=80)
    ax.text(0.12, 0.085, "Secure / Hardened Node", color=TEXT_WHITE, fontsize=8)

    save_fig(fig, "network_visualization.png")

# ==========================================
# 13. Figure 3.13: Real-Time Network Port Matrix
# ==========================================
def gen_fig3_13():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "Real-Time Network Port Matrix Interface", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.92, "Synchronized Port Telemetry, Banner Ingestion, and Risk Assessment Grid", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    # Table Header Card
    draw_card(ax, 0.05, 0.81, 0.90, 0.07, "", "", bg="#1E293B", border=ACCENT_CYAN)
    headers = [("PORT / PROTO", 0.07), ("SERVICE BANNER", 0.23), ("STATE", 0.44), ("RISK LEVEL", 0.56), ("DETECTED CVE / CWE", 0.70), ("ACTION", 0.88)]
    for hname, hx in headers:
        ax.text(hx, 0.84, hname, color=ACCENT_CYAN, fontsize=9.5, fontweight='bold', zorder=5)

    # Rows
    rows = [
        ("21 / TCP", "vsftpd 2.3.4 (Anonymous Access)", "OPEN", "CRITICAL", "CVE-2011-2523 (Backdoor)", "Launch Hydra", ACCENT_RED),
        ("22 / TCP", "OpenSSH 8.9p1 (Ubuntu Linux)", "OPEN", "LOW", "No Known Exploits", "Audit Keys", ACCENT_GREEN),
        ("53 / UDP", "BIND 9.16.1 (DNS Resolver)", "OPEN", "LOW", "Standard DNS", "DNS Query", ACCENT_GREEN),
        ("80 / TCP", "Apache/2.4.41 (PHP 7.4.3)", "OPEN", "HIGH", "CWE-89 SQL Injection", "Launch Nikto", ACCENT_RED),
        ("443 / TCP", "Apache/2.4.41 (OpenSSL 1.1.1)", "OPEN", "MODERATE", "TLS 1.0/1.1 Deprecated", "Run SSLyze", ACCENT_AMBER),
        ("3306 / TCP", "MariaDB 10.3.38 (MySQL Protocol)", "OPEN", "CRITICAL", "Remote Unauth Root", "Launch SQLMap", ACCENT_RED),
        ("8080 / TCP", "Werkzeug/2.0.2 Python/3.10", "OPEN", "HIGH", "Debug Console Exposed", "Audit HTTP", ACCENT_AMBER),
        ("9001 / TCP", "Custom Telemetry Daemon", "FILTERED", "LOW", "Firewall Dropped", "Probe Port", TEXT_MUTED)
    ]

    for idx, (port, serv, state, rlevel, cve, act, rcol) in enumerate(rows):
        ry = 0.72 - idx * 0.08
        draw_card(ax, 0.05, ry, 0.90, 0.068, "", "", bg="#111827", border=CARD_BORDER)
        ax.text(0.07, ry + 0.022, port, color=TEXT_WHITE, fontsize=9, fontweight='bold', zorder=5)
        ax.text(0.23, ry + 0.022, serv, color=TEXT_MUTED, fontsize=8.5, zorder=5)
        ax.text(0.44, ry + 0.022, state, color=ACCENT_GREEN if state=="OPEN" else TEXT_MUTED, fontsize=8.5, fontweight='bold', zorder=5)
        ax.text(0.56, ry + 0.022, rlevel, color=rcol, fontsize=8.5, fontweight='bold', zorder=5)
        ax.text(0.70, ry + 0.022, cve, color=TEXT_WHITE, fontsize=8, zorder=5)

        # Action button
        draw_card(ax, 0.86, ry + 0.01, 0.08, 0.048, "", "", bg="#1E293B", border=rcol)
        ax.text(0.90, ry + 0.025, act, color=rcol, fontsize=7.5, fontweight='bold', ha='center', zorder=5)

    save_fig(fig, "port_matrix.png")

# ==========================================
# 14. Figure 3.14: Radar-Based Network Visualization
# ==========================================
def gen_fig3_14():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "Radar-Based Network Threat Visualization", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.92, "Holographic 360-Degree Spatial Radar Sweep with Dynamic Target Blips", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    # Radar Center
    rcx, rcy = 0.50, 0.48
    # Concentric Rings
    radii = [0.10, 0.20, 0.30, 0.38]
    ring_labels = ["Internal LAN (Tier 1)", "DMZ / App Cluster (Tier 2)", "External Perimeter (Tier 3)", "Internet Gateway Scope"]
    for r, rlbl in zip(radii, ring_labels):
        circle = plt.Circle((rcx, rcy), r, color=ACCENT_CYAN, fill=False, lw=1.5, alpha=0.5, ls="--", zorder=3)
        ax.add_patch(circle)
        ax.text(rcx + r - 0.01, rcy + 0.01, rlbl, color=ACCENT_CYAN, fontsize=7.5, alpha=0.8, ha='right')

    # Crosshairs
    ax.plot([rcx - 0.40, rcx + 0.40], [rcy, rcy], color=ACCENT_CYAN, lw=1, alpha=0.4, ls=":", zorder=3)
    ax.plot([rcx, rcx], [rcy - 0.40, rcy + 0.40], color=ACCENT_CYAN, lw=1, alpha=0.4, ls=":", zorder=3)

    # Rotating Sweep Wedge
    wedge = patches.Wedge((rcx, rcy), 0.38, 45, 95, facecolor=ACCENT_GREEN, alpha=0.20, zorder=4)
    ax.add_patch(wedge)
    ax.plot([rcx, rcx + 0.38 * np.cos(np.radians(95))], [rcy, rcy + 0.38 * np.sin(np.radians(95))], color=ACCENT_GREEN, lw=2.5, zorder=5)

    # Blips
    blips = [
        (rcx + 0.07, rcy + 0.06, "192.168.1.1 (Gateway)", ACCENT_GREEN),
        (rcx + 0.15, rcy + 0.12, "192.168.1.105 (Web Target - SQLi)", ACCENT_RED),
        (rcx - 0.14, rcy + 0.08, "192.168.1.120 (DB Server)", ACCENT_AMBER),
        (rcx + 0.22, rcy - 0.18, "192.168.1.130 (FTP Backdoor)", ACCENT_RED),
        (rcx - 0.24, rcy - 0.14, "192.168.1.110 (Client Workstation)", ACCENT_CYAN)
    ]
    for bx, by, blbl, bcol in blips:
        # Ping ring
        pring = plt.Circle((bx, by), 0.02, color=bcol, fill=False, lw=1.2, alpha=0.8, zorder=5)
        ax.add_patch(pring)
        ax.scatter([bx], [by], color=bcol, s=100, zorder=6, edgecolor=TEXT_WHITE)
        ax.text(bx, by - 0.03, blbl, color=TEXT_WHITE, fontsize=8, fontweight='bold', ha='center', zorder=7)

    # Stats HUD Cards on Sides
    draw_card(ax, 0.04, 0.65, 0.22, 0.22, "RADAR TELEMETRY", "Live Sweep Metrics", border=ACCENT_GREEN)
    ax.text(0.06, 0.77, "Sweep Frequency: 20 FPS\nActive Sector: 045° - 095°\nTarget Host: 192.168.1.105\nHost Health: CRITICAL (78%)", color=TEXT_WHITE, fontsize=8.5)

    draw_card(ax, 0.74, 0.65, 0.22, 0.22, "SPATIAL SIGNALS", "Detection Log", border=ACCENT_RED)
    ax.text(0.76, 0.77, "Nodes Detected: 5 Active\nVulnerabilities: 7 Flagged\nPacket Rate: 1.4 kpps\nThreat Proximity: IMMEDIATE", color=TEXT_WHITE, fontsize=8.5)

    save_fig(fig, "radar_visualization.png")

# ==========================================
# 15. Figure 3.15: Dynamic Threat Risk Gauge
# ==========================================
def gen_fig3_15():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "Dynamic Threat Risk Gauge HUD", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.91, "Quantified Threat Score Visualization with Multi-Tier Severity Spectrum", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    # Large Center Gauge
    gcx, gcy = 0.50, 0.45
    r_outer = 0.28
    r_inner = 0.20

    # Draw arc segments
    angles_def = [
        (np.pi, np.pi * 0.75, ACCENT_GREEN, "LOW (0-25)"),
        (np.pi * 0.75, np.pi * 0.50, ACCENT_CYAN, "MODERATE (25-50)"),
        (np.pi * 0.50, np.pi * 0.25, ACCENT_AMBER, "ELEVATED (50-75)"),
        (np.pi * 0.25, 0, ACCENT_RED, "CRITICAL (75-100)")
    ]
    for start_a, end_a, col, lbl in angles_def:
        t = np.linspace(start_a, end_a, 50)
        ax.plot(gcx + r_outer * np.cos(t), gcy + r_outer * np.sin(t), color=col, lw=18, zorder=3)

    # Needle pointing at 78.4 (angle = pi * (1 - 0.784))
    needle_angle = np.pi * (1.0 - 0.784)
    nx = gcx + 0.25 * np.cos(needle_angle)
    ny = gcy + 0.25 * np.sin(needle_angle)
    ax.plot([gcx, nx], [gcy, ny], color=TEXT_WHITE, lw=4, zorder=6)
    ax.scatter([gcx], [gcy], color=ACCENT_RED, s=250, zorder=7, edgecolor=TEXT_WHITE, lw=2)

    # Digital Score Readout
    ax.text(gcx, gcy + 0.08, "78.4", color=TEXT_WHITE, fontsize=32, fontweight='bold', ha='center', zorder=8)
    ax.text(gcx, gcy + 0.03, "/ 100", color=TEXT_MUTED, fontsize=13, ha='center', zorder=8)
    ax.text(gcx, gcy - 0.06, "CRITICAL EXPOSURE DETECTED", color=ACCENT_RED, fontsize=13, fontweight='bold', ha='center', zorder=8)

    # Supporting Parameter Cards
    params = [
        ("Discovered Critical Ports", "4 Ports Open\n(21, 80, 443, 3306)", 0.08, ACCENT_AMBER),
        ("CVSS Weighted Vulnerabilities", "Score Sum: 64.2\n(CVE-2011-2523, SQLi)", 0.38, ACCENT_RED),
        ("Attack Surface Coefficient", "Alpha: 1.25 | Beta: 0.85\nNormalized Exposure: 84.3%", 0.68, ACCENT_PURPLE)
    ]
    for ptitle, pdesc, px, pcol in params:
        draw_card(ax, px, 0.06, 0.24, 0.18, ptitle, "", bg="#131B2E", border=pcol)
        ax.text(px + 0.12, 0.18, ptitle, color=pcol, fontsize=10, fontweight='bold', ha='center', zorder=5)
        ax.text(px + 0.12, 0.11, pdesc, color=TEXT_WHITE, fontsize=8.5, ha='center', zorder=5)

    save_fig(fig, "risk_gauge.png")

# ==========================================
# 16. Figure 3.16: Complete Tool Execution Workflow
# ==========================================
def gen_fig3_16():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "Complete Tool Execution Lifecycle", color=TEXT_WHITE, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.92, "Stateful Lifecycle from Parameter Serialization to Database Archiving", color=ACCENT_CYAN, fontsize=10.5, ha='center')

    lifecycle_nodes = [
        ("1. GUI Parameterization", "User configures target, timing,\nflags & mode in UI form", 0.06, 0.68, ACCENT_CYAN),
        ("2. Scope Validation", "Boundary CIDR validation\nenforces ethical scope", 0.29, 0.68, ACCENT_BLUE),
        ("3. Concurrency Thread", "CommandThread allocates PTY\nand spawns child process", 0.52, 0.68, ACCENT_PURPLE),
        ("4. Streaming Telemetry", "Asynchronous chunk reads\nstream stdout to Console", 0.75, 0.68, ACCENT_GREEN),

        ("8. Persistent Archiving", "Scan metadata, stdout hash,\nand risk saved to kalinova.db", 0.06, 0.24, ACCENT_GREEN),
        ("7. Copilot & ML Update", "ML Advisor recommends next step;\nAI Copilot generates patch", 0.29, 0.24, ACCENT_AMBER),
        ("6. Risk Recalculation", "RiskEngine computes new R_t\nupdates Threat Gauge & Radar", 0.52, 0.24, ACCENT_RED),
        ("5. Real-Time Regex Parser", "Output evaluated for open ports\nand vulnerability signatures", 0.75, 0.24, ACCENT_CYAN)
    ]

    for title, desc, nx, ny, ncol in lifecycle_nodes:
        draw_card(ax, nx, ny, 0.19, 0.18, title, "", bg="#131B2E", border=ncol, border_width=1.8)
        ax.text(nx + 0.095, ny + 0.13, title, color=ncol, fontsize=10, fontweight='bold', ha='center', zorder=5)
        ax.text(nx + 0.095, ny + 0.06, desc, color=TEXT_WHITE, fontsize=8, ha='center', zorder=5)

    # Forward arrows top row
    ax.annotate("", xy=(0.29, 0.77), xytext=(0.25, 0.77), arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=2))
    ax.annotate("", xy=(0.52, 0.77), xytext=(0.48, 0.77), arrowprops=dict(arrowstyle="->", color=ACCENT_BLUE, lw=2))
    ax.annotate("", xy=(0.75, 0.77), xytext=(0.71, 0.77), arrowprops=dict(arrowstyle="->", color=ACCENT_PURPLE, lw=2))

    # Turn down
    ax.annotate("", xy=(0.845, 0.42), xytext=(0.845, 0.68), arrowprops=dict(arrowstyle="->", color=ACCENT_GREEN, lw=2))

    # Reverse arrows bottom row
    ax.annotate("", xy=(0.71, 0.33), xytext=(0.75, 0.33), arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=2))
    ax.annotate("", xy=(0.48, 0.33), xytext=(0.52, 0.33), arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=2))
    ax.annotate("", xy=(0.25, 0.33), xytext=(0.29, 0.33), arrowprops=dict(arrowstyle="->", color=ACCENT_AMBER, lw=2))

    save_fig(fig, "tool_execution_workflow.png")

if __name__ == "__main__":
    print("Generating Figures 3.9 to 3.16...")
    gen_fig3_9()
    gen_fig3_10()
    gen_fig3_11()
    gen_fig3_12()
    gen_fig3_13()
    gen_fig3_14()
    gen_fig3_15()
    gen_fig3_16()
    print("Part 2 finished!")
