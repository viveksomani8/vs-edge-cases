"""Vertical YouTube Short cut from the Dutch flag video: why `equal` does not move.

It reuses the narration clips of the long video (hook, 02, 08-13) and the
drawing code in scene.py, laid out again for a 1080x1920 frame.

Render and add the narration (from the project root):
    uv run --system-certs --no-project --python 3.12 --with manim \
        python -m manim --fps 30 videos/001_dutch_flag/short.py DutchFlagShort
    uv run --system-certs --no-project --python 3.12 --with manim \
        python videos/001_dutch_flag/short.py \
        media/videos/short/1920p30/DutchFlagShort.mp4 media/short_timeline.json \
        videos/001_dutch_flag/dutch-national-flag-short.mp4
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from manim import *

from scene import (
    CHANNEL_NAME, EQUAL, EQUAL_LINES, EQUAL_PTR, GREATER, GREATER_LINES, INIT_LINES,
    LARGER_PTR, LESS, LESS_LINES, MONO, PIVOT_INDEX, PROSE, SMALLER_PTR, UNKNOWN,
    VALUES, DutchFlag, make_cell, text_color_on,
)

config.pixel_width, config.pixel_height = 1080, 1920
config.frame_width, config.frame_height = 9.0, 16.0

# Layout, top to bottom. YouTube draws its own controls over roughly the bottom
# fifth of a Short, so nothing sits below y = -4.8.
SIDE, STEP, X0 = 0.85, 0.95, -3.8  # slot 8 ("one past the end") is at x = +3.8
TITLE_Y, PIVOT_Y, ARRAY_Y, LEGEND_Y = 6.2, 5.5, 3.6, 1.45
CAPTION = [0, 0.3, 0]
CODE_WIDTH, CODE_Y = 8.0, -2.75


def slot_x(k):
    return X0 + k * STEP


class DutchFlagShort(DutchFlag):
    def construct(self):
        self.caption = None
        self.clip = 0
        self.voice_end = 0.0
        self.timeline = []
        self.hook()
        self.show_array()
        self.walkthrough()
        self.sign_off()
        timeline_path = Path(config.media_dir) / "short_timeline.json"
        timeline_path.write_text(json.dumps(self.timeline))

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

    def make_pointer(self, name, k, color, above):
        x = slot_x(k)
        if above:
            ends, side = ([x, ARRAY_Y + 1.05, 0], [x, ARRAY_Y + 0.52, 0]), UP
        else:
            ends, side = ([x, ARRAY_Y - 1.4, 0], [x, ARRAY_Y - 0.87, 0]), DOWN
        arrow = Arrow(*ends, buff=0, color=color, stroke_width=5,
                      max_tip_length_to_length_ratio=0.45)
        label = Text(name, font=MONO, font_size=24, color=color).next_to(arrow, side, buff=0.06)
        return VGroup(arrow, label)

    def step_pointer(self, pointer, slots):
        return pointer.animate.shift(RIGHT * slots * STEP)

    def build_legend(self):
        legend = VGroup()
        for words, fill in [("less", LESS), ("equal", EQUAL), ("unknown", UNKNOWN), ("greater", GREATER)]:
            swatch = Square(side_length=0.28).set_fill(fill, 1).set_stroke(WHITE, 1.5)
            label = Text(words, font=PROSE, font_size=22, color=GREY_A)
            legend.add(VGroup(swatch, label).arrange(RIGHT, buff=0.15))
        return legend.arrange(RIGHT, buff=0.5).move_to([0, LEGEND_Y, 0])

    # --------------------------------------------------------------------- hook
    def hook(self):
        pivot = VALUES[PIVOT_INDEX]
        rank = lambda v: (v > pivot) - (v < pivot)
        order = sorted(range(len(VALUES)), key=lambda k: rank(VALUES[k]))  # stable
        fills = {-1: LESS, 0: EQUAL, 1: GREATER}
        x0, y = -(len(VALUES) - 1) * STEP / 2, 3.0

        cells = VGroup(
            *[make_cell(v, side=SIDE).move_to([x0 + k * STEP, y, 0]) for k, v in enumerate(VALUES)]
        )
        claim = Text(
            "Three groups.\nIn place.\nOne pass.",
            font=PROSE, font_size=56, weight=BOLD, line_spacing=0.8,
        ).move_to([0, 0.3, 0])
        catch = Text(
            "Looks easy.\nMost people get\nthe indices wrong.",
            font=PROSE, font_size=44, color=YELLOW, line_spacing=0.8,
        ).move_to([0, -2.9, 0])

        self.voice("hook")
        self.play(FadeIn(cells, shift=DOWN * 0.2), run_time=0.6)
        for slot, k in enumerate(order):
            fill = fills[rank(VALUES[k])]
            cells[k].generate_target()
            cells[k].target.move_to([x0 + slot * STEP, y, 0])
            cells[k].target[0].set_fill(fill, 1)
            cells[k].target[1].set_color(text_color_on(fill))
        self.play(
            *[MoveToTarget(c, path_arc=PI / 3) for c in cells],
            FadeIn(claim, shift=UP * 0.15),
            run_time=1.8,
        )
        self.lead(2.6)
        self.play(FadeIn(catch, shift=UP * 0.15), run_time=0.6)
        self.hold(3.0, pad=0.3)
        self.play(FadeOut(cells), FadeOut(claim), FadeOut(catch), run_time=0.5)

    # -------------------------------------------------------------------- array
    def show_array(self):
        title = Text("Dutch National Flag", font=PROSE, font_size=44, weight=BOLD)
        title.move_to([0, TITLE_Y, 0])
        pivot_label = Text(
            f"pivot = {VALUES[PIVOT_INDEX]}", font=MONO, font_size=32, color=YELLOW
        ).move_to([0, PIVOT_Y, 0])

        self.cells = []
        indices = VGroup()
        for k, value in enumerate(VALUES):
            self.cells.append(make_cell(value, side=SIDE).move_to([slot_x(k), ARRAY_Y, 0]))
            indices.add(
                Text(str(k), font=MONO, font_size=18, color=GREY_B).move_to(
                    [slot_x(k), ARRAY_Y - 0.62, 0]
                )
            )

        self.voice("02")
        self.play(
            FadeIn(title),
            LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in self.cells], lag_ratio=0.1),
            FadeIn(indices),
            run_time=1.0,
        )
        self.play(
            self.cells[PIVOT_INDEX][0].animate.set_stroke(YELLOW, 7),
            FadeIn(pivot_label),
            run_time=0.6,
        )
        self.say(f"Here i = {PIVOT_INDEX}, so the pivot value is {VALUES[PIVOT_INDEX]}.")
        self.hold(2.0, pad=0.3)

    # -------------------------------------------------------------- walkthrough
    def walkthrough(self):
        """The first three steps of the loop: one equal, one greater, one less."""
        A = list(VALUES)
        assert A[:3] == [3, 5, 2] and A[PIVOT_INDEX] == 3, "the clips describe these values"

        panel = self.build_code()
        VGroup(panel, self.rows).scale_to_fit_width(CODE_WIDTH).move_to([0, CODE_Y, 0])
        legend = self.build_legend()
        self.highlight = self.highlight_rect(*INIT_LINES)
        self.play(
            FadeIn(panel), FadeIn(self.rows), FadeIn(legend),
            self.cells[PIVOT_INDEX][0].animate.set_stroke(WHITE, 2),
            run_time=0.8,
        )
        self.play(FadeIn(self.highlight), run_time=0.4)
        self.bring_to_front(self.rows)

        smaller, equal, larger = 0, 0, len(A)
        p_smaller = self.make_pointer("smaller", smaller, SMALLER_PTR, above=False)
        p_equal = self.make_pointer("equal", equal, EQUAL_PTR, above=True)
        p_larger = self.make_pointer("larger", larger, LARGER_PTR, above=False)
        self.voice("08")
        self.say(
            "Only the pivot's value matters now.\n"
            "smaller and equal start at 0.\n"
            "larger starts one past the end."
        )
        self.lead(1.6)
        self.play(FadeIn(p_smaller), FadeIn(p_equal), run_time=0.6)
        self.lead(2.2)
        self.play(FadeIn(p_larger), run_time=0.6)
        self.hold(2.5)

        # Step 1: A[equal] == pivot.
        self.play(Circumscribe(self.cells[equal], color=YELLOW, buff=0.06), run_time=0.7)
        self.voice("09")
        self.focus(EQUAL_LINES)
        self.say(
            f"A[equal] is {A[equal]}: equal to the pivot.\n"
            "It extends the equal block.\n"
            "Move equal one step right."
        )
        self.hold(3.0, pad=-1.6)
        equal += 1
        self.play(self.step_pointer(p_equal, 1), run_time=0.6)
        self.recolour(smaller, equal, larger)
        self.hold(0.6, pad=0.4)

        # Step 2: A[equal] > pivot. The point of the Short.
        self.play(Circumscribe(self.cells[equal], color=YELLOW, buff=0.06), run_time=0.7)
        self.voice("10")
        self.focus(GREATER_LINES)
        self.say(
            f"A[equal] is {A[equal]}: greater than the pivot.\n"
            "Move larger left, then swap\n"
            f"the {A[equal]} into the top region."
        )
        self.hold(3.0, pad=-4.0)
        larger -= 1
        self.play(self.step_pointer(p_larger, -1), run_time=0.6)
        A[equal], A[larger] = A[larger], A[equal]
        self.swap(equal, larger)
        self.recolour(smaller, equal, larger)
        self.hold(0.0)
        self.voice("11")
        self.say(
            "equal does NOT move.\n"
            f"The {A[equal]} that arrived has not\n"
            "been classified yet.",
            color=YELLOW,
        )
        self.lead(1.6)
        self.play(Circumscribe(self.cells[equal], color=YELLOW, buff=0.06), run_time=1.0)
        self.hold(3.0)
        self.hold(0.6, pad=0.4)

        # Step 3: A[equal] < pivot. Here equal does move, and why.
        self.play(Circumscribe(self.cells[equal], color=YELLOW, buff=0.06), run_time=0.7)
        self.voice("12")
        self.focus(LESS_LINES)
        self.say(f"A[equal] is {A[equal]}: less than the pivot.\nSwap it with A[smaller].")
        self.hold(2.5, pad=0.2)
        A[smaller], A[equal] = A[equal], A[smaller]
        self.swap(smaller, equal)
        self.voice("13")
        self.say(
            f"The {A[equal]} that came back is a pivot value,\n"
            "so it is already classified.\n"
            "Advance both smaller and equal.",
            color=YELLOW,
        )
        self.hold(3.5, pad=-1.5)
        smaller, equal = smaller + 1, equal + 1
        self.play(self.step_pointer(p_smaller, 1), self.step_pointer(p_equal, 1), run_time=0.6)
        self.recolour(smaller, equal, larger)
        self.hold(0.6, pad=0.4)

    def sign_off(self):
        self.play(FadeOut(self.highlight), run_time=0.3)
        self.say(f"Full walkthrough on the channel:\n{CHANNEL_NAME}", color=YELLOW)
        self.wait(2.2)


if __name__ == "__main__":
    # Add the narration: python short.py <silent.mp4> <timeline.json> <output.mp4>
    import av

    import mux_narration

    video, timeline_path, output = sys.argv[1:4]
    timeline = json.loads(Path(timeline_path).read_text())
    with av.open(video) as src:
        seconds = float(src.duration) / av.time_base
    mux_narration.mux(video, mux_narration.build_track(timeline, seconds), output)
    audio_seconds, missing = mux_narration.verify(output, timeline)
    print(f"video {seconds:.1f}s, audio {audio_seconds:.1f}s, clips {len(timeline)}, missing {missing or 'none'}")
    sys.exit(1 if missing else 0)
