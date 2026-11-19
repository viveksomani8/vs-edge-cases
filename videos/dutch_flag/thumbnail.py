"""YouTube thumbnail for the Dutch national flag video (1280x720 PNG).

Render (from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim -s -r 1280,720 videos/dutch_flag/thumbnail.py Thumbnail
"""

from manim import *

config.background_color = "#101418"

LESS, EQUAL, UNKNOWN, GREATER = "#C8102E", "#F2F2F2", "#3A3F47", "#2A5CAA"
PROSE, MONO = "Segoe UI", "Consolas"

# A mid-run state: two classified on each side, two still unknown.
CELLS = [(2, LESS), (1, LESS), (3, EQUAL), (3, EQUAL), (5, UNKNOWN), (2, UNKNOWN), (5, GREATER), (5, GREATER)]
POINTERS = [("smaller", 2, "#FF7B7B"), ("equal", 4, YELLOW), ("larger", 6, "#7FB2FF")]
STEP, SIDE, ROW_Y = 1.5, 1.38, 0.15


class Thumbnail(Scene):
    def construct(self):
        x0 = -(len(CELLS) - 1) * STEP / 2

        headline = Text("3 POINTERS. 1 PASS.", font=PROSE, font_size=96, weight=BOLD, color=YELLOW)
        headline.scale_to_fit_width(12.2).move_to([0, 2.75, 0])
        self.add(headline)

        for k, (value, fill) in enumerate(CELLS):
            square = Square(side_length=SIDE).set_fill(fill, 1).set_stroke(WHITE, 4)
            square.move_to([x0 + k * STEP, ROW_Y, 0])
            label = Text(str(value), font=PROSE, font_size=64, weight=BOLD)
            label.set_color(BLACK if fill == EQUAL else WHITE).move_to(square)
            self.add(square, label)

        for name, k, color in POINTERS:
            x = x0 + k * STEP
            arrow = Arrow(
                [x, ROW_Y - 1.75, 0], [x, ROW_Y - 0.8, 0], buff=0, color=color,
                stroke_width=10, max_tip_length_to_length_ratio=0.4,
            )
            label = Text(name, font=MONO, font_size=40, weight=BOLD, color=color)
            label.next_to(arrow, DOWN, buff=0.1)
            self.add(arrow, label)

        footer = Text("Dutch National Flag  |  Python", font=PROSE, font_size=40, color=GREY_A)
        footer.move_to([0, -3.45, 0])
        self.add(footer)
