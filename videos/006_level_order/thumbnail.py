"""YouTube thumbnail for the level order traversal video (1280x720 PNG).

Render (from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim -s -r 1280,720 videos/006_level_order/thumbnail.py Thumbnail
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from manim import *

from level_order_scene import LEVEL_FILL, PROSE, Board
from level_order import example_tree

config.background_color = "#101418"


class Thumbnail(Scene):
    def construct(self):
        headline = Text("LEVEL BY LEVEL.", font=PROSE, font_size=96, weight=BOLD, color=YELLOW)
        headline.scale_to_fit_width(10.6).move_to([0, 2.75, 0])
        self.add(headline)

        # The example tree, every node filled with the colour of its level.
        board = Board(example_tree(), origin=(0.0, 1.35), sx=1.55, sy=1.25, radius=0.5)
        for value, node in board.nodes.items():
            node[0].set_fill(LEVEL_FILL[board.depth[value]], 1).set_stroke(WHITE, 5)
            node[1].scale(1.5)
        board.lines.set_stroke(WHITE, 6)
        self.add(board.tree)

        footer = Text("Level Order Traversal  |  Python", font=PROSE, font_size=40, color=GREY_A)
        footer.move_to([0, -3.45, 0])
        self.add(footer)
