"""YouTube thumbnail for the syntax-mistakes video (1280x720 PNG).

Render (from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim -s -r 1280,720 videos/003_syntax_errors/thumbnail.py Thumbnail
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from manim import *

from syntax_errors import BAD, PROSE, TERMINAL_FILL, Panel

config.background_color = "#101418"


class Thumbnail(Scene):
    def construct(self):
        headline = Text("5 BUGS. 1 ERROR.", font=PROSE, font_size=96, weight=BOLD, color=YELLOW)
        headline.scale_to_fit_width(11.6).move_to([0, 2.6, 0])
        self.add(headline)

        # The one error Python reports for the file in the video.
        term = Panel(
            [
                ("$ python min_stack.py", GREY_B),
                ("    if self.top <= -1", WHITE),
                ("                     ^", BAD),
                ("SyntaxError: expected ':'", BAD),
            ],
            [0, -0.35, 0], 11.0, 3.2, fill=TERMINAL_FILL, font_size=60,
        )
        term.box.set_stroke(GREY_B, 3)
        self.add(term.all)

        footer = Text("Python traps for C, C++, Java, PHP devs", font=PROSE, font_size=40, color=GREY_A)
        footer.move_to([0, -3.45, 0])
        self.add(footer)
