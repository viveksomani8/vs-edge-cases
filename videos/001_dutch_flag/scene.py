"""Animated walkthrough of EPI 6.1, the Dutch national flag partition.

Render (from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim -qh --fps 30 videos/001_dutch_flag/scene.py DutchFlag
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/001_dutch_flag/mux_narration.py \
        media/videos/scene/1080p30/DutchFlag.mp4 media/narration_timeline.json \
        videos/001_dutch_flag/dutch-national-flag-narrated.mp4

Narration: the render itself is silent. Each beat is timed to the length of its
clip (audio/01.mp3 .. audio/25.mp3, in order) and the clip start times are
written to narration_timeline.json in the media folder; mux_narration.py then
adds the clips to the video. The clips describe the default VALUES and
PIVOT_INDEX below; if those are changed (or the audio folder is missing) the
scene uses fixed pauses and writes an empty timeline.
"""

import json
from pathlib import Path

import av
from manim import *

config.background_color = "#101418"

LESS, EQUAL, UNKNOWN, GREATER = "#C8102E", "#F2F2F2", "#3A3F47", "#2A5CAA"
SMALLER_PTR, EQUAL_PTR, LARGER_PTR = "#FF7B7B", YELLOW, "#7FB2FF"
PROSE, MONO = "Segoe UI", "Consolas"

VALUES = [3, 5, 2, 3, 1, 5, 3, 2]
PIVOT_INDEX = 3
X0, STEP, ARRAY_Y = -4.0, 1.0, 1.9

CHANNEL_NAME = "Edge Cases"
CHANNEL_TAGLINE = "Python, algorithms and system design, explained visually"

AUDIO_DIR = Path(__file__).parent / "audio"
NARRATED = (
    VALUES == [3, 5, 2, 3, 1, 5, 3, 2]
    and PIVOT_INDEX == 3
    and all((AUDIO_DIR / f"{n:02d}.mp3").exists() for n in range(1, 26))
    and all((AUDIO_DIR / f"{name}.mp3").exists() for name in ("hook", "outro"))
)


def clip_seconds(path):
    with av.open(str(path)) as container:
        return float(container.duration) / av.time_base


CODE = [
    "def dutch_flag_partition(pivot_index, A):",
    "    pivot = A[pivot_index]",
    "    smaller, equal, larger = 0, 0, len(A)",
    "    while equal < larger:",
    "        if A[equal] < pivot:",
    "            A[smaller], A[equal] = A[equal], A[smaller]",
    "            smaller, equal = smaller + 1, equal + 1",
    "        elif A[equal] == pivot:",
    "            equal += 1",
    "        else:",
    "            larger -= 1",
    "            A[equal], A[larger] = A[larger], A[equal]",
]
INIT_LINES, WHILE_LINE = (1, 2), (3, 3)
LESS_LINES, EQUAL_LINES, GREATER_LINES = (4, 6), (7, 8), (9, 11)

INTRO_CAPTION = [0, 0.35, 0]
RUN_CAPTION = [4.0, -2.35, 0]


def slot_x(k):
    return X0 + k * STEP


def text_color_on(fill):
    return BLACK if fill == EQUAL else WHITE


def make_cell(value, fill=UNKNOWN, side=0.9):
    square = Square(side_length=side).set_fill(fill, 1).set_stroke(WHITE, 2)
    label = Text(str(value), font=PROSE, font_size=34, weight=BOLD)
    label.set_color(text_color_on(fill))
    cell = VGroup(square, label)
    cell.region = fill
    return cell


class DutchFlag(Scene):
    def construct(self):
        self.caption = None
        self.clip = 0
        self.voice_end = 0.0
        self.timeline = []
        self.hook()
        self.intro()
        self.brute_force()
        self.invariant()
        self.run_algorithm()
        self.closing()
        self.end_card()
        # Start/end time of every narration clip, consumed by mux_narration.py.
        timeline_path = Path(config.media_dir) / "narration_timeline.json"
        timeline_path.write_text(json.dumps(self.timeline))

    # ------------------------------------------------------------------ helpers
    def voice(self, name=None):
        """Schedule a narration clip at the current time: the next numbered clip,
        or a named one such as "hook".

        The scene only records when each clip starts; mux_narration.py lays the
        clips onto the rendered video afterwards. (Manim's own add_sound dropped
        clips unpredictably on this machine.)"""
        if name is None:
            self.clip += 1
            name = f"{self.clip:02d}"
        self.voice_end = self.renderer.time
        if NARRATED:
            self.voice_end += clip_seconds(AUDIO_DIR / f"{name}.mp3")
            self.timeline.append([name, self.renderer.time, self.voice_end])

    def hold(self, silent=2.0, pad=0.5):
        """Wait until `pad` seconds after the current clip ends (negative pad: before
        it ends), or for `silent` seconds when there is no narration."""
        remaining = self.voice_end - self.renderer.time + pad if NARRATED else silent
        if remaining > 0.05:
            self.wait(remaining)

    def lead(self, seconds):
        """Pause before an action so the narration can introduce it first."""
        if NARRATED:
            self.wait(seconds)

    def say(self, text, pos, color=WHITE, width=5.6):
        new = Text(text, font=PROSE, font_size=26, color=color, line_spacing=0.7)
        if new.width > width:
            new.scale_to_fit_width(width)
        new.move_to(pos)
        anims = [FadeIn(new, shift=UP * 0.15)]
        if self.caption is not None:
            anims.append(FadeOut(self.caption))
        self.play(*anims, run_time=0.5)
        self.caption = new

    def clear_caption(self):
        if self.caption is not None:
            self.play(FadeOut(self.caption), run_time=0.4)
            self.caption = None

    # --------------------------------------------------------------------- hook
    def hook(self):
        """Cold open: the array sorts itself into three groups, then the catch."""
        pivot = VALUES[PIVOT_INDEX]
        rank = lambda v: (v > pivot) - (v < pivot)
        order = sorted(range(len(VALUES)), key=lambda k: rank(VALUES[k]))  # stable
        fills = {-1: LESS, 0: EQUAL, 1: GREATER}
        x0 = -(len(VALUES) - 1) * STEP / 2

        cells = VGroup(
            *[make_cell(v).move_to([x0 + k * STEP, 1.0, 0]) for k, v in enumerate(VALUES)]
        )
        claim = Text(
            "Three groups.  In place.  One pass.", font=PROSE, font_size=36, weight=BOLD
        ).move_to([0, -0.7, 0])
        catch = Text(
            "Looks easy. Most people get the indices wrong.",
            font=PROSE, font_size=32, color=YELLOW,
        ).move_to([0, -1.9, 0])

        self.voice("hook")
        self.play(FadeIn(cells, shift=DOWN * 0.2), run_time=0.6)
        for slot, k in enumerate(order):
            fill = fills[rank(VALUES[k])]
            cells[k].generate_target()
            cells[k].target.move_to([x0 + slot * STEP, 1.0, 0])
            cells[k].target[0].set_fill(fill, 1)
            cells[k].target[1].set_color(text_color_on(fill))
        self.play(
            *[MoveToTarget(c, path_arc=PI / 3) for c in cells],
            FadeIn(claim, shift=UP * 0.15),
            run_time=1.8,
        )
        self.lead(2.6)
        self.play(FadeIn(catch, shift=UP * 0.15), run_time=0.6)
        self.hold(3.0, pad=0.4)
        self.play(FadeOut(cells), FadeOut(claim), FadeOut(catch), run_time=0.6)

    # ----------------------------------------------------------------- end card
    def end_card(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.caption = None

        # Channel mark: an array whose edge cell is highlighted.
        mark = VGroup()
        for k in range(4):
            edge = k == 3
            cell = Square(side_length=0.46)
            cell.set_fill(YELLOW if edge else UNKNOWN, 1).set_stroke(YELLOW if edge else WHITE, 3)
            mark.add(cell)
        mark.arrange(RIGHT, buff=0.06)
        title = Text(CHANNEL_NAME, font=PROSE, font_size=62, weight=BOLD)
        name = VGroup(mark, title).arrange(RIGHT, buff=0.4).move_to([0, 3.05, 0])
        series = Text(CHANNEL_TAGLINE, font=PROSE, font_size=26, color=GREY_A)
        series.move_to([0, 2.15, 0])

        # The lower two thirds are left for YouTube's end-screen elements: a video
        # element over the outlined 16:9 box, the subscribe button under its label.
        video_box = RoundedRectangle(width=6.0, height=3.375, corner_radius=0.12)
        video_box.set_stroke(GREY_C, 2).set_fill(UNKNOWN, 0.25).move_to([-2.9, -1.35, 0])
        watch_next = Text("Watch next", font=PROSE, font_size=28, color=YELLOW)
        watch_next.next_to(video_box, UP, buff=0.22)
        subscribe = Text("Subscribe", font=PROSE, font_size=28, color=YELLOW)
        subscribe.move_to([4.0, watch_next.get_center()[1], 0])
        prompts = VGroup(video_box, watch_next, subscribe)

        self.voice("outro")
        self.play(FadeIn(name, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(series), run_time=0.6)
        self.lead(0.4)
        self.play(FadeIn(prompts, shift=UP * 0.15), run_time=0.6)
        self.hold(4.0, pad=3.0)

    # -------------------------------------------------------------------- intro
    def intro(self):
        title = Text(
            "Dutch National Flag Partition", font=PROSE, font_size=34, weight=BOLD
        ).move_to([0, 3.65, 0])

        self.cells = []
        indices = VGroup()
        for k, value in enumerate(VALUES):
            cell = make_cell(value).move_to([slot_x(k), ARRAY_Y, 0])
            self.cells.append(cell)
            indices.add(
                Text(str(k), font=MONO, font_size=16, color=GREY_B).move_to(
                    [slot_x(k), ARRAY_Y - 0.65, 0]
                )
            )

        self.voice()
        self.play(Write(title), run_time=1.2)
        self.play(
            LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in self.cells], lag_ratio=0.1),
            FadeIn(indices),
            run_time=1.5,
        )
        self.say(
            "Given an array A and an index i, rearrange A around the value A[i].",
            INTRO_CAPTION, width=11,
        )
        self.hold(2.5)

        self.pivot_label = Text(
            f"pivot = {VALUES[PIVOT_INDEX]}", font=MONO, font_size=26, color=YELLOW
        ).move_to([5.5, ARRAY_Y, 0])
        self.voice()
        self.play(
            self.cells[PIVOT_INDEX][0].animate.set_stroke(YELLOW, 7),
            FadeIn(self.pivot_label),
        )
        self.say(
            f"Here i = {PIVOT_INDEX}, so the pivot value is {VALUES[PIVOT_INDEX]}.",
            INTRO_CAPTION, width=11,
        )
        self.hold(2.0)

        chips = VGroup()
        pivot = VALUES[PIVOT_INDEX]
        for words, fill in [
            (f"less than {pivot}", LESS),
            (f"equal to {pivot}", EQUAL),
            (f"greater than {pivot}", GREATER),
        ]:
            box = Rectangle(width=3.2, height=0.8).set_fill(fill, 1).set_stroke(WHITE, 2)
            label = Text(words, font=PROSE, font_size=24, color=text_color_on(fill))
            chips.add(VGroup(box, label.move_to(box)))
        chips.arrange(RIGHT, buff=0).move_to([0, -1.6, 0])

        self.voice()
        self.say(
            "Goal: smaller values first, then the equal ones, then the larger ones.\n"
            "It should take O(n) time and O(1) extra space.",
            INTRO_CAPTION, width=11,
        )
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips], lag_ratio=0.3))
        self.hold(3.5)
        self.play(FadeOut(chips), run_time=0.5)

    # -------------------------------------------------------------- brute force
    def brute_force(self):
        pivot = VALUES[PIVOT_INDEX]
        self.voice()
        self.say(
            "Brute force: copy the values into three lists, then join them.",
            INTRO_CAPTION, width=11,
        )

        rows = {"lower": -1.0, "equal": -2.0, "higher": -3.0}
        fills = {"lower": LESS, "equal": EQUAL, "higher": GREATER}
        labels = VGroup(
            *[
                Text(name, font=MONO, font_size=24, color=GREY_A).move_to(
                    [-5.2, y, 0], aligned_edge=LEFT
                )
                for name, y in rows.items()
            ]
        )
        self.play(FadeIn(labels), run_time=0.5)

        counts = {name: 0 for name in rows}
        copies = VGroup()
        for k, value in enumerate(VALUES):
            name = "lower" if value < pivot else "higher" if value > pivot else "equal"
            copy = make_cell(value).move_to(self.cells[k])
            copy.generate_target()
            copy.target.scale(0.8).move_to([-3.3 + counts[name] * 0.85, rows[name], 0])
            copy.target[0].set_fill(fills[name], 1)
            copy.target[1].set_color(text_color_on(fills[name]))
            counts[name] += 1
            copies.add(copy)
            self.play(MoveToTarget(copy), run_time=0.45)

        self.hold(1.0)
        self.voice()
        self.say(
            "Correct, but the three lists cost O(n) extra space.",
            INTRO_CAPTION, color=YELLOW, width=11,
        )
        self.hold(3.0)
        self.play(FadeOut(copies), FadeOut(labels), run_time=0.6)

    # ---------------------------------------------------------------- invariant
    def build_bar(self):
        """The four-region diagram: one VGroup(box, word, slice label) per region."""
        segments = [
            ("A[:smaller]", "LESS", LESS, 2.6),
            ("A[smaller:equal]", "EQUAL", EQUAL, 2.6),
            ("A[equal:larger]", "UNKNOWN", UNKNOWN, 3.4),
            ("A[larger:]", "GREATER", GREATER, 2.4),
        ]
        bar = VGroup()
        x = -sum(w for *_, w in segments) / 2
        for slice_text, word, fill, width in segments:
            box = Rectangle(width=width, height=0.9).set_fill(fill, 1).set_stroke(WHITE, 2)
            box.move_to([x + width / 2, -1.5, 0])
            inner = Text(word, font=PROSE, font_size=26, color=text_color_on(fill)).move_to(box)
            below = Text(slice_text, font=MONO, font_size=20, color=GREY_A).next_to(
                box, DOWN, buff=0.2
            )
            bar.add(VGroup(box, inner, below))
            x += width
        return bar

    def invariant(self):
        self.voice()
        self.say(
            "Better: keep four regions inside the same array.",
            INTRO_CAPTION, width=11,
        )
        bar = self.build_bar()

        # The narration names the four regions, then the three boundary indices.
        self.lead(2.6)
        for segment in bar:
            self.play(FadeIn(VGroup(segment[0], segment[1]), shift=UP * 0.2), run_time=0.9)
        self.lead(0.8)
        self.play(FadeIn(VGroup(*[segment[2] for segment in bar])), run_time=0.8)
        self.hold(3.0)
        self.voice()
        self.say(
            "Each step classifies one unknown element,\n"
            "so the unknown region shrinks until it is empty.",
            INTRO_CAPTION, width=11,
        )
        self.hold(4.0)
        self.play(FadeOut(bar), run_time=0.5)
        self.clear_caption()

    # ------------------------------------------------------------ code + legend
    def build_code(self):
        char_w = Text("M" * 20, font=MONO, font_size=24).width / 20
        line_h = 0.38
        cols = max(len(line) for line in CODE) + 1

        self.rows = VGroup()
        for k, line in enumerate(CODE):
            row = Rectangle(width=cols * char_w, height=line_h)
            row.set_stroke(width=0).set_fill(BLACK, 0).move_to([0, -k * line_h, 0])
            indent = len(line) - len(line.lstrip())
            txt = Text(line.strip(), font=MONO, font_size=24, color=GREY_A)
            txt.move_to(row.get_left() + RIGHT * (indent + 0.6) * char_w, aligned_edge=LEFT)
            self.rows.add(VGroup(row, txt))

        self.rows.scale_to_fit_width(7.3)
        if self.rows.height > 3.4:
            self.rows.scale_to_fit_height(3.4)
        self.rows.move_to([-3.25, -1.95, 0])

        panel = Rectangle(width=self.rows.width + 0.3, height=self.rows.height + 0.3)
        panel.set_fill("#1A2028", 1).set_stroke(GREY_D, 1.5).move_to(self.rows)
        return panel

    def highlight_rect(self, first, last):
        span = VGroup(*[self.rows[k][0] for k in range(first, last + 1)])
        rect = Rectangle(width=span.width, height=span.height).move_to(span)
        return rect.set_fill(YELLOW, 0.2).set_stroke(YELLOW, 1.5)

    def focus(self, lines):
        self.play(Transform(self.highlight, self.highlight_rect(*lines)), run_time=0.4)

    def build_legend(self):
        legend = VGroup()
        items = [
            ("less than pivot", LESS, 1.2, -0.2),
            ("equal to pivot", EQUAL, 4.1, -0.2),
            ("unknown", UNKNOWN, 1.2, -0.7),
            ("greater than pivot", GREATER, 4.1, -0.7),
        ]
        for words, fill, x, y in items:
            swatch = Square(side_length=0.28).set_fill(fill, 1).set_stroke(WHITE, 1.5)
            swatch.move_to([x, y, 0])
            label = Text(words, font=PROSE, font_size=20, color=GREY_A).next_to(
                swatch, RIGHT, buff=0.15
            )
            legend.add(VGroup(swatch, label))
        return legend

    # ----------------------------------------------------------------- pointers
    def make_pointer(self, name, k, color, above):
        x = slot_x(k)
        if above:
            arrow = Arrow([x, 2.95, 0], [x, 2.42, 0], buff=0, color=color,
                          stroke_width=5, max_tip_length_to_length_ratio=0.45)
            label = Text(name, font=MONO, font_size=22, color=color).next_to(arrow, UP, buff=0.06)
        else:
            arrow = Arrow([x, 0.5, 0], [x, 1.03, 0], buff=0, color=color,
                          stroke_width=5, max_tip_length_to_length_ratio=0.45)
            label = Text(name, font=MONO, font_size=22, color=color).next_to(arrow, DOWN, buff=0.06)
        return VGroup(arrow, label)

    def step_pointer(self, pointer, slots):
        return pointer.animate.shift(RIGHT * slots * STEP)

    # ------------------------------------------------------------ array actions
    def swap(self, i, j):
        if i == j:
            self.play(Indicate(self.cells[i], scale_factor=1.15), run_time=0.8)
            return
        a, b = self.cells[i], self.cells[j]
        self.play(
            a.animate(path_arc=PI / 2.5).move_to(b.get_center()),
            b.animate(path_arc=PI / 2.5).move_to(a.get_center()),
            run_time=1.1,
        )
        self.cells[i], self.cells[j] = b, a

    def recolour(self, smaller, equal, larger):
        anims = []
        for k, cell in enumerate(self.cells):
            fill = LESS if k < smaller else EQUAL if k < equal else UNKNOWN if k < larger else GREATER
            if cell.region == fill:
                continue
            cell.region = fill
            cell.generate_target()
            cell.target[0].set_fill(fill, 1)
            cell.target[1].set_color(text_color_on(fill))
            anims.append(MoveToTarget(cell))
        if anims:
            self.play(*anims, run_time=0.5)

    # ---------------------------------------------------------------- main loop
    def run_algorithm(self):
        A = list(VALUES)
        pivot = A[PIVOT_INDEX]
        n = len(A)

        panel = self.build_code()
        legend = self.build_legend()
        self.highlight = self.highlight_rect(*INIT_LINES)
        self.play(
            FadeIn(panel), FadeIn(self.rows), FadeIn(legend),
            self.cells[PIVOT_INDEX][0].animate.set_stroke(WHITE, 2),
            run_time=0.8,
        )
        self.play(FadeIn(self.highlight), run_time=0.4)
        self.bring_to_front(self.rows)

        smaller, equal, larger = 0, 0, n
        p_smaller = self.make_pointer("smaller", smaller, SMALLER_PTR, above=False)
        p_equal = self.make_pointer("equal", equal, EQUAL_PTR, above=True)
        p_larger = self.make_pointer("larger", larger, LARGER_PTR, above=False)
        self.voice()
        self.say(
            "Only the pivot's value matters now.\n"
            "smaller and equal start at 0.\n"
            "larger starts one past the end.",
            RUN_CAPTION,
        )
        self.lead(1.6)
        self.play(FadeIn(p_smaller), FadeIn(p_equal), run_time=0.6)
        self.lead(2.2)
        self.play(FadeIn(p_larger), run_time=0.6)
        self.hold(2.5)

        seen = set()
        while equal < larger:
            value = A[equal]
            self.play(Circumscribe(self.cells[equal], color=YELLOW, buff=0.06), run_time=0.7)

            if value < pivot:
                self.voice()
                self.focus(LESS_LINES)
                if "less" not in seen:
                    self.say(
                        f"A[equal] is {value}: less than the pivot.\n"
                        "Swap it with A[smaller].",
                        RUN_CAPTION,
                    )
                    self.hold(2.5, pad=0.2)
                else:
                    self.say(
                        f"{value} is less than the pivot.\n"
                        "Swap with A[smaller], advance both.",
                        RUN_CAPTION,
                    )
                    self.hold(1.5, pad=-2.2)
                A[smaller], A[equal] = A[equal], A[smaller]
                self.swap(smaller, equal)
                if "less" not in seen:
                    self.voice()
                    self.say(
                        f"The {A[equal]} that came back is a pivot value,\n"
                        "so it is already classified.\n"
                        "Advance both smaller and equal.",
                        RUN_CAPTION, color=YELLOW,
                    )
                    self.hold(3.5, pad=-1.5)
                smaller, equal = smaller + 1, equal + 1
                self.play(self.step_pointer(p_smaller, 1), self.step_pointer(p_equal, 1), run_time=0.6)
                seen.add("less")

            elif value == pivot:
                self.voice()
                self.focus(EQUAL_LINES)
                if "equal" not in seen:
                    self.say(
                        f"A[equal] is {value}: equal to the pivot.\n"
                        "It extends the equal block.\n"
                        "Move equal one step right.",
                        RUN_CAPTION,
                    )
                else:
                    self.say(
                        f"{value} equals the pivot.\nMove equal right.",
                        RUN_CAPTION,
                    )
                self.hold(3.0 if "equal" not in seen else 1.5, pad=-1.6)
                equal += 1
                self.play(self.step_pointer(p_equal, 1), run_time=0.6)
                seen.add("equal")

            else:
                self.voice()
                self.focus(GREATER_LINES)
                if "greater" not in seen:
                    self.say(
                        f"A[equal] is {value}: greater than the pivot.\n"
                        "Move larger left, then swap\n"
                        f"the {value} into the top region.",
                        RUN_CAPTION,
                    )
                    self.hold(3.0, pad=-4.0)
                else:
                    self.say(
                        f"{value} is greater than the pivot.\n"
                        "Move larger left and swap.\n"
                        "equal stays put.",
                        RUN_CAPTION,
                    )
                    self.hold(2.0, pad=-3.6)
                larger -= 1
                self.play(self.step_pointer(p_larger, -1), run_time=0.6)
                A[equal], A[larger] = A[larger], A[equal]
                self.swap(equal, larger)
                if "greater" not in seen:
                    self.recolour(smaller, equal, larger)
                    self.hold(0.0)
                    self.voice()
                    self.say(
                        "equal does NOT move.\n"
                        f"The {A[equal]} that arrived has not\n"
                        "been classified yet.",
                        RUN_CAPTION, color=YELLOW,
                    )
                    self.lead(1.6)
                    self.play(
                        Circumscribe(self.cells[equal], color=YELLOW, buff=0.06), run_time=1.0
                    )
                    self.hold(3.0)
                seen.add("greater")

            self.recolour(smaller, equal, larger)
            self.hold(0.6, pad=0.4)

        self.voice()
        self.focus(WHILE_LINE)
        self.say(
            "equal has reached larger:\n"
            "no unknown elements are left.\n"
            "The loop ends.",
            RUN_CAPTION,
        )
        self.hold(3.5)
        self.play(FadeOut(self.highlight), run_time=0.4)
        self.voice()
        self.say(
            "One pass over the array: O(n) time.\n"
            "Three indices, no extra list: O(1) space.",
            RUN_CAPTION, color=YELLOW,
        )
        self.hold(5.0, pad=0.8)
        self.bounds = (smaller, larger)
        self.run_ui = VGroup(panel, self.rows, legend, p_smaller, p_equal, p_larger)

    # ------------------------------------------------------------------ closing
    def bracket(self, first, last, words, color):
        """A labelled bracket under cells first..last (inclusive)."""
        left, right, y = slot_x(first) - 0.4, slot_x(last) + 0.4, 0.85
        lines = VGroup(
            Line([left, y, 0], [right, y, 0]),
            Line([left, y, 0], [left, y + 0.15, 0]),
            Line([right, y, 0], [right, y + 0.15, 0]),
        ).set_stroke(color, 4)
        label = Text(words, font=PROSE, font_size=22, color=color).next_to(lines, DOWN, buff=0.12)
        return VGroup(lines, label)

    def closing(self):
        smaller, larger = self.bounds
        n = len(self.cells)
        low_caption = [0, -1.1, 0]
        self.play(FadeOut(self.run_ui), FadeOut(self.caption), run_time=0.8)
        self.caption = None

        # Where it is used: quicksort, then selection.
        settled = self.bracket(smaller, larger - 1, "final position", EQUAL)
        pending = VGroup()
        if smaller > 0:
            pending.add(self.bracket(0, smaller - 1, "still to sort", SMALLER_PTR))
        if larger < n:
            pending.add(self.bracket(larger, n - 1, "still to sort", LARGER_PTR))

        self.voice()
        self.say("Where it is used: the partition step of quicksort.", low_caption, width=11)
        self.lead(3.6)
        self.play(FadeIn(settled, shift=UP * 0.15), run_time=0.8)
        self.lead(3.2)
        self.play(FadeIn(pending, shift=UP * 0.15), run_time=0.8)
        self.hold(5.0)

        self.voice()
        self.say(
            "A two-way partition would sort the equal values again and again.\n"
            "A three-way partition settles all the duplicates in one pass.",
            low_caption, width=11,
        )
        self.lead(1.0)
        self.play(
            Circumscribe(VGroup(*self.cells[smaller:larger]), color=YELLOW, buff=0.08),
            run_time=1.5,
        )
        self.hold(5.0)

        self.voice()
        self.say(
            "The same step finds the median, or the k-th smallest value,\n"
            "without sorting everything.",
            low_caption, width=11,
        )
        self.hold(4.0)
        self.play(FadeOut(settled), FadeOut(pending), run_time=0.5)

        # Why interviewers ask it: the invariant.
        bar = self.build_bar()
        last_line_at = [0, -3.2, 0]
        self.voice()
        self.say(
            "In interviews: the idea is simple, the index bookkeeping is not.",
            INTRO_CAPTION, width=11,
        )
        self.lead(6.0)
        self.say(
            "State the invariant first: four regions, three boundaries.",
            INTRO_CAPTION, color=YELLOW, width=11,
        )
        self.play(FadeIn(bar, shift=UP * 0.2), run_time=1.0)
        self.lead(2.6)
        keep_true = Text(
            "Then every line of the loop only has to keep it true.",
            font=PROSE, font_size=26,
        ).move_to(last_line_at)
        self.play(FadeIn(keep_true, shift=UP * 0.15), run_time=0.6)
        self.hold(6.0)

        related = Text(
            "Same habit:  Sort Colors   |   Move Zeroes   |   Remove Duplicates in place",
            font=PROSE, font_size=26,
        )
        if related.width > 11:
            related.scale_to_fit_width(11)
        related.move_to(last_line_at)
        self.voice()
        self.play(FadeOut(keep_true), FadeIn(related, shift=UP * 0.15), run_time=0.6)
        self.hold(5.0, pad=1.2)
