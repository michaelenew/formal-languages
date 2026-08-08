"""Render the subclass x frame map as a PNG.

Rows are structured subclasses (with a representative statement and
its measured sizes from subclass_escapes.py); columns are the seven
named frames plus the two conjectured extension kinds (the GL(n,2)
parameter and the word-level moment lift). Green = home (small,
law-backed); red = escape (the family scales exponentially there);
dot = not measured. The right margin names each subclass's canonical
algorithm -- the classical algorithm family that IS that home's
canonicalisation.

Run this file directly; writes subclass_escape_map.png beside it.
"""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

FRAME_COLUMNS: list[str] = ["minterm", "ANF", "dual ANF", "Walsh",
                            "OBDD", "FDD", "negFDD", "GL-OBDD",
                            "*BMD"]
EXTENSION_COLUMN_COUNT: int = 2

HOME = "home"
ESCAPE = "escape"
UNMEASURED = "unmeasured"

CELL_COLORS = {HOME: "#b7e4c7", ESCAPE: "#f4b6ad",
               UNMEASURED: "#ececec"}


class SubclassRow:
    def __init__(self, label: str, witness: str, algorithm: str,
                 cells: dict[str, tuple[str, str]]) -> None:
        self.label = label
        self.witness = witness
        self.algorithm = algorithm
        self.cells = cells


def build_rows() -> list[SubclassRow]:
    dot = (UNMEASURED, "·")
    return [
        SubclassRow(
            "counting / symmetric", "majority, n = 12",
            "dynamic counting (DP)",
            {"minterm": (ESCAPE, "1586"), "ANF": (ESCAPE, "1287"),
             "dual ANF": (ESCAPE, "1420"), "Walsh": (ESCAPE, "4096"),
             "OBDD": (HOME, "55"), "FDD": (HOME, "59"),
             "negFDD": (HOME, "61"), "GL-OBDD": dot, "*BMD": dot}),
        SubclassRow(
            "sparse-model", "16 deals, n = 12",
            "enumerate / sweep",
            {"minterm": (HOME, "16"), "ANF": (ESCAPE, "1342"),
             "dual ANF": (ESCAPE, "806"), "Walsh": (ESCAPE, "3290"),
             "OBDD": (HOME, "106"), "FDD": (ESCAPE, "254"),
             "negFDD": (ESCAPE, "265"), "GL-OBDD": dot, "*BMD": dot}),
        SubclassRow(
            "parity-spread", "windowed parity, n = 16",
            "expand-and-cancel",
            {"minterm": (ESCAPE, "32640"), "ANF": (HOME, "8"),
             "dual ANF": (HOME, "24"), "Walsh": (ESCAPE, "65536"),
             "OBDD": (ESCAPE, "1021"), "FDD": (HOME, "95"),
             "negFDD": (HOME, "103"), "GL-OBDD": dot, "*BMD": dot}),
        SubclassRow(
            "selector / decision tree", "one-hot mux, n = 16",
            "branch and trace",
            {"minterm": (ESCAPE, "1024"), "ANF": (ESCAPE, "1024"),
             "dual ANF": (HOME, "24"), "Walsh": (ESCAPE, "2234"),
             "OBDD": (HOME, "95"), "FDD": (ESCAPE, "774"),
             "negFDD": (HOME, "103"), "GL-OBDD": dot, "*BMD": dot}),
        SubclassRow(
            "affine system", "8 parities, n = 16",
            "Gaussian elimination",
            {"minterm": (ESCAPE, "256"), "ANF": (ESCAPE, "12304"),
             "dual ANF": (ESCAPE, "3435"), "Walsh": (ESCAPE, "256"),
             "OBDD": (ESCAPE, "225"), "FDD": (ESCAPE, "314"),
             "negFDD": (ESCAPE, "510"), "GL-OBDD": (HOME, "33"),
             "*BMD": dot}),
        SubclassRow(
            "word arithmetic", "x·y middle bit, n = 14",
            "schoolbook arithmetic",
            {"minterm": dot, "ANF": (ESCAPE, "288"),
             "dual ANF": dot, "Walsh": dot,
             "OBDD": (ESCAPE, "634"), "FDD": (ESCAPE, "328"),
             "negFDD": (ESCAPE, "488"), "GL-OBDD": dot,
             "*BMD": (HOME, "40")}),
        SubclassRow(
            "median-closed (2-SAT)", "expander indep. sets, n = 16",
            "implication closure — poly, NO home",
            {"minterm": (ESCAPE, "1156"), "ANF": (ESCAPE, "10936"),
             "dual ANF": (ESCAPE, "439"), "Walsh": (ESCAPE, "60103"),
             "OBDD": (ESCAPE, "176"), "FDD": (ESCAPE, "589"),
             "negFDD": (ESCAPE, "265"), "GL-OBDD": (ESCAPE, "probes ✗"),
             "*BMD": (ESCAPE, "152↑")}),
        SubclassRow(
            "Horn (implications)", "bipartite implications, n = 16",
            "unit propagation — poly, NO home",
            {"minterm": (ESCAPE, "1230"), "ANF": (ESCAPE, "3357"),
             "dual ANF": (ESCAPE, "2773"), "Walsh": (ESCAPE, "58017"),
             "OBDD": (ESCAPE, "302"), "FDD": (ESCAPE, "1146"),
             "negFDD": (ESCAPE, "381"), "GL-OBDD": dot, "*BMD": dot}),
        SubclassRow(
            "generic", "random statement",
            "none — and not succinct",
            {name: (ESCAPE, "2^Ω(n)") for name in FRAME_COLUMNS})]


def render(output_path: str) -> None:
    rows = build_rows()
    cell_width, cell_height = 1.62, 0.94
    label_width, algorithm_width = 4.4, 4.2
    grid_width = len(FRAME_COLUMNS) * cell_width
    figure, axes = plt.subplots(
        figsize=(label_width + grid_width + algorithm_width + 0.6,
                 cell_height * len(rows) + 4.4))
    axes.set_xlim(-label_width, grid_width + algorithm_width)
    axes.set_ylim(-2.6, cell_height * len(rows) + 1.7)
    axes.axis("off")
    axes.set_aspect("equal")

    top = cell_height * len(rows)
    for column_index, name in enumerate(FRAME_COLUMNS):
        x = column_index * cell_width + cell_width / 2
        is_extension = column_index >= len(FRAME_COLUMNS) - \
            EXTENSION_COLUMN_COUNT
        axes.text(x, top + 0.30, name, ha="center", va="bottom",
                  fontsize=9.5, fontweight="bold",
                  color="#6b3fa0" if is_extension else "#222222")
        if is_extension:
            axes.text(x, top + 0.72, "conjectured\nextension kind",
                      ha="center", va="bottom", fontsize=6.4,
                      color="#6b3fa0")
    separator_x = (len(FRAME_COLUMNS) - EXTENSION_COLUMN_COUNT) * \
        cell_width
    axes.plot([separator_x, separator_x], [0, top], color="#6b3fa0",
              linewidth=2.2)

    for row_index, row in enumerate(rows):
        y = (len(rows) - 1 - row_index) * cell_height
        axes.text(-0.25, y + cell_height / 2 + 0.13, row.label,
                  ha="right", va="center", fontsize=10,
                  fontweight="bold")
        axes.text(-0.25, y + cell_height / 2 - 0.22, row.witness,
                  ha="right", va="center", fontsize=7.2,
                  color="#555555")
        for column_index, name in enumerate(FRAME_COLUMNS):
            verdict, text = row.cells[name]
            x = column_index * cell_width
            axes.add_patch(Rectangle((x, y), cell_width, cell_height,
                                     facecolor=CELL_COLORS[verdict],
                                     edgecolor="white",
                                     linewidth=1.1))
            axes.text(x + cell_width / 2, y + cell_height / 2, text,
                      ha="center", va="center", fontsize=8.2,
                      color="#222222")
        axes.text(grid_width + 0.35, y + cell_height / 2,
                  row.algorithm, ha="left", va="center", fontsize=8.8,
                  color="#1b4a6b", style="italic")
    axes.text(grid_width + 0.35, top + 0.30, "canonical algorithm",
              ha="left", va="bottom", fontsize=9.5,
              fontweight="bold", color="#1b4a6b")

    axes.set_title(
        "Subclass × frame map — homes (green), escapes (red), and "
        "each home's canonical algorithm",
        fontsize=13.5, pad=30)

    legend_top = -0.55
    for line_index, (verdict, meaning) in enumerate((
            (HOME, "home: small, law-backed polynomial for the "
                   "subclass"),
            (ESCAPE, "escape: the family scales exponentially in "
                     "this frame"),
            (UNMEASURED, "· not measured"))):
        y = legend_top - 0.32 * line_index
        axes.add_patch(Rectangle((0.0, y - 0.11), 0.4, 0.25,
                                 facecolor=CELL_COLORS[verdict],
                                 edgecolor="#888888", linewidth=0.7))
        axes.text(0.55, y, meaning, ha="left", va="center",
                  fontsize=8.2)
    axes.text(0.0, legend_top - 0.32 * 3 - 0.12,
              "Numbers from subclass_escapes.py (0030) and "
              "polymorphism_frames.py (0031) at the stated n; red "
              "cells are families with measured exponential growth "
              "or counting-bound scale.\n"
              "The affine and word-arithmetic rows escape every "
              "fixed frame and land exactly in the two conjectured "
              "extension kinds — the reason the extended parameters "
              "are mandatory.\n"
              "The median-closed and Horn rows are the DECISION-TASK "
              "FALSIFIERS (0031): polynomial-time deducible by "
              "formula-side closure, yet no frame home anywhere — "
              "portfolio optimality is false for decision, and the "
              "frame program re-scopes to deduction-with-counting "
              "(their counting task IS #P-complete, matching the "
              "blow-up).\n"
              "The generic row escapes everything by the counting "
              "bound but is not succinct: it cannot be posed as an "
              "input, so it witnesses nothing about hardness.",
              ha="left", va="top", fontsize=7.6, color="#555555")

    figure.savefig(output_path, dpi=180, bbox_inches="tight",
                   facecolor="white")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    render(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "subclass_escape_map.png"))
