#!/usr/bin/env python3
"""Generate publication-quality figures (300 DPI) for academic journal article.

Produces:
1. docs/figures/fig1_morphology_accuracy.png (Bar chart of morphological category accuracy)
2. docs/figures/fig2_dialect_performance.png (Grouped bar chart of dialect performance)
3. docs/figures/fig3_error_taxonomy.png (Donut chart of error distribution)
4. docs/figures/fig4_pipeline_benchmark.png (Latency and throughput benchmark summary)
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Setup publication style
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.linewidth"] = 0.8

output_dir = Path("docs/figures")
output_dir.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Figure 1: Morphological Affix Category Accuracy
# -----------------------------------------------------------------------------
def plot_morphology_accuracy():
    categories = [
        "Reduplication",
        "Prefix (ka-)",
        "Prefix (te-)",
        "Prefix (se-)",
        "Circumfix (te-...-ang)",
        "Clitic (-ku)",
        "Clitic (-ne)",
        "Infix (-in- / -um-)",
        "Prefix (pe- / be-)",
        "Base Root",
        "Clitic (-de / -te)",
        "Circumfix (pe-...-an)",
        "Suffix (-ang)",
        "Suffix (-an)",
        "Circumfix (be-...-an)"
    ]
    accuracies = [
        100.00, 98.40, 97.98, 97.88, 97.03, 97.14, 95.18, 93.34,
        91.85, 91.22, 88.54, 88.33, 84.00, 78.54, 65.32
    ]

    colors = []
    for acc in accuracies:
        if acc >= 95.0:
            colors.append("#1b7837")  # Deep forest green
        elif acc >= 85.0:
            colors.append("#2b83ba")  # Academic blue
        elif acc >= 75.0:
            colors.append("#fdae61")  # Warm orange
        else:
            colors.append("#d7191c")  # Crimson warning

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    y_pos = np.arange(len(categories))
    bars = ax.barh(y_pos, accuracies, color=colors, height=0.65, edgecolor="#222222", linewidth=0.6)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=9.5, fontweight="medium")
    ax.invert_yaxis()  # Highest at the top
    ax.set_xlabel("Stemming Accuracy (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_xlim(0, 110)
    ax.grid(axis="x", linestyle="--", alpha=0.5, color="#888888")
    ax.set_axisbelow(True)

    # Annotate percentages at bar ends
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 1.2,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.2f}%",
            ha="left",
            va="center",
            fontsize=8.5,
            fontweight="semibold",
            color="#222222"
        )

    ax.set_title(
        "SasakNLP Morphological Rule Accuracy across Grammatical Affixes\n(Evaluated on 100,000 Verified Test Pairs)",
        fontsize=12,
        fontweight="bold",
        pad=15
    )

    # Custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="#1b7837", edgecolor="#222", label="Excellent (>= 95%)"),
        Patch(facecolor="#2b83ba", edgecolor="#222", label="Good (85% - 94.9%)"),
        Patch(facecolor="#fdae61", edgecolor="#222", label="Moderate (75% - 84.9%)"),
        Patch(facecolor="#d7191c", edgecolor="#222", label="Complex / Needs Rule ( < 75%)")
    ]
    ax.legend(handles=legend_elements, loc="lower left", fontsize=8.5, framealpha=0.9)

    plt.tight_layout()
    save_path = output_dir / "fig1_morphology_accuracy.png"
    plt.savefig(save_path)
    plt.close()
    print(f"[✓] Saved Figure 1: {save_path}")


# -----------------------------------------------------------------------------
# Figure 2: Dialect Performance Comparison
# -----------------------------------------------------------------------------
def plot_dialect_performance():
    dialects = ["Sasak Umum\n(General)", "Kuto-Kute\n(North Lombok)", "Merikuq-Merikaq\n(South Lombok)", "Meno-Mene\n(Central Lombok)", "Ngeno-Ngene\n(East Lombok)"]
    acc_100k = [85.73, 80.31, 79.79, 77.04, 69.24]
    sample_counts = ["43,254 pairs", "10,475 pairs", "10,535 pairs", "23,023 pairs", "12,713 pairs"]

    x = np.arange(len(dialects))
    colors = ["#2b83ba", "#41b6c4", "#7bccc4", "#fdae61", "#e08250"]

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    bars = ax.bar(x, acc_100k, 0.55, color=colors, edgecolor="#222222", linewidth=0.8)

    ax.set_ylabel("Accuracy on 100k Dataset (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("SasakNLP Accuracy across Five Major Sasak Dialects\n(Evaluated on 100,000 Verified Test Pairs)", fontsize=12, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(dialects, fontsize=9.5, fontweight="medium")
    ax.set_ylim(0, 105)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#888888")
    ax.set_axisbelow(True)

    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(
            f"{height:.2f}%\n({sample_counts[i]})",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.0,
            fontweight="bold"
        )

    plt.tight_layout()
    save_path = output_dir / "fig2_dialect_performance.png"
    plt.savefig(save_path)
    plt.close()
    print(f"[✓] Saved Figure 2: {save_path}")


# -----------------------------------------------------------------------------
# Figure 3: Error Taxonomy Distribution (Two-Panel Publication Layout)
# -----------------------------------------------------------------------------
def plot_error_taxonomy():
    """Generates Figure 3: Donut chart with dedicated side-by-side diagnosis table."""
    fig, (ax_donut, ax_table) = plt.subplots(1, 2, figsize=(12.2, 5.8), dpi=300, gridspec_kw={"width_ratios": [1, 1.25]})

    # Exact metrics on 100,000 benchmark samples
    categories = [
        ("Correct Lemmatization", 80438, 80.44, "#1b7837", "Optimal recovery of base root"),
        ("Understemming", 15856, 15.86, "#d97706", "Multi-layer affix/clitic residual"),
        ("Overstemming", 2279, 2.28, "#dc2626", "Base root over-cut (affix-like ending)"),
        ("Incorrect Lemma", 1427, 1.43, "#2563eb", "Morphonemic nasal selection ambiguity"),
        ("Out-of-Vocabulary (OOV)", 0, 0.00, "#64748b", "100% Core lexicon coverage (0 OOV)")
    ]

    counts = [c[1] for c in categories]
    colors = [c[3] for c in categories]

    # Donut Chart on Left Panel
    plot_sizes = [c if c > 0 else 0.0001 for c in counts]
    wedges, _, _ = ax_donut.pie(
        plot_sizes,
        colors=colors,
        startangle=140,
        wedgeprops=dict(width=0.38, edgecolor="#ffffff", linewidth=2.0),
        autopct=lambda p: f"{p:.1f}%" if p >= 5.0 else "",
        pctdistance=0.78,
        textprops=dict(fontsize=9.0, fontweight="bold", color="#ffffff")
    )

    # Donut Center Summary Badge
    ax_donut.text(
        0, 0.10,
        "80.44%",
        ha="center", va="center",
        fontsize=18, fontweight="bold",
        color="#1b7837"
    )
    ax_donut.text(
        0, -0.07,
        "ACCURACY",
        ha="center", va="center",
        fontsize=9.0, fontweight="bold",
        color="#334155"
    )
    ax_donut.text(
        0, -0.22,
        "(N = 100,000)",
        ha="center", va="center",
        fontsize=8.0, fontweight="semibold",
        color="#64748b"
    )
    ax_donut.set_title("Proportion of Output Categories", fontsize=10.5, fontweight="bold", pad=12)

    # Structured Table / Breakdown Card on Right Panel
    ax_table.axis("off")
    ax_table.set_xlim(0, 100)
    ax_table.set_ylim(0, 100)

    # Table Title
    ax_table.text(
        0, 95,
        "Detailed Error Classification & Linguistic Diagnosis",
        fontsize=11.0, fontweight="bold", color="#0f172a"
    )
    ax_table.text(
        0, 89,
        "Quantitative taxonomy breakdown according to computational morphology standards",
        fontsize=8.2, fontstyle="italic", color="#475569"
    )

    # Divider line
    ax_table.plot([0, 100], [84, 84], color="#cbd5e1", lw=1.2)

    # Render each category as a clean structured card row
    row_y = 75
    for i, (cat_name, count, pct, col, desc) in enumerate(categories):
        # Color circle swatch
        circle = plt.Circle((3.2, row_y - 2.5), 2.2, color=col)
        ax_table.add_patch(circle)

        # Category Name
        ax_table.text(
            8.5, row_y - 1.0,
            cat_name,
            fontsize=9.0, fontweight="bold", color="#0f172a"
        )
        # Count & Percentage Badge
        badge_text = f"{count:,} ({pct:.2f}%)" if count > 0 else "0 (0.00%)"
        ax_table.text(
            98, row_y - 1.0,
            badge_text,
            ha="right", fontsize=9.0, fontweight="bold", color=col
        )
        # Linguistic Diagnosis / Remedy
        ax_table.text(
            8.5, row_y - 5.5,
            f"Diagnosis: {desc}",
            fontsize=7.8, fontweight="medium", color="#475569"
        )

        # Subtle row separator
        if i < len(categories) - 1:
            ax_table.plot([3.2, 98], [row_y - 8.5, row_y - 8.5], color="#f1f5f9", lw=1.0)

        row_y -= 15.5

    # Overall Figure Suptitle
    fig.suptitle("Figure 3: Morphological Error Taxonomy Distribution (100,000 Test Pairs)", fontsize=12.5, fontweight="bold", y=0.97)
    plt.subplots_adjust(top=0.84, bottom=0.08, left=0.05, right=0.95, wspace=0.18)

    save_path = output_dir / "fig3_error_taxonomy.png"
    plt.savefig(save_path, dpi=300, facecolor="#ffffff")
    plt.close()
    print(f"[✓] Saved Refined Figure 3: {save_path}")


# -----------------------------------------------------------------------------
# Figure 4: Pipeline Throughput & Latency Summary (Collision-Free Layout)
# -----------------------------------------------------------------------------
def plot_pipeline_benchmark():
    """Generates Figure 4: Throughput & Latency with generous headroom and margins."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 5.4), dpi=300)

    # 1. Processing Speed / Throughput Comparison
    # Concise, well-spaced category labels to prevent horizontal overlapping
    benchmarks = [
        "Baseline 1\n(Lookup)",
        "Baseline 2\n(Greedy)",
        "SasakNLP\n(100k Words)",
        "SasakNLP\n(Sentences)",
        "Sastrawi ID\n(Reference)*"
    ]
    speeds = [24500, 18200, 7612, 14751, 12500]
    colors = ["#94a3b8", "#64748b", "#1b7837", "#0284c7", "#0f766e"]

    x = np.arange(len(benchmarks))
    bars = ax1.bar(x, speeds, color=colors, edgecolor="#1e293b", width=0.50, linewidth=0.8)
    ax1.set_ylabel("Processing Speed (Words / Second)", fontsize=9.5, fontweight="bold", labelpad=8)
    ax1.set_title("Computational Throughput Comparison\n(Evaluated on 100,000 Morphological Words)", fontsize=10.5, fontweight="bold", pad=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(benchmarks, fontsize=8.5, fontweight="medium")
    ax1.set_ylim(0, 29000)  # Generous headroom so text never hits the border
    ax1.grid(axis="y", linestyle="--", alpha=0.5, color="#94a3b8")
    ax1.set_axisbelow(True)

    for bar in bars:
        h = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width()/2,
            h + 600,
            f"{h:,.0f} w/s",
            ha="center", va="bottom",
            fontsize=8.0, fontweight="bold", color="#0f172a"
        )

    # 2. Pipeline Sub-millisecond Latency per Real Sentence
    sentences = [
        "S1: Sasak Halus",
        "S2: Cerita Rakyat",
        "S3: Teks Diakritik",
        "S4: Legenda Sasak",
        "S5: Verba Resiprokal"
    ]
    latencies = [0.74, 0.90, 0.78, 0.86, 0.44]

    y_pos = np.arange(len(sentences))
    bars2 = ax2.barh(y_pos, latencies, color="#f59e0b", edgecolor="#b45309", height=0.52, linewidth=0.8)
    ax2.set_xlabel("Latency per Sentence (Milliseconds)", fontsize=9.5, fontweight="bold", labelpad=8)
    ax2.set_title("End-to-End Pipeline Latency on Authentic Sentences\n(Normalizer + Tokenizer + Dialect + Stemmer)", fontsize=10.5, fontweight="bold", pad=12)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(sentences, fontsize=8.5, fontweight="medium")
    ax2.set_xlim(0, 1.35)  # Generous margin on right edge
    ax2.set_ylim(-0.6, 4.8) # Clean vertical bounds
    ax2.grid(axis="x", linestyle="--", alpha=0.5, color="#94a3b8")
    ax2.set_axisbelow(True)

    # Sub-millisecond Threshold Vertical Reference Line
    threshold_line = ax2.axvline(1.0, color="#dc2626", linestyle="--", lw=1.6, zorder=2, label="Sub-ms Threshold (1.00 ms)")
    ax2.legend(loc="lower right", fontsize=8.2, framealpha=0.92, edgecolor="#cbd5e1")

    for bar in bars2:
        w = bar.get_width()
        ax2.text(
            w + 0.03,
            bar.get_y() + bar.get_height()/2,
            f"{w:.2f} ms",
            ha="left", va="center",
            fontsize=8.5, fontweight="bold", color="#0f172a"
        )

    fig.suptitle("Figure 4: Computational Efficiency, Throughput, and Latency of SasakNLP", fontsize=12.5, fontweight="bold", y=0.97)
    plt.subplots_adjust(top=0.84, bottom=0.14, left=0.07, right=0.96, wspace=0.38)

    save_path = output_dir / "fig4_pipeline_benchmark.png"
    plt.savefig(save_path, dpi=300, facecolor="#ffffff")
    plt.close()
    print(f"[✓] Saved Refined Figure 4: {save_path}")


if __name__ == "__main__":
    plot_morphology_accuracy()
    plot_dialect_performance()
    plot_error_taxonomy()
    plot_pipeline_benchmark()
    print("\n[✓] All publication figures regenerated with zero collisions!")

