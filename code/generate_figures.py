# -*- coding: utf-8 -*-
"""Conceptual figures for the neuroimmune engineering framework paper.
These are schematic diagrams, not data plots: no simulation or dataset underlies
them. The script exists so the figures are reproducible and version-controlled
rather than static images.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# Evidence-status palette (muted, print-safe, distinguishable in greyscale by order)
C_DEM = "#BFD8C2"   # Demonstrated
C_SUP = "#F2DFA7"   # Supported inference
C_UNT = "#E8BFBF"   # Untested hypothesis
EDGE = "#3A3A3A"
TXT = "#1A1A1A"


def box(ax, x, y, w, h, text, color, fontsize=8.2, bold=False):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle="round,pad=0.012,rounding_size=0.02",
                       linewidth=0.9, edgecolor=EDGE, facecolor=color, zorder=2)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, color=TXT, zorder=3,
            fontweight="bold" if bold else "normal", linespacing=1.35)


def arrow(ax, x1, y1, x2, y2, style="-|>", lw=1.0, color=EDGE, ls="-"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                        mutation_scale=11, linewidth=lw, color=color,
                        linestyle=ls, zorder=1, shrinkA=1.5, shrinkB=1.5)
    ax.add_patch(a)


def legend(ax, y=0.018):
    """Horizontal legend across the bottom, so it cannot collide with the flow."""
    items = [(C_DEM, "Demonstrated"), (C_SUP, "Supported inference"), (C_UNT, "Untested hypothesis")]
    xs = [0.075, 0.335, 0.640]
    for (c, lab), x in zip(items, xs):
        ax.add_patch(FancyBboxPatch((x, y), 0.026, 0.022,
                                    boxstyle="round,pad=0.004,rounding_size=0.006",
                                    linewidth=0.8, edgecolor=EDGE, facecolor=c, zorder=3))
        ax.text(x + 0.036, y + 0.011, lab, ha="left", va="center",
                fontsize=7.6, color=TXT, zorder=3)


# ============================================================ FIGURE 1
def figure1():
    fig, ax = plt.subplots(figsize=(7.4, 10.2))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    ax.text(0.5, 0.990, "Proposed neuroimmune engineering framework",
            ha="center", va="top", fontsize=11.5, fontweight="bold", color=TXT)

    # Row 1: four phenotypes
    y1 = 0.856
    labels = ["Postpartum", "Chronic /\ntreatment-resistant", "Post-deployment\n(PTSD-enriched)", "Perimenopausal"]
    for i, lab in enumerate(labels):
        box(ax, 0.045 + i * 0.235, y1, 0.205, 0.066, lab, C_DEM, fontsize=7.6)

    # Row 2
    y2 = 0.740
    box(ax, 0.18, y2, 0.64, 0.058,
        "Partially overlapping immune states\n(shared across a subset of cases, not all)", C_SUP, fontsize=8.2)
    for i in range(4):
        arrow(ax, 0.1475 + i * 0.235, y1, 0.35 + i * 0.055, y2 + 0.058)

    # Row 3
    y3 = 0.640
    box(ax, 0.18, y3, 0.64, 0.052, "Peripheral immune profiling  →  immune-state assignment", C_DEM)
    arrow(ax, 0.5, y2, 0.5, y3 + 0.052)

    # Row 4
    y4 = 0.540
    box(ax, 0.13, y4, 0.74, 0.052,
        "Immune-state–matched engineered autologous cells (ex vivo)", C_UNT, bold=True, fontsize=8.6)
    arrow(ax, 0.5, y3, 0.5, y4 + 0.052)

    # Row 5
    y5 = 0.418
    box(ax, 0.10, y5, 0.36, 0.070, "Trafficking to meninges /\ndural sinuses", C_UNT, fontsize=8.0)
    box(ax, 0.54, y5, 0.36, 0.070, "Trafficking to\nchoroid plexus", C_UNT, fontsize=8.0)
    arrow(ax, 0.44, y4, 0.28, y5 + 0.070)
    arrow(ax, 0.56, y4, 0.72, y5 + 0.070)

    # Row 6
    y6 = 0.282
    box(ax, 0.10, y6, 0.80, 0.086,
        "Local receptor–ligand signalling at the interface\n"
        "(IL-10R / TGF-βR on border-associated macrophages;\n"
        "cytokine tone sensed by microglia)",
        C_SUP, fontsize=8.0)
    arrow(ax, 0.28, y5, 0.36, y6 + 0.086)
    arrow(ax, 0.72, y5, 0.64, y6 + 0.086)

    # Row 7
    y7 = 0.176
    box(ax, 0.14, y7, 0.72, 0.058, "CNS consequence: microglial / astrocytic state, circuit function",
        C_SUP, fontsize=8.4)
    arrow(ax, 0.5, y6, 0.5, y7 + 0.058)

    # Row 8
    y8 = 0.080
    box(ax, 0.24, y8, 0.52, 0.052, "Behavioural phenotype (secondary endpoint)", C_UNT)
    arrow(ax, 0.5, y7, 0.5, y8 + 0.052)

    legend(ax, y=0.018)
    fig.savefig(os.path.join(OUT, "figure1_framework.png"), dpi=300, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("figure1 written")


# ============================================================ FIGURE 2
def figure2():
    fig, ax = plt.subplots(figsize=(7.6, 9.2))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    ax.text(0.5, 0.992, "Falsification architecture",
            ha="center", va="top", fontsize=11.5, fontweight="bold", color=TXT)

    NEU = "#DCE3EC"
    ys = [0.790, 0.625, 0.460, 0.295]
    qs = [
        "Q1.  Do infused engineered cells reach the\nmeningeal / choroid-plexus interface?",
        "Q2.  Is the local immune state at that interface\nmeasurably modified?",
        "Q3.  Is there a CNS consequence\n(microglial state, circuit readout)?",
        "Q4.  Is there a behavioural effect?",
    ]
    outs = [
        "NO → Mechanism as stated is\nfalsified. Effects, if any, are not\ninterface-mediated.",
        "NO → Construct-level failure.\nPayload or expression system\nrejected, not the framework.",
        "NO → Interface signalling is\ninsufficient to reach CNS.\nCoupling step rejected.",
        "NO → Peripheral/CNS-marker-only\neffect. Favours Model 3.",
    ]

    box(ax, 0.24, 0.898, 0.52, 0.050, "Infuse engineered autologous cells", NEU, bold=True)
    arrow(ax, 0.5, 0.898, 0.5, ys[0] + 0.066)

    for i, (y, q, o) in enumerate(zip(ys, qs, outs)):
        box(ax, 0.055, y, 0.50, 0.066, q, NEU, fontsize=8.0)
        box(ax, 0.615, y - 0.004, 0.345, 0.074, o, C_UNT, fontsize=7.4)
        arrow(ax, 0.555, y + 0.033, 0.615, y + 0.033)
        ax.text(0.585, y + 0.046, "no", ha="center", va="bottom", fontsize=7.0, color="#7A2F2F")
        if i < len(ys) - 1:
            arrow(ax, 0.305, y, 0.305, ys[i + 1] + 0.066)
            ax.text(0.318, (y + ys[i + 1] + 0.066) / 2, "yes", ha="left", va="center",
                    fontsize=7.0, color="#2F5A33")

    # terminal yes
    arrow(ax, 0.305, ys[-1], 0.305, 0.212)
    ax.text(0.318, 0.252, "yes", ha="left", va="center", fontsize=7.0, color="#2F5A33")
    box(ax, 0.055, 0.146, 0.50, 0.066,
        "Chain supported. Proceed to the necessity test:\n"
        "does the effect require interface localisation?", C_DEM, fontsize=8.0, bold=True)

    # necessity test
    box(ax, 0.055, 0.020, 0.50, 0.092,
        "Compare against a trafficking-deficient\nengineered-cell arm matched for payload output.\n"
        "Effect preserved → peripheral mechanism.\nEffect lost → interface mechanism confirmed.",
        NEU, fontsize=7.6)
    arrow(ax, 0.305, 0.146, 0.305, 0.112)

    # anomaly branch
    box(ax, 0.615, 0.030, 0.345, 0.092,
        "Anomaly: behavioural effect with\nno measurable immune modification\n→ alternative, non-immune\nmechanism. Framework does not\nexplain the result.",
        C_SUP, fontsize=7.4)
    arrow(ax, 0.788, 0.291, 0.788, 0.122, ls=(0, (3, 2)))

    fig.savefig(os.path.join(OUT, "figure2_falsification.png"), dpi=300, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("figure2 written")


if __name__ == "__main__":
    figure1()
    figure2()
