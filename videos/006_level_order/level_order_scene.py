"""Animated walkthrough of level order traversal of a binary tree.

Render, save one still per beat, add the narration and write the subtitles
(from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim -qh --fps 30 videos/006_level_order/level_order_scene.py LevelOrder
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/006_level_order/stills.py \
        media/videos/level_order_scene/1080p30/LevelOrder.mp4 media/level_order_stills.json \
        videos/006_level_order/preview
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/006_level_order/mux.py \
        media/videos/level_order_scene/1080p30/LevelOrder.mp4 media/level_order_timeline.json \
        videos/006_level_order/level-order-narrated.mp4
    uv run python videos/006_level_order/subtitles.py \
        media/level_order_timeline.json videos/006_level_order/level-order-narrated.en.srt

Each beat is timed to its narration clip (audio/<name>.mp3, text in
narration.py), or to the word count of the text while the clip is not recorded.

The code on screen is level_order() from level_order.py in this folder, and
every order, list and count shown is computed by running that file's functions
on the tree drawn here, so the picture cannot drift from the code. The panel
drawing and the timing helpers come from videos/003_syntax_errors; the code
highlight and the end card from videos/001_dutch_flag.
"""

import inspect
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
import numpy as np
from manim import *

from narration import NARRATION  # before syntax_errors, which imports the same module name
from level_order import TreeNode, brute_force, chain, example_tree, level_order, walk
from syntax_errors import (
    BAD, GOOD, LEAD_IN, MONO, PANEL_FILL, PROSE, QUIET, TERMINAL_FILL, WORDS_PER_SECOND,
    Panel, SyntaxErrors,
)

config.background_color = "#101418"

AUDIO_DIR = HERE / "audio"

IDLE_FILL = "#232931"
LEVEL_FILL = ["#C8102E", "#2A5CAA", "#2E8B57", "#B8860B"]  # one colour per depth
LEVEL_TEXT = ["#FF7B7B", "#7FB2FF", "#7CE38B", YELLOW]
STACK_FILL = "#5A4FCF"

# Horizontal position of each node of example_tree(), in tree units.
NODE_X = {3: 0.0, 9: -2.0, 20: 2.0, 4: -3.0, 7: -1.0, 15: 3.0, 1: -1.6, 8: 3.6}

CODE = inspect.getsource(level_order).rstrip().splitlines()
L_RESULT, L_EMPTY, L_QUEUE, L_WHILE, L_LEVEL, L_FOR = (1, 1), (2, 3), (4, 4), (5, 5), (6, 6), (7, 7)
L_TAKE, L_VISIT, L_LEFT, L_RIGHT, L_DONE, L_RETURN = (8, 8), (9, 9), (10, 11), (12, 13), (14, 14), (15, 15)
assert CODE[8].strip() == "node = q.popleft()" and CODE[14].strip() == "result.append(level)", "code lines moved"

HOOK_CODE = [
    "todo = deque([root])",
    "while todo:",
    "    node = todo.pop()",
    "    print(node.value)",
    "    if node.left:",
    "        todo.append(node.left)",
    "    if node.right:",
    "        todo.append(node.right)",
]
HOOK_TAKE = 2

CAPTION = [4.1, -2.5, 0]       # under the code panel
SIDE_CAPTION = [3.9, 1.2, 0]   # right of the tree, while there is no code panel
QUEUE_Y, LEVEL_Y, RESULT_Y = -1.35, -2.2, -3.05
LABEL_X, VALUE_X, SLOT = -6.6, -5.0, 0.72


def depths(root):
    """value -> depth, and (parent, child) value pairs, for a tree with distinct values."""
    depth, edges, todo = {}, [], [(root, 0)]
    while todo:
        node, d = todo.pop()
        depth[node.value] = d
        for child in (node.left, node.right):
            if child:
                edges.append((node.value, child.value))
                todo.append((child, d + 1))
    return depth, edges


class Board:
    """The example tree, and the queue drawn as a row of tokens under it.

    Tokens never move: taking from the front dims the token and moves the
    `front` marker, which is what a deque does (nothing shifts).
    """

    def __init__(self, root, origin=(-3.6, 2.7), sx=0.82, sy=0.95, radius=0.33):
        self.root, self.radius = root, radius
        self.depth, self.edges = depths(root)
        self.by_value = {}
        todo = [root]
        while todo:
            node = todo.pop()
            self.by_value[node.value] = node
            todo += [child for child in (node.left, node.right) if child]

        self.pos = {
            v: np.array([origin[0] + NODE_X[v] * sx, origin[1] - d * sy, 0.0]) for v, d in self.depth.items()
        }
        self.nodes = {}
        for v, at in self.pos.items():
            circle = Circle(radius=radius).set_fill(IDLE_FILL, 1).set_stroke(GREY_B, 3)
            label = Text(str(v), font=PROSE, font_size=26, weight=BOLD)
            self.nodes[v] = VGroup(circle, label).move_to(at)
        self.lines = VGroup()
        for parent, child in self.edges:
            a, b = self.pos[parent], self.pos[child]
            unit = (b - a) / np.linalg.norm(b - a)
            self.lines.add(Line(a + unit * radius, b - unit * radius, color=GREY_B, stroke_width=3))
        self.tree = VGroup(self.lines, *self.nodes.values())

        self.queue_label = Text("queue", font=MONO, font_size=22, color=GREY_A)
        self.queue_label.move_to([LABEL_X, QUEUE_Y, 0], aligned_edge=LEFT)
        self.front = Text("front", font=MONO, font_size=18, color=YELLOW)
        self.tokens, self.taken = [], 0
        self.front.move_to(self.slot(0) + DOWN * 0.58)

    # ---------------------------------------------------------------- geometry
    def slot(self, k):
        return np.array([VALUE_X + 0.3 + k * SLOT, QUEUE_Y, 0.0])

    def level(self, d):
        return [v for v in walk(self.root, from_front=True) if self.depth[v] == d]

    def waiting(self):
        return [value for value, _ in self.tokens[self.taken:]]

    # -------------------------------------------------------------- animations
    def restyle(self, value, fill=None, stroke=None):
        """Animation that recolours a node; the whole node moves so the number stays on top."""
        node = self.nodes[value]
        node.generate_target()
        if fill is not None:
            node.target[0].set_fill(fill, 1)
        if stroke is not None:
            node.target[0].set_stroke(stroke, 4)
        return MoveToTarget(node)

    def enqueue(self, value):
        token = VGroup(
            Circle(radius=0.27).set_fill(IDLE_FILL, 1).set_stroke(YELLOW, 3),
            Text(str(value), font=PROSE, font_size=22, weight=BOLD),
        ).move_to(self.slot(len(self.tokens)))
        self.tokens.append((value, token))
        return [FadeIn(token, target_position=self.pos[value]), self.restyle(value, stroke=YELLOW)]

    def dequeue(self):
        """Take the front token; returns its value and the animations."""
        value, token = self.tokens[self.taken]
        self.taken += 1
        anims = [token.animate.set_opacity(0.25), self.front.animate.move_to(self.slot(self.taken) + DOWN * 0.58)]
        return value, anims

    def visit(self, value):
        return self.restyle(value, fill=LEVEL_FILL[self.depth[value]], stroke=WHITE)

    def reset(self):
        """Animations that return the tree and the queue to their starting state."""
        anims = [FadeOut(token) for _, token in self.tokens]
        anims += [self.restyle(v, fill=IDLE_FILL, stroke=GREY_B) for v in self.nodes]
        anims.append(self.front.animate.move_to(self.slot(0) + DOWN * 0.58))
        self.tokens, self.taken = [], 0
        return anims


class LevelOrder(SyntaxErrors):
    def construct(self):
        self.caption = None
        self.clip = 0
        self.voice_start = self.voice_end = 0.0
        self.timeline, self.stills = [], []
        self.board = Board(example_tree())
        assert level_order(self.board.root) == [self.board.level(d) for d in range(4)]
        self.hook()
        self.problem()
        self.brute()
        self.idea()
        self.walkthrough()
        self.edge_cases()
        self.complexity()
        self.uses()
        self.end_card()
        media = Path(config.media_dir)
        (media / "level_order_timeline.json").write_text(json.dumps(self.timeline))
        (media / "level_order_stills.json").write_text(json.dumps(self.stills))
        estimated = [name for name, *_ in self.timeline if not (AUDIO_DIR / f"{name}.mp3").exists()]
        if estimated:
            print(f"Preview timing: {len(estimated)} of {len(self.timeline)} clips are not recorded yet.")

    # ------------------------------------------------------------------ helpers
    def voice(self, name=None):
        """As in the syntax video, but with this video's clips."""
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

    def note(self, text, color=WHITE, pos=CAPTION, width=5.6):
        self.say(text, pos, color=color, width=width)

    def value_text(self, text, y, color=WHITE, size=24):
        return Text(text, font=MONO, font_size=size, color=color).move_to([VALUE_X, y, 0], aligned_edge=LEFT)

    def row_label(self, words, y):
        return Text(words, font=MONO, font_size=22, color=GREY_A).move_to([LABEL_X, y, 0], aligned_edge=LEFT)

    def swap(self, name, text, y, color=WHITE, size=24):
        """Replace the text shown in a state row (self.level_text / self.result_text)."""
        new = self.value_text(text, y, color, size)
        old = getattr(self, name)
        setattr(self, name, new)
        return [FadeOut(old), FadeIn(new)]

    # --------------------------------------------------------------------- hook
    def hook(self):
        """One loop, two orders: the only change is which end the node is taken from."""
        board = self.board
        code = Panel(HOOK_CODE, [3.9, 1.3, 0], 5.8, 3.6, font_size=26)
        mark = code.rows[HOOK_TAKE][0].copy().set_fill(YELLOW, 0.22)
        order = Text("", font=MONO, font_size=24)

        def light(values, fill):
            return LaggedStart(*[board.restyle(v, fill=fill(v), stroke=WHITE) for v in values], lag_ratio=0.6)

        self.play(FadeIn(board.tree), FadeIn(code.box), FadeIn(mark), FadeIn(code.rows), run_time=0.7)
        self.wait(LEAD_IN - 0.7)
        self.voice("hook")
        self.until(0.3)
        stack_order = walk(board.root, from_front=False)
        self.play(light(stack_order, lambda v: STACK_FILL), run_time=2.6)
        self.note("pop(): it dives down one branch.", pos=[3.9, -1.5, 0])
        self.until(0.62)
        self.play(
            Transform(code.rows[HOOK_TAKE][1], code.text(HOOK_TAKE, "    node = todo.popleft()", GOOD)),
            *[board.restyle(v, fill=IDLE_FILL, stroke=GREY_B) for v in board.nodes],
            run_time=0.7,
        )
        queue_order = walk(board.root, from_front=True)
        self.play(light(queue_order, lambda v: LEVEL_FILL[board.depth[v]]), run_time=2.6)
        self.note("popleft(): level by level.", color=YELLOW, pos=[3.9, -1.5, 0])
        self.hold(pad=0.6)
        self.play(
            *[FadeOut(m) for m in (code.box, code.rows, mark, self.caption)],
            *[board.restyle(v, fill=IDLE_FILL, stroke=GREY_B) for v in board.nodes],
            run_time=0.6,
        )
        self.caption = None

    # ------------------------------------------------------------------ problem
    def problem(self):
        board = self.board
        self.title = Text("Level Order Traversal", font=PROSE, font_size=32, weight=BOLD)
        self.title.move_to([-6.6, 3.65, 0], aligned_edge=LEFT)
        expected = level_order(board.root)
        lines = []
        for d, level in enumerate(expected):
            opening = "[[" if d == 0 else " ["
            closing = "]]" if d == len(expected) - 1 else "],"
            lines.append((opening + ", ".join(map(str, level)) + closing, LEVEL_TEXT[d]))
        self.answer = Panel(lines, [3.9, 1.2, 0], 5.0, 2.6, fill=TERMINAL_FILL, font_size=32)
        tab = self.answer.tab("return")

        self.voice()
        self.play(Write(self.title), run_time=1.0)
        self.until(0.42)
        self.play(FadeIn(self.answer.box), FadeIn(tab), run_time=0.5)
        for d in range(len(expected)):
            self.play(
                *[board.restyle(v, fill=LEVEL_FILL[d], stroke=WHITE) for v in board.level(d)],
                FadeIn(self.answer.rows[d]),
                run_time=0.6,
            )
        self.note("One list per level:\ntop to bottom, left to right.", pos=[3.9, -1.4, 0])
        self.hold()
        self.answer_tab = tab

    # -------------------------------------------------------------- brute force
    def brute(self):
        board = self.board
        everything = walk(board.root, from_front=False)
        result, total = brute_force(board.root)
        per_pass = len(everything)
        counter = Text("nodes visited: 0", font=MONO, font_size=28, color=GREY_A).move_to([-3.6, -1.6, 0])

        self.voice()
        self.play(
            *[board.restyle(v, fill=IDLE_FILL, stroke=GREY_B) for v in board.nodes],
            *[row.animate.set_opacity(0.25) for row in self.answer.rows],
            FadeIn(counter),
            run_time=0.6,
        )
        self.note("Brute force: one walk of the whole tree\nfor each depth.", pos=[3.9, -1.4, 0])
        for d in range(len(result)):
            self.until(0.12 + d * 0.15)
            new = Text(f"nodes visited: {(d + 1) * per_pass}", font=MONO, font_size=28, color=GREY_A)
            new.move_to(counter)
            self.play(
                LaggedStart(*[Indicate(board.nodes[v], scale_factor=1.25, color=WHITE) for v in everything], lag_ratio=0.25),
                run_time=1.2,
            )
            self.play(
                *[board.restyle(v, fill=LEVEL_FILL[d], stroke=WHITE) for v in board.level(d)],
                self.answer.rows[d].animate.set_opacity(1),
                FadeOut(counter), FadeIn(new),
                run_time=0.5,
            )
            counter = new
        self.until(0.74)
        self.note(
            f"{len(result)} walks to place {per_pass} nodes.\nOn a chain of n nodes: O(n²).",
            color=YELLOW, pos=[3.9, -1.4, 0],
        )
        self.hold()
        self.play(
            *[FadeOut(m) for m in (counter, self.answer.box, self.answer.rows, self.answer_tab, self.caption)],
            *[board.restyle(v, fill=IDLE_FILL, stroke=GREY_B) for v in board.nodes],
            run_time=0.6,
        )
        self.caption = None

    # --------------------------------------------------------------------- idea
    def take(self, run_time=0.5):
        """Take the front node and visit it; returns its value."""
        value, anims = self.board.dequeue()
        self.play(*anims, self.board.visit(value), run_time=run_time)
        return value

    def add_children(self, value, run_time=0.5):
        node = self.board.by_value[value]
        for child in (node.left, node.right):
            if child:
                self.play(*self.board.enqueue(child.value), run_time=run_time)

    def idea(self):
        board = self.board
        self.voice()
        self.note("Never go back: keep a queue of nodes\nfound, but not visited yet.", pos=SIDE_CAPTION)
        self.play(FadeIn(board.queue_label), FadeIn(board.front), run_time=0.5)
        self.play(*board.enqueue(board.root.value), run_time=0.5)
        self.until(0.4)
        # The first two levels, so that the queue is left holding the third.
        for _ in range(3):
            self.add_children(self.take())
            if _ == 0:
                self.note("Take from the front. Visit it.\nAdd its children at the back.", pos=SIDE_CAPTION)
        self.hold()

        waiting = board.waiting()
        assert waiting == board.level(2), "the queue should hold exactly the third level here"
        tokens = VGroup(*[token for _, token in board.tokens[board.taken:]])
        frame = SurroundingRectangle(tokens, color=YELLOW, buff=0.08, stroke_width=4)
        size = Text(f"len(q) = {len(waiting)}", font=MONO, font_size=24, color=YELLOW)
        size.next_to(frame, RIGHT, buff=0.3)
        self.voice()
        self.note("Where does a level end?", pos=SIDE_CAPTION)
        self.until(0.36)
        self.play(Create(frame), run_time=0.6)
        self.play(*[Indicate(board.nodes[v], scale_factor=1.25, color=YELLOW) for v in waiting], run_time=1.0)
        self.note(
            "Before a pass starts, the queue holds\nexactly one level. Its length says\nhow many nodes to take.",
            color=YELLOW, pos=SIDE_CAPTION,
        )
        self.until(0.8)
        self.play(FadeIn(size), run_time=0.4)
        self.hold()
        self.play(*board.reset(), FadeOut(frame), FadeOut(size), FadeOut(self.caption), run_time=0.7)
        self.caption = None

    # -------------------------------------------------------------- walkthrough
    def step(self, at):
        """One pass of the inner loop: take a node, record it, add its children."""
        board = self.board
        self.until(at)
        self.focus(L_TAKE)
        value, anims = board.dequeue()
        self.play(*anims, board.restyle(value, stroke=WHITE), run_time=0.4)
        self.focus(L_VISIT)
        self.level_values.append(value)
        self.play(
            board.visit(value),
            *self.swap("level_text", str(self.level_values), LEVEL_Y, LEVEL_TEXT[board.depth[value]]),
            run_time=0.4,
        )
        node = board.by_value[value]
        for child, lines in ((node.left, L_LEFT), (node.right, L_RIGHT)):
            if child:
                self.focus(lines)
                self.play(*board.enqueue(child.value), run_time=0.4)

    def run_pass(self, cues):
        """One pass of the while loop: exactly the nodes waiting when it starts."""
        board = self.board
        count = len(board.waiting())
        assert count == len(cues), "one cue per node of this level"
        self.focus(L_LEVEL)
        self.level_values = []
        self.play(*self.swap("level_text", "[]", LEVEL_Y), run_time=0.3)
        self.focus(L_FOR)
        for at in cues:
            self.step(at)
        self.focus(L_DONE)
        self.result_values.append(self.level_values)
        self.play(*self.swap("result_text", str(self.result_values), RESULT_Y, size=22), run_time=0.4)

    def walkthrough(self):
        board = self.board
        code = Panel(CODE, [4.1, 1.0, 0], 5.6, 4.4)
        self.rows, self.highlight = code.rows, None
        self.highlight = self.highlight_rect(*L_RESULT)
        level_label, result_label = self.row_label("level", LEVEL_Y), self.row_label("result", RESULT_Y)
        self.level_text = self.value_text("", LEVEL_Y)
        self.result_text = self.value_text("[]", RESULT_Y, size=22)
        self.result_values = []

        self.voice()
        self.play(
            FadeIn(code.box), FadeIn(self.highlight), FadeIn(code.rows),
            FadeIn(level_label), FadeIn(result_label), FadeIn(self.result_text),
            run_time=0.7,
        )
        self.until(0.12)
        self.focus(L_QUEUE)
        self.play(*board.enqueue(board.root.value), run_time=0.5)
        self.note("The queue starts with the root.\nlen(q) is 1: take one node.")
        self.focus(L_WHILE)
        self.run_pass([0.38])
        self.hold()

        self.voice()
        self.note("len(q) is 2: the whole second level.\nTake two nodes, then stop.")
        self.focus(L_WHILE)
        self.run_pass([0.2, 0.52])
        self.hold()

        self.voice()
        self.note("len(q) is 3. Take three.\n4 has no children: nothing is added.")
        self.focus(L_WHILE)
        self.run_pass([0.22, 0.42, 0.62])
        self.hold()

        self.voice()
        self.note("Two nodes left, and no children.")
        self.focus(L_WHILE)
        self.run_pass([0.16, 0.36])
        self.until(0.62)
        self.play(FadeOut(board.front), run_time=0.3)
        self.focus(L_WHILE)
        self.note("The queue is empty: the loop ends.\nOne list for each level.", color=YELLOW)
        self.focus(L_RETURN)
        self.hold()
        assert self.result_values == level_order(board.root)

        self.code = code
        self.play(
            *[FadeOut(m) for m in (board.tree, board.queue_label, board.front, level_label, result_label,
                                   self.level_text, self.result_text, self.caption)],
            *[FadeOut(token) for _, token in board.tokens],
            run_time=0.7,
        )
        self.caption = None

    # --------------------------------------------------------------- edge cases
    def case(self, title, drawing, result, x):
        heading = Text(title, font=PROSE, font_size=24, weight=BOLD).move_to([x, 2.7, 0])
        drawing.move_to([x, 1.2, 0])
        answer = Text(str(result), font=MONO, font_size=22, color=YELLOW).move_to([x, -0.6, 0])
        return VGroup(heading, drawing), answer

    def small_node(self, value, at=ORIGIN):
        circle = Circle(radius=0.3).set_fill(IDLE_FILL, 1).set_stroke(GREY_B, 3)
        return VGroup(circle, Text(str(value), font=PROSE, font_size=22, weight=BOLD)).move_to(at)

    def edge_cases(self):
        nothing = Text("None", font=MONO, font_size=28, color=GREY_B)
        single = self.small_node(5)
        points = [np.array([-0.5, 0.75, 0]), np.array([0.0, 0.0, 0]), np.array([0.5, -0.75, 0])]
        links = VGroup()
        for a, b in zip(points, points[1:]):
            unit = (b - a) / np.linalg.norm(b - a)
            links.add(Line(a + unit * 0.3, b - unit * 0.3, color=GREY_B, stroke_width=3))
        long_chain = VGroup(links, *[self.small_node(k + 1, at) for k, at in enumerate(points)])
        cases = [
            self.case("Empty tree", nothing, level_order(None), -5.5),
            self.case("Single node", single, level_order(TreeNode(5)), -3.2),
            self.case("One long chain", long_chain, level_order(chain(3)), -0.7),
        ]

        self.voice()
        self.note("Edge cases")
        for (picture, answer), at, lines in zip(cases, (0.14, 0.44, 0.62), (L_EMPTY, L_WHILE, L_FOR)):
            self.until(at)
            self.play(FadeIn(picture, shift=UP * 0.15), run_time=0.5)
            self.focus(lines)
            self.play(FadeIn(answer), run_time=0.4)
        self.hold()
        self.play(*[FadeOut(m) for pair in cases for m in pair], FadeOut(self.caption), run_time=0.6)
        self.caption = None

    # --------------------------------------------------------------- complexity
    def complexity(self):
        def line(label, value, detail, y):
            name = Text(label, font=PROSE, font_size=34, weight=BOLD).move_to([-6.2, y, 0], aligned_edge=LEFT)
            big = Text(value, font=MONO, font_size=40, weight=BOLD, color=YELLOW).move_to([-3.4, y, 0], aligned_edge=LEFT)
            why = Text(detail, font=PROSE, font_size=26, color=GREY_A, line_spacing=0.7)
            why.move_to([-6.2, y - 0.95, 0], aligned_edge=LEFT)
            return VGroup(name, big), why

        time, time_why = line("Time", "O(n)", "every node enters the queue once,\nand leaves it once", 2.2)
        space, space_why = line("Space", "O(w)", "w = the widest level.\nThe queue holds at most two levels.", -0.3)

        self.voice()
        self.play(FadeOut(self.highlight), run_time=0.3)
        self.play(FadeIn(time, shift=UP * 0.15), run_time=0.5)
        self.until(0.14)
        self.play(FadeIn(time_why), run_time=0.4)
        self.until(0.48)
        self.play(FadeIn(space, shift=UP * 0.15), run_time=0.5)
        self.until(0.62)
        self.play(FadeIn(space_why), run_time=0.4)
        self.hold()
        self.play(*[FadeOut(m) for m in (time, time_why, space, space_why, self.code.box, self.code.rows)], run_time=0.6)

    # --------------------------------------------------------------------- uses
    def uses(self):
        def chip(words, y, color=WHITE):
            box = RoundedRectangle(width=9.0, height=0.9, corner_radius=0.12)
            box.set_fill(PANEL_FILL, 1).set_stroke(color, 2).move_to([0, y, 0])
            return VGroup(box, Text(words, font=PROSE, font_size=28, color=color).move_to(box))

        heading = Text("Breadth-first search", font=PROSE, font_size=40, weight=BOLD, color=YELLOW)
        heading.move_to([0, 2.6, 0])
        chips = [
            chip("Shortest path in a maze or a graph", 1.2),
            chip("Zigzag traversal  |  Right side view", 0.0),
            chip("Minimum depth of a tree", -1.2),
        ]

        self.voice()
        self.until(0.14)
        self.play(FadeIn(heading, shift=UP * 0.15), run_time=0.5)
        for item, at in zip(chips, (0.34, 0.62, 0.8)):
            self.until(at)
            self.play(FadeIn(item, shift=UP * 0.15), run_time=0.5)
        self.hold()
        self.play(*[FadeOut(m) for m in (heading, *chips)], run_time=0.5)

        def choice(code, meaning, color, y):
            left = Text(code, font=MONO, font_size=40, weight=BOLD, color=color).move_to([-5.0, y, 0], aligned_edge=LEFT)
            right = Text(meaning, font=PROSE, font_size=34).move_to([0.6, y, 0], aligned_edge=LEFT)
            return VGroup(left, right)

        queue = choice("q.popleft()", "level by level", GOOD, 1.0)
        stack = choice("q.pop()", "depth first", QUIET, -0.4)
        last = Text("Same loop. One word.", font=PROSE, font_size=36, weight=BOLD, color=YELLOW).move_to([0, -2.2, 0])

        self.voice()
        self.play(FadeIn(queue), run_time=0.5)
        self.until(0.3)
        self.play(FadeIn(stack), run_time=0.5)
        self.until(0.66)
        self.play(FadeIn(last, shift=UP * 0.15), run_time=0.5)
        self.hold(pad=0.8)
