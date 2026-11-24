# YouTube upload notes: import is not #include (Short)

Video file: `import-is-not-include-short.mp4` (1:07, 1080x1920)
Subtitles: `import-is-not-include-short.en.srt`
Playlist: Python for Programmers Who Already Code

## Title (pick one)

1. Python's import Is Not #include #shorts
2. Why import Gives You a NameError in Python #shorts
3. Python Can't Find the File Right Next to It #shorts

## Description (paste everything between the lines)

---

In C, #include pastes a file into yours. In PHP, require does the same. Python's import does not, and that causes three surprises.

1. import gives you one name: the module.
After `import tree_node`, the class is `tree_node.TreeNode`. Using `TreeNode` on its own is a NameError. To get the bare name, write `from tree_node import TreeNode`.

2. Python looks in the folder of the script you ran.
#include "x.h" and PHP's require __DIR__ look next to the file that asks. Python does not: a file inside utils/ that imports its neighbour with `from tree_node import TreeNode` fails with ModuleNotFoundError when you run main.py from the folder above. Spell the path from the folder of the script you ran: `from utils.tree_node import TreeNode`.

3. A file name is a module name.
`import tree-node` and `import 01_test_utils` are both a SyntaxError. Use letters, digits and underscores, and never start with a digit.

Kept simple for a Short: Python also searches the standard library and installed packages, and inside a package you can write a relative import, `from .tree_node import TreeNode`.

Full video on what Python does with habits from C, C++, Java and PHP: (paste the main video's link here)

Narration is a synthetic voice.

#python #shorts #programming #learnpython

---

## Tags

python import, python import vs include, python modulenotfounderror, python nameerror import, from import python, python import from another folder, python module names, python for c programmers, python for php developers, python tips, python shorts, learn python

## Upload checklist

- Add it to the playlist "Python for Programmers Who Already Code".
- Set "Python Won't Tell You" as the Related video so the link shows on the Shorts player, and paste its link into the description above.
- It runs 1:07. YouTube accepts Shorts up to three minutes, so it still publishes as a Short.
- Category: Education. Language: English.
- Check YouTube's altered/synthetic content question in the upload flow for the AI narration.
- The error messages on screen were produced with Python 3.14.4 on 2026-11-24 (see the top of `narration.py`). Long messages are wrapped and paths trimmed.
