"""Narration script for the Short "Stack and queue in Python".

One entry per audio clip, keyed by the file stem under audio/. The text is
written for the voice ("a deck", "pop zero"); subtitles.py swaps in the real
spellings for the .srt file.
"""

# Measured on this machine with Python 3.12.13 on 2026-11-23: a queue of
# 200,000 integers drained from the front, median of 3 runs (list) and 5 runs
# (deque): list.pop(0) 5.309 s, deque.popleft() 9.23 ms. Clips 02 and 03 quote
# these figures, so change both together.
TIMING = {"items": "200,000", "list": "5.3 s", "deque": "9 ms"}

NARRATION = {
    "hook": "Coming from C plus plus or PHP, you write a stack class in Python. You do not need it. Python already has one.",
    # The list is the stack
    "01": "A list is the stack. Append pushes. Minus one peeks at the top. Pop takes the last item. All of it happens at the end of the list, so nothing else has to move.",
    # A queue on a list: correct, and slow
    "02": "A queue takes from the front. With a list, that is pop zero. The answer is correct. But every item behind it shifts one place left. Drain two hundred thousand items this way, and on this machine it takes about five seconds.",
    # deque
    "03": "So use a deck, from the collections module. Pop left takes the front, and nothing else moves. The same job takes nine milliseconds.",
    # When a class is worth writing
    "04": "So when do you write the class? When it adds something. To limit callers to push and pop. Or to add behaviour, like a stack that also knows its minimum.",
    # The rule
    "05": "So. For a stack, use a list. For a queue, use a deck. And write a class only when it earns its place.",
}

# Spoken form -> what the subtitle should show.
SUBTITLE_SPELLINGS = [
    ("C plus plus", "C++"),
    ("a deck", "a deque"),
    ("pop left", "popleft()"),
    ("pop zero", "pop(0)"),
    ("minus one", "[-1]"),
]
