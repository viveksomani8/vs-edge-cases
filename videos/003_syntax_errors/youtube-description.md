# YouTube upload notes: Python Won't Tell You

Video file: `python-wont-tell-you-narrated.mp4` (5:08, 1920x1080)
Thumbnail: `thumbnail.png` (1280x720)
Subtitles: `python-wont-tell-you-narrated.en.srt`

## Title (pick one)

1. Python Won't Tell You: Syntax Traps for C, C++, Java and PHP Developers
2. 5 Bugs, 1 Error: What Python Does Not Check Until It Runs
3. Switching to Python from C++ or PHP? The Mistakes Python Stays Quiet About

## Description (paste everything between the lines)

---

This Python file has five mistakes, and Python reports exactly one of them. If you are coming from C, C++, Java or PHP, your hands already know a syntax. Python rejects some of it, crashes on some of it, and silently accepts the rest.

This video sorts the common mistakes by when you find out:
1. Python refuses to start (SyntaxError, IndentationError)
2. It fails when the line runs (NameError, TypeError, IndexError)
3. It says nothing at all

The middle part fixes one real file a mistake at a time. Every error message on screen is what Python actually printed for that version of the file.

You will see:
- the missing colon, braces and indentation
- the first-day habits: the double ampersand, i++, else if, the three-part for loop, null
- why a list does not grow by index assignment
- why an exception class must inherit from Exception
- why a wrong name in an untested branch survives until that branch runs
- the silent ones: "main" instead of "__main__", ++i, range stopping one short, / returning a float, b = a not copying, the mutable default argument
- two things that are not mistakes: trailing semicolons and parentheses around a condition

Chapters
0:00 Five mistakes, one error
0:08 Three kinds of mistake
0:34 Kind 1: Python refuses to start
1:28 Kind 2: it fails when the line runs
2:47 More of the same kind
3:10 Kind 3: it says nothing
4:16 Not mistakes: semicolons and parentheses
4:30 The pattern, and two habits

Two habits to take away: run the file after every small edit, and make every branch run at least once. Python only checks the lines it runs.

Animation made with Manim Community Edition. Narration is a synthetic voice.

#python #programming #cplusplus #php #java #learnpython

---

## Tags

python syntax errors, python for c++ programmers, python for php developers, python for java developers, switching to python, python mistakes, python gotchas, python beginner mistakes, SyntaxError expected colon, IndentationError, NameError, TypeError exceptions must derive from BaseException, mutable default argument, python ++ operator, if __name__ == __main__, python range, python integer division, learn python

## Playlist: Python for Programmers Who Already Code

New playlist; this is its first video. Description (paste everything between the lines):

---

Python for people who already program. If you come from C, C++, Java or PHP, you do not need "what is a variable". You need to know where Python behaves differently from the language your hands already know.

Each video takes real code written with habits from another language and shows what Python does with it: what it rejects, what it crashes on, and what it silently accepts. Error messages on screen are the ones Python actually printed.

Covered so far:
- syntax your hands type from habit, and how Python responds
- errors Python only reports when the line runs
- code that runs without complaint and does the wrong thing

Short, visual, no setup tutorials. New videos are added as they are published.

From Edge Cases: Python, algorithms and system design, explained visually.

---

Extend the "Covered so far" list when the next video is added.

## Upload checklist

- Create the playlist "Python for Programmers Who Already Code" with the description above, and add this video to it.
- Category: Education. Language: English.
- End screen: the channel card starts at 4:58 and runs to the end; place the subscribe element and a "next video" element over it.
- Check YouTube's altered/synthetic content question in the upload flow for the AI narration.
- YouTube rejects the angle-bracket characters in descriptions, so the description above avoids them (no code with comparison operators).
- The error messages on screen are from Python 3.14; older versions word a few of them slightly differently.
- Source list and the full catalogue behind the video: `research/02-syntax-errors-comprehensive.md` and `research/03-syntax-errors-by-frequency.md`.
