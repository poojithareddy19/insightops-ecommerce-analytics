"""
Draw the dbt lineage graph (raw sources -> staging -> marts) from dbt's manifest.json
and save it to dashboards/dbt_lineage.png.

Run `dbt docs generate` (or `dbt build`) from the dbt/ folder first.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = PROJECT_ROOT / "dbt" / "target" / "manifest.json"
OUTPUT_FILE = PROJECT_ROOT / "dashboards" / "dbt_lineage.png"

# One color per layer, from the project chart palette
LAYER_COLORS = {"source": "#9a9893", "staging": "#2a78d6", "marts": "#eb6834"}
SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
EDGE = "#c9c8c3"


def load_graph() -> tuple[dict, list]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    nodes, edges = {}, []
    for uid, source in manifest["sources"].items():
        nodes[uid] = ("raw." + source["name"], "source")
    for uid, node in manifest["nodes"].items():
        if node["resource_type"] != "model":
            continue
        layer = "marts" if "marts" in node["fqn"] else "staging"
        nodes[uid] = (node["name"], layer)
        for parent in node["depends_on"]["nodes"]:
            edges.append((parent, uid))
    return nodes, edges


uid_layers: dict = {}


def column_of(uid: str, edges: list, cache: dict) -> int:
    """Longest path from a source, so every model sits right of all its parents."""
    if uid not in cache:
        parents = [p for p, child in edges if child == uid]
        cache[uid] = 0 if not parents else 1 + max(column_of(p, edges, cache) for p in parents)
        if uid.startswith("model.") and "marts" in uid_layers.get(uid, ""):
            cache[uid] = max(cache[uid], 2)  # marts never sit left of staging
    return cache[uid]


def main() -> None:
    nodes, edges = load_graph()
    uid_layers.update({uid: layer for uid, (_, layer) in nodes.items()})
    cache: dict = {}
    columns: dict[int, list] = {}
    for uid in nodes:
        columns.setdefault(column_of(uid, edges, cache), []).append(uid)

    # Put each column in a stable order, then spread it vertically
    position = {}
    tallest = max(len(v) for v in columns.values())
    for col, uids in columns.items():
        uids.sort(key=lambda u: nodes[u][0])
        offset = (tallest - len(uids)) / 2
        for row, uid in enumerate(uids):
            position[uid] = (col * 3.2, -(row + offset))

    fig, ax = plt.subplots(figsize=(15, 7.5), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)

    # Draw the boxes first, then anchor each arrow to the box edges
    boxes = {}
    for uid, (x, y) in position.items():
        name, layer = nodes[uid]
        boxes[uid] = ax.text(x, y, name, ha="center", va="center", fontsize=9, color="white",
                             bbox=dict(boxstyle="round,pad=0.45", fc=LAYER_COLORS[layer], ec=SURFACE, lw=2))

    for parent, child in edges:
        ax.annotate("", xy=(0, 0.5), xycoords=boxes[child], xytext=(1, 0.5), textcoords=boxes[parent],
                    arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=1, shrinkA=6, shrinkB=6))

    for layer, color in LAYER_COLORS.items():
        ax.scatter([], [], s=90, color=color, marker="s", label=layer)
    ax.legend(loc="upper left", frameon=False, fontsize=10, labelcolor=TEXT, ncol=3,
              bbox_to_anchor=(0, 1.06))

    ax.set_title("dbt lineage: raw sources -> staging views -> mart tables",
                 loc="left", fontsize=13, color=TEXT, pad=28)
    ax.axis("off")
    xs = [p[0] for p in position.values()]
    ys = [p[1] for p in position.values()]
    ax.set_xlim(min(xs) - 1.6, max(xs) + 1.6)
    ax.set_ylim(min(ys) - 0.8, max(ys) + 0.8)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.03)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=150, facecolor=SURFACE)
    print("Saved", OUTPUT_FILE)


if __name__ == "__main__":
    main()
