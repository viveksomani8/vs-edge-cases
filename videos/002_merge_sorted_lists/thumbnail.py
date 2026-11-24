"""YouTube thumbnail for the merge-sorted-lists video (1280x720 PNG).

Render (from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim -s -r 1280,720 videos/002_merge_sorted_lists/thumbnail.py Thumbnail
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from manim import *

from merge_lists import PROSE, Lists

config.background_color = "#101418"


class Thumbnail(Scene):
    def construct(self):
        headline = Text("0 NEW NODES.", font=PROSE, font_size=96, weight=BOLD, color=YELLOW)
        headline.scale_to_fit_width(10.4).move_to([0, 2.7, 0])
        self.add(headline)

        # The finished merge: two rows of nodes joined into one chain.
        lists = Lists(x0=-5.9, step=2.25, y_a=0.85, y_b=-1.45, radius=0.62, font_size=54)
        order = lists.order
        last = (order[-1][0], len(lists.values[order[-1][0]]))
        for key in order:
            lists.nodes[key][0].set_fill(lists.fills[key[0]], 1).set_stroke(width=5)
        for src, dst in zip(order, order[1:] + [last]):
            lists.links[src] = lists.arrow(src, dst, merged=True).set_stroke(width=9)
        self.add(*lists.links.values(), *lists.nodes.values(), lists.nones[last[0]])

        footer = Text("Merge Two Sorted Lists  |  Python", font=PROSE, font_size=40, color=GREY_A)
        footer.move_to([0, -3.45, 0])
        self.add(footer)
