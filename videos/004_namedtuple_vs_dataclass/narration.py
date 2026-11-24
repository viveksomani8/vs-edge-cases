"""Narration script for the Short "NamedTuple or @dataclass?".

One entry per audio clip, keyed by the file stem under audio/. The text is
written for the voice ("named tuple", "data class"); subtitles.py swaps in the
real spellings for the .srt file.
"""

NARRATION = {
    "hook": "In C, you would write a struct. Python has two ways to do it, and they are not the same.",
    # What a NamedTuple is
    "01": "First, named tuple. It is a tuple whose fields have names. You list the fields, and Python writes the constructor. Read a field by name, or by position. But once it is created, it cannot be changed.",
    # What a dataclass is
    "02": "Second, data class. It is an ordinary class, where Python writes the boilerplate for you: the constructor, the printout, and the equality check. And its fields can be changed.",
    # The comparison
    "03": "So compare them. Assign to a field: the named tuple raises an error, the data class is fine. Unpack it into two names: the named tuple works, the data class does not. Use it as a dictionary key: again, only the named tuple.",
    # The rule
    "04": "The rule: if it never changes after it is created, use a named tuple. If its fields get reassigned, use a data class. A stack entry is the first. A linked list node, whose next pointer keeps moving, is the second.",
}

# Spoken form -> what the subtitle should show.
SUBTITLE_SPELLINGS = [
    ("named tuple", "NamedTuple"),
    ("data class", "@dataclass"),
]
