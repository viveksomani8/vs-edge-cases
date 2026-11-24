"""Animated walkthrough of EPI 7.1, merging two sorted linked lists in place.

Render, add the narration and write the subtitles (from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim -qh --fps 30 videos/002_merge_sorted_lists/merge_lists.py MergeLists
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/002_merge_sorted_lists/mux.py \
        media/videos/merge_lists/1080p30/MergeLists.mp4 media/merge_lists_timeline.json \
        videos/002_merge_sorted_lists/merge-sorted-lists-narrated.mp4
    uv run python videos/002_merge_sorted_lists/subtitles.py \
        media/merge_lists_timeline.json videos/002_merge_sorted_lists/merge-sorted-lists-narrated.en.srt

Narration: the render is silent. Each beat is timed to the length of its clip
(audio/<name>.mp3, text in narration.py) and the clip start times are written
to a timeline file in the media folder; mux.py then lays the clips onto the
video. A clip that has not been recorded yet is timed from its word count, so
the scene can be previewed before any audio exists.

The helpers shared with the Dutch flag video (captions, code highlight, end
card) are inherited from videos/001_dutch_flag/scene.py.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "001_dutch_flag"))

import re

import av
import numpy as np
from manim import *

import mux_narration

from narration import NARRATION
from scene import MONO, PROSE, DutchFlag

config.background_color = "#101418"

A_VALUES = [2, 5, 8]
B_VALUES = [1, 5, 9, 13]

A_LINE, A_FILL = "#FF7B7B", "#C8102E"
B_LINE, B_FILL = "#7FB2FF", "#2A5CAA"
IDLE_FILL = "#232931"
HEAD = "#7CE38B"

AUDIO_DIR = HERE / "audio"
LEAD_IN = 1.0  # seconds of picture before the first narration clip starts
WORDS_PER_SECOND = 2.5  # the pace of the recorded Dutch flag narration

CODE = [
    "def merge_sorted_lists(a, b):",
    "    dummy = tail = Node(0)",
    "    while a and b:",
    "        if a.data <= b.data:",
    "            tail.next, a = a, a.next",
    "        else:",
    "            tail.next, b = b, b.next",
    "        tail = tail.next",
    "    tail.next = a or b",
    "    return dummy.next",
]
INIT_LINE, WHILE_LINE, COMPARE_LINE = (1, 1), (2, 2), (3, 3)
TAKE_A_LINE, TAKE_B_LINES, ADVANCE_LINE = (4, 4), (5, 6), (7, 7)
LOOP_LINES, REST_LINE, RETURN_LINE = (2, 7), (8, 8), (9, 9)

INTRO_CAPTION = [0, -0.85, 0]
RUN_CAPTION = [3.55, -2.1, 0]

# One entry per pass of the loop for the default lists: caption, colour, and the
# cues (see MergeLists.until) at which the link is made and tail is advanced.
STEPS = [
    ("Fronts: 2 and 1. 1 is smaller.\ntail.next = that node,\nand b moves forward.", WHITE, (2, 0), None),
    ("2 against 5: take 2.\nThe arrow out of 1 pointed at 5.\nNow it points at 2. No node moved.", WHITE, (4, 0), (6, 0)),
    ("5 against 5: a tie.\n<= takes the node from a first,\nso the merge is stable.", YELLOW, (1, 0.5), (2, 0.3)),
    ("5 (from b) against 8: take 5.\nLink it, advance b, advance tail.", WHITE, (2, 0), (2, 0.7)),
    ("8 against 9: take 8.\nNow a is None:\nlist a has run out.", WHITE, (2, 0), (3, 0.5)),
]


def clip_seconds(name):
    """Length of a narration clip, estimated from the script until it is recorded."""
    path = AUDIO_DIR / f"{name}.mp3"
    if path.exists():
        with av.open(str(path)) as container:
            return float(container.duration) / av.time_base
    return len(NARRATION[name].split()) / WORDS_PER_SECOND + 0.4


_SENTENCE_STARTS = {}


def sentence_starts(name):
    """Seconds into a clip at which each of its sentences starts.

    The first guess shares the clip between its sentences by length; with the
    recording present, each guess is then moved to the nearest place where the
    voice resumes after a pause.
    """
    if name in _SENTENCE_STARTS:
        return _SENTENCE_STARTS[name]
    sentences = re.split(r"(?<=[.?!])\s+", NARRATION[name].strip())
    edges = np.cumsum([0] + [len(sentence) + 1 for sentence in sentences])
    starts = list(edges[:-1] / edges[-1] * clip_seconds(name))

    path = AUDIO_DIR / f"{name}.mp3"
    if path.exists():
        rate, window = 16000, 320  # 20 ms windows
        samples = mux_narration.decode_mono(path, rate=rate)
        frames = samples[: len(samples) // window * window].reshape(-1, window)
        quiet = np.sqrt((frames ** 2).mean(axis=1)) < 0.03
        resumes, run = [], 0
        for k, is_quiet in enumerate(quiet):
            if is_quiet:
                run += 1
            else:
                if run >= 10 and k > run:  # a pause of 0.2 s or more, not the lead-in
                    resumes.append(k * window / rate)
                run = 0
        for k in range(1, len(starts)):
            near = [r for r in resumes if abs(r - starts[k]) < 1.5 and r > starts[k - 1] + 0.3]
            if near:
                starts[k] = min(near, key=lambda r: abs(r - starts[k]))
    _SENTENCE_STARTS[name] = [float(t) for t in starts]
    return _SENTENCE_STARTS[name]


def merge_order(a=A_VALUES, b=B_VALUES):
    """Node keys ("a", i) / ("b", j) in merged order; on a tie the node from a first."""
    i = j = 0
    order = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            order.append(("a", i))
            i += 1
        else:
            order.append(("b", j))
            j += 1
    order += [("a", k) for k in range(i, len(a))] + [("b", k) for k in range(j, len(b))]
    return order


def link_arrow(start, end, color, width, tip=0.2):
    return Arrow(
        start, end, buff=0, color=color, stroke_width=width, tip_length=tip,
        max_tip_length_to_length_ratio=0.6, max_stroke_width_to_length_ratio=20,
    )


def code_block(code, width, max_height, center):
    """A code panel and its rows; each row is VGroup(background, text)."""
    char_w = Text("M" * 20, font=MONO, font_size=24).width / 20
    line_h = 0.38
    cols = max(len(line) for line in code) + 1

    rows = VGroup()
    for k, line in enumerate(code):
        row = Rectangle(width=cols * char_w, height=line_h)
        row.set_stroke(width=0).set_fill(BLACK, 0).move_to([0, -k * line_h, 0])
        indent = len(line) - len(line.lstrip())
        txt = Text(line.strip(), font=MONO, font_size=24, color=GREY_A)
        txt.move_to(row.get_left() + RIGHT * (indent + 0.6) * char_w, aligned_edge=LEFT)
        rows.add(VGroup(row, txt))

    rows.scale_to_fit_width(width)
    if rows.height > max_height:
        rows.scale_to_fit_height(max_height)
    rows.move_to(center)
    panel = Rectangle(width=rows.width + 0.3, height=rows.height + 0.3)
    panel.set_fill("#1A2028", 1).set_stroke(GREY_D, 1.5).move_to(rows)
    return panel, rows


class Lists:
    """The two lists drawn as two rows of nodes.

    Each list is evenly spaced (node i sits in column i + 1; the dummy has
    column 0) and the nodes never move: merging only re-aims the `next` arrows.
    For the default lists the merged chain only ever goes right or straight up
    and down; other values could need an arrow that points back to the left.
    Keys: "dummy", ("a", i), ("b", j); the key one past the end of a list is
    that list's None marker.
    """

    def __init__(self, x0=-4.0, step=1.6, y_a=2.3, y_b=0.9, radius=0.34, font_size=28):
        self.x0, self.step, self.radius = x0, step, radius
        self.rows = {"a": y_a, "b": y_b}
        self.values = {"a": A_VALUES, "b": B_VALUES}
        self.lines = {"a": A_LINE, "b": B_LINE}
        self.fills = {"a": A_FILL, "b": B_FILL}
        self.scale = radius / 0.34
        self.placed = {}  # positions set by straighten(), which override the grid

        self.order = merge_order()
        self.slot = {
            (name, i): i + 1 for name, values in self.values.items() for i in range(len(values) + 1)
        }

        self.nodes = {}
        for name, i in self.order:
            circle = Circle(radius=radius).set_fill(IDLE_FILL, 1).set_stroke(self.lines[name], 3)
            label = Text(str(self.values[name][i]), font=PROSE, font_size=font_size, weight=BOLD)
            self.nodes[(name, i)] = VGroup(circle, label).move_to(self.pos((name, i)))

        self.nones = {
            name: Text("None", font=MONO, font_size=20 * self.scale, color=GREY_B).move_to(
                self.pos((name, len(values)))
            )
            for name, values in self.values.items()
        }
        self.links = {
            (name, i): self.arrow((name, i), (name, i + 1))
            for name, values in self.values.items()
            for i in range(len(values))
        }

        ring = Circle(radius=radius).set_fill(IDLE_FILL, 1).set_stroke(GREY_A, 3)
        tag = Text("dummy", font=MONO, font_size=20 * self.scale, color=GREY_A)
        ring.move_to(self.pos("dummy"))
        tag.next_to(ring, DOWN, buff=0.12 * self.scale)
        self.dummy = VGroup(ring, tag)

    # ---------------------------------------------------------------- geometry
    def pos(self, key):
        if key in self.placed:
            return self.placed[key]
        if key == "dummy":
            return np.array([self.x0, (self.rows["a"] + self.rows["b"]) / 2, 0.0])
        return np.array([self.x0 + self.slot[key] * self.step, self.rows[key[0]], 0.0])

    def is_none(self, key):
        return key != "dummy" and key[1] == len(self.values[key[0]])

    def label_pos(self, key, gap=0.3):
        """Where a text label for this node goes: outside its row."""
        up = key == "dummy" or key[0] == "a"
        return self.pos(key) + (UP if up else DOWN) * (self.radius + gap * self.scale)

    def arrow(self, src, dst, merged=False):
        start, end = self.pos(src), self.pos(dst)
        unit = (end - start) / np.linalg.norm(end - start)
        clear = self.radius + 0.07 * self.scale
        clear_end = 0.45 * self.scale if self.is_none(dst) else clear
        return link_arrow(
            start + unit * clear, end - unit * clear_end,
            WHITE if merged else GREY_B, 5 if merged else 3, tip=0.2 * self.scale,
        )

    # -------------------------------------------------------------- animations
    def relink(self, src, dst):
        """Animation that points src.next at dst and draws it as part of the result."""
        new = self.arrow(src, dst, merged=True)
        if src in self.links:
            return Transform(self.links[src], new)
        self.links[src] = new
        return GrowArrow(new)

    def fill(self, key):
        # Animate the whole node, not just its circle, so the number stays on top.
        node = self.nodes[key]
        node.generate_target()
        node.target[0].set_fill(self.fills[key[0]], 1)
        return MoveToTarget(node)

    def straighten(self, x_first, step, dummy_opacity=1.0):
        """Animations that redraw the finished merge as one row, level with the dummy.

        Only the drawing changes: every node keeps its links, and the arrows
        travel with the nodes. Call it once all the links are merged.
        """
        chain = list(self.order)
        last = chain[-1]
        end = (last[0], len(self.values[last[0]]))  # the None after the last node
        y = self.pos("dummy")[1]
        for k, key in enumerate(chain + [end]):
            self.placed[key] = np.array([x_first + k * step, y, 0.0])

        anims = [self.nodes[key].animate.move_to(self.placed[key]) for key in chain]
        anims.append(self.nones[last[0]].animate.move_to(self.placed[end]))
        for src, dst in zip(["dummy"] + chain, chain + [end]):
            new = self.arrow(src, dst, merged=True)
            if src == "dummy":
                new.set_opacity(dummy_opacity)
            anims.append(Transform(self.links[src], new))
        return anims

    # ------------------------------------------------------------------ pieces
    def row(self, name):
        n = len(self.values[name])
        return VGroup(
            *[self.nodes[(name, i)] for i in range(n)],
            *[self.links[(name, i)] for i in range(n)],
            self.nones[name],
        )

    def pointer(self, name, key):
        """A labelled arrow at a node, above list a's row or below list b's."""
        up = key[0] == "a"
        side = UP if up else DOWN
        at = self.pos(key)
        arrow = link_arrow(
            at + side * (self.radius + 0.46 * self.scale),
            at + side * (self.radius + 0.08 * self.scale),
            self.lines[key[0]], 5, tip=0.18 * self.scale,
        )
        label = Text(name, font=MONO, font_size=24 * self.scale, color=self.lines[key[0]])
        label.next_to(arrow, side, buff=0.06)
        return VGroup(arrow, label)

    def tail_marker(self, key):
        ring = Circle(radius=self.radius + 0.1 * self.scale).set_stroke(YELLOW, 5)
        ring.move_to(self.pos(key))
        label = Text("tail", font=MONO, font_size=24 * self.scale, color=YELLOW)
        label.move_to(self.label_pos(key))
        return ring, label

    def head_tag(self):
        tag = Text("head", font=MONO, font_size=24 * self.scale, color=HEAD)
        return tag.move_to(self.label_pos(self.order[0]))


class MergeLists(DutchFlag):
    TIMELINE = "merge_lists_timeline.json"

    def construct(self):
        self.begin()
        self.hook()
        self.intro()
        self.brute_force()
        self.idea()
        self.run_algorithm()
        self.closing()
        self.end_card()
        self.write_timeline()

    def begin(self):
        self.caption = None
        self.clip = 0
        self.voice_start = self.voice_end = 0.0
        self.timeline = []

    def write_timeline(self):
        """Start/end time of every narration clip, consumed by mux.py."""
        (Path(config.media_dir) / self.TIMELINE).write_text(json.dumps(self.timeline))
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
        self.voice_name = name
        self.voice_start = self.renderer.time
        self.voice_end = self.voice_start + clip_seconds(name)
        self.timeline.append([name, self.voice_start, self.voice_end])

    def hold(self, silent=None, pad=0.5):
        """Wait until `pad` seconds after the current clip ends."""
        remaining = self.voice_end - self.renderer.time + pad
        if remaining > 0.05:
            self.wait(remaining)

    def lead(self, seconds):
        self.wait(seconds)

    def until(self, cue):
        """Wait until a point in the current clip: a fraction of its length, or
        (sentence, fraction) for a point inside one of its sentences."""
        length = self.voice_end - self.voice_start
        if isinstance(cue, tuple):
            sentence, into = cue
            starts = sentence_starts(self.voice_name) + [length]
            offset = starts[sentence] + into * (starts[sentence + 1] - starts[sentence])
        else:
            offset = cue * length
        remaining = self.voice_start + offset - self.renderer.time
        if remaining > 0.05:
            self.wait(remaining)

    def build_code(self):
        self.panel, self.rows = code_block(CODE, 6.3, 3.1, [-3.45, -2.05, 0])

    def move_tail(self, key, run_time=0.6):
        self.play(
            self.tail_ring.animate.move_to(self.lists.pos(key)),
            self.tail_label.animate.move_to(self.lists.label_pos(key)),
            run_time=run_time,
        )

    # --------------------------------------------------------------------- hook
    def hook(self):
        """Cold open: the two lists zip into one, and nothing moves but the arrows."""
        lists = Lists(x0=-4.8, y_a=2.4, y_b=1.0)
        claim = Text(
            "Two sorted lists.  One merged list.", font=PROSE, font_size=36, weight=BOLD
        ).move_to([0, -0.7, 0])
        catch = Text(
            "No new nodes. Only the arrows change.", font=PROSE, font_size=32, color=YELLOW
        ).move_to([0, -1.9, 0])
        drawing = VGroup(lists.row("a"), lists.row("b"))

        self.play(FadeIn(drawing, shift=DOWN * 0.2), run_time=0.6)
        self.wait(LEAD_IN - 0.6)
        self.voice("hook")
        self.until(0.12)
        order = lists.order
        zips = [AnimationGroup(lists.fill(order[0]))]
        for src, dst in zip(order, order[1:]):
            zips.append(AnimationGroup(lists.relink(src, dst), lists.fill(dst)))
        self.play(
            LaggedStart(*zips, lag_ratio=0.5),
            FadeIn(claim, shift=UP * 0.15),
            FadeOut(lists.nones["a"]),  # nothing points at it once the lists are merged
            run_time=2.6,
        )
        self.until((1, 0))
        self.play(FadeIn(catch, shift=UP * 0.15), run_time=0.6)
        self.hold(pad=0.4)
        self.play(FadeOut(drawing), FadeOut(claim), FadeOut(catch), run_time=0.6)

    # -------------------------------------------------------------------- intro
    def node_fields(self):
        """A node drawn as its two fields, with `next` picked out."""
        data = Rectangle(width=1.7, height=0.8).set_fill(IDLE_FILL, 1).set_stroke(WHITE, 2)
        nxt = Rectangle(width=1.7, height=0.8).set_fill(IDLE_FILL, 1).set_stroke(WHITE, 2)
        boxes = VGroup(data, nxt).arrange(RIGHT, buff=0).move_to([-2.2, -2.5, 0])
        words = VGroup(
            Text("data", font=MONO, font_size=26).move_to(data),
            Text("next", font=MONO, font_size=26).move_to(nxt),
        )
        name = Text("Node", font=MONO, font_size=22, color=GREY_A).next_to(boxes, UP, buff=0.15)
        out = link_arrow(nxt.get_right(), nxt.get_right() + RIGHT * 1.1, YELLOW, 5)
        note = Text("the only field you may change", font=PROSE, font_size=24, color=YELLOW)
        note.next_to(out, RIGHT, buff=0.25)
        return VGroup(boxes, words, name), nxt, VGroup(out, note)

    def intro(self):
        title = Text(
            "Merge Two Sorted Linked Lists", font=PROSE, font_size=34, weight=BOLD
        ).move_to([0, 3.65, 0])
        self.lists = lists = Lists()
        self.pointers = {
            "a": lists.pointer("a", ("a", 0)),
            "b": lists.pointer("b", ("b", 0)),
        }

        self.voice()
        self.play(Write(title), run_time=1.2)
        self.until((1, 0))
        self.play(FadeIn(lists.row("a"), shift=DOWN * 0.2), FadeIn(self.pointers["a"]), run_time=0.8)
        self.play(FadeIn(lists.row("b"), shift=UP * 0.2), FadeIn(self.pointers["b"]), run_time=0.8)
        self.say(
            "Two linked lists, a and b. Each one is already sorted.",
            INTRO_CAPTION, width=11,
        )
        self.hold()

        self.voice()
        self.say(
            "Return one sorted list that contains every node from both.",
            INTRO_CAPTION, width=11,
        )
        self.hold()

        node, next_box, note = self.node_fields()
        self.voice()
        self.say(
            "Reuse the existing nodes: only `next` may change.\n"
            "So the extra space must be O(1).",
            INTRO_CAPTION, width=11,
        )
        self.play(FadeIn(node, shift=UP * 0.2), run_time=0.6)
        self.until((1, 0))
        self.play(next_box.animate.set_stroke(YELLOW, 6), FadeIn(note), run_time=0.6)
        self.hold()
        self.play(FadeOut(node), FadeOut(note), run_time=0.5)

    # -------------------------------------------------------------- brute force
    def brute_force(self):
        """The same walk as the real solution, but every node is copied."""
        lists = self.lists
        order = lists.order
        n = len(order)
        x = lambda k: (k - (n - 1) / 2) * 1.1
        list_y = -2.6

        self.voice()
        self.say(
            "Both lists are sorted, so the smallest value left\n"
            "is always at the front of one of them.",
            INTRO_CAPTION, width=11,
        )
        self.until(0.3)
        fronts = [lists.nodes[("a", 0)], lists.nodes[("b", 0)]]
        self.play(*[Indicate(node, scale_factor=1.3) for node in fronts], run_time=1.2)
        self.until((1, 0))
        self.say(
            "Brute force: compare the two fronts,\n"
            "copy the smaller into a brand new list. Repeat.",
            INTRO_CAPTION, width=11,
        )
        label = Text("new list", font=MONO, font_size=22, color=GREY_A)
        label.move_to([-6.3, list_y, 0], aligned_edge=LEFT)
        self.play(FadeIn(label), run_time=0.4)

        copies, arrows = VGroup(), VGroup()
        for slot, (name, i) in enumerate(order):
            circle = Circle(radius=0.3).set_fill(IDLE_FILL, 1).set_stroke(HEAD, 3)
            value = Text(str(lists.values[name][i]), font=PROSE, font_size=24, weight=BOLD)
            copy = VGroup(circle, value).move_to([x(slot), list_y, 0])
            copies.add(copy)
            anims = [FadeIn(copy, target_position=lists.pos((name, i)))]
            if slot:
                arrow = link_arrow(
                    [x(slot - 1) + 0.36, list_y, 0], [x(slot) - 0.36, list_y, 0], GREY_B, 3, tip=0.16
                )
                arrows.add(arrow)
                anims.append(GrowArrow(arrow))
            self.play(*anims, run_time=0.6)
        self.hold()

        self.voice()
        self.say(
            "Time: O(n + m), already linear.\n"
            "But n + m copied nodes: O(n + m) extra space. Not allowed.",
            INTRO_CAPTION, color=YELLOW, width=11,
        )
        self.hold()
        self.play(FadeOut(copies), FadeOut(arrows), FadeOut(label), run_time=0.6)

    # --------------------------------------------------------------------- idea
    def idea(self):
        lists = self.lists
        fronts = [lists.nodes[("a", 0)], lists.nodes[("b", 0)]]

        self.voice()
        self.say(
            "Better: the same walk, but stop copying.\n"
            "Take the node itself, and re-aim a `next` at it.",
            INTRO_CAPTION, width=11,
        )
        self.until((2, 0))
        self.play(*[Indicate(node, scale_factor=1.3) for node in fronts], run_time=1.2)
        self.hold()

        self.voice()
        self.say(
            "Which node will be the head? Not known yet.\n"
            "So start with a placeholder: a dummy node.",
            INTRO_CAPTION, width=11,
        )
        self.until((2, 0))
        self.play(FadeIn(lists.dummy, shift=RIGHT * 0.2), run_time=0.7)
        self.hold()

        self.tail_ring, self.tail_label = lists.tail_marker("dummy")
        self.voice()
        self.play(Create(self.tail_ring), FadeIn(self.tail_label), run_time=0.7)
        self.say(
            "tail: the last node of the merged list.\n"
            "Invariant: dummy to tail is merged and sorted.",
            INTRO_CAPTION, width=11,
        )
        self.hold()
        self.clear_caption()

    # ---------------------------------------------------------------- main loop
    def run_algorithm(self):
        lists = self.lists
        assert (A_VALUES, B_VALUES) == ([2, 5, 8], [1, 5, 9, 13]), "the clips describe these lists"

        self.build_code()
        self.highlight = self.highlight_rect(*INIT_LINE)
        self.play(FadeIn(self.panel), FadeIn(self.rows), run_time=0.8)
        self.play(FadeIn(self.highlight), run_time=0.4)
        self.bring_to_front(self.rows)

        self.voice()
        self.say(
            "dummy and tail start on one new node.\n"
            "Loop while both lists have nodes.",
            RUN_CAPTION,
        )
        self.until((1, 0))
        self.focus(WHILE_LINE)
        self.hold()

        at = {"a": 0, "b": 0}
        tail_key = "dummy"
        for step, (text, color, link_at, tail_at) in enumerate(STEPS):
            front = {name: (name, at[name]) for name in "ab"}
            take = "a" if A_VALUES[at["a"]] <= B_VALUES[at["b"]] else "b"
            key = front[take]

            self.voice()
            self.focus(COMPARE_LINE)
            self.say(text, RUN_CAPTION, color=color)
            self.play(*[Indicate(lists.nodes[k], scale_factor=1.25) for k in front.values()], run_time=0.9)
            self.until(link_at)
            self.focus(TAKE_A_LINE if take == "a" else TAKE_B_LINES)
            self.play(lists.relink(tail_key, key), lists.fill(key), run_time=0.9)
            at[take] += 1
            slots = lists.slot[(take, at[take])] - lists.slot[key]
            self.play(self.pointers[take].animate.shift(RIGHT * slots * lists.step), run_time=0.5)

            if step == 0:
                self.hold(pad=0.3)
                self.voice()
                self.say(
                    "tail steps onto the node just linked.\n"
                    "Merged so far: one node.",
                    RUN_CAPTION,
                )
            else:
                self.until(tail_at)
            self.focus(ADVANCE_LINE)
            self.move_tail(key)
            tail_key = key
            self.hold(pad=0.4)
        assert at["a"] == len(A_VALUES), "the default lists end with a running out"

        # tail.next = a or b: the rest of b is attached by one assignment.
        self.voice()
        self.focus(REST_LINE)
        self.say(
            "One list is empty. The rest of the other\n"
            "is already sorted and already linked.\n"
            "tail.next = a or b attaches all of it.",
            RUN_CAPTION,
        )
        self.until((2, 0))
        attach = [lists.relink(tail_key, ("b", at["b"]))]
        for j in range(at["b"], len(B_VALUES)):
            attach += [lists.fill(("b", j)), lists.relink(("b", j), ("b", j + 1))]
        self.play(*attach, run_time=1.2)
        self.hold()

        head = lists.head_tag()
        self.dummy_part = VGroup(lists.dummy, lists.links["dummy"])
        self.voice()
        self.focus(RETURN_LINE)
        self.say(
            "Skip the placeholder: return dummy.next.\n"
            "That node is the real head.",
            RUN_CAPTION, color=YELLOW,
        )
        self.until((1, 0))
        self.play(self.dummy_part.animate.set_opacity(0.3), FadeIn(head, shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(lists.nodes[lists.order[0]], scale_factor=1.25), run_time=0.9)

        # The function has returned: its local names go away, and the same nodes
        # and links are redrawn in one row so the result reads as sorted.
        self.until((3, 0))
        self.say(
            "Same nodes, same links.\n"
            "Just redrawn in a straight line:\n"
            "sorted.",
            RUN_CAPTION, color=YELLOW,
        )
        spent = lists.nones["b" if lists.order[-1][0] == "a" else "a"]
        straight = lists.straighten(x_first=-2.6, step=1.1, dummy_opacity=0.3)
        self.play(
            *straight,
            head.animate.move_to(lists.label_pos(lists.order[0])),
            FadeOut(self.pointers["a"]), FadeOut(self.pointers["b"]),
            FadeOut(self.tail_ring), FadeOut(self.tail_label), FadeOut(spent),
            run_time=1.8,
        )
        self.hold()

        self.play(FadeOut(self.highlight), run_time=0.4)
        self.voice()
        self.say(
            "Each pass of the loop links exactly one node.\n"
            "Time: O(n + m).",
            RUN_CAPTION, color=YELLOW,
        )
        self.hold()
        self.voice()
        self.say(
            "One dummy node and a few references,\n"
            "whatever the size of the input.\n"
            "Extra space: O(1).",
            RUN_CAPTION, color=YELLOW,
        )
        self.hold(pad=0.8)
        self.run_ui = VGroup(self.panel, self.rows, head)

    # ------------------------------------------------------------------ closing
    def merge_sort_diagram(self):
        def box(words, x, color=WHITE):
            rect = RoundedRectangle(width=3.1, height=0.8, corner_radius=0.1)
            rect.set_fill(IDLE_FILL, 1).set_stroke(color, 2).move_to([x, -2.6, 0])
            return VGroup(rect, Text(words, font=PROSE, font_size=24, color=color).move_to(rect))

        left, right = box("sort the left half", -4.6), box("sort the right half", -1.2)
        merge = box("merge the two", 3.6, YELLOW)
        arrow = link_arrow(right.get_right() + RIGHT * 0.2, merge.get_left() + LEFT * 0.2, GREY_A, 4)
        return VGroup(left, right), VGroup(arrow, merge)

    def closing(self):
        low_caption = [0, -1.0, 0]
        self.play(FadeOut(self.run_ui), FadeOut(self.caption), run_time=0.8)
        self.caption = None

        halves, merge = self.merge_sort_diagram()
        self.voice()
        self.say("Where it is used: the merge step of merge sort.", low_caption, width=11)
        self.until((1, 0))
        self.play(FadeIn(halves, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(merge, shift=UP * 0.15), run_time=0.7)
        self.until((2, 0))
        self.say(
            "Merge sort is the usual way to sort a linked list.",
            low_caption, width=11,
        )
        self.hold()
        self.play(FadeOut(halves), FadeOut(merge), run_time=0.5)

        related = Text(
            "Try next:  Merge k Sorted Lists   |   Sort List",
            font=PROSE, font_size=26,
        ).move_to([0, -2.6, 0])
        self.voice()
        self.say(
            "Also the building block for merging k sorted lists:\n"
            "merge them in pairs, or use a heap.",
            low_caption, width=11,
        )
        self.until(0.5)
        self.play(FadeIn(related, shift=UP * 0.15), run_time=0.6)
        self.hold()

        self.voice()
        self.say(
            "The dummy node removes edge cases far beyond this problem.\n"
            "That story has its own Short: link in the description.",
            low_caption, color=YELLOW, width=11,
        )
        self.play(FadeOut(related), self.dummy_part.animate.set_opacity(1), run_time=0.7)
        self.play(Indicate(self.lists.dummy, scale_factor=1.3), run_time=1.2)
        self.hold(pad=1.0)
