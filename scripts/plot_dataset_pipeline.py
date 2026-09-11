#!/usr/bin/env python3
"""Generate publication-quality diagram of the 100k Dataset Acquisition and Curation Pipeline.

Optimized for:
- Crystal-clear typography and high-contrast styling (publication-grade for IEEE / ECTI-CIT)
- Perfectly calculated coordinates with zero collisions and generous padding
- Distinct visual cards with prominent empirical metrics
- Clean orthogonal flowchart paths
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Canvas configuration: 15.5 x 10.5 inches @ 300 DPI (sharp 4650 x 3150 resolution)
fig, ax = plt.subplots(figsize=(15.5, 10.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Typography
plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
plt.rcParams["font.family"] = "sans-serif"

# Academic Color Palette
c_title = "#0f172a"
c_subtitle = "#334155"

# Phase 1: Sources (Navy / Royal Blue)
c_src_hdr = "#1e40af"
c_src_bg = "#eff6ff"
c_src_border = "#93c5fd"

# Phase 2: Pipeline Stages
c_p1_hdr = "#0284c7"  # Sky Blue (Normalization)
c_p1_bg = "#f0f9ff"
c_p1_border = "#7dd3fc"

c_p2_hdr = "#dc2626"  # Crimson (Heuristic Purge)
c_p2_bg = "#fef2f2"
c_p2_border = "#fca5a5"

c_p3_hdr = "#d97706"  # Amber / Bronze (Root Extraction)
c_p3_bg = "#fffbeb"
c_p3_border = "#fcd34d"

c_p4_hdr = "#7c3aed"  # Violet / Purple (Permutation)
c_p4_bg = "#f5f3ff"
c_p4_border = "#c4b5fd"

c_p5_hdr = "#059669"  # Emerald (QA & Dialect Stratification)
c_p5_bg = "#ecfdf5"
c_p5_border = "#6ee7b7"

# Phase 3: Research Artifacts (Deep Teal)
c_art_hdr = "#0f766e"
c_art_bg = "#f0fdfa"
c_art_border = "#5eead4"


def draw_card(ax, x, y, w, h, badge, title, items, hdr_color, body_bg="#ffffff", border_color="#cbd5e1", line_spacing=2.5):
    """Draw an elegant scientific card container with distinct header and clear typography."""
    # Subtle drop shadow
    shadow = patches.FancyBboxPatch(
        (x + 0.35, y - 0.4), w, h,
        boxstyle="round,pad=0.0,rounding_size=1.2",
        facecolor="#000000",
        edgecolor="none",
        alpha=0.06,
        zorder=1
    )
    ax.add_patch(shadow)

    # Main Card Body
    body = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=1.2",
        facecolor=body_bg,
        edgecolor=border_color,
        linewidth=1.4,
        zorder=2
    )
    ax.add_patch(body)

    # Header Strip
    hdr_h = 4.2
    hdr = patches.FancyBboxPatch(
        (x, y + h - hdr_h), w, hdr_h,
        boxstyle="round,pad=0.0,rounding_size=1.2",
        facecolor=hdr_color,
        edgecolor=hdr_color,
        linewidth=0.5,
        zorder=3
    )
    ax.add_patch(hdr)

    # Merge bottom corners of header with card body
    rect_fill = patches.Rectangle(
        (x, y + h - hdr_h), w, 1.6,
        facecolor=hdr_color,
        edgecolor="none",
        zorder=3
    )
    ax.add_patch(rect_fill)

    # Badge & Title Text
    if badge:
        ax.text(
            x + 1.2, y + h - hdr_h/2,
            badge,
            ha="left", va="center",
            fontsize=8.8, fontweight="bold",
            color="#fef08a",  # Light yellow accent
            zorder=4
        )
        ax.text(
            x + w/2 + 1.8, y + h - hdr_h/2,
            title,
            ha="center", va="center",
            fontsize=10.2, fontweight="bold",
            color="#ffffff",
            zorder=4
        )
    else:
        ax.text(
            x + w/2, y + h - hdr_h/2,
            title,
            ha="center", va="center",
            fontsize=10.4, fontweight="bold",
            color="#ffffff",
            zorder=4
        )

    # Body Items (Generous spacing and clear hierarchy)
    text_y = y + h - hdr_h - 1.8
    for item in items:
        if item.startswith("[OK]") or item.startswith("[Yield]") or item.startswith("[Verified]"):
            # Metric / Status Pill Badge (Placed safely at bottom with clear margin)
            pill_h = 2.4
            pill_y = y + 0.9
            tag_box = patches.FancyBboxPatch(
                (x + 1.2, pill_y), w - 2.4, pill_h,
                boxstyle="round,pad=0.0,rounding_size=0.6",
                facecolor=hdr_color,
                edgecolor=hdr_color,
                linewidth=0.8,
                alpha=0.15,
                zorder=3
            )
            ax.add_patch(tag_box)
            ax.text(
                x + w/2, pill_y + pill_h / 2,
                item,
                ha="center", va="center",
                fontsize=8.8, fontweight="bold",
                color=hdr_color,
                zorder=4
            )
        elif item.startswith("•"):
            ax.text(
                x + 1.2, text_y,
                item,
                ha="left", va="top",
                fontsize=9.0, fontweight="normal",
                color="#0f172a",
                zorder=4
            )
            text_y -= line_spacing
        else:
            # Sub-item / indented description
            ax.text(
                x + 2.4, text_y,
                item,
                ha="left", va="top",
                fontsize=8.4, fontweight="normal",
                color="#334155",
                zorder=4
            )
            text_y -= (line_spacing - 0.3)


def draw_arrow(ax, x1, y1, x2, y2, label="", color="#334155", lw=1.8):
    """Draw a clean, bold connecting arrow with high-contrast label."""
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=lw,
            mutation_scale=14,
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
            fontsize=8.2, fontweight="bold",
            color="#0f172a",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#ffffff", edgecolor="#64748b", lw=1.0),
            zorder=7
        )


# ====================================================================
# TITLE BLOCK
# ====================================================================
ax.text(
    50, 97.6,
    "Standardized Three-Phase Dataset Acquisition, Curation, and Benchmark Pipeline",
    ha="center", va="center",
    fontsize=15.0, fontweight="bold",
    color=c_title
)
ax.text(
    50, 95.0,
    "End-to-End Scientific Protocol for 100,000 Verified Morphological Pairs in Low-Resource Sasak Regional NLP",
    ha="center", va="center",
    fontsize=10.2, fontstyle="italic",
    color=c_subtitle
)

# Divider Line
ax.plot([2.0, 98.0], [93.4, 93.4], color="#94a3b8", lw=1.4, zorder=1)


# ====================================================================
# SECTION 1: RAW MULTI-SOURCE INGESTION (Top Row: y = 73.2 to 88.8)
# ====================================================================
# Section Title Banner
sec1_badge = patches.FancyBboxPatch(
    (2.0, 89.8), 46.0, 2.8,
    boxstyle="round,pad=0.0,rounding_size=0.6",
    facecolor="#dbeafe", edgecolor=c_src_hdr, lw=1.0, zorder=2
)
ax.add_patch(sec1_badge)
ax.text(
    3.6, 91.2,
    "PHASE 1: MULTI-SOURCE CORPUS & LEXICAL INGESTION",
    ha="left", va="center",
    fontsize=9.4, fontweight="bold",
    color=c_src_hdr, zorder=3
)

draw_card(
    ax, x=2.0, y=73.2, w=30.6, h=15.6,
    badge="", title="Source A: Balai Bahasa NTB",
    items=[
        "• Kamus Terpadu Sasambo (Official)",
        "• 2,761 Verified Dictionary Entries",
        "• Standard Part-of-Speech & Dialect Tags",
        "[Verified] Official State Language Archive"
    ],
    hdr_color=c_src_hdr, body_bg=c_src_bg, border_color=c_src_border,
    line_spacing=2.4
)

draw_card(
    ax, x=34.7, y=73.2, w=30.6, h=15.6,
    badge="", title="Source B: Authentic Literary Corpus",
    items=[
        "• 12,591 Folk Literature Sentences",
        "• Folklore: Putri Mandalika, Dewi Anjani",
        "• 188,881 Tokens of Authentic Context",
        "[Verified] High-Vitality Native Folklore"
    ],
    hdr_color=c_src_hdr, body_bg=c_src_bg, border_color=c_src_border,
    line_spacing=2.4
)

draw_card(
    ax, x=67.4, y=73.2, w=30.6, h=15.6,
    badge="", title="Source C: Dialectal Informants",
    items=[
        "• Native Speakers from 5 Dialect Regions",
        "• Traditional Oral Literature & Lontar",
        "• Distinct Regional Shibboleth Markers",
        "[Verified] Broad Cross-Island Coverage"
    ],
    hdr_color=c_src_hdr, body_bg=c_src_bg, border_color=c_src_border,
    line_spacing=2.4
)

# Consolidation arrows from Source Cards down to Bus at y = 70.2
draw_arrow(ax, 17.3, 73.2, 17.3, 70.2, lw=1.6)
draw_arrow(ax, 50.0, 73.2, 50.0, 70.2, lw=1.6)
draw_arrow(ax, 82.7, 73.2, 82.7, 70.2, lw=1.6)

# Orthogonal Ingestion Bus: runs horizontally at y = 70.2 from x = 82.7 left to x = 10.8
ax.plot([10.8, 82.7], [70.2, 70.2], color="#334155", lw=2.0, zorder=5)

# Feeder arrow: runs straight down from bus (10.8, 70.2) into Stage 1 top at (10.8, 63.6)
draw_arrow(ax, 10.8, 70.2, 10.8, 63.6, label="Data Ingestion", color="#1e40af", lw=2.0)


# ====================================================================
# SECTION 2: FIVE-STAGE QUALITY CURATION PIPELINE (y = 30.8 to 63.6)
# ====================================================================
# Section Title Banner (Placed comfortably at x = 23.0 to 98.0, clear of the feeder at x = 10.8)
sec2_badge = patches.FancyBboxPatch(
    (23.0, 65.4), 66.0, 2.8,
    boxstyle="round,pad=0.0,rounding_size=0.6",
    facecolor="#f1f5f9", edgecolor="#334155", lw=1.0, zorder=2
)
ax.add_patch(sec2_badge)
ax.text(
    25.0, 66.8,
    "PHASE 2: FIVE-STAGE SCIENTIFIC QUALITY CURATION & MORPHOLOGICAL PIPELINE",
    ha="left", va="center",
    fontsize=9.4, fontweight="bold",
    color="#0f172a", zorder=3
)

# Stage 1: Normalization (x = 2.0 to 19.6, center = 10.8)
draw_card(
    ax, x=2.0, y=30.8, w=17.6, h=32.8,
    badge="STAGE 1", title="Normalization",
    items=[
        "• Unicode NFC Standard",
        "• Glottal Grapheme Fixing:",
        "  Apostrophes (’/`) -> (') & (q)",
        "• Diacritic Preservation:",
        "  (képéng -> kepeng)",
        "• Whitespace & Case Folding",
        "[OK] 100% Normalized Text"
    ],
    hdr_color=c_p1_hdr, body_bg=c_p1_bg, border_color=c_p1_border,
    line_spacing=3.2
)

# Transition 1 -> 2
draw_arrow(ax, 19.6, 47.2, 21.6, 47.2, lw=2.2)

# Stage 2: Heuristic Purge (x = 21.6 to 39.2, center = 30.4)
draw_card(
    ax, x=21.6, y=30.8, w=17.6, h=32.8,
    badge="STAGE 2", title="Heuristic Purge",
    items=[
        "• 3,450 Foreign Names Purged:",
        "  Biblical blacklist entities",
        "  (nahason, abihud, zadok)",
        "• Dictionary Code Stripping",
        "• Non-Phonotactic Filter",
        "• Defective Fragment Cleanup",
        "[OK] Zero Corpus Artifacts"
    ],
    hdr_color=c_p2_hdr, body_bg=c_p2_bg, border_color=c_p2_border,
    line_spacing=3.2
)

# Transition 2 -> 3
draw_arrow(ax, 39.2, 47.2, 41.2, 47.2, lw=2.2)

# Stage 3: Root Extraction (x = 41.2 to 58.8, center = 50.0)
draw_card(
    ax, x=41.2, y=30.8, w=17.6, h=32.8,
    badge="STAGE 3", title="Root Extraction",
    items=[
        "• Multi-Pass Affix Stripping",
        "• Root Protection (jaran, etc.)",
        "• Sasak Phonotactic Check:",
        "  Length >= 3 & Valid Vowel",
        "• Balai Bahasa Grounding",
        "[Yield] 1,790 Pure Lemmas"
    ],
    hdr_color=c_p3_hdr, body_bg=c_p3_bg, border_color=c_p3_border,
    line_spacing=3.2
)

# Transition 3 -> 4
draw_arrow(ax, 58.8, 47.2, 60.8, 47.2, lw=2.2)

# Stage 4: Permutation (x = 60.8 to 78.4, center = 69.6)
draw_card(
    ax, x=60.8, y=30.8, w=17.6, h=32.8,
    badge="STAGE 4", title="Permutation",
    items=[
        "• 42 Productive Affix Rules:",
        "  - Prefixes (te-, se-, ka-)",
        "  - Nasal Verba (N- assimilation)",
        "  - Suffixes (-ang, -an, -i)",
        "  - Circumfixes & Reduplication",
        "  - Enclitic Compounding",
        "[Yield] 100,000 Systematic Pairs"
    ],
    hdr_color=c_p4_hdr, body_bg=c_p4_bg, border_color=c_p4_border,
    line_spacing=3.2
)

# Transition 4 -> 5
draw_arrow(ax, 78.4, 47.2, 80.4, 47.2, lw=2.2)

# Stage 5: Dialect Stratification & QA (x = 80.4 to 98.0, center = 89.2)
draw_card(
    ax, x=80.4, y=30.8, w=17.6, h=32.8,
    badge="STAGE 5", title="QA & Stratify",
    items=[
        "• 5-Dialect Cluster Stratification:",
        "  - General Standard: 43.2%",
        "  - Meno-Mene: 23.0%",
        "  - Ngeno-Ngene: 12.7%",
        "  - Merikuq / Kuto-Kute: 21.1%",
        "• Expert Validation (κ = 0.91)",
        "[Verified] 0.00% OOV Benchmark"
    ],
    hdr_color=c_p5_hdr, body_bg=c_p5_bg, border_color=c_p5_border,
    line_spacing=3.2
)

# Flow from Stage 5 down to Phase 3 Distribution Bus
draw_arrow(ax, 89.2, 30.8, 89.2, 23.6, label="Curated Output", color="#0f766e", lw=2.0)


# ====================================================================
# SECTION 3: PUBLISHED GOLD-STANDARD DATASET ARTIFACTS (Bottom Row: y = 2.2 to 19.4)
# ====================================================================
# Section Title Banner
sec3_badge = patches.FancyBboxPatch(
    (2.0, 25.2), 50.0, 2.8,
    boxstyle="round,pad=0.0,rounding_size=0.6",
    facecolor="#ccfbf1", edgecolor=c_art_hdr, lw=1.0, zorder=2
)
ax.add_patch(sec3_badge)
ax.text(
    3.6, 26.6,
    "PHASE 3: PUBLISHED GOLD-STANDARD RESEARCH ARTIFACTS",
    ha="left", va="center",
    fontsize=9.4, fontweight="bold",
    color=c_art_hdr, zorder=3
)

# Distribution bus at y = 23.6 (runs from x = 89.2 left to x = 17.3)
ax.plot([17.3, 89.2], [23.6, 23.6], color="#334155", lw=2.0, zorder=5)

# Arrows pointing down to top of Artifact Cards at y = 19.4
draw_arrow(ax, 17.3, 23.6, 17.3, 19.4, lw=1.8)
draw_arrow(ax, 50.0, 23.6, 50.0, 19.4, lw=1.8)
draw_arrow(ax, 82.7, 23.6, 82.7, 19.4, lw=1.8)

draw_card(
    ax, x=2.0, y=2.2, w=30.6, h=17.2,
    badge="", title="Artifact 1: benchmark_100k.csv",
    items=[
        "• EXACTLY 100,000 Morphological Pairs",
        "• Columns: surface, lemma, prefix, infix, suffix, dialect",
        "• SasakNLP Accuracy: 80.44% vs Baselines (1.01%, 55.21%)",
        "[Verified] Gold-Standard Stress-Test Benchmark"
    ],
    hdr_color=c_art_hdr, body_bg=c_art_bg, border_color=c_art_border,
    line_spacing=2.6
)

draw_card(
    ax, x=34.7, y=2.2, w=30.6, h=17.2,
    badge="", title="Artifact 2: sasak_sentences_large.csv",
    items=[
        "• 12,591 Authentic Sentences (188,881 Tokens)",
        "• Real Discourse Context from Oral Literature & Folklore",
        "• Vocabulary Feature Space Compression: 31.98%",
        "[Verified] Large-Scale Natural Evaluation Corpus"
    ],
    hdr_color=c_art_hdr, body_bg=c_art_bg, border_color=c_art_border,
    line_spacing=2.6
)

draw_card(
    ax, x=67.4, y=2.2, w=30.6, h=17.2,
    badge="", title="Artifact 3: kamus_balai_bahasa_ntb.csv",
    items=[
        "• 2,761 Verified Root Entries (Balai Bahasa NTB)",
        "• High-Speed PrefixTrie Verification Structure: O(L)",
        "• Overstemming Restriction: 2.28% (vs 24.8% Greedy)",
        "[Verified] Foundational Machine Lexicon (SasakLex)"
    ],
    hdr_color=c_art_hdr, body_bg=c_art_bg, border_color=c_art_border,
    line_spacing=2.6
)

plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)

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
    print(f"✅ Generated high-clarity Figure 5 at: {p}")

plt.close()
print("🎉 All Figure 5 assets successfully updated!")
