"""Narration script for the syntax-mistakes video ("Python won't tell you").

DRAFT, not recorded. One entry per audio clip, keyed by the file stem under
audio/, as in the merge video. The scene times each beat from the word count
until its clip exists, so this file is the single place to edit the wording.

Source material: research/02-syntax-errors-comprehensive.md (IDs in comments).
"""

NARRATION = {
    "hook": "This Python file has five mistakes. Run it, and Python tells you about exactly one.",
    # What the video is about
    "01": "If you are coming from C, C plus plus, Java or PHP, your hands already know a syntax. Python will reject some of it, crash on some of it, and silently accept the rest.",
    "02": "So we will sort the mistakes by when you find out. One: Python refuses to start. Two: it fails when the line runs. Three: it says nothing at all.",

    # ------------------------------------------------ 1: refuses to start
    # Missing colon (A1)
    "03": "Start with the one Python did report. In C or PHP, parentheses and braces mark the block. In Python, the colon does. Leave it out, and nothing in the file runs. Not even line one.",
    # Indentation (A2, A5, A6, A7)
    "04": "Braces are gone too. In Python, the indentation is the block. One line that does not line up, or a tab mixed in with spaces, and again the file will not start.",
    # First-day habits (A9, A11, A19, A21, B1)
    "05": "The rest of this group are the same kind of habit. Double ampersand becomes and. Plus plus becomes plus equals one. Else if becomes elif. The three part for loop becomes a range. And null becomes None, with a capital N. But look at that last one. It is not a syntax error. The file starts, and fails later. That is the second kind.",

    # ------------------------------------------ 2: fails when the line runs
    # Colon fixed; "main" makes the run silent (C2), parked for part 3
    "06": "Back to our file. Add the colon, and run it again. No error. But no output either. Nothing ran. That silence is the third kind, and we will come back to it. For now, the fix is two underscores on each side of main.",
    # Index assignment on an empty list (B29)
    "07": "Run again. Now the file starts, and crashes inside push. In C, you write into an array by index. In PHP, assigning to an index creates the slot. A Python list never grows that way. You append.",
    # Names and classes are only checked when the line runs (B4)
    "08": "Run again. Thirty, twenty. It works. And this is the trap. Two mistakes are still in the file, in lines that have not run yet. A C compiler checks every line before the program starts. Python checks a line when it runs it.",
    # Exception class without a base (B24)
    "09": "So make those lines run. Pop a third time, from an empty stack. Type error: exceptions must derive from BaseException. In C plus plus you can throw anything. In Python, an exception class has to inherit from Exception.",
    # Undefined name in the except branch (B4)
    "10": "Run again. The except branch runs for the first time, and finds a name that was never defined. One wrong letter, sitting there since the first version. Fix it, and the file is finally clean.",
    # More of the same kind (B2, B12, B18, B23, B21)
    "11": "The same kind shows up everywhere. Lowercase true. Calling length as a method. Adding a number to a string. Forgetting self in a method. Dividing with one slash, and using the result as an index. All of them start fine, and fail when the line runs. So the rule is: make every branch run at least once.",

    # ------------------------------------------------- 3: says nothing
    # "main" (C2)
    "12": "Now the third kind: no error at all. Remember the silence? The name is compared with the wrong string, so the condition is simply false. Python has no complaint. Your program just does nothing.",
    # ++i (C1)
    "13": "Plus plus i is legal Python. It is a plus sign, applied twice. The value does not change, and nothing warns you. As the counter of a while loop, that is an infinite loop.",
    # range end, true division (C8, C6)
    "14": "Range one to five stops at four. The end is never included. And five divided by two is two point five. For integer division, use two slashes.",
    # Aliasing (C15)
    "15": "Assignment does not copy. In PHP, and with a C plus plus vector, b equals a gives you a second array. In Python, both names point at the same list. Change one, and the other changes too.",
    # Mutable default argument (C18)
    "16": "And a default argument is created once, not once per call. Give a function an empty list as a default, and every call shares that one list.",

    # --------------------------------------------------------- wrap-up
    # Myths (Part D)
    "17": "Two things that are not mistakes. A semicolon at the end of a line is legal. So are parentheses around a condition. Some lists online call them syntax errors. They are not. They are just noise.",
    "18": "Put the three kinds side by side, and there is a pattern. The mistakes you make most often are the ones Python catches first. The ones that cost you hours are the rare, quiet ones.",
    "19": "So, two habits. Run the file after every small edit. And make every branch run at least once. Python will tell you a lot. But only about the lines it has actually run.",
    "outro": "Thanks for watching. Subscribe to Edge Cases for more Python, algorithms, and system design, explained visually.",
}
