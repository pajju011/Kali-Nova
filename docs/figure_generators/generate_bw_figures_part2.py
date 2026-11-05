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

def draw_box(ax, x, y, w, h, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5, ls='-', hatch=None, zorder=3):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.015",
                                 facecolor=bg, edgecolor=border, linewidth=lw, linestyle=ls, hatch=hatch, zorder=zorder)
    ax.add_patch(box)
    return box

# ==========================================
# 9. Figure 3.9: Machine Learning Scenario Advisor
# ==========================================
def gen_fig3_9():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Box 1: Feature Vector
    draw_box(ax, 0.04, 0.30, 0.28, 0.66, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.06, 0.925, "1. Feature Vector phi(S_t)", color=TEXT_BLACK, fontsize=15.5, fontweight='bold')
    ax.plot([0.06, 0.30], [0.898, 0.898], color=BORDER_BLACK, lw=1.2)
    features = [
        "x_1: Discovered Ports",
        "x_2: Web Protocol (80/443)",
        "x_3: Database Port (3306)",
        "x_4: Auth Protocol (21/22)",
        "x_5: Web Parameter Vuln",
        "x_6: Execution Trace |H|",
        "x_7: Composite Risk R_t"
    ]
    for idx, f in enumerate(features):
        ax.text(0.06, 0.835 - idx * 0.076, f, color=TEXT_BLACK, fontsize=12.5, fontweight='bold')

    # Box 2: Classifier
    draw_box(ax, 0.35, 0.30, 0.30, 0.66, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.50, 0.925, "2. Scenario Model Engine", color=TEXT_BLACK, fontsize=15.5, fontweight='bold', ha='center')
    ax.plot([0.38, 0.62], [0.898, 0.898], color=BORDER_BLACK, lw=1.2)
    ax.text(0.50, 0.825, r"$P(A = a \mid \mathbf{x}_t) = \mathrm{Softmax}(\mathbf{W}\mathbf{x}_t + \mathbf{b})$", color=TEXT_BLACK, fontsize=14.8, ha='center')
    ax.plot([0.38, 0.62], [0.770, 0.770], color=BORDER_BLACK, lw=1.2)
    summary_text = (
        "- 500+ Operational Scenarios\n\n"
        "- Dependency Precondition Filter\n\n"
        "- Prevents Illegal Tool Sequences\n\n"
        "- Top-1 Acc: 96.2% | Top-3: 99.3%"
    )
    ax.text(0.50, 0.545, summary_text, color=TEXT_MUTED, fontsize=13.0, ha='center', va='center')

    # Box 3: Recommendations
    draw_box(ax, 0.68, 0.30, 0.28, 0.66, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.70, 0.925, "3. Action Probabilities", color=TEXT_BLACK, fontsize=15.5, fontweight='bold')
    ax.plot([0.70, 0.94], [0.898, 0.898], color=BORDER_BLACK, lw=1.2)
    actions = [
        ("SQLMap (Audit)", "94.2%", 0.942, FILL_GRAY3),
        ("Nikto (Web Scan)", "88.5%", 0.885, FILL_GRAY2),
        ("Gobuster (Brute)", "72.1%", 0.721, FILL_GRAY2),
        ("Hydra (Auth)", "45.0%", 0.450, FILL_GRAY1),
        ("SSLyze (TLS)", "18.3%", 0.183, FILL_LIGHT)
    ]
    for idx, (tname, tprob, barw, fcol) in enumerate(actions):
        ay = 0.835 - idx * 0.106
        ax.text(0.70, ay, tname, color=TEXT_BLACK, fontsize=12.5, fontweight='bold')
        ax.text(0.94, ay, tprob, color=TEXT_BLACK, fontsize=12.5, fontweight='bold', ha='right')
        rect = patches.Rectangle((0.70, ay - 0.036), barw * 0.24, 0.018, facecolor=fcol, edgecolor=BORDER_BLACK, lw=1, zorder=5)
        ax.add_patch(rect)

    # Inter-box connecting arrows
    ax.annotate("", xy=(0.345, 0.63), xytext=(0.325, 0.63), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.675, 0.63), xytext=(0.655, 0.63), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

    # Bottom Guardrail Box
    draw_box(ax, 0.04, 0.04, 0.92, 0.23, bg=FILL_WHITE, lw=1.5)
    ax.text(0.06, 0.225, "Decision Rule Integration & Safety Guardrails", color=TEXT_BLACK, fontsize=15.5, fontweight='bold')
    ax.plot([0.06, 0.46], [0.198, 0.198], color=BORDER_BLACK, lw=1.2)
    ax.text(0.06, 0.135, "- Logical Preconditions: SQL injection audits are suppressed until active HTTP/HTTPS endpoints are verified.", color=TEXT_BLACK, fontsize=12.2)
    ax.text(0.06, 0.075, "- Autonomous Guidance: Replaces trial-and-error CLI workflows with automated, evidence-backed next actions.", color=TEXT_BLACK, fontsize=12.2)

    save_fig(fig, "ml_advisor.png")

# ==========================================
# 10. Figure 3.10: AI Copilot Diagnostic Workflow
# ==========================================
def gen_fig3_10():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    steps = [
        ("1. Vulnerability\nTrigger", "Parsing flags threat:\nSQLi on /search.php\nCVSS Triggered", 0.04),
        ("2. Context\nAssembly", "Aggregates banner,\nendpoint URI, payload,\nand target tech stack", 0.28),
        ("3. AI Copilot\nEngine", "Hybrid Rule + LLM\n(Groq / Mistral)\nRule Verification", 0.52),
        ("4. Code\nSynthesis", "Synthesizes patches:\n- Parameterized SQL\n- Prepared Statements\n- IPTables WAF Rule", 0.76)
    ]

    for stitle, sdesc, sx in steps:
        draw_box(ax, sx, 0.52, 0.20, 0.44, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(sx + 0.10, 0.88, stitle, color=TEXT_BLACK, fontsize=13.5, fontweight='bold', ha='center', va='center')
        ax.plot([sx + 0.02, sx + 0.18], [0.805, 0.805], color=BORDER_BLACK, lw=1.0)
        ax.text(sx + 0.10, 0.645, sdesc, color=TEXT_MUTED, fontsize=11.5, ha='center', va='center')

    for i in range(len(steps) - 1):
        x1 = steps[i][2] + 0.20 + 0.005
        x2 = steps[i+1][2] - 0.005
        ax.annotate("", xy=(x2, 0.78), xytext=(x1, 0.78), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

    # Bottom remediation code drawer
    draw_box(ax, 0.04, 0.04, 0.92, 0.44, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5)
    ax.text(0.06, 0.435, "Generated Remediation Code Artifact (Embedded in Sliding Drawer)", color=TEXT_BLACK, fontsize=15.5, fontweight='bold')
    ax.plot([0.06, 0.58], [0.410, 0.410], color=BORDER_BLACK, lw=1.2)

    draw_box(ax, 0.05, 0.06, 0.90, 0.33, bg=FILL_GRAY1, border=BORDER_BLACK, lw=1.2)
    code_text = (
        "# [Vulnerability Remediation: CWE-89 SQL Injection in Python / SQLite]\n"
        "# VULNERABLE: cursor.execute(f\"SELECT * FROM users WHERE id = '{user_id}'\")\n\n"
        "# SECURE REFACTORED CODE (Synthesized by Kali-Nova AI Copilot):\n"
        "def get_user_secure(cursor, user_id: str):\n"
        "    query = 'SELECT id, username, role FROM users WHERE id = ?'\n"
        "    cursor.execute(query, (user_id,))\n"
        "    return cursor.fetchone()  # Parameterized query eliminates injection\n\n"
        "# WAF Rule (Bash): iptables -A INPUT -p tcp --dport 80 -m string --string \"UNION SELECT\" -j DROP"
    )
    ax.text(0.07, 0.362, code_text, color=TEXT_BLACK, fontsize=11.2, family='monospace', va='top')

    save_fig(fig, "ai_copilot.png")

# ==========================================
# 11. Figure 3.11: CVSS-Based Vulnerability Assessment
# ==========================================
def gen_fig3_11():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Polar Chart
    ax_sub = fig.add_axes([0.02, 0.10, 0.36, 0.78], polar=True, facecolor=BG_WHITE)
    metrics = ['Attack Vector\n(AV: 0.85)', 'Attack Comp.\n(AC: 0.77)', 'Priv. Req.\n(PR: 0.85)',
               'User Interact.\n(UI: 0.85)', 'Scope\n(S: 1.0)', 'Confidentiality\n(C: 0.56)',
               'Integrity\n(I: 0.56)', 'Availability\n(A: 0.56)']
    values = [0.85, 0.77, 0.85, 0.85, 1.0, 0.56, 0.56, 0.56]
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    ax_sub.plot(angles, values, color=BORDER_BLACK, linewidth=2.4, linestyle='solid')
    ax_sub.fill(angles, values, color=FILL_GRAY2, alpha=0.45)
    ax_sub.set_ylim(0, 1.15)
    ax_sub.set_xticks(angles[:-1])
    ax_sub.set_xticklabels(metrics, color=TEXT_BLACK, fontsize=11.5, fontweight='bold')
    ax_sub.set_yticklabels([])
    ax_sub.grid(color=FILL_GRAY3, lw=1.2)
    ax_sub.spines['polar'].set_visible(False)

    # Right Card
    draw_box(ax, 0.50, 0.05, 0.47, 0.90, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.52, 0.905, "CVSS v3.1 Metrics & Vector Breakdown", color=TEXT_BLACK, fontsize=15.0, fontweight='bold')
    ax.plot([0.52, 0.94], [0.878, 0.878], color=BORDER_BLACK, lw=1.2)

    ax.text(0.52, 0.835, "VECTOR: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", color=TEXT_BLACK, fontsize=10.8, family='monospace', fontweight='bold')
    ax.text(0.52, 0.780, "BASE SCORE: 9.8", color=TEXT_BLACK, fontsize=16.5, fontweight='bold')
    ax.text(0.74, 0.780, "SEVERITY: CRITICAL", color=TEXT_BLACK, fontsize=15.0, fontweight='bold')
    ax.plot([0.52, 0.94], [0.745, 0.745], color=BORDER_BLACK, lw=1.2)

    specs = [
        ("Attack Vector (AV: Network)", "Exploitable remotely across internet / LAN"),
        ("Attack Complexity (AC: Low)", "No specialized timing or race conditions required"),
        ("Privileges Required (PR: None)", "Unauthenticated attacker can trigger exploit"),
        ("User Interaction (UI: None)", "Zero user action required to achieve compromise"),
        ("Scope (S: Unchanged)", "Directly impacts targeted database / host component"),
        ("Impact Metrics (C:H, I:H, A:H)", "Total loss of confidentiality, integrity & availability")
    ]
    for idx, (head, desc) in enumerate(specs):
        sy = 0.675 - idx * 0.096
        ax.text(0.52, sy, head, color=TEXT_BLACK, fontsize=12.5, fontweight='bold')
        ax.text(0.52, sy - 0.038, desc, color=TEXT_MUTED, fontsize=11.5)

    save_fig(fig, "cvss_analysis.png")

# ==========================================
# 12. Figure 3.12: Network Visualization Interface
# ==========================================
def gen_fig3_12():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Main Canvas Frame
    draw_box(ax, 0.03, 0.04, 0.94, 0.92, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5, zorder=1)

    # Core Router Center
    rcx, rcy = 0.50, 0.54

    net_nodes = [
        (0.50, 0.83, "DNS / AD Controller", ".100 (Win Server)", "STATUS: FILTERED", "Ports: 53, 389"),
        (0.18, 0.70, "Target Web App", ".105 (Apache/PHP)", "STATUS: VULNERABLE", "Ports: 80, 443"),
        (0.82, 0.70, "Database Cluster", ".120 (MySQL 8.0)", "STATUS: AT-RISK", "Port: 3306"),
        (0.18, 0.35, "Auth Gateway", ".115 (OpenSSH/PAM)", "STATUS: AUDITED", "Port: 22"),
        (0.82, 0.35, "Internal File Server", ".130 (vsftpd 2.3.4)", "STATUS: COMPROMISED", "Port: 21")
    ]

    # Draw connection lines
    for nx, ny, _, _, _, _ in net_nodes:
        ax.plot([rcx, nx], [rcy, ny], color=BORDER_BLACK, lw=1.8, zorder=2)

    # Draw Internal SQL Traffic Link
    ax.plot([0.18, 0.82], [0.70, 0.70], color=BORDER_BLACK, lw=1.6, ls=":", zorder=2)
    ax.text(0.50, 0.67, "Internal SQL Traffic Link (Port 3306)", color=TEXT_BLACK, fontsize=11.5, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=BORDER_BLACK, lw=1), zorder=6)

    # Draw Central Gateway Box
    draw_box(ax, rcx - 0.13, rcy - 0.08, 0.26, 0.16, bg=FILL_GRAY2, border=BORDER_BLACK, lw=2, zorder=3)
    ax.text(rcx, rcy + 0.040, "Core Gateway / Firewall", color=TEXT_BLACK, fontsize=14.5, fontweight='bold', ha='center', zorder=5)
    ax.text(rcx, rcy + 0.006, "192.168.1.1", color=TEXT_BLACK, fontsize=13.0, fontweight='bold', ha='center', zorder=5)
    ax.plot([rcx - 0.10, rcx + 0.10], [rcy - 0.015, rcy - 0.015], color=BORDER_BLACK, lw=0.8, zorder=5)
    ax.text(rcx, rcy - 0.050, "[Subnet Root: /24]", color=TEXT_MUTED, fontsize=11.8, ha='center', zorder=5)

    # Draw Peripheral Node Boxes
    for nx, ny, ntitle, nsub, nstat, nports in net_nodes:
        draw_box(ax, nx - 0.125, ny - 0.078, 0.25, 0.155, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5, zorder=3)
        ax.text(nx, ny + 0.045, ntitle, color=TEXT_BLACK, fontsize=13.5, fontweight='bold', ha='center', zorder=5)
        ax.text(nx, ny + 0.015, nsub, color=TEXT_MUTED, fontsize=12.0, ha='center', zorder=5)
        ax.plot([nx - 0.09, nx + 0.09], [ny - 0.005, ny - 0.005], color=BORDER_BLACK, lw=0.6, zorder=5)
        ax.text(nx, ny - 0.028, nstat, color=TEXT_BLACK, fontsize=12.0, fontweight='bold', ha='center', zorder=5)
        ax.text(nx, ny - 0.056, nports, color=TEXT_MUTED, fontsize=11.5, ha='center', zorder=5)

    # Bottom Legend Banner
    draw_box(ax, 0.05, 0.048, 0.90, 0.16, bg=FILL_WHITE, border=BORDER_BLACK, lw=1.5, zorder=3)
    ax.text(0.50, 0.175, "Node Security Posture & Vulnerability Status Legend", color=TEXT_BLACK, fontsize=14.0, fontweight='bold', ha='center', zorder=5)
    ax.plot([0.10, 0.90], [0.155, 0.155], color=BORDER_BLACK, lw=0.8, zorder=5)

    legend_items = [
        (0.16, "VULNERABLE", "Critical RCE / SQLi", FILL_GRAY2),
        (0.39, "AT-RISK", "Exposed DB / Surface", FILL_GRAY1),
        (0.61, "COMPROMISED", "Backdoor Exploit (Root)", FILL_GRAY3),
        (0.84, "AUDITED", "Hardened / Verified", FILL_WHITE)
    ]
    for lx, ltag, ldesc, lcol in legend_items:
        draw_box(ax, lx - 0.10, 0.065, 0.20, 0.072, bg=lcol, border=BORDER_BLACK, lw=1.2, zorder=4)
        ax.text(lx, 0.108, f"[{ltag}]", color=TEXT_BLACK, fontsize=12.5, fontweight='bold', ha='center', zorder=5)
        ax.text(lx, 0.082, ldesc, color=TEXT_MUTED, fontsize=10.8, ha='center', zorder=5)

    save_fig(fig, "network_visualization.png")

# ==========================================
# 13. Figure 3.13: Real-Time Network Port Matrix
# ==========================================
def gen_fig3_13():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Top Rule
    ax.plot([0.04, 0.96], [0.93, 0.93], color=BORDER_BLACK, lw=2.5)
    headers = [("PORT", 0.055), ("SERVICE BANNER", 0.180), ("STATE", 0.400), ("RISK", 0.500), ("VULNERABILITY / CVE", 0.610), ("ACTION", 0.865)]
    for hname, hx in headers:
        ax.text(hx, 0.895, hname, color=TEXT_BLACK, fontsize=13.5, fontweight='bold', va='center')
    ax.plot([0.04, 0.96], [0.86, 0.86], color=BORDER_BLACK, lw=1.5)

    rows = [
        ("21 / TCP", "vsftpd 2.3.4 (Anon)", "OPEN", "CRITICAL", "CVE-2011-2523 (RCE)", "Hydra Audit"),
        ("22 / TCP", "OpenSSH 8.9p1", "OPEN", "LOW", "No Known Exploits", "Audit Keys"),
        ("53 / UDP", "BIND 9.16.1 (DNS)", "OPEN", "LOW", "Standard DNS Protocol", "DNS Query"),
        ("80 / TCP", "Apache 2.4.41 (PHP)", "OPEN", "HIGH", "CWE-89 SQL Injection", "Nikto Scan"),
        ("443 / TCP", "Apache OpenSSL", "OPEN", "MODERATE", "TLS 1.0 Deprecated", "Run SSLyze"),
        ("3306 / TCP", "MariaDB 10.3 (MySQL)", "OPEN", "CRITICAL", "Unauth Root Access", "SQLMap Audit"),
        ("8080 / TCP", "Werkzeug Py/3.10", "OPEN", "HIGH", "Debug Console Exposed", "Audit HTTP"),
        ("9001 / TCP", "Telemetry Daemon", "FILTERED", "LOW", "Firewall Dropped", "Probe Port")
    ]

    for idx, (port, serv, state, rlevel, cve, act) in enumerate(rows):
        ry = 0.805 - idx * 0.088
        bg_col = FILL_GRAY1 if idx % 2 == 0 else FILL_WHITE
        rect = patches.Rectangle((0.04, ry - 0.025), 0.92, 0.075, facecolor=bg_col, edgecolor='none', zorder=1)
        ax.add_patch(rect)
        ax.text(0.055, ry + 0.012, port, color=TEXT_BLACK, fontsize=12.8, fontweight='bold', va='center')
        ax.text(0.180, ry + 0.012, serv, color=TEXT_MUTED, fontsize=12.0, va='center')
        ax.text(0.400, ry + 0.012, state, color=TEXT_BLACK, fontsize=12.2, fontweight='bold', va='center')
        ax.text(0.500, ry + 0.012, rlevel, color=TEXT_BLACK, fontsize=12.2, fontweight='bold', va='center')
        ax.text(0.610, ry + 0.012, cve, color=TEXT_BLACK, fontsize=11.8, va='center')

        draw_box(ax, 0.835, ry - 0.016, 0.122, 0.058, bg=FILL_WHITE, border=BORDER_BLACK, lw=1)
        ax.text(0.896, ry + 0.012, act, color=TEXT_BLACK, fontsize=11.2, fontweight='bold', ha='center', va='center')

    ax.plot([0.04, 0.96], [0.08, 0.08], color=BORDER_BLACK, lw=2.5)
    save_fig(fig, "port_matrix.png")

# ==========================================
# 14. Figure 3.14: Radar-Based Network Visualization
# ==========================================
def gen_fig3_14():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    rcx, rcy = 0.50, 0.46
    radii = [0.08, 0.16, 0.24, 0.32]
    ring_labels = ["Internal LAN (Tier 1)", "DMZ / App Cluster (Tier 2)", "External Perimeter (Tier 3)", "Gateway Perimeter"]
    for r, rlbl in zip(radii, ring_labels):
        circle = plt.Circle((rcx, rcy), r, color=BORDER_BLACK, fill=False, lw=1.2, ls="--", zorder=3)
        ax.add_patch(circle)
        ax.text(rcx, rcy + r + 0.005, rlbl, color=TEXT_MUTED, fontsize=11.2, fontweight='bold', ha='center', va='bottom',
                bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"), zorder=5)

    ax.plot([rcx - 0.35, rcx + 0.35], [rcy, rcy], color=BORDER_BLACK, lw=1, ls=":", zorder=3)
    ax.plot([rcx, rcx], [rcy - 0.35, rcy + 0.35], color=BORDER_BLACK, lw=1, ls=":", zorder=3)

    # Smooth transparent sweep wedge
    wedge = patches.Wedge((rcx, rcy), 0.32, 45, 95, facecolor=FILL_GRAY2, alpha=0.35, zorder=4)
    ax.add_patch(wedge)
    ax.plot([rcx, rcx + 0.32 * np.cos(np.radians(95))], [rcy, rcy + 0.32 * np.sin(np.radians(95))], color=BORDER_BLACK, lw=2.4, zorder=5)

    blips = [
        (rcx + 0.08, rcy + 0.04, "192.168.1.1 (Gateway)", "o"),
        (rcx + 0.18, rcy + 0.10, "192.168.1.105 (Web Target)", "s"),
        (rcx - 0.18, rcy + 0.10, "192.168.1.120 (DB Server)", "^"),
        (rcx + 0.19, rcy - 0.14, "192.168.1.130 (FTP Server)", "D"),
        (rcx - 0.19, rcy - 0.14, "192.168.1.110 (Client PC)", "v")
    ]
    for bx, by, blbl, bmarker in blips:
        pring = plt.Circle((bx, by), 0.018, color=BORDER_BLACK, fill=False, lw=1, ls=":", zorder=5)
        ax.add_patch(pring)
        ax.scatter([bx], [by], color=BORDER_BLACK, marker=bmarker, s=130, zorder=6)
        ax.text(bx, by - 0.038, blbl, color=TEXT_BLACK, fontsize=11.2, fontweight='bold', ha='center',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=BORDER_BLACK, lw=0.8), zorder=7)

    # Left & Right Telemetry Cards
    draw_box(ax, 0.03, 0.63, 0.24, 0.33, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.05, 0.925, "RADAR TELEMETRY", color=TEXT_BLACK, fontsize=15.0, fontweight='bold')
    ax.plot([0.05, 0.25], [0.898, 0.898], color=BORDER_BLACK, lw=0.8)
    ax.text(0.05, 0.765, "Sweep Rate: 20 FPS\nActive Sector: 045° - 095°\nTarget: 192.168.1.105\nHealth: CRITICAL (78%)", color=TEXT_BLACK, fontsize=12.2)

    draw_box(ax, 0.73, 0.63, 0.24, 0.33, bg=FILL_LIGHT, lw=1.5)
    ax.text(0.75, 0.925, "SPATIAL SIGNALS", color=TEXT_BLACK, fontsize=15.0, fontweight='bold')
    ax.plot([0.75, 0.95], [0.898, 0.898], color=BORDER_BLACK, lw=0.8)
    ax.text(0.75, 0.765, "Nodes: 5 Active\nVulns: 7 Flagged\nPacket Rate: 1.4 kpps\nProximity: IMMEDIATE", color=TEXT_BLACK, fontsize=12.2)

    save_fig(fig, "radar_visualization.png")

# ==========================================
# 15. Figure 3.15: Dynamic Threat Risk Gauge
# ==========================================
def gen_fig3_15():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    gcx, gcy = 0.50, 0.58
    r_outer = 0.27

    angles_def = [
        (np.pi, np.pi * 0.75, FILL_LIGHT, "LOW\n(0-25)"),
        (np.pi * 0.75, np.pi * 0.50, FILL_GRAY1, "MODERATE\n(25-50)"),
        (np.pi * 0.50, np.pi * 0.25, FILL_GRAY2, "ELEVATED\n(50-75)"),
        (np.pi * 0.25, 0, FILL_GRAY3, "CRITICAL\n(75-100)")
    ]
    for start_a, end_a, col, lbl in angles_def:
        t = np.linspace(start_a, end_a, 50)
        ax.plot(gcx + r_outer * np.cos(t), gcy + r_outer * np.sin(t), color=BORDER_BLACK, lw=16, zorder=3)
        mid_a = (start_a + end_a) / 2
        ax.text(gcx + 0.37 * np.cos(mid_a), gcy + 0.37 * np.sin(mid_a), lbl, color=TEXT_BLACK, fontsize=12.8, fontweight='bold', ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.9), zorder=5)

    # Needle at 78.4%
    needle_angle = np.pi * (1.0 - 0.784)
    nx = gcx + 0.23 * np.cos(needle_angle)
    ny = gcy + 0.23 * np.sin(needle_angle)
    ax.plot([gcx, nx], [gcy, ny], color=BORDER_BLACK, lw=4, zorder=6)
    ax.scatter([gcx], [gcy], color=BORDER_BLACK, s=240, zorder=7)

    # Dedicated score box safely placed with generous clearance
    draw_box(ax, 0.30, 0.25, 0.40, 0.17, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
    ax.text(0.50, 0.355, "78.4 / 100", color=TEXT_BLACK, fontsize=32, fontweight='bold', ha='center')
    ax.text(0.50, 0.280, "CRITICAL RISK LEVEL DETECTED", color=TEXT_BLACK, fontsize=14.5, fontweight='bold', ha='center')

    params = [
        ("Critical Open Ports", "4 Ports Open\n(21, 80, 443, 3306)", 0.05),
        ("CVSS Vulnerabilities", "Score Sum: 64.2\n(CVE-2011-2523, SQLi)", 0.37),
        ("Surface Exposure", "Alpha: 1.25 | Beta: 0.85\nNormalized Exposure: 84.3%", 0.69)
    ]
    for ptitle, pdesc, px in params:
        draw_box(ax, px, 0.04, 0.26, 0.16, bg=FILL_WHITE, lw=1.2)
        ax.text(px + 0.13, 0.155, ptitle, color=TEXT_BLACK, fontsize=13.5, fontweight='bold', ha='center')
        ax.plot([px + 0.02, px + 0.24], [0.130, 0.130], color=BORDER_BLACK, lw=0.8)
        ax.text(px + 0.13, 0.075, pdesc, color=TEXT_MUTED, fontsize=12.0, ha='center', va='center')

    save_fig(fig, "risk_gauge.png")

# ==========================================
# 16. Figure 3.16: Complete Tool Execution Workflow
# ==========================================
def gen_fig3_16():
    fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    lifecycle_nodes = [
        ("1. GUI\nParameterization", "Target, CIDR & flags\nconfigured in UI form", 0.045, 0.55),
        ("2. Scope\nValidation", "CIDR verification\nenforces ethical\naudit boundary", 0.285, 0.55),
        ("3. Concurrency\nThread", "CommandThread\nallocates PTY &\nspawns process", 0.525, 0.55),
        ("4. Streaming\nTelemetry", "Asynchronous chunk\nreads stream stdout\nto cyber console", 0.765, 0.55),

        ("8. Persistent\nArchiving", "Scan metadata &\nrisk score sealed\nin kalinova.db", 0.045, 0.07),
        ("7. Copilot &\nML Update", "ML recommends action;\nAI Copilot generates\ncode patch", 0.285, 0.07),
        ("6. Risk\nRecalculation", "RiskEngine computes\nnew composite R_t\nupdates radar & dial", 0.525, 0.07),
        ("5. Real-Time\nRegex Parser", "Output evaluated for\nopen ports & CVE\nsignatures", 0.765, 0.07)
    ]

    for title, desc, nx, ny in lifecycle_nodes:
        draw_box(ax, nx, ny, 0.19, 0.38, bg=FILL_LIGHT, border=BORDER_BLACK, lw=1.5)
        ax.text(nx + 0.095, ny + 0.295, title, color=TEXT_BLACK, fontsize=13.5, fontweight='bold', ha='center', va='center')
        ax.plot([nx + 0.02, nx + 0.17], [ny + 0.22, ny + 0.22], color=BORDER_BLACK, lw=0.8)
        ax.text(nx + 0.095, ny + 0.110, desc, color=TEXT_MUTED, fontsize=12.0, ha='center', va='center')

    # Top row forward arrows
    ax.annotate("", xy=(0.280, 0.74), xytext=(0.240, 0.74), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.520, 0.74), xytext=(0.480, 0.74), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.760, 0.74), xytext=(0.720, 0.74), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

    # Turn down
    ax.annotate("", xy=(0.86, 0.46), xytext=(0.86, 0.54), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

    # Bottom row reverse arrows
    ax.annotate("", xy=(0.720, 0.26), xytext=(0.760, 0.26), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.480, 0.26), xytext=(0.520, 0.26), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))
    ax.annotate("", xy=(0.240, 0.26), xytext=(0.280, 0.26), arrowprops=dict(arrowstyle="->", color=BORDER_BLACK, lw=2.4))

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
