"""Render the eigen-frame flow grid as a PNG.

One cell per ordered frame pair (row = the frame a statement is small
in, column = the frame asked about), carrying the verdict, the
governing law, and the witness. Sources: 0024 (conjugate axis), 0025
(crossing law), 0026 (path/span/degree laws, free pairs, complement
symmetry), 0027 (exact ceilings, FDD), 0028 (fiber/survivor laws,
zeta conjugacy, transported multiplexer witness).

Verdict classes:
  P     polynomial law -- row-small forces column-small
  QP    quasipolynomial law
  E     witnessed exponential escape
  CONJ  conjugate axis (Donoho-Stark: never both small past 2^n)
  B     bounded by a law, tightness OPEN
  deriv suffix ' *' -- cell derived by the complement symmetry
  open  unmeasured (the cross-polarity shared cells)

Run this file directly; writes frame_flow_grid.png beside it.
"""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class GridCell:
    def __init__(self, verdict: str, rule: str, witness: str,
                 derived_by_symmetry: bool = False) -> None:
        self.verdict = verdict
        self.rule = rule
        self.witness = witness
        self.derived_by_symmetry = derived_by_symmetry


FRAME_NAMES: list[str] = ["minterm", "ANF", "dual ANF", "Walsh",
                          "OBDD", "FDD", "negFDD"]
FRAME_DESCRIPTIONS: list[str] = [
    "flat Shannon\n(model list)", "flat posDavio\n(ring form)",
    "flat negDavio", "flat, ℤ lift\n(spectrum)",
    "shared Shannon\n(automaton)", "shared posDavio",
    "shared negDavio"]
FLAT_FRAME_COUNT: int = 4

VERDICT_COLORS: dict[str, str] = {
    "P": "#b7e4c7", "QP": "#a8dadc", "E": "#f4b6ad",
    "CONJ": "#d9c7ee", "B": "#ffe08a", "open": "#e0e0e0"}
VERDICT_EDGE_COLORS: dict[str, str] = {
    "P": "#1b6e3c", "QP": "#146b74", "E": "#a12f22",
    "CONJ": "#6b3fa0", "B": "#9a7200", "open": "#8a8a8a"}


def build_grid() -> dict[tuple[str, str], GridCell]:
    grid: dict[tuple[str, str], GridCell] = {}

    def put(row: str, column: str, verdict: str, rule: str,
            witness: str, derived: bool = False) -> None:
        grid[(row, column)] = GridCell(verdict, rule, witness, derived)

    # ---- row: minterm ------------------------------------------------
    put("minterm", "ANF", "E", "no law",
        "δ at 0: 1 model,\n4096 terms")
    put("minterm", "dual ANF", "E", "no law",
        "δ at all-ones", derived=True)
    put("minterm", "Walsh", "CONJ", "Donoho–Stark\nσ·μ ≥ 2ⁿ (tight)",
        "δ at 0: 1 model,\nσ = 4096")
    put("minterm", "OBDD", "P", "path law\n≤ (n+1)(μ+1)",
        "exact: model\nsuffix-sets")
    put("minterm", "FDD", "E", "survivor law\nceiling 2^μ",
        "one-hot models:\nμ=8 → width 256")
    put("minterm", "negFDD", "E", "survivor law 2^μ",
        "", derived=True)

    # ---- row: ANF ----------------------------------------------------
    put("ANF", "minterm", "E", "no law",
        "parity: 12 terms,\n2048 models")
    put("ANF", "dual ANF", "E", "free pair (0026)",
        "full monomial:\n1 term, dual 4096")
    put("ANF", "Walsh", "E", "no law",
        "full monomial:\nσ = 4096")
    put("ANF", "OBDD", "E", "crossing law\nceiling 2^straddle",
        "windowed parity:\n10 terms, 1021 states")
    put("ANF", "FDD", "P", "fiber law\n≤ (n+1)(t+1)",
        "exact: distinct\nleft fibers")
    put("ANF", "negFDD", "open", "unmeasured",
        "cross-polarity\ncell")

    # ---- row: dual ANF -----------------------------------------------
    put("dual ANF", "minterm", "E", "free pair",
        "", derived=True)
    put("dual ANF", "ANF", "E", "free pair (0026)",
        "at-least-one:\n2 dual, 4095 terms")
    put("dual ANF", "Walsh", "E", "no law",
        "", derived=True)
    put("dual ANF", "OBDD", "E", "crossing law\n2^straddle",
        "", derived=True)
    put("dual ANF", "FDD", "open", "unmeasured",
        "cross-polarity\ncell")
    put("dual ANF", "negFDD", "P", "fiber law",
        "", derived=True)

    # ---- row: Walsh --------------------------------------------------
    put("Walsh", "minterm", "CONJ", "Donoho–Stark",
        "parity: σ = 2,\n2048 models")
    put("Walsh", "ANF", "QP", "degree law\ndeg ≤ log₂σ → n^log σ",
        "AND of parities:\nσ=4, (n/2)² terms")
    put("Walsh", "dual ANF", "QP", "degree law",
        "", derived=True)
    put("Walsh", "OBDD", "B", "span law ≤ 2^d\ntightness OPEN",
        "d can reach about √σ,\nno witness either way")
    put("Walsh", "FDD", "QP", "degree ∘ fiber\nlaws composed",
        "AND of parities:\nFDD 34")
    put("Walsh", "negFDD", "QP", "degree ∘ fiber",
        "", derived=True)

    # ---- row: OBDD ---------------------------------------------------
    put("OBDD", "minterm", "E", "no law",
        "at-least-one:\n25 states, 4095 models")
    put("OBDD", "ANF", "E", "no law",
        "at-least-one:\n4095 terms")
    put("OBDD", "dual ANF", "E", "no law",
        "not-all-ones", derived=True)
    put("OBDD", "Walsh", "E", "no law",
        "at-least-one:\nσ = 4096")
    put("OBDD", "FDD", "E", "ζ-transported\nwitness (0028)",
        "one-hot mux:\n95 states, FDD 774")
    put("OBDD", "negFDD", "E", "ζ-transported",
        "", derived=True)

    # ---- row: FDD ----------------------------------------------------
    put("FDD", "minterm", "E", "no law",
        "at-least-one:\nFDD 25, 4095 models")
    put("FDD", "ANF", "E", "no law",
        "at-least-one:\n4095 terms")
    put("FDD", "dual ANF", "E", "no law",
        "full monomial:\nFDD 25, dual 4096")
    put("FDD", "Walsh", "E", "no law",
        "at-least-one:\nσ = 4096")
    put("FDD", "OBDD", "E", "shared frames\nincomparable (0027)",
        "windowed parity:\nFDD 95, 1021 states")
    put("FDD", "negFDD", "open", "unmeasured",
        "cross-polarity\ncell")

    # ---- row: negFDD -------------------------------------------------
    for column, mirrored in (("minterm", "minterm"), ("ANF",
                             "dual ANF"), ("dual ANF", "ANF"),
                            ("Walsh", "Walsh"), ("OBDD", "OBDD")):
        source = grid[("FDD", mirrored)]
        put("negFDD", column, source.verdict, source.rule, "",
            derived=True)
    put("negFDD", "FDD", "open", "unmeasured",
        "cross-polarity\ncell")
    return grid


def render(output_path: str) -> None:
    grid = build_grid()
    frame_count = len(FRAME_NAMES)
    cell_width, cell_height = 2.35, 1.55
    figure, axes = plt.subplots(
        figsize=(cell_width * frame_count + 3.4,
                 cell_height * frame_count + 4.6))
    axes.set_xlim(-1.55, frame_count * cell_width)
    axes.set_ylim(-3.35, frame_count * cell_height + 1.35)
    axes.axis("off")
    axes.set_aspect("equal")

    def cell_origin(row_index: int, column_index: int) -> tuple[float,
                                                                float]:
        return (column_index * cell_width,
                (frame_count - 1 - row_index) * cell_height)

    for row_index, row_name in enumerate(FRAME_NAMES):
        for column_index, column_name in enumerate(FRAME_NAMES):
            x, y = cell_origin(row_index, column_index)
            if row_name == column_name:
                axes.add_patch(Rectangle((x, y), cell_width,
                                         cell_height,
                                         facecolor="#3c4048",
                                         edgecolor="white",
                                         linewidth=1.2))
                axes.text(x + cell_width / 2, y + cell_height / 2,
                          row_name, ha="center", va="center",
                          fontsize=8.5, color="white", style="italic")
                continue
            cell = grid[(row_name, column_name)]
            face = VERDICT_COLORS[cell.verdict]
            edge = VERDICT_EDGE_COLORS[cell.verdict]
            hatch = "///" if cell.verdict == "open" else None
            axes.add_patch(Rectangle((x, y), cell_width, cell_height,
                                     facecolor=face,
                                     edgecolor="white", linewidth=1.2,
                                     hatch=hatch))
            verdict_label = cell.verdict + \
                (" *" if cell.derived_by_symmetry else "")
            axes.text(x + 0.09, y + cell_height - 0.13, verdict_label,
                      ha="left", va="top", fontsize=10.5,
                      fontweight="bold", color=edge)
            axes.text(x + cell_width / 2, y + cell_height - 0.52,
                      cell.rule, ha="center", va="top", fontsize=7.1,
                      color="#222222")
            if cell.witness:
                axes.text(x + cell_width / 2, y + 0.10, cell.witness,
                          ha="center", va="bottom", fontsize=6.4,
                          color="#555555")

    # axis labels
    for column_index, (name, description) in enumerate(
            zip(FRAME_NAMES, FRAME_DESCRIPTIONS)):
        x = column_index * cell_width + cell_width / 2
        top = frame_count * cell_height
        axes.text(x, top + 0.62, name, ha="center", va="bottom",
                  fontsize=10.5, fontweight="bold")
        axes.text(x, top + 0.50, description, ha="center", va="top",
                  fontsize=7.0, color="#555555")
    for row_index, (name, description) in enumerate(
            zip(FRAME_NAMES, FRAME_DESCRIPTIONS)):
        y = (frame_count - 1 - row_index) * cell_height + \
            cell_height / 2
        axes.text(-0.22, y + 0.14, name, ha="right", va="center",
                  fontsize=10.5, fontweight="bold")
        axes.text(-0.22, y - 0.24, description.replace("\n", ", "),
                  ha="right", va="center", fontsize=6.8,
                  color="#555555")

    # flat / shared separators
    separator_x = FLAT_FRAME_COUNT * cell_width
    separator_y = (frame_count - FLAT_FRAME_COUNT) * cell_height
    axes.plot([separator_x, separator_x],
              [0, frame_count * cell_height], color="#3c4048",
              linewidth=2.6)
    axes.plot([0, frame_count * cell_width],
              [separator_y, separator_y], color="#3c4048",
              linewidth=2.6)
    axes.text(separator_x / 2, frame_count * cell_height + 1.16,
              "FLAT frames", ha="center", va="bottom", fontsize=9.5,
              color="#3c4048", fontweight="bold")
    axes.text(separator_x + (frame_count * cell_width -
                             separator_x) / 2,
              frame_count * cell_height + 1.16, "SHARED frames",
              ha="center", va="bottom", fontsize=9.5, color="#3c4048",
              fontweight="bold")

    # zeta bracket between the two shared Shannon/Davio columns
    obdd_center = (FRAME_NAMES.index("OBDD") + 0.5) * cell_width
    fdd_center = (FRAME_NAMES.index("FDD") + 0.5) * cell_width
    bracket_y = -0.30
    axes.annotate("", xy=(obdd_center, bracket_y),
                  xytext=(fdd_center, bracket_y),
                  arrowprops={"arrowstyle": "<->",
                              "color": "#6b3fa0", "linewidth": 1.6})
    axes.text((obdd_center + fdd_center) / 2, bracket_y - 0.16,
              "ζ-conjugate cut-by-cut (ζ an involution; witnesses "
              "transport both ways, 0028)", ha="center", va="top",
              fontsize=8.0, color="#6b3fa0")

    axes.set_title(
        "Eigen-frame flow grid — statement small in ROW frame: what "
        "does that force in the COLUMN frame?",
        fontsize=13.5, pad=42)

    legend_lines = [
        ("P", "polynomial law — small stays small (P preserved)"),
        ("QP", "quasipolynomial law"),
        ("E", "witnessed exponential escape (P → E possible)"),
        ("CONJ", "conjugate axis — never both small past "
                 "Donoho–Stark"),
        ("B", "bounded by span law 2^d; tightness OPEN — the one "
              "open law cell"),
        ("open", "unmeasured (the four cross-polarity shared cells)")]
    legend_top = -0.92
    for line_index, (verdict, meaning) in enumerate(legend_lines):
        y = legend_top - 0.34 * line_index
        axes.add_patch(Rectangle((0.0, y - 0.115), 0.42, 0.26,
                                 facecolor=VERDICT_COLORS[verdict],
                                 edgecolor="#888888", linewidth=0.7,
                                 hatch="///" if verdict == "open"
                                 else None))
        axes.text(0.58, y, meaning, ha="left", va="center",
                  fontsize=8.2, color="#222222")
    axes.text(0.0, legend_top - 0.34 * len(legend_lines) - 0.10,
              "*  derived by the complement symmetry (0026): full "
              "complement swaps ANF↔dualANF and FDD↔negFDD, fixes "
              "minterm/Walsh/OBDD sizes.\n"
              "Witness numbers at n = 12 (windowed parity and "
              "multiplexer at k = 8, n = 16). μ = models, t = ANF "
              "terms, σ = Walsh support, d = dim span(support).\n"
              "The ℤ-lift shared kinds of the finite-frame "
              "conjecture (MTBDD, *BMD, WHDD) are unmeasured; Walsh "
              "is the one measured ℤ-lift frame (0028 §5).",
              ha="left", va="top", fontsize=7.6, color="#555555")

    figure.savefig(output_path, dpi=180, bbox_inches="tight",
                   facecolor="white")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    render(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "frame_flow_grid.png"))
