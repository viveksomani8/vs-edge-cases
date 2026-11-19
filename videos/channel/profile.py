"""Channel profile picture (800x800 PNG): an array whose edge cell is highlighted.

Render (from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim -s videos/channel/profile.py Profile
"""

from manim import *

config.pixel_width, config.pixel_height = 800, 800
config.frame_height = 8.0
config.frame_width = 8.0
config.background_color = "#101418"

CELL_FILL, EDGE_FILL = "#3A3F47", YELLOW
CELLS, SIDE, STEP = 4, 1.3, 1.42  # kept well inside the circular crop


class Profile(Scene):
    def construct(self):
        x0 = -(CELLS - 1) * STEP / 2
        for k in range(CELLS):
            edge = k == CELLS - 1
            square = Square(side_length=SIDE)
            square.set_fill(EDGE_FILL if edge else CELL_FILL, 1)
            square.set_stroke(EDGE_FILL if edge else WHITE, 7)
            self.add(square.move_to([x0 + k * STEP, 0, 0]))
