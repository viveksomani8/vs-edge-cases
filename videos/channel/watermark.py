"""Video watermark (150x150 PNG, transparent background): the channel mark,
sized to fill the square so it stays legible in the corner of a video.

Render (from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim -s -t videos/channel/watermark.py Watermark
"""

from manim import *

config.pixel_width, config.pixel_height = 150, 150
config.frame_height = 8.0
config.frame_width = 8.0
config.background_opacity = 0.0

CELL_FILL, EDGE_FILL = "#3A3F47", YELLOW
CELLS, SIDE, STEP = 4, 1.68, 1.9


class Watermark(Scene):
    def construct(self):
        x0 = -(CELLS - 1) * STEP / 2
        for k in range(CELLS):
            edge = k == CELLS - 1
            square = Square(side_length=SIDE)
            square.set_fill(EDGE_FILL if edge else CELL_FILL, 1)
            square.set_stroke(EDGE_FILL if edge else WHITE, 10)
            self.add(square.move_to([x0 + k * STEP, 0, 0]))
