"""Narration script for the Short "import is not #include".

One entry per audio clip, keyed by the file stem under audio/. The text is
written for the voice ("hash include", "tree node"); subtitles.py swaps in the
real spellings for the .srt file.

Every error message on screen was produced on this machine with Python 3.14.4
on 2026-11-24, from a three-file copy of src/epi/tree_node.py and
src/epi/test_utils/utils.py.
"""

NARRATION = {
    "hook": "In C, hash include pastes a file into yours. In PHP, require does the same. Python's import does not.",
    # import gives you one name
    "01": "Import tree node, then use the class, and you get a name error. Import gave you one name: the module. The class is still inside it.",
    # Two ways to reach it
    "02": "So reach the class through the module, with a dot. Or use from, import, to bring in that one name.",
    # Where Python looks
    "03": "Second surprise. This file imports its neighbour, in the same folder, and Python cannot find it. Include looks next to the file that asks. Python looks in the folder of the script you ran.",
    "04": "So write the path from that folder: utils, dot, tree node.",
    # File names
    "05": "One more. A file name is a module name. So no hyphens, and no leading digits. Use underscores.",
    # The rule
    "06": "So. Import gives you a module, not its contents. Paths start from the script you ran. And name your files like variables.",
}

# Spoken form -> what the subtitle should show. Longer phrases first.
SUBTITLE_SPELLINGS = [
    ("utils, dot, tree node", "utils.tree_node"),
    ("hash include", "#include"),
    ("from, import,", "from … import"),
    ("tree node", "tree_node"),
    ("a name error", "a NameError"),
]
