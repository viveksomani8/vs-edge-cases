# Python syntax mistakes for switchers, ranked by frequency

A curated shortlist from `02-syntax-errors-comprehensive.md`, most frequent first. IDs point back to that document.

## How the ranking was made

There is no measured dataset behind this order. It is a judgement built from three signals:

1. **Agreement**: how many of the four AI lists in file 01 mention the mistake (0 to 4).
2. **Your own record**: whether you made it in the EPI files, and how many times.
3. **My estimate** of how early and how often it hits someone coming from C, C++, Java or PHP.

Treat the tiers as reliable and the order inside a tier as approximate.

"Kind" tells you how the mistake shows up: **Start** = Python refuses to run the file, **Run** = it fails when the line executes, **Silent** = no error at all.

## Tier 1: almost everyone, on the first day

| Rank | Mistake | Kind | Lists | You | ID |
|---|---|---|---|---|---|
| 1 | Missing `:` after `if`, `for`, `while`, `def`, `class`, `else` | Start | 3 | Twice | A1 |
| 2 | Braces for blocks, and indentation that does not line up | Start | 4 | Near miss | A2, A3, A5, A6, A7 |
| 3 | `&&`, `\|\|`, `!` instead of `and`, `or`, `not` | Start | 2 | Asked | A9, A10 |
| 4 | `i++` and `i--` | Start | 3 | Own notes | A11 |
| 5 | `null`, `true`, `false`, `NULL` instead of `None`, `True`, `False` | Run | 3 | | B1, B2 |
| 6 | `else if` instead of `elif` | Start | 1 | | A19, A20 |
| 7 | The three-part `for (int i = 0; i < n; i++)` loop | Start | 3 | | A21 |
| 8 | Type names in declarations and function signatures (`int x = 10`, `int add(int a, int b)`) | Start | 2 | | A31, A32 |
| 9 | `//` and `/* */` comments | Start | 1 | | A37, A38 |
| 10 | `.length()`, `.size()`, `count()` instead of `len()` | Run | 1 | Own notes | B12, B9 |

## Tier 2: most people, in the first week

| Rank | Mistake | Kind | Lists | You | ID |
|---|---|---|---|---|---|
| 11 | Forgetting `self` in a method definition, or `self.` when using an attribute | Run | 1 | Once | B23, B11, B10 |
| 12 | `"Age: " + age`: joining a string and a number | Run | 2 | | B18 |
| 13 | `=` inside a condition | Start | 4 | | A13 |
| 14 | `condition ? a : b` | Start | 2 | | A12 |
| 15 | `range(1, 5)` and slices stopping one short of the end | Silent | 3 | | C8 |
| 16 | `/` returning a float | Silent, then Run | 1 | | C6, B21 |
| 17 | `catch` and `throw` instead of `except` and `raise` | Start | 1 | | A25, A27 |
| 18 | An empty block with no `pass` | Start | 0 | | A4 |
| 19 | Writing to a list index that does not exist yet | Run | 0 | Once | B29 |
| 20 | `switch` and `do ... while` | Start | 2 | | A23, A24 |

## Tier 3: bites later, and costs more when it does

| Rank | Mistake | Kind | Lists | You | ID |
|---|---|---|---|---|---|
| 21 | A wrong name or attribute in code that is never executed | Run, late | 0 | Three times | B4, B7, B13 |
| 22 | `if __name__ == "main":`, or expecting `main()` to run by itself | Silent | 0 | Once | C2 |
| 23 | A custom exception class that does not inherit from `Exception` | Run | 0 | Twice | B24 |
| 24 | A line one indent level off that is still legal | Silent | 3 | | C3 |
| 25 | `b = a` expected to copy a list; `A = []` expected to clear the caller's list | Silent | 0 | Own notes | C15, C16 |
| 26 | `++i` accepted and ignored | Silent | 1 | Own notes | C1 |
| 27 | Mutable default argument `def f(items=[])` | Silent | 1 | | C18 |
| 28 | Using a variable before assigning to it; assigning to a global inside a function | Run | 0 | | B5, B8 |
| 29 | `&` and `\|` used as logical operators | Silent or Run | 0 | Asked | C5, B25 |
| 30 | A variable named `list`, `len`, `max`, `str`, `id` | Run, late | 1 | | B27 |
| 31 | A method named without parentheses (`q.empty`) | Silent | 0 | | C21 |
| 32 | `x is 5`, and confusing empty with `None` | Silent | 1 | Asked | C27, C28 |
| 33 | Removing items from a list while looping over it | Silent | 1 | | C29 |
| 34 | Missing dictionary key raising `KeyError` | Run | 0 | | B31 |
| 35 | Tuple commas: `(10)` is not a tuple, `x = 10,` is | Silent | 1 | | C13, C14 |

## Frequent, but not an error

Trailing semicolons are probably the single most common habit of all (you did it in two files), and they are legal Python. They belong in a video as a myth to correct, not as a mistake: one of the source lists wrongly says they raise a `SyntaxError`.

## What the ranking shows

- **Tier 1 is almost entirely "Start" errors.** They are frequent but cheap: Python stops immediately and points at the line.
- **Frequency and cost run in opposite directions.** Moving down the list, mistakes get rarer and move from "Start" to "Run" to "Silent", which is the order of increasing time lost.
- **Your own record is weighted toward Tier 3.** Apart from the colon, the mistakes you actually made (names checked late, `"main"`, exception base class, index assignment) are ones the AI lists barely mention. That is the part of this material other videos on the topic do not cover.
