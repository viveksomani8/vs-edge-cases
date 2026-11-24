"""Syntax mistakes when switching to Python: "Python won't tell you".

Render the silent preview and save one still per beat (from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim -qm --fps 30 videos/003_syntax_errors/syntax_errors.py SyntaxErrors
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/003_syntax_errors/stills.py \
        media/videos/syntax_errors/720p30/SyntaxErrors.mp4 media/syntax_errors_stills.json \
        videos/003_syntax_errors/preview

Narration: the render is silent. Each beat is timed to the length of its clip
(audio/<name>.mp3, text in narration.py); a clip that has not been recorded is
timed from its word count, so the scene can be previewed before any audio
exists. The clip start times are written to media/syntax_errors_timeline.json.

The story in part 2 is real: it is the first version of
src/epi/08-01-min-stack.py, fixed one mistake at a time, and every terminal
panel shows what Python printed for that version (paths and the "~~^^" marker
lines trimmed, long messages wrapped). The caption, fonts and end card come from
videos/001_dutch_flag/scene.py.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "001_dutch_flag"))

import av
from manim import *

from narration import NARRATION
from scene import MONO, PROSE, DutchFlag

config.background_color = "#101418"

AUDIO_DIR = HERE / "audio"
WORDS_PER_SECOND = 2.5
LEAD_IN = 1.0

BAD, GOOD, QUIET = "#FF7B7B", "#7CE38B", "#7FB2FF"
PANEL_FILL, TERMINAL_FILL = "#1A2028", "#0B0E11"

# The first version of src/epi/08-01-min-stack.py, blank lines removed.
STACK_FILE = [
    "class EmptyStack:",
    "    pass",
    "class Stack:",
    "    def __init__( self ):",
    "        self.values = []",
    "        self.top = -1",
    "    def push( self, value ):",
    "        self.top += 1",
    "        self.values[ self.top ] = value",
    "    def pop( self ):",
    "        if self.top <= -1",
    "            raise EmptyStack",
    "        value = self.values[ self.top]",
    "        self.top -= 1",
    "        return value",
    'if __name__ == "main":',
    "    stack = Stack()",
    "    stack.push( 20 )",
    "    stack.push( 30 )",
    "    try:",
    "        print( stack.pop() )",
    "        print( stack.pop() )",
    "    except EmptyStack as e:",
    "        print( a )",
]
R_CLASS, R_ASSIGN, R_IF, R_MAIN, R_EXCEPT, R_PRINT_A = 0, 8, 10, 15, 22, 23
MISTAKE_ROWS = [R_CLASS, R_ASSIGN, R_IF, R_MAIN, R_PRINT_A]

RUN = ("$ python min_stack.py", GREY_B)
TRACEBACK = [
    RUN,
    ('  File "min_stack.py", line 14', GREY_A),
    ("    if self.top <= -1", GREY_A),
    ("                     ^", BAD),
    ("SyntaxError: expected ':'", BAD),
]
SILENT_RUN = [RUN, ("$", GREY_B)]
INDEX_ERROR = [
    RUN,
    ('  File "min_stack.py", line 11, in push', GREY_A),
    ("    self.values[ self.top ] = value", GREY_A),
    ("IndexError: list assignment index", BAD),
    ("            out of range", BAD),
]
WORKS = [RUN, ("30", WHITE), ("20", WHITE)]
TYPE_ERROR = [
    RUN,
    ("30", WHITE),
    ("20", WHITE),
    ('  File "min_stack.py", line 15, in pop', GREY_A),
    ("    raise EmptyStack", GREY_A),
    ("TypeError: exceptions must derive", BAD),
    ("           from BaseException", BAD),
]
NAME_ERROR = [
    RUN,
    ("30", WHITE),
    ("20", WHITE),
    ('  File "min_stack.py", line 31, in <module>', GREY_A),
    ("    print( a )", GREY_A),
    ("NameError: name 'a' is not defined", BAD),
]

C_BLOCK = ["if (top <= -1) {", "    throw EmptyStack();", "}"]
PY_BLOCK = ["if self.top <= -1", "    raise EmptyStack"]

# habit, Python, what Python says to the habit
FIRST_DAY = [
    ("x > 0 && y > 0", "x > 0 and y > 0", "SyntaxError"),
    ("i++", "i += 1", "SyntaxError"),
    ("else if x == 0:", "elif x == 0:", "SyntaxError"),
    ("for (i = 0; i < n; i++)", "for i in range(n):", "SyntaxError"),
    ("result = null", "result = None", "NameError"),
]
WHEN_IT_RUNS = [
    ("flag = true", "flag = True", "NameError"),
    ("items.length()", "len(items)", "AttributeError"),
    ('"Age: " + age', 'f"Age: {age}"', "TypeError"),
    ("def size():", "def size(self):", "TypeError"),
    ("a[len(a) / 2]", "a[len(a) // 2]", "TypeError"),
]


class Panel:
    """A panel of monospaced lines: code, or a terminal.

    `lines` holds strings or (string, colour) pairs. rows[k] is
    VGroup(background, text) for line k; an empty line keeps its slot.
    """

    def __init__(self, lines, center, max_width, max_height, fill=PANEL_FILL, font_size=24):
        lines = [(line, GREY_A) if isinstance(line, str) else line for line in lines]
        self.font_size = font_size
        self.char_w = Text("M" * 20, font=MONO, font_size=font_size).width / 20
        line_h = 0.38 * font_size / 24
        cols = max(len(line) for line, _ in lines) + 1

        self.rows = VGroup()
        for k, (line, color) in enumerate(lines):
            row = Rectangle(width=cols * self.char_w, height=line_h)
            row.set_stroke(width=0).set_fill(BLACK, 0).move_to([0, -k * line_h, 0])
            self.rows.add(VGroup(row, VGroup()))
        self.scale = 1.0
        for limit, size in ((max_width, self.rows.width), (max_height, self.rows.height)):
            if size * self.scale > limit:
                self.scale = limit / size
        self.rows.scale(self.scale).move_to(center)
        for k, (line, color) in enumerate(lines):
            if line.strip():
                self.rows[k].submobjects[1] = self.text(k, line, color)

        self.box = Rectangle(width=self.rows.width + 0.4, height=self.rows.height + 0.4)
        self.box.set_fill(fill, 1).set_stroke(GREY_D, 1.5).move_to(self.rows)
        self.all = VGroup(self.box, self.rows)

    def text(self, k, line, color=GREY_A):
        """The text of `line`, sized and placed for slot k."""
        indent = len(line) - len(line.lstrip())
        txt = Text(line.strip(), font=MONO, font_size=self.font_size, color=color).scale(self.scale)
        left = self.rows[k][0].get_left() + RIGHT * (indent + 0.6) * self.char_w * self.scale
        return txt.move_to(left, aligned_edge=LEFT)

    def tab(self, words, color=GREY_A):
        """A small label sitting on the top-left corner of the panel."""
        label = Text(words, font=PROSE, font_size=22, color=color, weight=BOLD)
        return label.next_to(self.box, UP, buff=0.12).align_to(self.box, LEFT)


class SyntaxErrors(DutchFlag):
    def construct(self):
        self.caption = None
        self.clip = 0
        self.voice_start = self.voice_end = 0.0
        self.timeline, self.stills = [], []
        self.hook()
        self.three_kinds()
        self.missing_colon()
        self.indentation()
        self.first_day()
        self.fix_the_file()
        self.when_it_runs()
        self.says_nothing()
        self.myths()
        self.pattern()
        self.habits()
        self.end_card()
        media = Path(config.media_dir)
        (media / "syntax_errors_timeline.json").write_text(json.dumps(self.timeline))
        (media / "syntax_errors_stills.json").write_text(json.dumps(self.stills))
        estimated = [name for name, *_ in self.timeline if not (AUDIO_DIR / f"{name}.mp3").exists()]
        if estimated:
            print(f"Preview timing: {len(estimated)} of {len(self.timeline)} clips are not recorded yet.")

    # ------------------------------------------------------------------ helpers
    def voice(self, name=None):
        """Schedule a narration clip at the current time: the next numbered clip,
        or a named one such as "hook"."""
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

    def until(self, fraction):
        """Wait until a fraction of the current clip has been spoken."""
        target = self.voice_start + fraction * (self.voice_end - self.voice_start)
        if target - self.renderer.time > 0.05:
            self.wait(target - self.renderer.time)

    def hold(self, silent=None, pad=0.5):
        """Wait until `pad` seconds after the current clip ends."""
        remaining = self.voice_end - self.renderer.time + pad
        if remaining > 0.05:
            self.wait(remaining)
        self.stills.append([self.timeline[-1][0], self.renderer.time - 0.1])

    def lead(self, seconds):
        self.wait(seconds)

    def wipe(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.caption = None

    def section(self, number, words, color):
        """The label in the top-left corner that says which kind we are in."""
        badge = Circle(radius=0.26).set_fill(color, 1).set_stroke(width=0)
        digit = Text(str(number), font=PROSE, font_size=24, weight=BOLD, color=BLACK).move_to(badge)
        label = Text(words, font=PROSE, font_size=30, weight=BOLD, color=color)
        label.next_to(badge, RIGHT, buff=0.25)
        return VGroup(badge, digit, label).move_to([-6.5, 3.45, 0], aligned_edge=LEFT)

    def table(self, entries, cues):
        """Three columns: what you type, what Python wants, what Python says."""
        heads = VGroup(
            Text("Your hands type", font=PROSE, font_size=24, weight=BOLD, color=BAD).move_to([-3.9, 2.45, 0]),
            Text("Python wants", font=PROSE, font_size=24, weight=BOLD, color=GOOD).move_to([1.5, 2.45, 0]),
            Text("Python says", font=PROSE, font_size=24, weight=BOLD, color=GREY_A).move_to([5.2, 2.45, 0]),
        )
        self.play(FadeIn(heads), run_time=0.5)
        for k, ((habit, python, says), at) in enumerate(zip(entries, cues)):
            y = 1.5 - k * 0.95
            strip = RoundedRectangle(width=13.2, height=0.75, corner_radius=0.1)
            strip.set_fill(PANEL_FILL, 1).set_stroke(GREY_D, 1).move_to([0, y, 0])
            left = Text(habit, font=MONO, font_size=26, color=BAD).move_to([-3.9, y, 0])
            arrow = Arrow([-1.3, y, 0], [-0.6, y, 0], buff=0, color=GREY_B, stroke_width=4, tip_length=0.18)
            right = Text(python, font=MONO, font_size=26, color=GOOD).move_to([1.5, y, 0])
            kind = BAD if says == "SyntaxError" else YELLOW  # yellow: the second kind
            tag = Text(says, font=MONO, font_size=20, color=kind).move_to([5.2, y, 0])
            self.until(at)
            self.play(FadeIn(VGroup(strip, left, arrow, right, tag), shift=UP * 0.15), run_time=0.5)

    def case(self, code, output, captions, show_output=0.3, output_tab="output"):
        """One small program on the left, what Python prints on the right.

        `captions` is a list of (fraction of the clip, text, colour). Starts a
        new clip and clears its own panels; the section header stays.
        """
        left = Panel(code, [-3.5, 0.9, 0], 6.0, 3.0, font_size=30)
        right = Panel(output, [3.6, 0.9, 0], 6.0, 3.0, fill=TERMINAL_FILL, font_size=30)
        right.all.align_to(left.box, UP)
        left_tab, right_tab = left.tab("Python"), right.tab(output_tab)

        self.voice()
        self.play(FadeIn(left.all), FadeIn(left_tab), run_time=0.6)
        self.until(show_output)
        self.play(FadeIn(right.all), FadeIn(right_tab), run_time=0.6)
        for at, text, color in captions:
            self.until(at)
            self.say(text, [0, -1.9, 0], color=color, width=11)
        self.hold()
        self.play(
            *[FadeOut(m) for m in (left.all, left_tab, right.all, right_tab, self.caption)], run_time=0.5
        )
        self.caption = None

    # --------------------------------------------------------------------- hook
    def hook(self):
        """Cold open: five marked lines in one file, one error in the terminal."""
        file = Panel(STACK_FILE, [-3.5, -0.25, 0], 6.2, 6.5)
        name = file.tab("min_stack.py")
        dots = {
            k: Dot(radius=0.07, color=BAD).next_to(file.rows[k][0], LEFT, buff=0.02)
            for k in MISTAKE_ROWS
        }
        claim = Text("Five mistakes.", font=PROSE, font_size=44, weight=BOLD).move_to([3.5, 2.6, 0])
        term = Panel(TRACEBACK, [3.5, 0.2, 0], 6.0, 2.6, fill=TERMINAL_FILL)
        catch = Text("Python reports one.", font=PROSE, font_size=36, weight=BOLD, color=YELLOW)
        catch.move_to([3.5, -2.2, 0])

        self.play(FadeIn(file.all), FadeIn(name), run_time=0.6)
        self.wait(LEAD_IN - 0.6)
        self.voice("hook")
        self.play(
            LaggedStart(*[FadeIn(dots[k], scale=2.5) for k in MISTAKE_ROWS], lag_ratio=0.35),
            FadeIn(claim, shift=UP * 0.15),
            run_time=1.8,
        )
        self.until(0.45)
        self.play(FadeIn(term.box), FadeIn(term.rows, lag_ratio=0.15), run_time=1.0)
        others = [dots[k] for k in MISTAKE_ROWS if k != R_IF]
        self.play(
            *[dot.animate.set_opacity(0.25) for dot in others],
            file.rows[R_IF][0].animate.set_fill(BAD, 0.3),
            FadeIn(catch, shift=UP * 0.15),
            run_time=0.7,
        )
        self.hold(pad=0.8)
        self.wipe()

    # -------------------------------------------------------------- three kinds
    def chip(self, number, words, detail, color, x, y=-1.5):
        box = RoundedRectangle(width=4.1, height=2.3, corner_radius=0.15)
        box.set_fill(PANEL_FILL, 1).set_stroke(color, 3).move_to([x, y, 0])
        digit = Text(str(number), font=PROSE, font_size=44, weight=BOLD, color=color)
        digit.move_to(box.get_top() + DOWN * 0.5)
        head = Text(words, font=PROSE, font_size=26, weight=BOLD)
        if head.width > 3.6:
            head.scale_to_fit_width(3.6)
        head.move_to(box.get_center() + DOWN * 0.1)
        note = Text(detail, font=MONO, font_size=18, color=GREY_B).move_to(box.get_bottom() + UP * 0.4)
        return VGroup(box, digit, head, note)

    def chips(self, y=-1.5):
        return [
            self.chip(1, "Refuses to start", "SyntaxError", BAD, -4.5, y),
            self.chip(2, "Fails when the line runs", "NameError, TypeError", YELLOW, 0, y),
            self.chip(3, "Says nothing", "no error at all", QUIET, 4.5, y),
        ]

    def three_kinds(self):
        title = Text("Python Won't Tell You", font=PROSE, font_size=60, weight=BOLD).move_to([0, 2.5, 0])
        sub = Text(
            "Syntax habits from C, C++, Java and PHP, sorted by when you find out",
            font=PROSE, font_size=26, color=GREY_A,
        ).move_to([0, 1.5, 0])

        self.voice()
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.6)
        self.hold()

        self.voice()
        for chip, at in zip(self.chips(), (0.3, 0.52, 0.76)):
            self.until(at)
            self.play(FadeIn(chip, shift=UP * 0.2), run_time=0.6)
        self.hold()
        self.wipe()

    # ------------------------------------------------------- 1: refuses to start
    def missing_colon(self):
        header = self.section(1, "Python refuses to start", BAD)
        c = Panel(C_BLOCK, [-3.6, 1.2, 0], 5.6, 2.0, font_size=30)
        py = Panel(PY_BLOCK, [3.6, 1.2, 0], 5.6, 2.0, font_size=30)
        py.all.align_to(c.box, UP)
        c_tab, py_tab = c.tab("C, C++, PHP"), py.tab("Python")
        term = Panel(TRACEBACK[1:], [3.6, -1.6, 0], 5.6, 2.0, fill=TERMINAL_FILL)
        colon = py.text(0, PY_BLOCK[0] + ":")[-1].set_color(GOOD)

        self.voice()
        self.play(FadeIn(header, shift=RIGHT * 0.2), run_time=0.6)
        self.until(0.14)
        self.play(FadeIn(c.all), FadeIn(c_tab), run_time=0.6)
        self.say("Parentheses and braces mark the block.", [-3.6, -0.6, 0])
        self.until(0.42)
        self.play(FadeIn(py.all), FadeIn(py_tab), run_time=0.6)
        self.until(0.62)
        self.play(FadeIn(term.box), FadeIn(term.rows, lag_ratio=0.15), run_time=0.8)
        self.say("No colon: nothing in the file runs.\nNot even line 1.", [-3.6, -1.6, 0], color=YELLOW)
        self.until(0.86)
        self.play(
            FadeIn(colon, scale=3), Flash(colon, color=GOOD, flash_radius=0.4),
            term.all.animate.set_opacity(0.25),
            run_time=0.7,
        )
        self.hold()
        self.play(
            *[FadeOut(m) for m in (c.all, c_tab, py.all, py_tab, term.all, colon, self.caption)],
            run_time=0.6,
        )
        self.caption = None

    def indentation(self):
        self.case(
            ["for x in items:", "    total += x", "  print(total)"],
            [("IndentationError:", BAD), ("unindent does not match any", BAD), ("outer indentation level", BAD)],
            [
                (0.32, "No braces: the indentation is the block.", WHITE),
                (0.6, "A line that does not line up, or a tab mixed\nwith spaces (TabError): the file will not start.", YELLOW),
            ],
            show_output=0.45,
            output_tab="Python says",
        )

    def first_day(self):
        """The first-day habits; the last row is the bridge to the second kind."""
        self.voice()
        self.table(FIRST_DAY, (0.1, 0.18, 0.26, 0.33, 0.44))
        self.hold(pad=0.8)
        self.wipe()

    # ------------------------------------------------ 2: fails when the line runs
    def terminal(self, lines):
        new = Panel(lines, [3.6, 1.2, 0], 6.2, 3.0, fill=TERMINAL_FILL, font_size=22)
        anims = [FadeIn(new.all)]
        if self.term is not None:
            anims.append(FadeOut(self.term.all))
        self.play(*anims, run_time=0.6)
        self.term = new

    def note(self, text, color=WHITE):
        self.say(text, [3.6, -2.0, 0], color=color, width=6.2)

    def mark(self, *slots, color=BAD):
        self.play(*[self.file.rows[k][0].animate.set_fill(color, 0.3) for k in slots], run_time=0.5)
        self.hot.update(slots)

    def rewrite(self, slot, line):
        """Replace the text in a slot with the corrected line, shown in green."""
        self.play(
            Transform(self.code[slot], self.file.text(slot, line, GOOD)),
            self.file.rows[slot][0].animate.set_fill(GOOD, 0.2),
            run_time=0.7,
        )
        self.hot.add(slot)

    def settle(self, keep=()):
        """Return the marked lines to normal, except those still to be fixed."""
        slots = [k for k in self.hot if k not in keep]
        if slots:
            self.play(
                *[self.file.rows[k][0].animate.set_fill(BLACK, 0) for k in slots],
                *[self.code[k].animate.set_color(GREY_A) for k in slots],
                run_time=0.4,
            )
        self.hot = set(keep)

    def fix_the_file(self):
        """The stack file again, fixed one mistake at a time, each run for real."""
        header = self.section(2, "It fails when the line runs", YELLOW)
        # One spare slot at the bottom: a third pop is added later.
        self.file = Panel(STACK_FILE + [""], [-3.5, -0.45, 0], 6.2, 6.1)
        self.code = {k: self.file.rows[k][1] for k in range(len(STACK_FILE))}
        self.term, self.hot = None, set()
        line = self.file.rows[2].get_center() - self.file.rows[1].get_center()  # one row down

        # Colon fixed: the file starts, and prints nothing.
        self.voice()
        self.play(FadeIn(header, shift=RIGHT * 0.2), FadeIn(self.file.all), run_time=0.7)
        self.until(0.1)
        self.rewrite(R_IF, STACK_FILE[R_IF] + ":")
        self.until(0.22)
        self.terminal(SILENT_RUN)
        self.note("No error. No output.\nNothing ran.", QUIET)
        self.until(0.72)
        self.settle()
        self.mark(R_MAIN, color=QUIET)
        self.rewrite(R_MAIN, 'if __name__ == "__main__":')
        self.hold()
        self.settle()

        # Index assignment on an empty list.
        self.voice()
        self.terminal(INDEX_ERROR)
        self.mark(R_ASSIGN)
        self.until(0.3)
        self.note("C: write into an array by index.\nPHP: the index creates the slot.\nPython: a list never grows that way.")
        self.until(0.85)
        self.rewrite(R_ASSIGN, "        self.values.append( value )")
        self.hold()
        self.settle()

        # It works, with two mistakes still inside.
        self.voice()
        self.terminal(WORKS)
        self.note("It works.", GOOD)
        self.until(0.3)
        self.mark(R_CLASS, R_PRINT_A)
        self.note("Two mistakes are still here,\nin lines that have not run yet.", YELLOW)
        self.until(0.62)
        self.note("A C compiler checks every line.\nPython checks a line when it runs it.")
        self.hold()

        # A third pop makes the raise run.
        self.voice()
        self.until(0.08)
        third = self.file.text(R_EXCEPT, "        print( stack.pop() )", GOOD)
        self.play(
            self.code[R_EXCEPT].animate.shift(line),
            self.code[R_PRINT_A].animate.shift(line),
            self.file.rows[R_PRINT_A][0].animate.set_fill(BLACK, 0),
            self.file.rows[R_PRINT_A + 1][0].animate.set_fill(BAD, 0.3),
            FadeIn(third),
            run_time=0.7,
        )
        last = R_PRINT_A + 1  # where `print( a )` sits now
        self.code[last], self.code[R_PRINT_A] = self.code[R_PRINT_A], self.code[R_EXCEPT]
        self.code[R_EXCEPT] = third
        self.hot = {R_CLASS, R_EXCEPT, last}
        self.until(0.28)
        self.terminal(TYPE_ERROR)
        self.until(0.58)
        self.note("C++ can throw anything.\nPython: inherit from Exception.")
        self.until(0.8)
        self.rewrite(R_CLASS, "class EmptyStack( Exception ):")
        self.hold()
        self.settle(keep=[last])

        # The except branch runs for the first time.
        self.voice()
        self.terminal(NAME_ERROR)
        self.note("The except branch runs\nfor the first time.")
        self.until(0.7)
        self.rewrite(last, "        print( e )")
        self.terminal(WORKS)
        self.note("Clean.", GOOD)
        self.hold()
        self.wipe()

    def when_it_runs(self):
        header = self.section(2, "It fails when the line runs", YELLOW)
        self.voice()
        self.play(FadeIn(header), run_time=0.4)
        self.table(WHEN_IT_RUNS, (0.08, 0.15, 0.24, 0.33, 0.42))
        self.until(0.78)
        self.say("Rule: make every branch run at least once.", [0, -3.3, 0], color=YELLOW, width=11)
        self.hold(pad=0.8)
        self.wipe()

    # ------------------------------------------------------------ 3: says nothing
    def says_nothing(self):
        header = self.section(3, "It says nothing", QUIET)
        self.play(FadeIn(header, shift=RIGHT * 0.2), run_time=0.6)
        self.case(
            ['if __name__ == "main":', "    run_tests()"],
            SILENT_RUN,
            [(0.42, 'The name is "__main__", so the condition is false.\nNo complaint. The program does nothing.', WHITE)],
            output_tab="terminal",
        )
        self.case(
            ["i = 5", "++i", "print(i)"],
            [("5", WHITE)],
            [
                (0.2, "++i is +(+i): a plus sign, applied twice.", WHITE),
                (0.62, "No error, no change. Write i += 1.", YELLOW),
            ],
            show_output=0.45,
        )
        self.case(
            ["print(list(range(1, 5)))", "print(5 / 2)", "print(5 // 2)"],
            [("[1, 2, 3, 4]", WHITE), ("2.5", WHITE), ("2", WHITE)],
            [
                (0.25, "The end of a range is never included.", WHITE),
                (0.55, "/ gives a float. // is integer division.", WHITE),
            ],
            show_output=0.12,
        )
        self.case(
            ["a = [1, 2]", "b = a", "b.append(3)", "print(a)"],
            [("[1, 2, 3]", WHITE)],
            [
                (0.12, "PHP arrays and C++ vectors copy on assignment.", WHITE),
                (0.58, "Python: two names, one list.\nTo copy, write b = a.copy().", YELLOW),
            ],
            show_output=0.5,
        )
        self.case(
            ["def add(x, items=[]):", "    items.append(x)", "    return items", "print(add(1))", "print(add(2))"],
            [("[1]", WHITE), ("[1, 2]", WHITE)],
            [(0.45, "The default list is created once and shared\nby every call. Use items=None instead.", YELLOW)],
            show_output=0.4,
        )
        self.wipe()

    # ------------------------------------------------------------------ wrap-up
    def myths(self):
        title = Text("Not mistakes", font=PROSE, font_size=34, weight=BOLD, color=GOOD)
        title.move_to([-6.5, 3.45, 0], aligned_edge=LEFT)
        rows = []
        for code, y in (("x = 10;", 1.3), ("if (x > 10):", 0.1)):
            strip = RoundedRectangle(width=10.5, height=0.9, corner_radius=0.1)
            strip.set_fill(PANEL_FILL, 1).set_stroke(GREY_D, 1).move_to([0, y, 0])
            left = Text(code, font=MONO, font_size=30).move_to([-2.6, y, 0])
            tag = Text("valid Python", font=MONO, font_size=24, color=GOOD).move_to([3.0, y, 0])
            rows.append(VGroup(strip, left, tag))

        self.voice()
        self.play(FadeIn(title), run_time=0.5)
        for row, at in zip(rows, (0.14, 0.34)):
            self.until(at)
            self.play(FadeIn(row, shift=UP * 0.15), run_time=0.5)
        self.until(0.55)
        self.say(
            "Some lists online call these syntax errors.\nThey are not. They are just noise.",
            [0, -1.7, 0], color=YELLOW, width=11,
        )
        self.hold()
        self.wipe()

    def pattern(self):
        chips = self.chips(y=1.2)
        arrow = Arrow([-6.2, -0.9, 0], [6.2, -0.9, 0], buff=0, color=GREY_B, stroke_width=5, tip_length=0.25)
        often = Text("most common", font=PROSE, font_size=28, weight=BOLD, color=BAD).move_to([-4.5, -1.5, 0])
        costly = Text("most expensive", font=PROSE, font_size=28, weight=BOLD, color=QUIET).move_to([4.5, -1.5, 0])

        self.voice()
        self.play(LaggedStart(*[FadeIn(chip, shift=UP * 0.2) for chip in chips], lag_ratio=0.3), run_time=1.4)
        self.until(0.38)
        self.play(GrowArrow(arrow), FadeIn(often), run_time=0.8)
        self.until(0.7)
        self.play(FadeIn(costly), run_time=0.6)
        self.hold()
        self.wipe()

    def habits(self):
        title = Text("Two habits", font=PROSE, font_size=44, weight=BOLD).move_to([0, 2.6, 0])
        first = Text("1.  Run the file after every small edit.", font=PROSE, font_size=34)
        second = Text("2.  Make every branch run at least once.", font=PROSE, font_size=34)
        first.move_to([-5.2, 1.0, 0], aligned_edge=LEFT)
        second.move_to([-5.2, -0.1, 0], aligned_edge=LEFT)
        last = Text(
            "Python only checks the lines it runs.", font=PROSE, font_size=36, weight=BOLD, color=YELLOW
        ).move_to([0, -2.0, 0])

        self.voice()
        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.6)
        self.until(0.14)
        self.play(FadeIn(first, shift=RIGHT * 0.2), run_time=0.6)
        self.until(0.38)
        self.play(FadeIn(second, shift=RIGHT * 0.2), run_time=0.6)
        self.until(0.66)
        self.play(FadeIn(last, shift=UP * 0.15), run_time=0.6)
        self.hold(pad=0.8)
