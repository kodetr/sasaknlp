#!/usr/bin/env python3
"""Generate a clean, high-legibility publication flowchart of the Dataset Acquisition and Curation Pipeline.

Design Specifications:
- Pure monochrome / grayscale styling (zero chromatic colors) optimized for academic print standards.
- No internal graphic title banner (as paper caption provides the title).
- Streamlined flowchart boxes containing only bold titles / stage names.
- Clean orthogonal flowchart paths with zero overlap, generous whitespace, and 300 DPI export.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Canvas configuration: 12.0 x 5.8 inches @ 300 DPI
fig, ax = plt.subplots(figsize=(12.0, 5.8), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(5.5, 99.5)
ax.axis("off")

# Typography
plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
plt.rcParams["font.family"] = "sans-serif"


def draw_arrow(ax, x1, y1, x2, y2, label="", lw=1.8):
    """Draw an orthogonal connecting arrow in solid black with an optional high-contrast label."""
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>",
            color="#000000",
            lw=lw,
            mutation_scale=13,
            shrinkA=0,
            shrinkB=0
        ),
        zorder=6
    )
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        ax.text(
            mid_x, mid_y,
            label,
            ha="center", va="center",
            fontsize=8.5, fontweight="bold",
            color="#000000",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", edgecolor="#000000", lw=1.0),
            zorder=7
        )


def draw_phase_banner(ax, x, y, w, h, text):
    """Draw a clean, minimalist phase banner in neutral grayscale."""
    banner = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.6",
        facecolor="#f3f4f6",
        edgecolor="#000000",
        linewidth=1.2,
        zorder=2
    )
    ax.add_patch(banner)
    ax.text(
        x + w / 2, y + h / 2,
        text,
        ha="center", va="center",
        fontsize=10.0, fontweight="bold",
        color="#000000",
        zorder=3
    )


# ====================================================================
# PHASE 1: DATA SOURCES
# ====================================================================
draw_phase_banner(ax, x=2.0, y=93.5, w=46.0, h=4.0, text="PHASE 1: MULTI-SOURCE INGESTION")

sources = [
    ("NTB Language Agency Lexicon", 2.0, 30.6),
    ("Authentic Literary Corpus", 34.7, 30.6),
    ("Dialectal Informants (5 Regions)", 67.4, 30.6)
]

for title, x, w in sources:
    card = patches.FancyBboxPatch(
        (x, 76.5), w, 15.0,
        boxstyle="round,pad=0.0,rounding_size=0.8",
        facecolor="#ffffff",
        edgecolor="#000000",
        linewidth=1.4,
        zorder=2
    )
    ax.add_patch(card)
    ax.text(
        x + w / 2, 76.5 + 7.5,
        title,
        ha="center", va="center",
        fontsize=11.5, fontweight="bold",
        color="#000000",
        linespacing=1.3,
        zorder=3
    )

# Source consolidation arrows to bus at y = 72.0
draw_arrow(ax, 2.0 + 30.6 / 2, 76.5, 2.0 + 30.6 / 2, 72.0)
draw_arrow(ax, 34.7 + 30.6 / 2, 76.5, 34.7 + 30.6 / 2, 72.0)
draw_arrow(ax, 67.4 + 30.6 / 2, 76.5, 67.4 + 30.6 / 2, 72.0)

# Ingestion Bus
ax.plot([10.8, 82.7], [72.0, 72.0], color="#000000", lw=1.8, zorder=5)
draw_arrow(ax, 10.8, 72.0, 10.8, 58.5, label="Data Ingestion", lw=1.8)


# ====================================================================
# PHASE 2: FIVE-STAGE CURATION PIPELINE
# ====================================================================
draw_phase_banner(ax, x=22.1, y=60.5, w=57.8, h=4.0, text="PHASE 2: FIVE-STAGE QUALITY CURATION PIPELINE")

stages = [
    ("STAGE 1", "Normalization", 2.0, 17.6),
    ("STAGE 2", "Heuristic Purge", 22.1, 17.6),
    ("STAGE 3", "Root Extraction", 42.2, 17.6),
    ("STAGE 4", "Affix Permutation", 62.3, 17.6),
    ("STAGE 5", "QA & Stratify", 82.4, 17.6)
]

y_p2 = 44.5
h_p2 = 14.0
mid_y = y_p2 + h_p2 / 2

for badge, title, x, w in stages:
    card = patches.FancyBboxPatch(
        (x, y_p2), w, h_p2,
        boxstyle="round,pad=0.0,rounding_size=0.8",
        facecolor="#ffffff",
        edgecolor="#000000",
        linewidth=1.4,
        zorder=2
    )
    ax.add_patch(card)

    # Stage Badge (tight spacing)
    ax.text(
        x + w / 2, mid_y + 1.25,
        badge,
        ha="center", va="center",
        fontsize=9.2, fontweight="bold",
        color="#4b5563",
        zorder=3
    )
    # Stage Title
    ax.text(
        x + w / 2, mid_y - 1.25,
        title,
        ha="center", va="center",
        fontsize=10.8, fontweight="bold",
        color="#000000",
        zorder=3
    )

# Stage-to-stage horizontal arrows
draw_arrow(ax, 2.0 + 17.6, mid_y, 22.1, mid_y)
draw_arrow(ax, 22.1 + 17.6, mid_y, 42.2, mid_y)
draw_arrow(ax, 42.2 + 17.6, mid_y, 62.3, mid_y)
draw_arrow(ax, 62.3 + 17.6, mid_y, 82.4, mid_y)

# Flow from Stage 5 to distribution bus at y = 28.0
draw_arrow(ax, 82.4 + 17.6 / 2, y_p2, 82.4 + 17.6 / 2, 28.0, label="Curated Output", lw=1.8)


# ====================================================================
# PHASE 3: PUBLISHED RESEARCH ARTIFACTS
# ====================================================================
draw_phase_banner(ax, x=2.0, y=32.5, w=50.0, h=4.0, text="PHASE 3: PUBLISHED RESEARCH ARTIFACTS")

# Distribution bus line
ax.plot([17.3, 91.2], [28.0, 28.0], color="#000000", lw=1.8, zorder=5)

# Arrows down to artifact cards at y = 23.5
draw_arrow(ax, 2.0 + 30.6 / 2, 28.0, 2.0 + 30.6 / 2, 23.5)
draw_arrow(ax, 34.7 + 30.6 / 2, 28.0, 34.7 + 30.6 / 2, 23.5)
draw_arrow(ax, 67.4 + 30.6 / 2, 28.0, 67.4 + 30.6 / 2, 23.5)

artifacts = [
    ("benchmark_100k.csv\n(100k Pairs)", 2.0, 30.6),
    ("sasak_sentences_large.csv\n(12,591 Sentences)", 34.7, 30.6),
    ("official_sasak_lexicon.csv\n(2,761 Roots)", 67.4, 30.6)
]

for title, x, w in artifacts:
    card = patches.FancyBboxPatch(
        (x, 8.5), w, 15.0,
        boxstyle="round,pad=0.0,rounding_size=0.8",
        facecolor="#ffffff",
        edgecolor="#000000",
        linewidth=1.4,
        zorder=2
    )
    ax.add_patch(card)
    ax.text(
        x + w / 2, 8.5 + 7.5,
        title,
        ha="center", va="center",
        fontsize=11.5, fontweight="bold",
        color="#000000",
        linespacing=1.3,
        zorder=3
    )

plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.03)

# Save to all target locations
output_paths = [
    Path("docs/figures/fig5_dataset_acquisition_pipeline.png"),
    Path("artikel/figures/fig5_dataset_acquisition_pipeline.png"),
    Path("sasaknlp/artikel/figures/fig5_dataset_acquisition_pipeline.png"),
    Path("sasaknlp/docs/figures/fig5_dataset_acquisition_pipeline.png"),
    Path("huggingface/space/figures/fig5_dataset_acquisition_pipeline.png"),
]

for p in output_paths:
    p.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(p, dpi=300, facecolor="#ffffff", edgecolor="none")
    print(f"✅ Generated high-clarity monochrome Figure 5 at: {p}")

plt.close()
print("🎉 All Figure 5 assets successfully updated in monochrome format without title!")
