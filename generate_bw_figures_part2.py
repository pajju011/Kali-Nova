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
    r"c:\Users\ASUS\Desktop\Kali-Nova\report_images"
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

def draw_box(ax, x, y, w, h, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5, ls='-', hatch=None, zorder=3):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.02",
                                 facecolor=bg, edgecolor=border, linewidth=lw, linestyle=ls, hatch=hatch, zorder=zorder)
    ax.add_patch(box)
    return box

# ==========================================
# 9. Figure 3.9: Machine Learning Scenario Advisor
# ==========================================
def gen_fig3_9():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.965, "Machine Learning Scenario Advisor Architecture", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "State Vector Featurization and Probabilistic Next-Action Tool Recommendation", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    # Box 1: Feature Vector
    draw_box(ax, 0.04, 0.35, 0.26, 0.52, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.06, 0.835, "1. Feature Vector phi(S_t)", color=TEXT_BLACK, fontsize=10.5, fontweight='bold')
    ax.plot([0.06, 0.28], [0.815, 0.815], color=BORDER_BLACK, lw=0.8)
    features = [
        "x_1: Discovered Ports Bitmask",
        "x_2: Web Protocol (80/443)",
        "x_3: Database Port (3306/5432)",
        "x_4: Auth Protocol (21/22)",
        "x_5: Web Parameter Vulnerability",
        "x_6: Execution Trace Length |H|",
        "x_7: Current Composite Risk R_t"
    ]
    for idx, f in enumerate(features):
        ax.text(0.06, 0.76 - idx * 0.058, f, color=TEXT_BLACK, fontsize=8.5)

    # Box 2: Classifier
    draw_box(ax, 0.35, 0.35, 0.30, 0.52, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.50, 0.835, "2. Scenario Model Engine", color=TEXT_BLACK, fontsize=10.5, fontweight='bold', ha='center')
    ax.plot([0.38, 0.62], [0.815, 0.815], color=BORDER_BLACK, lw=0.8)
    ax.text(0.50, 0.75, r"$P(A = a \mid \mathbf{x}_t) = \mathrm{Softmax}(\mathbf{W}\mathbf{x}_t + \mathbf{b})$", color=TEXT_BLACK, fontsize=9.5, ha='center')
    ax.plot([0.38, 0.62], [0.71, 0.71], color=BORDER_BLACK, lw=0.8)
    summary_text = (
        "- 500+ Operational Scenarios\n\n"
        "- Dependency Precondition Filter\n\n"
        "- Prevents Illegal Tool Sequences\n\n"
        "- Top-1 Acc: 96.2% | Top-3: 99.3%"
    )
    ax.text(0.50, 0.54, summary_text, color=TEXT_MUTED, fontsize=8.5, ha='center', va='center')

    # Box 3: Recommendations
    draw_box(ax, 0.70, 0.35, 0.26, 0.52, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.72, 0.835, "3. Action Probabilities", color=TEXT_BLACK, fontsize=10.5, fontweight='bold')
    ax.plot([0.72, 0.94], [0.815, 0.815], color=BORDER_BLACK, lw=0.8)
    actions = [
        ("SQLMap (Exploit Audit)", "94.2%", 0.942, FILL_GRAY3),
        ("Nikto (Web Vuln Scan)", "88.5%", 0.885, FILL_GRAY2),
        ("Gobuster (Dir Brute)", "72.1%", 0.721, FILL_GRAY2),
        ("Hydra (Auth Resiliency)", "45.0%", 0.450, FILL_GRAY1),
        ("SSLyze (TLS Audit)", "18.3%", 0.183, FILL_LIGHT)
    ]
    for idx, (tname, tprob, barw, fcol) in enumerate(actions):
        ay = 0.76 - idx * 0.082
        ax.text(0.72, ay, tname, color=TEXT_BLACK, fontsize=8.5, fontweight='bold')
        ax.text(0.93, ay, tprob, color=TEXT_BLACK, fontsize=8.5, fontweight='bold', ha='right')
        rect = patches.Rectangle((0.72, ay - 0.027), barw * 0.21, 0.014, facecolor=fcol, edgecolor=BORDER_BLACK, lw=1, zorder=5)
        ax.add_patch(rect)

    ax.annotate("", xy=(0.35, 0.61), xytext=(0.30, 0.61), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))
    ax.annotate("", xy=(0.70, 0.61), xytext=(0.65, 0.61), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    draw_box(ax, 0.04, 0.08, 0.92, 0.22, bg=FILL_WHITE, lw=1.5)
    ax.text(0.06, 0.25, "Decision Rule Integration & Safety Guardrails", color=TEXT_BLACK, fontsize=10.5, fontweight='bold')
    ax.plot([0.06, 0.42], [0.23, 0.23], color=BORDER_BLACK, lw=0.8)
    ax.text(0.06, 0.175, "- Logical Preconditions: SQL injection audits are suppressed until active HTTP/HTTPS endpoints are verified.", color=TEXT_BLACK, fontsize=9.5)
    ax.text(0.06, 0.12, "- Autonomous Guidance: Replaces trial-and-error CLI workflows with automated, evidence-backed next actions.", color=TEXT_BLACK, fontsize=9.5)

    save_fig(fig, "ml_advisor.png")

# ==========================================
# 10. Figure 3.10: AI Copilot Diagnostic Workflow
# ==========================================
def gen_fig3_10():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.965, "AI Copilot Diagnostic & Remediation Workflow", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Real-Time Vulnerability Analysis, CVSS Scoring, and Automated Code Patch Synthesis", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    steps = [
        ("1. Vulnerability Trigger", "Parsing engine flags threat:\nSQLi on /search.php?id=1\nCVSS Indicator Triggered", 0.05),
        ("2. Context Assembly", "Aggregates banner info,\nendpoint URI, payload,\nand target tech stack", 0.29),
        ("3. AI Copilot Engine", "Hybrid Rule + LLM model\n(Groq Llama-3 / Mistral)\nReasoning & Verification", 0.53),
        ("4. Code Synthesis", "Generates production patch:\n- Parameterized SQL (Py)\n- Node.js Prepared Stmt\n- Iptables / WAF Rule", 0.77)
    ]

    for stitle, sdesc, sx in steps:
        draw_box(ax, sx, 0.52, 0.18, 0.34, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(sx + 0.09, 0.81, stitle, color=TEXT_BLACK, fontsize=10, fontweight='bold', ha='center')
        ax.plot([sx + 0.02, sx + 0.16], [0.78, 0.78], color=BORDER_BLACK, lw=0.8)
        ax.text(sx + 0.09, 0.65, sdesc, color=TEXT_MUTED, fontsize=8.5, ha='center', va='center')

    for i in range(len(steps) - 1):
        x1 = steps[i][2] + 0.18
        x2 = steps[i+1][2]
        ax.annotate("", xy=(x2, 0.69), xytext=(x1, 0.69), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2))

    draw_box(ax, 0.05, 0.05, 0.90, 0.42, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5)
    ax.text(0.07, 0.425, "Generated Remediation Code Artifact (Embedded in Sliding Drawer)", color=TEXT_BLACK, fontsize=10.5, fontweight='bold')
    ax.plot([0.07, 0.55], [0.405, 0.405], color=BORDER_BLACK, lw=0.8)

    draw_box(ax, 0.06, 0.07, 0.88, 0.31, bg=FILL_GRAY1, border=BORDER_BLACK, lw=1)
    code_text = (
        "# [Vulnerability Remediation: CWE-89 SQL Injection in Python / SQLite]\n"
        "# VULNERABLE CODE: cursor.execute(f\"SELECT * FROM users WHERE id = '{user_id}'\")\n\n"
        "# SECURE REFACTORED CODE (Synthesized by Kali-Nova AI Copilot):\n"
        "def get_user_secure(cursor, user_id: str):\n"
        "    query = 'SELECT id, username, role FROM users WHERE id = ?'\n"
        "    cursor.execute(query, (user_id,))   # Bound parameterized query eliminates SQLi injection\n"
        "    return cursor.fetchone()\n\n"
        "# WAF Firewall Rule (Bash): iptables -A INPUT -p tcp --dport 80 -m string --string \"UNION SELECT\" --algo bm -j DROP"
    )
    ax.text(0.08, 0.35, code_text, color=TEXT_BLACK, fontsize=8, family='monospace', va='top')

    save_fig(fig, "ai_copilot.png")

# ==========================================
# 11. Figure 3.11: CVSS-Based Vulnerability Assessment
# ==========================================
def gen_fig3_11():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.965, "CVSS v3.1 Vulnerability Assessment Framework", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Multi-Vector Metric Quantification and Base Score Computation", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    # Polar Chart safely on left
    ax_sub = fig.add_axes([0.04, 0.14, 0.39, 0.70], polar=True, facecolor=BG_WHITE)
    metrics = ['Attack Vector\n(AV: 0.85)', 'Attack Comp.\n(AC: 0.77)', 'Priv. Req.\n(PR: 0.85)',
               'User Interact.\n(UI: 0.85)', 'Scope\n(S: 1.0)', 'Confidentiality\n(C: 0.56)',
               'Integrity\n(I: 0.56)', 'Availability\n(A: 0.56)']
    values = [0.85, 0.77, 0.85, 0.85, 1.0, 0.56, 0.56, 0.56]
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    ax_sub.plot(angles, values, color=BORDER_BLACK, linewidth=2, linestyle='solid')
    ax_sub.fill(angles, values, color=FILL_GRAY2, alpha=0.45)
    ax_sub.set_xticks(angles[:-1])
    ax_sub.set_xticklabels(metrics, color=TEXT_BLACK, fontsize=8)
    ax_sub.set_yticklabels([])
    ax_sub.grid(color=FILL_GRAY3)
    ax_sub.spines['polar'].set_color(BORDER_BLACK)

    # Right Card safely separated
    draw_box(ax, 0.48, 0.14, 0.48, 0.72, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.50, 0.815, "CVSS v3.1 Metric Breakdown & Vector String", color=TEXT_BLACK, fontsize=11, fontweight='bold')
    ax.plot([0.50, 0.94], [0.795, 0.795], color=BORDER_BLACK, lw=0.8)

    ax.text(0.50, 0.755, "VECTOR: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", color=TEXT_BLACK, fontsize=8.5, family='monospace', fontweight='bold')
    ax.text(0.50, 0.705, "BASE SCORE: 9.8   //   SEVERITY: CRITICAL", color=TEXT_BLACK, fontsize=13, fontweight='bold')
    ax.plot([0.50, 0.94], [0.68, 0.68], color=BORDER_BLACK, lw=1)

    specs = [
        ("Attack Vector (AV: Network)", "Exploitable remotely across internet / LAN"),
        ("Attack Complexity (AC: Low)", "No specialized timing or race conditions required"),
        ("Privileges Required (PR: None)", "Unauthenticated attacker can trigger exploit"),
        ("User Interaction (UI: None)", "Zero user action required to achieve compromise"),
        ("Scope (S: Unchanged)", "Directly impacts targeted database / host component"),
        ("Impact Metrics (C:H, I:H, A:H)", "Total loss of confidentiality, integrity & availability")
    ]
    for idx, (head, desc) in enumerate(specs):
        sy = 0.62 - idx * 0.075
        ax.text(0.50, sy, head, color=TEXT_BLACK, fontsize=9, fontweight='bold')
        ax.text(0.50, sy - 0.028, desc, color=TEXT_MUTED, fontsize=8)

    save_fig(fig, "cvss_analysis.png")

# ==========================================
# 12. Figure 3.12: Network Visualization Interface
# ==========================================
def gen_fig3_12():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.965, "Network Topology Visualization Interface", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Spatial Network Mapping with Node Vulnerability Indicators and Live Traffic Links", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    # Main Canvas Frame
    draw_box(ax, 0.03, 0.04, 0.94, 0.87, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5, zorder=1)

    # Core Router Center
    rcx, rcy = 0.50, 0.48

    # Network Nodes configuration (x, y, title, subtitle, status_badge, ports)
    net_nodes = [
        (0.50, 0.77, "DNS / AD Controller", "100 (Windows Server)", "STATUS: FILTERED", "Ports: 53, 389"),
        (0.18, 0.67, "Target Web App", ".105 (Apache/PHP)", "STATUS: VULNERABLE", "Ports: 80, 443"),
        (0.82, 0.67, "Database Cluster", ".120 (MySQL 8.0)", "STATUS: AT-RISK", "Port: 3306"),
        (0.18, 0.32, "Auth Gateway", ".115 (OpenSSH/PAM)", "STATUS: AUDITED", "Port: 22"),
        (0.82, 0.32, "Internal File Server", ".130 (vsftpd 2.3.4)", "STATUS: COMPROMISED", "Port: 21")
    ]

    # Draw connection lines FIRST at zorder=2 so they terminate cleanly behind node boxes
    for nx, ny, _, _, _, _ in net_nodes:
        ax.plot([rcx, nx], [rcy, ny], color=BORDER_BLACK, lw=1.6, zorder=2)

    # Draw Internal SQL Traffic Link between Web App and Database
    ax.plot([0.18, 0.82], [0.67, 0.67], color=BORDER_BLACK, lw=1.4, ls=":", zorder=2)
    ax.text(0.50, 0.625, "Internal SQL Traffic Link (Port 3306)", color=TEXT_BLACK, fontsize=8, ha='center',
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=BORDER_BLACK, lw=0.8), zorder=6)

    # Draw Central Gateway Box at zorder=3 (solid white fill, cleanly covers lines)
    draw_box(ax, rcx - 0.11, rcy - 0.07, 0.22, 0.14, bg=FILL_GRAY2, border=BORDER_BLACK, lw=2, zorder=3)
    ax.text(rcx, rcy + 0.035, "Core Gateway / Firewall", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', zorder=5)
    ax.text(rcx, rcy + 0.005, "192.168.1.1", color=TEXT_BLACK, fontsize=9, ha='center', zorder=5)
    ax.plot([rcx - 0.08, rcx + 0.08], [rcy - 0.015, rcy - 0.015], color=BORDER_BLACK, lw=0.8, zorder=5)
    ax.text(rcx, rcy - 0.045, "[Subnet Root: /24]", color=TEXT_MUTED, fontsize=8.5, ha='center', zorder=5)

    # Draw Peripheral Node Boxes at zorder=3 with NO HATCHING
    for nx, ny, ntitle, nsub, nstat, nports in net_nodes:
        draw_box(ax, nx - 0.11, ny - 0.07, 0.22, 0.14, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5, zorder=3)
        ax.text(nx, ny + 0.042, ntitle, color=TEXT_BLACK, fontsize=9, fontweight='bold', ha='center', zorder=5)
        ax.text(nx, ny + 0.015, nsub, color=TEXT_MUTED, fontsize=8, ha='center', zorder=5)
        ax.plot([nx - 0.08, nx + 0.08], [ny - 0.005, ny - 0.005], color=BORDER_BLACK, lw=0.6, zorder=5)
        ax.text(nx, ny - 0.026, nstat, color=TEXT_BLACK, fontsize=8, fontweight='bold', ha='center', zorder=5)
        ax.text(nx, ny - 0.052, nports, color=TEXT_MUTED, fontsize=7.5, ha='center', zorder=5)

    # Bottom Legend Banner - placed safely below all nodes with NO overlap
    draw_box(ax, 0.08, 0.06, 0.84, 0.12, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.2, zorder=3)
    ax.text(0.50, 0.155, "Node Security Posture & Vulnerability Status Legend", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center', zorder=5)
    ax.plot([0.12, 0.88], [0.14, 0.14], color=BORDER_BLACK, lw=0.6, zorder=5)

    legend_items = [
        (0.18, "VULNERABLE", "Critical RCE / SQLi Exploitable", FILL_GRAY2),
        (0.40, "AT-RISK", "Exposed Database / High Attack Surface", FILL_GRAY1),
        (0.62, "COMPROMISED", "Backdoor Daemon Exploited (Root)", FILL_GRAY3),
        (0.84, "AUDITED", "Hardened Perimeter / Verified Secure", FILL_WHITE)
    ]
    for lx, ltag, ldesc, lcol in legend_items:
        draw_box(ax, lx - 0.08, 0.075, 0.16, 0.05, bg=lcol, border=BORDER_BLACK, lw=1, zorder=4)
        ax.text(lx, 0.105, f"[{ltag}]", color=TEXT_BLACK, fontsize=7.5, fontweight='bold', ha='center', zorder=5)
        ax.text(lx, 0.085, ldesc, color=TEXT_MUTED, fontsize=6.8, ha='center', zorder=5)

    save_fig(fig, "network_visualization.png")

# ==========================================
# 13. Figure 3.13: Real-Time Network Port Matrix
# ==========================================
def gen_fig3_13():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.965, "Real-Time Network Port Matrix Interface", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Synchronized Port Telemetry, Banner Ingestion, and Risk Assessment Grid", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    # Top Rule
    ax.plot([0.05, 0.95], [0.86, 0.86], color=BORDER_BLACK, lw=2.5)
    headers = [("PORT / PROTO", 0.07), ("SERVICE BANNER", 0.22), ("STATE", 0.44), ("RISK LEVEL", 0.55), ("DETECTED CVE / CWE", 0.68), ("ACTION", 0.88)]
    for hname, hx in headers:
        ax.text(hx, 0.825, hname, color=TEXT_BLACK, fontsize=9.5, fontweight='bold', va='center')
    ax.plot([0.05, 0.95], [0.79, 0.79], color=BORDER_BLACK, lw=1.5)

    rows = [
        ("21 / TCP", "vsftpd 2.3.4 (Anonymous Access)", "OPEN", "CRITICAL", "CVE-2011-2523 (Backdoor)", "Launch Hydra"),
        ("22 / TCP", "OpenSSH 8.9p1 (Ubuntu Linux)", "OPEN", "LOW", "No Known Exploits", "Audit Keys"),
        ("53 / UDP", "BIND 9.16.1 (DNS Resolver)", "OPEN", "LOW", "Standard DNS Protocol", "DNS Query"),
        ("80 / TCP", "Apache/2.4.41 (PHP 7.4.3)", "OPEN", "HIGH", "CWE-89 SQL Injection", "Launch Nikto"),
        ("443 / TCP", "Apache/2.4.41 (OpenSSL 1.1.1)", "OPEN", "MODERATE", "TLS 1.0/1.1 Deprecated", "Run SSLyze"),
        ("3306 / TCP", "MariaDB 10.3.38 (MySQL Protocol)", "OPEN", "CRITICAL", "Remote Unauth Root", "Launch SQLMap"),
        ("8080 / TCP", "Werkzeug/2.0.2 Python/3.10", "OPEN", "HIGH", "Debug Console Exposed", "Audit HTTP"),
        ("9001 / TCP", "Custom Telemetry Daemon", "FILTERED", "LOW", "Firewall Dropped Packet", "Probe Port")
    ]

    for idx, (port, serv, state, rlevel, cve, act) in enumerate(rows):
        ry = 0.73 - idx * 0.075
        bg_col = FILL_GRAY1 if idx % 2 == 0 else FILL_WHITE
        rect = patches.Rectangle((0.05, ry - 0.02), 0.90, 0.065, facecolor=bg_col, edgecolor='none', zorder=1)
        ax.add_patch(rect)
        ax.text(0.07, ry + 0.012, port, color=TEXT_BLACK, fontsize=9, fontweight='bold', va='center')
        ax.text(0.22, ry + 0.012, serv, color=TEXT_MUTED, fontsize=8.5, va='center')
        ax.text(0.44, ry + 0.012, state, color=TEXT_BLACK, fontsize=8.5, fontweight='bold', va='center')
        ax.text(0.55, ry + 0.012, rlevel, color=TEXT_BLACK, fontsize=8.5, fontweight='bold', va='center')
        ax.text(0.68, ry + 0.012, cve, color=TEXT_BLACK, fontsize=8, va='center')

        draw_box(ax, 0.86, ry - 0.01, 0.08, 0.045, bg=FILL_WHITE, border=BORDER_BLACK, lw=1)
        ax.text(0.90, ry + 0.012, act, color=TEXT_BLACK, fontsize=7.5, fontweight='bold', ha='center', va='center')

    ax.plot([0.05, 0.95], [0.14, 0.14], color=BORDER_BLACK, lw=2.5)
    save_fig(fig, "port_matrix.png")

# ==========================================
# 14. Figure 3.14: Radar-Based Network Visualization
# ==========================================
def gen_fig3_14():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.965, "Radar-Based Network Threat Visualization", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Spatial Radar Sweep Interface with Real-Time Node Position Markers", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    rcx, rcy = 0.50, 0.48
    radii = [0.08, 0.16, 0.24, 0.32]
    ring_labels = ["Internal LAN (Tier 1)", "DMZ / App Cluster (Tier 2)", "External Perimeter (Tier 3)", "Gateway Perimeter"]
    for r, rlbl in zip(radii, ring_labels):
        circle = plt.Circle((rcx, rcy), r, color=BORDER_BLACK, fill=False, lw=1.2, ls="--", zorder=3)
        ax.add_patch(circle)
        # Position ring label safely along bottom-center to avoid sweep sector
        ax.text(rcx, rcy - r - 0.015, rlbl, color=TEXT_MUTED, fontsize=7.5, ha='center',
                bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"), zorder=5)

    ax.plot([rcx - 0.34, rcx + 0.34], [rcy, rcy], color=BORDER_BLACK, lw=1, ls=":", zorder=3)
    ax.plot([rcx, rcx], [rcy - 0.34, rcy + 0.34], color=BORDER_BLACK, lw=1, ls=":", zorder=3)

    # Smooth transparent wedge with NO hatching
    wedge = patches.Wedge((rcx, rcy), 0.32, 45, 95, facecolor=FILL_GRAY2, alpha=0.35, zorder=4)
    ax.add_patch(wedge)
    ax.plot([rcx, rcx + 0.32 * np.cos(np.radians(95))], [rcy, rcy + 0.32 * np.sin(np.radians(95))], color=BORDER_BLACK, lw=2, zorder=5)

    blips = [
        (rcx + 0.06, rcy + 0.05, "192.168.1.1 (Gateway)", "o"),
        (rcx + 0.14, rcy + 0.12, "192.168.1.105 (Web Target)", "s"),
        (rcx - 0.13, rcy + 0.08, "192.168.1.120 (DB Server)", "^"),
        (rcx + 0.18, rcy - 0.14, "192.168.1.130 (FTP Server)", "D"),
        (rcx - 0.20, rcy - 0.12, "192.168.1.110 (Client PC)", "v")
    ]
    for bx, by, blbl, bmarker in blips:
        pring = plt.Circle((bx, by), 0.018, color=BORDER_BLACK, fill=False, lw=1, ls=":", zorder=5)
        ax.add_patch(pring)
        ax.scatter([bx], [by], color=BORDER_BLACK, marker=bmarker, s=100, zorder=6)
        ax.text(bx, by - 0.035, blbl, color=TEXT_BLACK, fontsize=8, fontweight='bold', ha='center',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=BORDER_BLACK, lw=0.8), zorder=7)

    # Left & Right cards with ample clearance
    draw_box(ax, 0.03, 0.64, 0.19, 0.23, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.05, 0.835, "RADAR TELEMETRY", color=TEXT_BLACK, fontsize=9.5, fontweight='bold')
    ax.plot([0.05, 0.20], [0.815, 0.815], color=BORDER_BLACK, lw=0.6)
    ax.text(0.05, 0.73, "Sweep Rate: 20 FPS\nActive Sector: 045° - 095°\nTarget: 192.168.1.105\nHealth: CRITICAL (78%)", color=TEXT_BLACK, fontsize=8)

    draw_box(ax, 0.78, 0.64, 0.19, 0.23, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.80, 0.835, "SPATIAL SIGNALS", color=TEXT_BLACK, fontsize=9.5, fontweight='bold')
    ax.plot([0.80, 0.95], [0.815, 0.815], color=BORDER_BLACK, lw=0.6)
    ax.text(0.80, 0.73, "Nodes: 5 Active\nVulns: 7 Flagged\nPacket Rate: 1.4 kpps\nProximity: IMMEDIATE", color=TEXT_BLACK, fontsize=8)

    save_fig(fig, "radar_visualization.png")

# ==========================================
# 15. Figure 3.15: Dynamic Threat Risk Gauge
# ==========================================
def gen_fig3_15():
    fig, ax = plt.subplots(figsize=(15, 9), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.965, "Dynamic Threat Risk Gauge HUD", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Quantified Threat Score Visualization with Multi-Tier Severity Spectrum", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    gcx, gcy = 0.50, 0.54
    r_outer = 0.28

    # Clean arc bands with solid grayscale shades - NO HATCHING
    angles_def = [
        (np.pi, np.pi * 0.75, FILL_LIGHT, "LOW (0-25)"),
        (np.pi * 0.75, np.pi * 0.50, FILL_GRAY1, "MODERATE (25-50)"),
        (np.pi * 0.50, np.pi * 0.25, FILL_GRAY2, "ELEVATED (50-75)"),
        (np.pi * 0.25, 0, FILL_GRAY3, "CRITICAL (75-100)")
    ]
    for start_a, end_a, col, lbl in angles_def:
        t = np.linspace(start_a, end_a, 50)
        ax.plot(gcx + r_outer * np.cos(t), gcy + r_outer * np.sin(t), color=BORDER_BLACK, lw=14, zorder=3)
        mid_a = (start_a + end_a) / 2
        ax.text(gcx + 0.33 * np.cos(mid_a), gcy + 0.33 * np.sin(mid_a), lbl, color=TEXT_BLACK, fontsize=8, fontweight='bold', ha='center', va='center')

    # Needle at 78.4%
    needle_angle = np.pi * (1.0 - 0.784)
    nx = gcx + 0.24 * np.cos(needle_angle)
    ny = gcy + 0.24 * np.sin(needle_angle)
    ax.plot([gcx, nx], [gcy, ny], color=BORDER_BLACK, lw=3.5, zorder=6)
    ax.scatter([gcx], [gcy], color=BORDER_BLACK, s=220, zorder=7)

    # Dedicated score box safely placed BELOW needle pivot
    draw_box(ax, 0.35, 0.24, 0.30, 0.15, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
    ax.text(0.50, 0.33, "78.4 / 100", color=TEXT_BLACK, fontsize=20, fontweight='bold', ha='center')
    ax.text(0.50, 0.27, "CRITICAL RISK LEVEL DETECTED", color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center')

    params = [
        ("Discovered Critical Ports", "4 Ports Open\n(21, 80, 443, 3306)", 0.06),
        ("CVSS Weighted Vulnerabilities", "Score Sum: 64.2\n(CVE-2011-2523, SQLi)", 0.38),
        ("Attack Surface Coefficient", "Alpha: 1.25 | Beta: 0.85\nNormalized Exposure: 84.3%", 0.70)
    ]
    for ptitle, pdesc, px in params:
        draw_box(ax, px, 0.05, 0.24, 0.16, bg=FILL_WHITE, lw=1.2)
        ax.text(px + 0.12, 0.16, ptitle, color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center')
        ax.plot([px + 0.02, px + 0.22], [0.14, 0.14], color=BORDER_BLACK, lw=0.8)
        ax.text(px + 0.12, 0.09, pdesc, color=TEXT_MUTED, fontsize=8.5, ha='center', va='center')

    save_fig(fig, "risk_gauge.png")

# ==========================================
# 16. Figure 3.16: Complete Tool Execution Workflow
# ==========================================
def gen_fig3_16():
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.965, "Complete Tool Execution Lifecycle", color=TEXT_BLACK, fontsize=18, fontweight='bold', ha='center')
    ax.text(0.5, 0.93, "Stateful Lifecycle from Parameter Serialization to Database Archiving", color=TEXT_MUTED, fontsize=11, style='italic', ha='center')

    lifecycle_nodes = [
        ("1. GUI Parameterization", "User configures target, timing,\nflags & mode in UI form", 0.06, 0.58),
        ("2. Scope Validation", "Boundary CIDR validation\nenforces ethical scope", 0.29, 0.58),
        ("3. Concurrency Thread", "CommandThread allocates PTY\nand spawns child process", 0.52, 0.58),
        ("4. Streaming Telemetry", "Asynchronous chunk reads\nstream stdout to Console", 0.75, 0.58),

        ("8. Persistent Archiving", "Scan metadata, stdout hash,\nand risk saved to kalinova.db", 0.06, 0.12),
        ("7. Copilot & ML Update", "ML Advisor recommends next step;\nAI Copilot generates patch", 0.29, 0.12),
        ("6. Risk Recalculation", "RiskEngine computes new R_t\nupdates Threat Gauge & Radar", 0.52, 0.12),
        ("5. Real-Time Regex Parser", "Output evaluated for open ports\nand vulnerability signatures", 0.75, 0.12)
    ]

    for title, desc, nx, ny in lifecycle_nodes:
        draw_box(ax, nx, ny, 0.18, 0.25, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(nx + 0.09, ny + 0.205, title, color=TEXT_BLACK, fontsize=9.5, fontweight='bold', ha='center')
        ax.plot([nx + 0.02, nx + 0.16], [ny + 0.18, ny + 0.18], color=BORDER_BLACK, lw=0.8)
        ax.text(nx + 0.09, ny + 0.09, desc, color=TEXT_MUTED, fontsize=8.5, ha='center', va='center')

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

    save_fig(fig, "tool_execution_workflow.png")

if __name__ == "__main__":
    print("Generating Clean B&W Figures 3.9 to 3.16...")
    gen_fig3_9()
    gen_fig3_10()
    gen_fig3_11()
    gen_fig3_12()
    gen_fig3_13()
    gen_fig3_14()
    gen_fig3_15()
    gen_fig3_16()
    print("Part 2 finished!")
