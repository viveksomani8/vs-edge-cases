"""Vertical YouTube Short: Python's import is not #include or require.

Render, save one still per beat, add the narration and write the subtitles
(from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim --fps 30 videos/007_import_not_include/import_not_include.py ImportShort
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/007_import_not_include/stills.py \
        media/videos/import_not_include/1920p30/ImportShort.mp4 media/import_not_include_stills.json \
        videos/007_import_not_include/preview
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/007_import_not_include/mux.py \
        media/videos/import_not_include/1920p30/ImportShort.mp4 media/import_not_include_timeline.json \
        videos/007_import_not_include/import-is-not-include-short.mp4
    uv run python videos/007_import_not_include/subtitles.py \
        media/import_not_include_timeline.json videos/007_import_not_include/import-is-not-include-short.en.srt

Each beat is timed to its narration clip (audio/<name>.mp3, text in
narration.py), or to the word count of the text while the clip is not recorded.

The terminal panels show what Python 3.14.4 printed on this machine for a
three-file copy of src/epi/tree_node.py and src/epi/test_utils/utils.py (paths
and the traceback frames trimmed, long messages wrapped). The panel drawing and
the timing helpers come from videos/003_syntax_errors.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
# Inserted in this order so that this folder ends up first: its narration.py
# must win over the one in 003_syntax_errors.
sys.path.insert(0, str(HERE.parent / "001_dutch_flag"))
sys.path.insert(0, str(HERE.parent / "003_syntax_errors"))
sys.path.insert(0, str(HERE))

import av
from manim import *

from narration import NARRATION  # before syntax_errors, which imports the same module name
from syntax_errors import (
    BAD, GOOD, LEAD_IN, MONO, PANEL_FILL, PROSE, QUIET, TERMINAL_FILL, WORDS_PER_SECOND,
    Panel, SyntaxErrors,
)

config.pixel_width, config.pixel_height = 1080, 1920
config.frame_width, config.frame_height = 9.0, 16.0

AUDIO_DIR = HERE / "audio"

# Layout, top to bottom. YouTube draws its own controls over roughly the bottom
# fifth of a Short, so nothing sits below y = -4.8.
TITLE_Y, HEADER_Y, CAPTION = 6.3, 5.0, [0, -3.5, 0]

C_CODE = ['#include "tree_node.h"', "", "TreeNode root;"]
PHP_CODE = ["require 'tree_node.php';", "", "$root = new TreeNode(314);"]
PY_CODE = ["import tree_node", "", "root = TreeNode(314)"]

NAME_ERROR = [
    ("$ python level_order.py", GREY_B),
    ("    root = TreeNode(314)", GREY_A),
    ("NameError: name 'TreeNode' is not defined.", BAD),
    ("           Did you mean: 'tree_node'?", BAD),
]

THROUGH_MODULE = ["import tree_node", "", "root = tree_node.TreeNode(314)"]
ONE_NAME = ["from tree_node import TreeNode", "", "root = TreeNode(314)"]

# The first line is padded so the panel has room for the notes added later.
FOLDERS = [
    "project/".ljust(40),
    "  main.py",
    "  utils/",
    "    test_utils.py",
    "    tree_node.py",
]
NOTE_COLUMN = 19
NEIGHBOUR_IMPORT = "from tree_node import TreeNode"
PATH_IMPORT = "from utils.tree_node import TreeNode"
NOT_FOUND = [
    ("$ python main.py".ljust(32), GREY_B),
    ("ModuleNotFoundError:", BAD),
    ("    No module named 'tree_node'", BAD),
]
FOUND = [("$ python main.py".ljust(32), GREY_B), ("314", WHITE)]

# what was typed, where the caret sits, Python's message, the rename
BAD_NAMES = [
    ("import tree-node", 11, "SyntaxError: invalid syntax", "tree-node.py", "tree_node.py"),
    ("import 01_test_utils", 9, "SyntaxError: invalid decimal literal", "01_test_utils.py", "test_utils.py"),
]


class ImportShort(SyntaxErrors):
    def construct(self):
        self.caption = None
        self.clip = 0
        self.voice_start = self.voice_end = 0.0
        self.timeline, self.stills = [], []
        self.hook()
        self.one_name()
        self.two_ways()
        self.where_python_looks()
        self.file_names()
        self.rule()
        media = Path(config.media_dir)
        (media / "import_not_include_timeline.json").write_text(json.dumps(self.timeline))
        (media / "import_not_include_stills.json").write_text(json.dumps(self.stills))
        estimated = [name for name, *_ in self.timeline if not (AUDIO_DIR / f"{name}.mp3").exists()]
        if estimated:
            print(f"Preview timing: {len(estimated)} of {len(self.timeline)} clips are not recorded yet.")

    # ------------------------------------------------------------------ helpers
    def voice(self, name=None):
        """As in the syntax video, but with this Short's clips."""
        if name is None:
            self.clip += 1
            name = f"{self.clip:02d}"
        path = AUDIO_DIR / f"{name}.mp3"
        if path.exists():
            with av.open(str(path)) as container:
                seconds = float(container.duration) / av.time_base
        else:
            seconds = len(NARRATION[name].split()) / WORDS_PER_SECOND + 0.4
        self.voice_start = self.renderer.time
        self.voice_end = self.voice_start + seconds
        self.timeline.append([name, self.voice_start, self.voice_end])

    def say(self, text, pos=CAPTION, color=WHITE, width=8.2):
        new = Text(text, font=PROSE, font_size=34, color=color, line_spacing=0.7)
        if new.width > width:
            new.scale_to_fit_width(width)
        new.move_to(pos)
        anims = [FadeIn(new, shift=UP * 0.15)]
        if self.caption is not None:
            anims.append(FadeOut(self.caption))
        self.play(*anims, run_time=0.5)
        self.caption = new

    def clear(self, *mobjects):
        """Fade out a beat's pieces and its caption; the title stays."""
        gone = [m for m in (*mobjects, self.caption) if m is not None]
        self.play(*[FadeOut(m) for m in gone], run_time=0.5)
        self.caption = None

    def header(self, words, color):
        label = Text(words, font=PROSE, font_size=40, weight=BOLD, color=color)
        return label.move_to([0, HEADER_Y, 0])

    def mark(self, panel, k, color):
        """Animation that tints the background of line k of a panel."""
        return panel.rows[k][0].animate.set_fill(color, 0.22)

    # --------------------------------------------------------------------- hook
    def hook(self):
        self.title = Text("import is not #include", font=PROSE, font_size=44, weight=BOLD)
        self.title.move_to([0, TITLE_Y, 0])
        c = Panel(C_CODE, [0, 3.7, 0], 7.7, 2.0, font_size=30)
        php = Panel(PHP_CODE, [0, 0.9, 0], 7.7, 2.0, font_size=30)
        py = Panel(PY_CODE, [0, -1.9, 0], 7.7, 2.0, font_size=30)
        c_tab, php_tab, py_tab = c.tab("C: pastes the file in"), php.tab("PHP: pastes the file in"), py.tab("Python")

        self.play(FadeIn(self.title), run_time=0.5)
        self.wait(LEAD_IN - 0.5)
        self.voice("hook")
        self.play(FadeIn(c.all), FadeIn(c_tab), run_time=0.5)
        self.until(0.4)
        self.play(FadeIn(php.all), FadeIn(php_tab), run_time=0.5)
        self.until(0.7)
        self.play(FadeIn(py.all), FadeIn(py_tab), run_time=0.5)
        self.play(py.box.animate.set_stroke(BAD, 4), run_time=0.3)
        self.say("Python's import does not paste.", [0, -3.9, 0], color=YELLOW)
        self.hold(pad=0.3)
        self.clear(c.all, c_tab, php.all, php_tab, py.all, py_tab)

    # ----------------------------------------------------------------- one name
    def holder(self, label, name, x, color):
        """A labelled box holding one name."""
        box = RoundedRectangle(width=3.3, height=1.6, corner_radius=0.15)
        box.set_fill(PANEL_FILL, 1).set_stroke(color, 3).move_to([x, -1.85, 0])
        above = Text(label, font=PROSE, font_size=26, color=GREY_A).next_to(box, UP, buff=0.15)
        inside = Text(name, font=MONO, font_size=34, weight=BOLD, color=color).move_to(box)
        return VGroup(box, above, inside)

    def one_name(self):
        head = self.header("import gives you one name", BAD)
        code = Panel(PY_CODE, [0, 3.15, 0], 7.7, 2.0, font_size=32)
        tab = code.tab("level_order.py")
        term = Panel(NAME_ERROR, [0, 0.85, 0], 7.7, 2.2, fill=TERMINAL_FILL, font_size=26)
        yours = self.holder("names in your file", "tree_node", -2.4, QUIET)
        module = self.holder("inside the module", "TreeNode", 2.4, YELLOW)
        arrow = Arrow(yours[0].get_right(), module[0].get_left(), buff=0.08, color=QUIET, stroke_width=6)

        self.voice()
        self.play(FadeIn(head), FadeIn(code.all), FadeIn(tab), run_time=0.6)
        self.bring_to_front(code.rows)
        self.until(0.2)
        self.play(self.mark(code, 2, BAD), run_time=0.3)
        self.play(FadeIn(term.all), run_time=0.5)
        self.until(0.5)
        self.play(self.mark(code, 0, QUIET), FadeIn(yours, shift=UP * 0.15), run_time=0.5)
        self.until(0.75)
        self.play(GrowArrow(arrow), FadeIn(module, shift=UP * 0.15), run_time=0.5)
        self.say("One name arrives: the module.\nThe class stays inside it.", [0, -3.9, 0], color=YELLOW)
        self.hold(pad=0.3)
        self.clear(head, code.all, tab, term.all, yours, module, arrow)

    # ----------------------------------------------------------------- two ways
    def two_ways(self):
        head = self.header("Two ways to reach it", GOOD)
        dotted = Panel(THROUGH_MODULE, [0, 3.0, 0], 7.7, 2.0, font_size=30)
        named = Panel(ONE_NAME, [0, -0.2, 0], 7.7, 2.0, font_size=30)
        dotted_tab = dotted.tab("1. through the module, with a dot", GOOD)
        named_tab = named.tab("2. bring in the one name", GOOD)

        self.voice()
        self.play(FadeIn(head), FadeIn(dotted.all), FadeIn(dotted_tab), run_time=0.6)
        self.bring_to_front(dotted.rows)
        self.until(0.2)
        self.play(self.mark(dotted, 2, GOOD), run_time=0.4)
        self.until(0.5)
        self.play(FadeIn(named.all), FadeIn(named_tab), run_time=0.5)
        self.bring_to_front(named.rows)
        self.play(self.mark(named, 0, GOOD), run_time=0.4)
        self.say("Either way, you name what you want.\nNothing is pasted in.", [0, -2.9, 0])
        self.hold(pad=0.3)
        self.clear(head, dotted.all, dotted_tab, named.all, named_tab)

    # ------------------------------------------------------- where Python looks
    def note(self, tree, k, words, color):
        return tree.text(k, " " * NOTE_COLUMN + words, color)

    def where_python_looks(self):
        head = self.header("Where does Python look?", BAD)
        tree = Panel(FOLDERS, [0, 3.2, 0], 7.7, 2.8, font_size=28)
        code = Panel([PATH_IMPORT], [0, 0.55, 0], 7.7, 1.0, font_size=28)
        code.rows[0].submobjects[1] = code.text(0, NEIGHBOUR_IMPORT)
        tab = code.tab("utils/test_utils.py")
        failed = Panel(NOT_FOUND, [0, -1.45, 0], 7.7, 1.8, fill=TERMINAL_FILL, font_size=28)
        you_ran = self.note(tree, 1, "<- you ran this", YELLOW)
        asks = self.note(tree, 3, "<- asks", QUIET)
        neighbour = self.note(tree, 4, "<- is right here", QUIET)
        looks = self.note(tree, 0, "<- Python looks here", YELLOW)

        self.voice()
        self.play(FadeIn(head), FadeIn(tree.all), FadeIn(you_ran), run_time=0.6)
        self.bring_to_front(tree.rows, you_ran)
        self.until(0.1)
        self.play(FadeIn(code.all), FadeIn(tab), self.mark(tree, 3, QUIET), FadeIn(asks), run_time=0.5)
        self.until(0.25)
        self.play(self.mark(tree, 4, QUIET), FadeIn(neighbour), run_time=0.4)
        self.until(0.36)
        self.play(FadeIn(failed.all), run_time=0.5)
        self.until(0.5)
        self.say("#include looks next to the file that asks.", [0, -3.3, 0])
        self.until(0.74)
        self.play(
            self.mark(tree, 0, YELLOW), self.mark(tree, 1, YELLOW),
            tree.rows[3][0].animate.set_fill(BLACK, 0), tree.rows[4][0].animate.set_fill(BLACK, 0),
            FadeIn(looks), run_time=0.5,
        )
        self.say("Python looks in the folder\nof the script you ran.", [0, -3.5, 0], color=YELLOW)
        self.hold(pad=0.3)

        # The fix: the same import, spelled from the folder Python looks in.
        fixed = code.text(0, PATH_IMPORT, GOOD)
        found = Panel(FOUND, [0, -1.45, 0], 7.7, 1.8, fill=TERMINAL_FILL, font_size=28)
        self.voice()
        self.play(FadeOut(code.rows[0][1]), FadeIn(fixed), FadeOut(asks), FadeOut(neighbour), run_time=0.5)
        self.play(self.mark(code, 0, GOOD), run_time=0.3)
        self.until(0.5)
        self.play(FadeOut(failed.all), FadeIn(found.all), run_time=0.5)
        self.say("Spell the path from that folder.", [0, -3.3, 0], color=GOOD)
        self.hold(pad=0.3)
        self.clear(head, tree.all, you_ran, looks, code.box, code.rows[0][0], fixed, tab, found.all)

    # --------------------------------------------------------------- file names
    def bad_name(self, typed, caret, message, old, new, y):
        lines = [(typed.ljust(len(message)), WHITE), (" " * caret + "^", BAD), (message, BAD)]
        term = Panel(lines, [0, y, 0], 7.7, 2.0, fill=TERMINAL_FILL, font_size=28)
        was = Text(old, font=MONO, font_size=30, color=BAD)
        arrow = Text("->", font=MONO, font_size=30, color=GREY_A)
        now = Text(new, font=MONO, font_size=30, weight=BOLD, color=GOOD)
        rename = VGroup(was, arrow, now).arrange(RIGHT, buff=0.3).move_to([0, y - 1.5, 0])
        strike = Line(was.get_left(), was.get_right(), color=BAD, stroke_width=4)
        return term, VGroup(rename, strike)

    def file_names(self):
        head = self.header("A file name is a module name", YELLOW)
        first, first_fix = self.bad_name(*BAD_NAMES[0], 3.3)
        second, second_fix = self.bad_name(*BAD_NAMES[1], 0.0)

        self.voice()
        self.play(FadeIn(head), run_time=0.5)
        self.until(0.3)
        self.play(FadeIn(first.all), run_time=0.5)
        self.until(0.55)
        self.play(FadeIn(second.all), run_time=0.5)
        self.until(0.8)
        self.play(FadeIn(first_fix), FadeIn(second_fix), run_time=0.5)
        self.say("Letters, digits and underscores.\nNever a digit first.", [0, -3.4, 0], color=GOOD)
        self.hold(pad=0.3)
        self.clear(head, first.all, first_fix, second.all, second_fix)

    # --------------------------------------------------------------------- rule
    def point(self, number, words, example, y):
        box = RoundedRectangle(width=8.2, height=1.9, corner_radius=0.15)
        box.set_fill(PANEL_FILL, 1).set_stroke(YELLOW, 3).move_to([0, y, 0])
        badge = Text(str(number), font=PROSE, font_size=44, weight=BOLD, color=YELLOW)
        badge.move_to([-3.55, y + 0.3, 0])
        what = Text(words, font=PROSE, font_size=32, weight=BOLD)
        if what.width > 6.6:
            what.scale_to_fit_width(6.6)
        what.move_to([-2.95, y + 0.3, 0], aligned_edge=LEFT)
        like = Text(example, font=MONO, font_size=26, color=GREY_A).move_to([-2.95, y - 0.45, 0], aligned_edge=LEFT)
        return VGroup(box, badge, what, like)

    def rule(self):
        points = [
            self.point(1, "import gives you a module", "tree_node.TreeNode", 4.0),
            self.point(2, "Paths start from the script you ran", "from utils.tree_node import ...", 1.8),
            self.point(3, "Name files like variables", "test_utils.py", -0.4),
        ]
        footer = Text(
            "Python for Programmers Who Already Code", font=PROSE, font_size=26, color=GREY_A
        ).move_to([0, -3.6, 0])
        channel = Text("Edge Cases", font=PROSE, font_size=34, weight=BOLD, color=YELLOW)
        channel.move_to([0, -4.3, 0])

        self.voice()
        for point, start in zip(points, (0.08, 0.42, 0.72)):
            self.until(start)
            self.play(FadeIn(point, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(footer), FadeIn(channel), run_time=0.5)
        self.hold(pad=1.2)
