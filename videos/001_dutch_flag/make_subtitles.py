"""Write an .srt subtitle file from the narration script and the clip timeline.

Usage:
    python make_subtitles.py <narration_timeline.json> <output.srt>

Each clip's text is split into sentences; a clip's time span is shared between
its sentences in proportion to their length, so cue timing inside a clip is
approximate (clip start and end are exact).
"""

import json
import re
import sys
from pathlib import Path

NARRATION = {
    "hook": "Rearrange an array into three groups, in place, in a single pass. It looks easy. But most people get the indices wrong.",
    "01": "The Dutch national flag problem. You are given an array, A, and an index, i. Rearrange the array around the value at that index.",
    "02": "Here, i is three, so the pivot value is three.",
    "03": "The goal: every smaller value first, then the values equal to the pivot, then the larger ones. And it should take linear time, and constant extra space.",
    "04": "The brute force way is to copy the values into three lists: lower, equal, and higher. Then join them.",
    "05": "That is correct, but the three lists cost extra space, proportional to the size of the array.",
    "06": "A better idea is to keep four regions inside the same array: less than the pivot, equal to it, unknown, and greater. Three indices, called smaller, equal, and larger, mark the boundaries.",
    "07": "Each step classifies one unknown element, so the unknown region shrinks until it is empty.",
    "08": "From here, only the pivot's value matters. Smaller and equal both start at zero. Larger starts one past the end.",
    "09": "The element at equal is three, the same as the pivot. It extends the equal block, so equal moves one step right.",
    "10": "Next is five, which is greater than the pivot. Move larger one step left, then swap the five into the top region.",
    "11": "Notice that equal does not move. The two that just arrived has not been classified yet.",
    "12": "Two is less than the pivot, so swap it with the element at smaller.",
    "13": "The three that came back is a pivot value, so it is already classified. Both smaller and equal advance.",
    "14": "Two again: less than the pivot. Swap, and advance both.",
    "15": "Three equals the pivot. Equal moves right.",
    "16": "One is less than the pivot. Swap it down, and advance both.",
    "17": "Five is greater. Move larger left, and swap. Equal stays put.",
    "18": "The three that arrived equals the pivot, so equal moves right.",
    "19": "Equal has now reached larger. No unknown elements are left, and the loop ends.",
    "20": "One pass over the array is linear time. And three indices, with no extra list, is constant space.",
    "21": "So, where is this used? In quicksort. After one partition, every value equal to the pivot is already in its final place. Only the smaller and the larger parts still need sorting.",
    "22": "A plain two-way partition would sort those equal values again and again. That is why a three-way partition is used when the data has many duplicates.",
    "23": "The same step also finds the median, or the k-th smallest value, without sorting everything.",
    "24": "And why do interviewers ask it? The idea is simple, but the index bookkeeping is easy to get wrong. The fix is to state the invariant first: four regions, three boundaries. Then every line of the loop only has to keep it true.",
    "25": "The same habit solves related problems, like sort colors, move zeros to the end, and remove duplicates in place.",
    "outro": "Thanks for watching. Subscribe to Edge Cases for more Python, algorithms, and system design, explained visually.",
}

MAX_CUE_CHARS = 84  # two lines of about 42 characters


def stamp(seconds):
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def pieces(text):
    """Sentences, with any sentence longer than a cue split at a comma or colon."""
    out = []
    for sentence in re.split(r"(?<=[.?!])\s+", text.strip()):
        while len(sentence) > MAX_CUE_CHARS:
            cut = max(sentence.rfind(", ", 0, MAX_CUE_CHARS), sentence.rfind(": ", 0, MAX_CUE_CHARS))
            if cut < 20:
                cut = sentence.rfind(" ", 0, MAX_CUE_CHARS) - 1
            out.append(sentence[: cut + 1])
            sentence = sentence[cut + 2 :]
        out.append(sentence)
    # Merge very short sentences into the previous cue when they fit.
    merged = []
    for piece in out:
        if merged and len(merged[-1]) + 1 + len(piece) <= MAX_CUE_CHARS and len(piece) < 28:
            merged[-1] += " " + piece
        else:
            merged.append(piece)
    return merged


def two_lines(text):
    if len(text) <= 42:
        return text
    middle = len(text) // 2
    spaces = [i for i, ch in enumerate(text) if ch == " "]
    split = min(spaces, key=lambda i: abs(i - middle))
    return text[:split] + "\n" + text[split + 1 :]


def main(timeline_path, output_path):
    timeline = json.loads(Path(timeline_path).read_text())
    cues = []
    for clip, start, end in timeline:
        parts = pieces(NARRATION[clip])
        total = sum(len(p) for p in parts)
        at = start
        for part in parts:
            span = (end - start) * len(part) / total
            cues.append((at, at + span, part))
            at += span
    lines = []
    for n, (start, end, text) in enumerate(cues, 1):
        lines += [str(n), f"{stamp(start)} --> {stamp(end - 0.05)}", two_lines(text), ""]
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(cues)} cues, last ends at {stamp(cues[-1][1])}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
