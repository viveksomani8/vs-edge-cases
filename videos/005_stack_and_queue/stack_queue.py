"""Vertical YouTube Short: do you need to hand-code a stack and a queue in Python?

Render, save one still per beat, add the narration and write the subtitles
(from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim --fps 30 videos/005_stack_and_queue/stack_queue.py StackQueueShort
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/005_stack_and_queue/stills.py \
        media/videos/stack_queue/1920p30/StackQueueShort.mp4 media/stack_queue_stills.json \
        videos/005_stack_and_queue/preview
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/005_stack_and_queue/mux.py \
        media/videos/stack_queue/1920p30/StackQueueShort.mp4 media/stack_queue_timeline.json \
        videos/005_stack_and_queue/stack-and-queue-short.mp4
    uv run python videos/005_stack_and_queue/subtitles.py \
        media/stack_queue_timeline.json videos/005_stack_and_queue/stack-and-queue-short.en.srt

Each beat is timed to its narration clip (audio/<name>.mp3, text in
narration.py), or to the word count of the text while the clip is not recorded.

The class in the hook is the Stack from src/epi/08-01-min-stack-with-named-tuple.py.
The two timings on screen were measured on this machine with Python 3.12
(see TIMING below); they are not general benchmarks. The panel drawing and the
timing helpers come from videos/003_syntax_errors.
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

from narration import NARRATION, TIMING  # before syntax_errors, which imports the same module name
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
BOX, GAP = 1.1, 1.25  # side of an item box, distance between box centres

STACK_CLASS = [
    "class EmptyStackError(Exception):",
    "    pass",
    "",
    "class Stack:",
    "    def __init__( self ):",
    "        self._values = []",
    "    def push( self, value ):",
    "        self._values.append(value)",
    "    def pop( self ):",
    "        if not self._values:",
    "            raise EmptyStackError(...)",
    "        return self._values.pop()",
]

LIST_AS_STACK = [
    "stack = []",
    "stack.append(20)     # push",
    "stack.append(30)     # push",
    "stack[-1]            # peek: 30",
    "stack.pop()          # pop: 30",
]

LIST_AS_QUEUE = ["queue = [5, 8, 10, 12, 14]", "queue.pop(0)         # 5"]
DEQUE = [
    "from collections import deque",
    "queue = deque([5, 8, 10, 12, 14])",
    "queue.popleft()      # 5",
]
QUEUE_VALUES = [5, 8, 10, 12, 14]


class StackQueueShort(SyntaxErrors):
    def construct(self):
        self.caption = None
        self.clip = 0
        self.voice_start = self.voice_end = 0.0
        self.timeline, self.stills = [], []
        self.hook()
        self.list_is_the_stack()
        self.queue_on_a_list()
        self.queue_on_a_deque()
        self.when_to_write_one()
        self.rule()
        media = Path(config.media_dir)
        (media / "stack_queue_timeline.json").write_text(json.dumps(self.timeline))
        (media / "stack_queue_stills.json").write_text(json.dumps(self.stills))
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

    def item(self, value, x, y, color=QUIET):
        square = Square(side_length=BOX).set_fill(PANEL_FILL, 1).set_stroke(color, 4)
        label = Text(str(value), font=PROSE, font_size=38, weight=BOLD)
        return VGroup(square, label).move_to([x, y, 0])

    def row(self, values, y, color=QUIET):
        n = len(values)
        return [self.item(v, (k - (n - 1) / 2) * GAP, y, color) for k, v in enumerate(values)]

    # --------------------------------------------------------------------- hook
    def hook(self):
        self.title = Text("Stack and queue in Python", font=PROSE, font_size=42, weight=BOLD)
        self.title.move_to([0, TITLE_Y, 0])
        code = Panel(STACK_CLASS, [0, 1.9, 0], 7.7, 5.6, font_size=30)
        tab = code.tab("the habit from C++ and PHP")
        strike = Line(code.box.get_corner(UL), code.box.get_corner(DR), color=BAD, stroke_width=8)

        self.play(FadeIn(self.title), FadeIn(code.all), FadeIn(tab), run_time=0.7)
        self.wait(LEAD_IN - 0.7)
        self.voice("hook")
        self.until(0.5)
        self.play(Create(strike), code.rows.animate.set_opacity(0.35), run_time=0.6)
        self.say("You do not need this class.\nPython already has one.", color=YELLOW)
        self.hold(pad=0.3)
        self.clear(code.all, tab, strike)

    # -------------------------------------------------------------------- stack
    def list_is_the_stack(self):
        head = self.header("A list is the stack", GOOD)
        code = Panel(LIST_AS_STACK, [0, 2.7, 0], 7.7, 3.2, font_size=32)
        y = -1.0
        first, second = self.item(20, -GAP / 2, y), self.item(30, GAP / 2, y)
        top = Text("top", font=MONO, font_size=30, weight=BOLD, color=YELLOW)
        top.next_to(first, UP, buff=0.2)
        cursor = code.rows[0][0].copy().set_fill(YELLOW, 0.2)

        def step(k):
            return cursor.animate.move_to(code.rows[k][0])

        self.voice()
        self.play(FadeIn(head), FadeIn(code.all), FadeIn(cursor), run_time=0.6)
        self.bring_to_front(code.rows)
        self.until(0.14)
        self.play(step(1), FadeIn(first, shift=LEFT * 0.4), FadeIn(top), run_time=0.5)
        self.play(step(2), FadeIn(second, shift=LEFT * 0.4), top.animate.next_to(second, UP, buff=0.2), run_time=0.5)
        self.until(0.42)
        self.play(step(3), Indicate(second, scale_factor=1.2), run_time=0.7)
        self.until(0.56)
        self.play(step(4), FadeOut(second, shift=UP * 0.6), top.animate.next_to(first, UP, buff=0.2), run_time=0.6)
        self.say("Everything happens at the end of the list,\nso nothing else has to move.")
        self.hold(pad=0.3)
        self.clear(head, code.all, cursor, first, top)

    # -------------------------------------------------------------------- queue
    def take_front(self, items, moved_label, color):
        """Animations for removing the front item; returns the items that are left."""
        self.play(items[0][0].animate.set_stroke(color, 6), run_time=0.3)
        self.play(FadeOut(items[0], shift=UP * 0.9), run_time=0.5)
        return items[1:]

    def measured(self, y):
        lines = [
            (f"{TIMING['items']} items, taken from the front", GREY_A),
            (f"list.pop(0)       {TIMING['list']}", BAD),
            (f"deque.popleft()   {TIMING['deque']}", GOOD),
        ]
        return Panel(lines, [0, y, 0], 7.7, 2.2, fill=TERMINAL_FILL, font_size=28)

    def queue_on_a_list(self):
        head = self.header("A queue on a list", BAD)
        code = Panel(LIST_AS_QUEUE, [0, 3.6, 0], 7.7, 1.6, font_size=32)
        items = self.row(QUEUE_VALUES, 1.2)
        front = Text("front", font=MONO, font_size=30, weight=BOLD, color=YELLOW)
        front.next_to(items[0], DOWN, buff=0.2)
        self.times = self.measured(-2.3)

        self.voice()
        self.play(FadeIn(head), FadeIn(code.all), *[FadeIn(i) for i in items], FadeIn(front), run_time=0.7)
        self.until(0.2)
        rest = self.take_front(items, None, BAD)
        self.until(0.42)
        # Every item behind the front one moves down one index.
        for item in rest:
            self.play(item[0].animate.set_stroke(YELLOW, 6), run_time=0.12)
            self.play(item.animate.shift(LEFT * GAP), run_time=0.4)
            self.play(item[0].animate.set_stroke(QUIET, 4), run_time=0.12)
        self.say(f"Right answer. But {len(rest)} items had to move.", [0, -0.6, 0], color=YELLOW)
        self.until(0.72)
        self.play(FadeIn(self.times.box), FadeIn(self.times.rows[0]), FadeIn(self.times.rows[1]), run_time=0.6)
        self.hold(pad=0.3)
        self.clear(head, code.all, *rest, front)

    def queue_on_a_deque(self):
        head = self.header("A deque is the queue", GOOD)
        code = Panel(DEQUE, [0, 3.5, 0], 7.7, 2.0, font_size=30)
        items = self.row(QUEUE_VALUES, 1.0)
        front = Text("front", font=MONO, font_size=30, weight=BOLD, color=YELLOW)
        front.next_to(items[0], DOWN, buff=0.2)
        note = Text(
            "queue.Queue is a different tool: it is for threads.", font=PROSE, font_size=26, color=GREY_A
        ).move_to([0, -4.3, 0])

        self.voice()
        self.play(FadeIn(head), FadeIn(code.all), *[FadeIn(i) for i in items], FadeIn(front), run_time=0.7)
        self.until(0.42)
        rest = self.take_front(items, None, GOOD)
        self.play(front.animate.next_to(rest[0], DOWN, buff=0.2), run_time=0.4)
        self.say("Nothing else moves.", [0, -0.75, 0], color=GOOD)
        self.until(0.72)
        self.play(FadeIn(self.times.rows[2]), run_time=0.5)
        self.play(FadeIn(note), run_time=0.4)
        self.hold(pad=0.3)
        self.clear(head, code.all, *rest, front, note, self.times.box, *self.times.rows)

    # ------------------------------------------------------- when to write one
    def reason(self, number, words, example, y):
        box = RoundedRectangle(width=8.2, height=2.3, corner_radius=0.15)
        box.set_fill(PANEL_FILL, 1).set_stroke(YELLOW, 3).move_to([0, y, 0])
        badge = Text(str(number), font=PROSE, font_size=44, weight=BOLD, color=YELLOW)
        badge.move_to([-3.5, y + 0.35, 0])
        what = Text(words, font=PROSE, font_size=32, weight=BOLD).move_to([-2.9, y + 0.35, 0], aligned_edge=LEFT)
        like = Text(example, font=MONO, font_size=26, color=GREY_A).move_to([-2.9, y - 0.5, 0], aligned_edge=LEFT)
        return VGroup(box, badge, what, like)

    def when_to_write_one(self):
        head = self.header("When you do write the class", YELLOW)
        first = self.reason(1, "To limit what callers can do", "only push() and pop()", 2.6)
        second = self.reason(2, "To add behaviour", "a stack with min()", -0.2)

        self.voice()
        self.play(FadeIn(head), run_time=0.5)
        self.until(0.36)
        self.play(FadeIn(first, shift=UP * 0.15), run_time=0.5)
        self.until(0.62)
        self.play(FadeIn(second, shift=UP * 0.15), run_time=0.5)
        self.hold(pad=0.3)
        self.clear(head, first, second)

    # --------------------------------------------------------------------- rule
    def answer(self, need, use, color, y):
        left = Text(need, font=PROSE, font_size=44, weight=BOLD).move_to([-3.6, y, 0], aligned_edge=LEFT)
        right = Text(use, font=MONO, font_size=44, weight=BOLD, color=color).move_to([3.6, y, 0], aligned_edge=RIGHT)
        return VGroup(left, right)

    def rule(self):
        rows = [
            self.answer("Stack", "list", GOOD, 3.6),
            self.answer("Queue", "deque", GOOD, 2.0),
        ]
        last = Text("A class: only when it adds something.", font=PROSE, font_size=34, color=YELLOW)
        last.move_to([0, 0.2, 0])
        footer = Text(
            "Python for Programmers Who Already Code", font=PROSE, font_size=26, color=GREY_A
        ).move_to([0, -3.6, 0])
        channel = Text("Edge Cases", font=PROSE, font_size=34, weight=BOLD, color=YELLOW)
        channel.move_to([0, -4.3, 0])

        self.voice()
        self.until(0.08)
        self.play(FadeIn(rows[0], shift=UP * 0.15), run_time=0.5)
        self.until(0.36)
        self.play(FadeIn(rows[1], shift=UP * 0.15), run_time=0.5)
        self.until(0.62)
        self.play(FadeIn(last), run_time=0.5)
        self.play(FadeIn(footer), FadeIn(channel), run_time=0.5)
        self.hold(pad=1.2)
