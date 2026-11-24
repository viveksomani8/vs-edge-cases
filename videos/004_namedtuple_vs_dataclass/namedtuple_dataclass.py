"""Vertical YouTube Short: NamedTuple or @dataclass?

Render, save one still per beat, add the narration and write the subtitles
(from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim --fps 30 videos/004_namedtuple_vs_dataclass/namedtuple_dataclass.py StructShort
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/004_namedtuple_vs_dataclass/stills.py \
        media/videos/namedtuple_dataclass/1920p30/StructShort.mp4 media/struct_short_stills.json \
        videos/004_namedtuple_vs_dataclass/preview
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/004_namedtuple_vs_dataclass/mux.py \
        media/videos/namedtuple_dataclass/1920p30/StructShort.mp4 media/struct_short_timeline.json \
        videos/004_namedtuple_vs_dataclass/namedtuple-or-dataclass-short.mp4
    uv run python videos/004_namedtuple_vs_dataclass/subtitles.py \
        media/struct_short_timeline.json videos/004_namedtuple_vs_dataclass/namedtuple-or-dataclass-short.en.srt

Each beat is timed to its narration clip (audio/<name>.mp3, text in
narration.py), or to the word count of the text while the clip is not recorded.

The examples are the two record types from the earlier videos: the min-stack
entry (src/epi/08-01-min-stack-with-named-tuple.py) and the linked-list node.
Every result and error message on screen is what Python 3.12 printed. The panel
drawing and the timing helpers come from videos/003_syntax_errors.
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
NT, DC = QUIET, YELLOW  # one colour per type, used everywhere

# Layout, top to bottom. YouTube draws its own controls over roughly the bottom
# fifth of a Short, so nothing sits below y = -4.8.
TITLE_Y, HEADER_Y, CAPTION = 6.3, 5.0, [0, -3.3, 0]

C_STRUCT = ["struct Entry {", "    int value;", "    int min_so_far;", "};"]

NT_CODE = ["class Entry(NamedTuple):", "    value: int", "    min_so_far: int"]
NT_USE = [
    ("e = Entry(20, 10)", WHITE),
    ("e.value            # 20", WHITE),
    ("e[0]               # 20", WHITE),
    ("e.value = 5", BAD),
    ("AttributeError: can't set attribute", BAD),
]

DC_CODE = ["@dataclass", "class Node:", "    data: int", "    next: Node | None = None"]
DC_WRITES = [
    ("__init__   Node(5)", WHITE),
    ("__repr__   Node(data=5, next=None)", WHITE),
    ("__eq__     Node(5) == Node(5)   # True", WHITE),
]

WORKS = ("works", GOOD)
# title, code, result for the NamedTuple, result for the dataclass
COMPARE = [
    ("Assign to a field", "x.field = 5",
     ("AttributeError:\ncan't set attribute", BAD), WORKS),
    ("Unpack it", "a, b = x",
     WORKS, ("TypeError: cannot unpack\nnon-iterable Node object", BAD)),
    ("Use it as a dict key", "{x: 1}",
     WORKS, ("TypeError:\nunhashable type: 'Node'", BAD)),
]


class StructShort(SyntaxErrors):
    def construct(self):
        self.caption = None
        self.clip = 0
        self.voice_start = self.voice_end = 0.0
        self.timeline, self.stills = [], []
        self.hook()
        self.named_tuple()
        self.dataclass()
        self.compare()
        self.rule()
        media = Path(config.media_dir)
        (media / "struct_short_timeline.json").write_text(json.dumps(self.timeline))
        (media / "struct_short_stills.json").write_text(json.dumps(self.stills))
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

    def header(self, number, words, color):
        badge = Circle(radius=0.34).set_fill(color, 1).set_stroke(width=0)
        digit = Text(str(number), font=PROSE, font_size=32, weight=BOLD, color=BLACK).move_to(badge)
        label = Text(words, font=MONO, font_size=44, weight=BOLD, color=color)
        label.next_to(badge, RIGHT, buff=0.3)
        return VGroup(badge, digit, label).move_to([0, HEADER_Y, 0])

    # --------------------------------------------------------------------- hook
    def hook(self):
        self.title = Text("NamedTuple or @dataclass?", font=PROSE, font_size=42, weight=BOLD)
        self.title.move_to([0, TITLE_Y, 0])
        struct = Panel(C_STRUCT, [0, 2.9, 0], 7.4, 3.2, font_size=36)
        tab = struct.tab("C")

        def chip(words, color, x):
            box = RoundedRectangle(width=3.9, height=1.3, corner_radius=0.15)
            box.set_fill(PANEL_FILL, 1).set_stroke(color, 4).move_to([x, -0.9, 0])
            return VGroup(box, Text(words, font=MONO, font_size=32, weight=BOLD, color=color).move_to(box))

        chips = [chip("NamedTuple", NT, -2.15), chip("@dataclass", DC, 2.15)]

        self.play(FadeIn(self.title), FadeIn(struct.all), FadeIn(tab), run_time=0.7)
        self.wait(LEAD_IN - 0.7)
        self.voice("hook")
        self.until(0.38)
        self.play(*[FadeIn(c, shift=UP * 0.2) for c in chips], run_time=0.6)
        self.say("Python has two.\nThey are not the same.", color=YELLOW)
        self.hold(pad=0.3)
        self.clear(struct.all, tab, *chips)

    # --------------------------------------------------------------- NamedTuple
    def named_tuple(self):
        head = self.header(1, "NamedTuple", NT)
        code = Panel(NT_CODE, [0, 3.2, 0], 7.7,2.4, font_size=34)
        use = Panel(NT_USE, [0, -0.3, 0], 7.7,3.2, fill=TERMINAL_FILL, font_size=30)

        self.voice()
        self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.5)
        self.until(0.1)
        self.play(FadeIn(code.all), run_time=0.6)
        self.say("A tuple whose fields have names.")
        self.until(0.38)
        self.play(FadeIn(use.box), FadeIn(use.rows[0]), run_time=0.5)
        self.until(0.52)
        self.play(FadeIn(use.rows[1]), run_time=0.4)
        self.until(0.62)
        self.play(FadeIn(use.rows[2]), run_time=0.4)
        self.until(0.74)
        self.play(FadeIn(use.rows[3]), FadeIn(use.rows[4]), run_time=0.5)
        self.say("Once created, it cannot be changed.", color=YELLOW)
        self.hold(pad=0.3)
        self.clear(head, code.all, use.box, *use.rows)

    # ---------------------------------------------------------------- dataclass
    def dataclass(self):
        head = self.header(2, "@dataclass", DC)
        code = Panel(DC_CODE, [0, 3.0, 0], 7.7,2.8, font_size=34)
        label = Text("Python writes for you:", font=PROSE, font_size=30, color=GREY_A, weight=BOLD)
        writes = Panel(DC_WRITES, [0, -0.7, 0], 7.7,2.2, fill=TERMINAL_FILL, font_size=28)
        label.next_to(writes.box, UP, buff=0.15).align_to(writes.box, LEFT)

        self.voice()
        self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.5)
        self.until(0.1)
        self.play(FadeIn(code.all), run_time=0.6)
        self.say("An ordinary class,\nminus the boilerplate.")
        self.until(0.42)
        self.play(FadeIn(label), FadeIn(writes.box), FadeIn(writes.rows[0]), run_time=0.5)
        self.until(0.58)
        self.play(FadeIn(writes.rows[1]), run_time=0.4)
        self.until(0.7)
        self.play(FadeIn(writes.rows[2]), run_time=0.4)
        self.until(0.84)
        self.say("Its fields can be changed:\nn.next = other_node", color=YELLOW)
        self.hold(pad=0.3)
        self.clear(head, code.all, label, writes.box, *writes.rows)

    # --------------------------------------------------------------- comparison
    def card(self, title, code, named, data, y):
        box = RoundedRectangle(width=8.4, height=2.6, corner_radius=0.15)
        box.set_fill(PANEL_FILL, 1).set_stroke(GREY_D, 1.5).move_to([0, y, 0])
        heading = Text(title, font=PROSE, font_size=32, weight=BOLD)
        heading.move_to([-3.9, y + 0.85, 0], aligned_edge=LEFT)
        snippet = Text(code, font=MONO, font_size=28, color=GREY_A)
        snippet.move_to([3.9, y + 0.85, 0], aligned_edge=RIGHT)
        rows = VGroup()
        for label, color, (result, tone), dy in (("NamedTuple", NT, named, 0.1), ("@dataclass", DC, data, -0.75)):
            name = Text(label, font=MONO, font_size=26, weight=BOLD, color=color)
            name.move_to([-3.9, y + dy, 0], aligned_edge=LEFT)
            says = Text(result, font=MONO, font_size=24, color=tone, line_spacing=0.7)
            says.move_to([-0.9, y + dy, 0], aligned_edge=LEFT)
            rows.add(VGroup(name, says))
        return VGroup(box, heading, snippet), rows

    def compare(self):
        cards = [self.card(*entry, y) for entry, y in zip(COMPARE, (3.5, 0.7, -2.1))]

        self.voice()
        for (frame, rows), at in zip(cards, (0.08, 0.4, 0.7)):
            self.until(at)
            self.play(FadeIn(frame, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(rows[0]), run_time=0.4)
            self.wait(0.9)
            self.play(FadeIn(rows[1]), run_time=0.4)
        self.hold(pad=0.4)
        self.clear(*[m for card in cards for m in card])

    # --------------------------------------------------------------------- rule
    def choice(self, when, name, color, example, y):
        condition = Text(when, font=PROSE, font_size=38, weight=BOLD).move_to([0, y + 0.9, 0])
        answer = Text(name, font=MONO, font_size=54, weight=BOLD, color=color).move_to([0, y, 0])
        like = Text(example, font=PROSE, font_size=28, color=GREY_A).move_to([0, y - 0.85, 0])
        return VGroup(condition, answer), like

    def rule(self):
        first, first_example = self.choice(
            "Never changes after it is created", "NamedTuple", NT,
            "a stack entry: (value, min so far)", 3.3,
        )
        second, second_example = self.choice(
            "Its fields get reassigned", "@dataclass", DC,
            "a linked-list node: next keeps moving", -0.3,
        )
        footer = Text(
            "Python for Programmers Who Already Code", font=PROSE, font_size=26, color=GREY_A
        ).move_to([0, -3.6, 0])
        channel = Text("Edge Cases", font=PROSE, font_size=34, weight=BOLD, color=YELLOW)
        channel.move_to([0, -4.3, 0])

        self.voice()
        self.until(0.06)
        self.play(FadeIn(first, shift=UP * 0.15), run_time=0.6)
        self.until(0.34)
        self.play(FadeIn(second, shift=UP * 0.15), run_time=0.6)
        self.until(0.6)
        self.play(FadeIn(first_example), run_time=0.4)
        self.until(0.72)
        self.play(FadeIn(second_example), run_time=0.4)
        self.play(FadeIn(footer), FadeIn(channel), run_time=0.5)
        self.hold(pad=1.2)
