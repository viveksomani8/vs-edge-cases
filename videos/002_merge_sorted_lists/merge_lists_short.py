"""Vertical YouTube Short that goes with the merge video: the dummy head trick.

It has its own narration clips (audio/short/*.mp3, text in narration.py) and
reuses the drawing code in merge_lists.py, laid out for a 1080x1920 frame.

Render, add the narration and write the subtitles (from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim --fps 30 videos/002_merge_sorted_lists/merge_lists_short.py DummyHeadShort
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/002_merge_sorted_lists/mux.py \
        media/videos/merge_lists_short/1920p30/DummyHeadShort.mp4 media/merge_lists_short_timeline.json \
        videos/002_merge_sorted_lists/dummy-head-short.mp4
    uv run python videos/002_merge_sorted_lists/subtitles.py \
        media/merge_lists_short_timeline.json videos/002_merge_sorted_lists/dummy-head-short.en.srt
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from manim import *

from merge_lists import (
    A_LINE, A_VALUES, B_VALUES, CODE, INIT_LINE, LEAD_IN, LOOP_LINES, PROSE, RETURN_LINE,
    Lists, MergeLists, code_block,
)
from scene import CHANNEL_NAME

config.pixel_width, config.pixel_height = 1080, 1920
config.frame_width, config.frame_height = 9.0, 16.0

# Layout, top to bottom. YouTube draws its own controls over roughly the bottom
# fifth of a Short, so nothing sits below y = -4.8.
TITLE_Y, CAPTION = 6.3, [0, 1.75, 0]
CODE_WIDTH, CODE_HEIGHT, CODE_TOP = 8.0, 5.5, 0.7

# The same merge without a dummy: the head is picked by hand before the loop.
CODE_NO_DUMMY = [
    "def merge_sorted_lists(a, b):",
    "    if not a or not b:",
    "        return a or b",
    "    if a.data <= b.data:",
    "        head, a = a, a.next",
    "    else:",
    "        head, b = b, b.next",
    "    tail = head",
    "    while a and b:",
    "        if a.data <= b.data:",
    "            tail.next, a = a, a.next",
    "        else:",
    "            tail.next, b = b, b.next",
    "        tail = tail.next",
    "    tail.next = a or b",
    "    return head",
]
EMPTY_CHECK, HEAD_PICK, LOOP_PICK = (1, 2), (3, 6), (9, 12)


class DummyHeadShort(MergeLists):
    TIMELINE = "merge_lists_short_timeline.json"

    def construct(self):
        self.begin()
        self.opening()
        self.without_dummy()
        self.with_dummy()
        self.rule()
        self.write_timeline()

    # ------------------------------------------------------------------ helpers
    def say(self, text, pos=CAPTION, color=WHITE, width=8.2):
        new = Text(text, font=PROSE, font_size=32, color=color, line_spacing=0.7)
        if new.width > width:
            new.scale_to_fit_width(width)
        new.move_to(pos)
        anims = [FadeIn(new, shift=UP * 0.15)]
        if self.caption is not None:
            anims.append(FadeOut(self.caption))
        self.play(*anims, run_time=0.5)
        self.caption = new

    def place_code(self, code, max_height=CODE_HEIGHT):
        panel, rows = code_block(code, CODE_WIDTH, max_height, ORIGIN)
        VGroup(panel, rows).shift(UP * (CODE_TOP - panel.get_top()[1]))
        return panel, rows

    def mark(self, lines, color):
        return self.highlight_rect(*lines).set_fill(color, 0.22).set_stroke(color, 2)

    # ------------------------------------------------------------------ opening
    def opening(self):
        title = Text("The Dummy Head Trick", font=PROSE, font_size=46, weight=BOLD)
        title.move_to([0, TITLE_Y, 0])
        self.lists = lists = Lists(x0=-3.5, step=1.4, y_a=4.85, y_b=3.45, radius=0.34, font_size=28)
        claim = Text(
            "One extra node.\nSimpler linked list code.",
            font=PROSE, font_size=50, weight=BOLD, line_spacing=0.8,
        ).move_to([0, -0.6, 0])

        self.play(
            FadeIn(title),
            FadeIn(lists.row("a"), shift=DOWN * 0.2),
            FadeIn(lists.row("b"), shift=UP * 0.2),
            run_time=0.8,
        )
        self.wait(LEAD_IN - 0.8)
        self.voice("short/hook")
        self.play(FadeIn(claim, shift=UP * 0.15), run_time=0.6)
        self.hold(pad=0.3)
        self.play(FadeOut(claim), run_time=0.4)

    # ----------------------------------------------------------- without a dummy
    def without_dummy(self):
        lists = self.lists
        fronts = [lists.nodes[("a", 0)], lists.nodes[("b", 0)]]
        panel, self.rows = self.place_code(CODE_NO_DUMMY)
        head_pick = self.mark(HEAD_PICK, A_LINE)
        head = lists.head_tag()

        self.voice("short/01")
        self.play(FadeIn(panel), FadeIn(self.rows), run_time=0.7)
        self.say("Without a dummy: pick the head by hand,\nbefore the loop can start.")
        self.until((2, 0))
        self.play(FadeIn(head_pick), run_time=0.4)
        self.bring_to_front(self.rows)
        self.play(*[Indicate(node, scale_factor=1.3) for node in fronts], run_time=1.0)
        self.play(FadeIn(head, shift=UP * 0.1), run_time=0.5)
        self.hold(pad=0.3)

        loop_pick = self.mark(LOOP_PICK, A_LINE)
        empty_check = self.mark(EMPTY_CHECK, YELLOW)
        self.voice("short/02")
        self.say("The same comparison, written twice.\nPlus an extra check for an empty list.")
        self.play(FadeIn(loop_pick), run_time=0.4)
        self.bring_to_front(self.rows)
        self.until((1, 0))
        self.play(FadeIn(empty_check), run_time=0.4)
        self.bring_to_front(self.rows)
        self.hold(pad=0.3)
        self.old_code = VGroup(panel, self.rows, head_pick, loop_pick, empty_check, head)

    # -------------------------------------------------------------- with a dummy
    def with_dummy(self):
        lists = self.lists
        line_height = self.rows[0][0].height
        panel, rows = self.place_code(CODE, max_height=line_height * len(CODE))
        self.tail_ring, self.tail_label = lists.tail_marker("dummy")

        self.voice("short/03")
        self.play(FadeOut(self.old_code), run_time=0.5)
        self.rows = rows
        self.highlight = self.highlight_rect(*INIT_LINE)
        self.play(FadeIn(panel), FadeIn(rows), FadeIn(self.highlight), run_time=0.6)
        self.bring_to_front(rows)
        self.say("Put a placeholder node in front: a dummy.\ntail starts on it.")
        self.play(FadeIn(lists.dummy, shift=RIGHT * 0.2), run_time=0.6)
        self.play(Create(self.tail_ring), FadeIn(self.tail_label), run_time=0.6)
        self.hold(pad=0.3)

        # The whole merge, quickly: the first node is linked exactly like the rest.
        self.voice("short/04")
        self.focus(LOOP_LINES)
        self.say(
            "The first node is no longer special.\n"
            "The loop links it like every other node.\n"
            "Empty lists just work."
        )
        at = {"a": 0, "b": 0}
        tail_key = "dummy"
        while at["a"] < len(A_VALUES) and at["b"] < len(B_VALUES):
            take = "a" if A_VALUES[at["a"]] <= B_VALUES[at["b"]] else "b"
            key = (take, at[take])
            self.play(lists.relink(tail_key, key), lists.fill(key), run_time=0.45)
            self.move_tail(key, run_time=0.3)
            at[take] += 1
            tail_key = key
        rest = "a" if at["a"] < len(A_VALUES) else "b"
        attach = [lists.relink(tail_key, (rest, at[rest]))]
        for k in range(at[rest], len(lists.values[rest])):
            attach += [lists.fill((rest, k)), lists.relink((rest, k), (rest, k + 1))]
        self.play(*attach, run_time=0.7)
        self.hold(pad=0.3)

        head = lists.head_tag()
        self.voice("short/05")
        self.focus(RETURN_LINE)
        self.say("Return dummy.next: the real head.", color=YELLOW)
        self.play(
            VGroup(lists.dummy, lists.links["dummy"]).animate.set_opacity(0.3),
            FadeIn(head, shift=UP * 0.1),
            run_time=0.6,
        )
        self.hold(pad=0.3)

    # --------------------------------------------------------------------- rule
    def rule(self):
        self.voice("short/06")
        self.play(FadeOut(self.highlight), run_time=0.3)
        self.say(
            "Rule of thumb: use a dummy when the head\n"
            "is not known up front, or might change.",
            color=YELLOW,
        )
        self.hold(pad=0.3)

        self.voice("short/07")
        self.say("Same trick: Remove N-th Node From End,\nPartition List, Add Two Numbers.")
        self.until((1, 0))
        self.say(f"Full merge walkthrough on the channel:\n{CHANNEL_NAME}", color=YELLOW)
        self.hold(pad=1.2)
