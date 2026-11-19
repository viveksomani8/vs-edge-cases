"""Channel banner (2560x1440 PNG).

Name, mark and tagline sit inside the central area that YouTube shows on every
device (about 1546x423 px of the 2560x1440 image); the grid is decoration.

Render (from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim -s videos/channel/banner.py Banner
"""

from manim import *

config.pixel_width, config.pixel_height = 2560, 1440
config.frame_height = 8.0
config.frame_width = 8.0 * 2560 / 1440
config.background_color = "#101418"

NAME = "Edge Cases"
TAGLINE = "Python, algorithms and system design, explained visually"
PROSE = "Segoe UI"
CELL_FILL, EDGE_FILL = "#3A3F47", YELLOW

SAFE_W = 1546 / 2560 * config.frame_width   # ~8.6 units
SAFE_H = 423 / 1440 * config.frame_height   # ~2.35 units
GRID_STEP, GRID_SIDE = 0.9, 0.78


class Banner(Scene):
    def construct(self):
        self.add_grid()

        mark = VGroup()
        for k in range(4):
            edge = k == 3
            square = Square(side_length=0.5)
            square.set_fill(EDGE_FILL if edge else CELL_FILL, 1)
            square.set_stroke(EDGE_FILL if edge else WHITE, 3)
            mark.add(square)
        mark.arrange(RIGHT, buff=0.06)

        name = Text(NAME, font=PROSE, font_size=96, weight=BOLD)
        name.scale_to_fit_height(0.95)
        title = VGroup(mark, name).arrange(RIGHT, buff=0.45).move_to([0, 0.42, 0])

        tagline = Text(TAGLINE, font=PROSE, font_size=40, color=GREY_A)
        tagline.scale_to_fit_width(min(SAFE_W - 1.2, 7.4)).move_to([0, -0.62, 0])

        assert title.width < SAFE_W - 0.6 and title.get_top()[1] < SAFE_H / 2
        assert tagline.get_bottom()[1] > -SAFE_H / 2
        self.add(title, tagline)

    def add_grid(self):
        """Faint array cells everywhere except behind the text; the cell at the
        far right edge of the middle row is the highlighted one."""
        cols = int(config.frame_width / GRID_STEP) + 2
        rows = int(config.frame_height / GRID_STEP) + 2
        xs = [(c - (cols - 1) / 2) * GRID_STEP for c in range(cols)]
        ys = [(r - (rows - 1) / 2) * GRID_STEP for r in range(rows)]
        visible_xs = [x for x in xs if abs(x) + GRID_SIDE / 2 <= config.frame_width / 2]
        for y in ys:
            in_band = abs(y) < SAFE_H / 2          # the strip desktop viewers see
            for x in xs:
                if abs(x) < SAFE_W / 2 + 0.3 and abs(y) < SAFE_H / 2 + 0.3:
                    continue                        # keep the text area clear
                square = Square(side_length=GRID_SIDE).move_to([x, y, 0])
                if y == max(ys, key=lambda v: (-abs(v), v)) and x == max(visible_xs):
                    square.set_fill(EDGE_FILL, 1).set_stroke(EDGE_FILL, 3)
                elif in_band:
                    square.set_fill(CELL_FILL, 0.55).set_stroke(WHITE, 2, opacity=0.35)
                else:
                    square.set_fill(CELL_FILL, 0.18).set_stroke(WHITE, 2, opacity=0.10)
                self.add(square)
