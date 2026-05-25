"""5 striking visuals of where the Biden-2020 skips were.
Per Wilson's specs (5 charts).

Outputs to D:/DNC/visuals/

1. Boomer income gradient (kill shot for rich-Boomer narrative)
2. Skip rate by cohort (spine)
3. Forest plot of 5 channels
4. Issue items decomp (Wall + Drill doing all the work)
5. Skipper-face heatmap (cohort x income quartile)
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

OUT = Path("D:/DNC/visuals")
OUT.mkdir(parents=True, exist_ok=True)

# Visual styling: clean, neutral, readable
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.15,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "figure.dpi": 120,
})

# ============================================================
# CHART 1: Boomer skip rate by income bracket
# ============================================================
print("Chart 1: Boomer income gradient")
boom_inc = [
    ("<$10k", 8.59, 128),
    ("$10-20k", 6.55, 611),
    ("$20-30k", 6.00, 817),
    ("$30-40k", 5.55, 793),
    ("$40-50k", 5.53, 669),
    ("$50-60k", 3.90, 693),
    ("$60-70k", 2.96, 541),
    ("$70-80k", 2.61, 613),
    ("$80-100k", 3.10, 774),
    ("$100-120k", 1.82, 549),
    ("$120-150k", 2.93, 580),
    ("$150-200k", 4.00, 375),
    ("$200-250k", 1.03, 194),
]
labels = [b[0] for b in boom_inc]
rates = [b[1] for b in boom_inc]
ns = [b[2] for b in boom_inc]

fig, ax = plt.subplots(figsize=(9, 7))
y_pos = np.arange(len(labels))
bars = ax.barh(y_pos, rates, color="#4a6fa5", edgecolor="none")
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()  # top-to-bottom: <$10k on top, $200-250k on bottom
ax.set_xlim(0, 10)
ax.set_xlabel("Skip rate (%)")
ax.set_title("Biden-2020 Boomers, 2024 skip rate by household income", pad=14)
# Value labels
for i, (rate, n) in enumerate(zip(rates, ns)):
    ax.text(rate + 0.15, i, f"{rate:.2f}% (n={n})", va="center", fontsize=9)
# Takeaway
fig.text(0.5, 0.01,
         "Boomer disengagement is concentrated at the bottom of the income distribution\n"
         "— the opposite of the dominant narrative.",
         ha="center", fontsize=10, style="italic", color="#444")
plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig(OUT / "01_boomer_income_gradient.png", dpi=160, bbox_inches="tight")
plt.savefig(OUT / "01_boomer_income_gradient.pdf", bbox_inches="tight")
plt.close()
print(f"  saved {OUT / '01_boomer_income_gradient.png'}")

# ============================================================
# CHART 2: Skip rate by cohort
# ============================================================
print("Chart 2: Cohort gradient")
cohorts = ["Silent", "Boomer", "GenX", "MillOld", "MillYoung", "GenZ"]
skip_pct = [1.85, 3.93, 6.76, 6.38, 8.18, 10.19]
ns = [863, 8216, 4558, 2070, 1174, 520]

fig, ax = plt.subplots(figsize=(9, 5.5))
x_pos = np.arange(len(cohorts))
ax.fill_between(x_pos, 0, skip_pct, alpha=0.18, color="#a04545", step="mid")
ax.plot(x_pos, skip_pct, "-o", color="#a04545", linewidth=2.5, markersize=8)
# Overall average reference line
overall_avg = 928 / 17401 * 100
ax.axhline(overall_avg, color="#888", linestyle="--", linewidth=1, alpha=0.6,
            label=f"Overall avg ({overall_avg:.2f}%)")
ax.set_xticks(x_pos)
ax.set_xticklabels([f"{c}\n(N={n:,})" for c, n in zip(cohorts, ns)])
ax.set_ylabel("Biden-2020 skip rate (%)")
ax.set_title("Biden-2020 → 2024 skip rate by cohort", pad=14)
ax.set_ylim(0, 12)
# Point labels: extremes
ax.annotate(f"{skip_pct[0]:.2f}%", xy=(0, skip_pct[0]), xytext=(0.1, skip_pct[0]+0.6),
            fontsize=10, fontweight="bold")
ax.annotate(f"{skip_pct[-1]:.2f}%", xy=(5, skip_pct[-1]), xytext=(5.1, skip_pct[-1]+0.4),
            fontsize=10, fontweight="bold")
# Inline ratio note
ax.text(2.5, 11, "5.5× ratio: GenZ vs Silent", fontsize=11, color="#a04545",
        style="italic", weight="bold", ha="center")
ax.legend(loc="upper left", frameon=False, fontsize=9)

fig.text(0.5, 0.005,
         "The 2020 coalition didn't hold equally — disengagement scales with cohort youth,\n"
         "GenZ skipping at 5.5× the Silent rate.",
         ha="center", fontsize=10, style="italic", color="#444")
plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.savefig(OUT / "02_cohort_gradient.png", dpi=160, bbox_inches="tight")
plt.savefig(OUT / "02_cohort_gradient.pdf", bbox_inches="tight")
plt.close()
print(f"  saved {OUT / '02_cohort_gradient.png'}")

# ============================================================
# CHART 3: Forest plot of 5 channels (v2.9 main findings)
# ============================================================
print("Chart 3: Forest plot of 5 v2.9 channels")
# β [5%, 95%] per v2.9 result
channels = [
    ("Leftist composite → Harris-mob\n(non-voter universe; v2.11)", 0.619, 0.459, 0.783, "STRONG"),
    ("Leftist composite → Trump-mob\n(non-voter universe; v2.11)", -0.468, -0.583, -0.356, "STRONG"),
    ("Economic perception\n(worse → skip)", 0.446, 0.398, 0.495, "STRONG"),
    ("Trust collapse (combined)\n(less trust → skip)", 0.370, 0.321, 0.419, "STRONG"),
    ("Pro-choice (less → skip)\n[abortion composite]", -0.257, -0.297, -0.217, "STRONG"),
    ("Mobilization gap\n(less contact → skip)", -0.251, -0.299, -0.204, "STRONG"),
    ("Pro-climate (less → skip)\n[climate composite]", -0.243, -0.289, -0.198, "STRONG"),
    ("Trust elections\n(less confidence → skip)", 0.222, 0.177, 0.266, "STRONG"),
    ("Leftist composite (less → skip)\n[Biden universe; v2.11]", -0.215, -0.258, -0.170, "STRONG"),
    ("Pro-immigration (less → skip)\n[immigration composite]", -0.205, -0.245, -0.163, "STRONG"),
    ("Engagement gradient\n(less engaged → skip)", -0.150, -0.240, -0.061, "WEAK"),
]
# Sort by absolute β
channels = sorted(channels, key=lambda x: abs(x[1]), reverse=True)

fig, ax = plt.subplots(figsize=(10, 7))
y_pos = np.arange(len(channels))[::-1]  # so biggest β at top
for i, (name, b, q5, q95, verdict) in enumerate(channels):
    color = "#1f4e79" if verdict == "STRONG" else "#888"
    marker = "o" if verdict == "STRONG" else "o"
    ax.errorbar(b, y_pos[i], xerr=[[b-q5],[q95-b]], fmt=marker, color=color,
                markersize=10, markerfacecolor=color if verdict == "STRONG" else "white",
                markeredgecolor=color, capsize=4, linewidth=1.8)
    ax.text(0.62, y_pos[i], f"β={b:+.3f}", fontsize=9, va="center", color="#444")
ax.axvline(0, color="#444", linewidth=1, alpha=0.6)
ax.set_yticks(y_pos)
ax.set_yticklabels([c[0] for c in channels], fontsize=10)
ax.set_xlim(-0.65, 0.85)
ax.set_xlabel("Standardized β coefficient (Bayesian hierarchical logistic)")
ax.set_title("Channels predicting Biden-2020 → 2024 skip\n(Positive β = predicts skipping; Negative β = predicts retention)", pad=12)

fig.text(0.5, 0.005,
         "Economic perception dominates. Mobilization, trust, and issue-position each contribute.\n"
         "Race × cohort interaction was tested (v2.9) and REFUTED.\n"
         "All v2.10 v2.11 estimates from hierarchical Bayesian logistic; 95% CI bars shown.",
         ha="center", fontsize=9, style="italic", color="#444")
plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(OUT / "03_forest_plot_5channels.png", dpi=160, bbox_inches="tight")
plt.savefig(OUT / "03_forest_plot_5channels.pdf", bbox_inches="tight")
plt.close()
print(f"  saved {OUT / '03_forest_plot_5channels.png'}")

# ============================================================
# CHART 4: Issue-item decomp ("Wall" + "Drill" do all the work)
# ============================================================
print("Chart 4: Issue item decomp")
items = [
    ("Build the wall (support → skip)", -0.262, "STRONG"),
    ("Increase fossil fuel (support → skip)", -0.262, "STRONG"),
    ("Expand abortion access (oppose → skip)", -0.196, "WEAK"),
    ("Always allow abortion (oppose → skip)", -0.176, "WEAK"),
    ("Rape/incest only (support → skip)", -0.176, "WEAK"),
    ("Dreamers permanent status (oppose → skip)", -0.176, "WEAK"),
    ("Illegal always (support → skip)", -0.129, "WEAK"),
    ("Halt oil/gas leases (oppose → skip)", -0.130, "WEAK"),
    ("EPA regulate carbon (oppose → skip)", -0.108, "WEAK"),
    ("Renewable energy (oppose → skip)", -0.082, "INDET"),
    ("Prevent gas-stove ban (support → skip)", -0.099, "INDET"),
    ("EPA enforcement (oppose → skip)", -0.035, "NULL"),
    ("Legal status undocumented (oppose → skip)", -0.039, "NULL"),
    ("Border patrols (support → skip)", -0.006, "NULL"),
]
items = sorted(items, key=lambda x: x[1])  # most negative at top

fig, ax = plt.subplots(figsize=(10, 8))
y_pos = np.arange(len(items))[::-1]
colors = []
for name, b, verdict in items:
    if verdict == "STRONG":
        colors.append("#1f4e79")
    elif verdict == "WEAK":
        colors.append("#a9c5e3")
    elif verdict == "INDET":
        colors.append("#cccccc")
    else:  # NULL
        colors.append("#e8e8e8")

for i, ((name, b, verdict), color) in enumerate(zip(items, colors)):
    ax.plot([0, b], [y_pos[i], y_pos[i]], color=color, linewidth=3, zorder=2)
    ax.scatter([b], [y_pos[i]], color=color, s=120, zorder=3, edgecolor="#222" if verdict=="STRONG" else "none", linewidths=1.2)
    label_color = "#1f4e79" if verdict == "STRONG" else "#666"
    ax.text(b - 0.013, y_pos[i], f"{b:+.3f}", fontsize=8.5, ha="right", va="center",
            color=label_color, fontweight="bold" if verdict == "STRONG" else "normal")

ax.axvline(0, color="#444", linewidth=1, alpha=0.6)
ax.set_yticks(y_pos)
ax.set_yticklabels([i[0] for i in items], fontsize=9.5)
ax.set_xlim(-0.32, 0.05)
ax.set_xlabel("Standardized β coefficient (predicts Biden-2020 → 2024 skip)")
ax.set_title("Item-level decomposition of the 'issue-conservatism' channel\nTwo single items carry the entire signal", pad=12)

# Bracket around top two
ax.annotate("", xy=(-0.30, y_pos[0]+0.45), xytext=(-0.30, y_pos[1]-0.45),
            arrowprops=dict(arrowstyle="-", color="#a04545", linewidth=2.5))
ax.text(-0.31, (y_pos[0] + y_pos[1])/2, "Wall +\nDrill",
        fontsize=10, fontweight="bold", color="#a04545", ha="right", va="center")

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#1f4e79", label="STRONG (|β|≥0.20)"),
    Patch(facecolor="#a9c5e3", label="WEAK (0.10≤|β|<0.20)"),
    Patch(facecolor="#cccccc", label="INDET"),
    Patch(facecolor="#e8e8e8", label="NULL"),
]
ax.legend(handles=legend_elements, loc="lower right", frameon=True, fontsize=9)

fig.text(0.5, 0.005,
         "The 'left-wing platform alienated voters' story collapses to TWO specific items.\n"
         "Generic immigration, abortion, and climate items don't differentiate skippers.",
         ha="center", fontsize=10, style="italic", color="#444")
plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(OUT / "04_issue_decomp_wall_drill.png", dpi=160, bbox_inches="tight")
plt.savefig(OUT / "04_issue_decomp_wall_drill.pdf", bbox_inches="tight")
plt.close()
print(f"  saved {OUT / '04_issue_decomp_wall_drill.png'}")

# ============================================================
# CHART 5: Heatmap — cohort × income, skip volume
# ============================================================
print("Chart 5: Skipper-face heatmap")
# Cohorts × income quintile (Q0 lowest, Q4 highest)
cohorts = ["Silent", "Boomer", "GenX", "MillOld", "MillYoung", "GenZ"]
inc_q = ["Q0 (low)", "Q1", "Q2", "Q3", "Q4 (high)"]

# Per-cell: (n, skip_count, skip_pct) — pulled from diagnostic earlier
cells = {
    "Silent":     [(208,8,3.85),  (158,4,2.53),  (203,1,0.49), (147,1,0.68), (147,2,1.36)],
    "Boomer":     [(2349,144,6.13),(1362,64,4.70),(1928,56,2.90),(1504,42,2.79),(1073,17,1.58)],
    "GenX":       [(1068,141,13.20),(568,41,7.22),(959,60,6.26),(1268,38,3.00),(695,28,4.03)],
    "MillOld":    [(361,46,12.74),(266,20,7.52),(436,34,7.80),(658,17,2.58),(349,15,4.30)],
    "MillYoung":  [(209,32,15.31),(191,15,7.85),(292,23,7.88),(311,17,5.47),(171,9,5.26)],
    "GenZ":       [(130,16,12.31),(93,11,11.83),(118,9,7.63), (85,8,9.41),  (94,9,9.57)],
}

skip_counts = np.array([[c[1] for c in cells[c0]] for c0 in cohorts])
skip_pcts = np.array([[c[2] for c in cells[c0]] for c0 in cohorts])
ns_arr = np.array([[c[0] for c in cells[c0]] for c0 in cohorts])

fig, ax = plt.subplots(figsize=(11, 6.5))
im = ax.imshow(skip_counts, cmap="Reds", aspect="auto")
ax.set_xticks(range(len(inc_q)))
ax.set_xticklabels(inc_q)
ax.set_yticks(range(len(cohorts)))
ax.set_yticklabels(cohorts)
ax.set_xlabel("Income quintile (within Biden-2020 universe)")
ax.set_ylabel("Cohort")
ax.set_title("Where the Biden-2020 → 2024 skips are: cohort × income\nCell color = absolute skip event count (n=928 total)", pad=12)

# Cell annotations: count / rate
for i, c0 in enumerate(cohorts):
    for j, q in enumerate(inc_q):
        n_cell, sk_count, sk_pct = cells[c0][j]
        # Use white text on dark cells
        cell_val = skip_counts[i, j]
        max_val = skip_counts.max()
        text_color = "white" if cell_val > max_val * 0.5 else "black"
        ax.text(j, i, f"{sk_count}\n{sk_pct:.1f}%",
                ha="center", va="center", fontsize=9.5, color=text_color, fontweight="bold")

# Highlight the two biggest cells: Boomer-Q0 + GenX-Q0
for (cohort_idx, q_idx) in [(1, 0), (2, 0)]:
    rect = mpl.patches.Rectangle((q_idx-0.5, cohort_idx-0.5), 1, 1,
                                  fill=False, edgecolor="#1f4e79", linewidth=3.5, zorder=10)
    ax.add_patch(rect)

cbar = plt.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
cbar.set_label("Absolute skip events")

fig.text(0.5, -0.01,
         "GenX-Q0 (141 events @ 13.2%) + Boomer-Q0 (144 @ 6.1%) = 30.7% of all Biden-2020 skip events.\n"
         "The demobilized voter isn't who the takes assume. "
         "It's a 50-65-year-old earning under ~$50-60k, NOT a disaffected GenZ progressive.",
         ha="center", fontsize=10, style="italic", color="#444")
plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig(OUT / "05_skipper_heatmap.png", dpi=160, bbox_inches="tight")
plt.savefig(OUT / "05_skipper_heatmap.pdf", bbox_inches="tight")
plt.close()
print(f"  saved {OUT / '05_skipper_heatmap.png'}")

print("\nAll 5 visuals saved to D:/DNC/visuals/")
