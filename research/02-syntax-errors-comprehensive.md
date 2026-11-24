# Syntax mistakes when switching to Python from C, C++, Java or PHP

A catalogue of what people type out of habit from another language, and what Python does in response.

**Scope.** This is about mistakes that produce an error or a wrong result. Style questions (PEP 8 spacing, "pythonic" alternatives that work either way) are left out on purpose.

**Sources.** The four AI lists in `01-most-common-syntax-errors.txt`, the mistakes from your own EPI files, and additions of mine. The "Seen in" column uses:

| Tag | Meaning |
|---|---|
| GPT, Kimi, Gem, DS | Listed by ChatGPT, Kimi, Gemini, Deepseek in file 01 |
| **You** | You made this one (details in Part E) |
| + | Added by me |

**Verification.** Every "Python's response" below was produced by running the snippet on Python 3.14.4, the default `python` on this machine. Wording of messages changes a little between versions.

## The organising idea: three kinds of failure

A C or C++ compiler reports every mistake before the program starts. Python does not, and that is the real lesson behind the list:

| Part | When you find out | Typical error |
|---|---|---|
| **A** | Before the program starts. One of these and not even line 1 runs. | `SyntaxError`, `IndentationError`, `TabError` |
| **B** | Only when the faulty line executes. An untested branch hides it. | `NameError`, `TypeError`, `AttributeError`, `IndexError` |
| **C** | Never. The code runs and does something else. | none |

Part D lists things often called errors that are not. Part E indexes your own mistakes.

---

## Part A: Python refuses to start

### A.1 Blocks and indentation

| ID | You write | Python's response | Write instead | Seen in |
|---|---|---|---|---|
| A1 | `if x > 0` / `def f()` / `else` with no colon | `SyntaxError: expected ':'` | End every block header with `:` | GPT, Kimi, Gem, **You** ×2 |
| A2 | `if x > 10 {` | `SyntaxError: invalid syntax` | Colon plus indentation, no braces | GPT, Kimi, Gem, DS |
| A3 | `if x > 10:` then `{` on its own line | `IndentationError: expected an indented block after 'if' statement on line N` | Same as A2 | GPT |
| A4 | An empty body, or a body with only a comment | `IndentationError: expected an indented block after function definition on line N` | Put `pass` in the body | + |
| A5 | A line indented deeper for no reason | `IndentationError: unexpected indent` | Align with the surrounding block | Kimi, Gem, DS |
| A6 | A line dedented to a level that matches no outer block | `IndentationError: unindent does not match any outer indentation level` | Use one indent width everywhere (4 spaces) | Kimi, DS |
| A7 | Tabs on one line, spaces on the next, same block | `TabError: inconsistent use of tabs and spaces in indentation` | Spaces only; set the editor to insert spaces | Kimi, Gem, DS, **You** (near miss) |
| A8 | `else:` indented inside the `if` body | `SyntaxError: invalid syntax` | `else` lines up with its `if` | GPT |

### A.2 Operators

| ID | You write | Python's response | Write instead | Seen in |
|---|---|---|---|---|
| A9 | `x > 10 && x < 20`, `a \|\| b` | `SyntaxError: invalid syntax` | `and`, `or` | GPT, Gem |
| A10 | `if !x:` | `SyntaxError: invalid syntax` | `not x` (`!=` is still valid) | GPT, Gem, **You** (2026-11-23) |
| A11 | `i++`, `i--`, `a[i++]` | `SyntaxError: invalid syntax` | `i += 1`, `i -= 1` (see C1 for `++i`) | GPT, Gem, DS, **You** (own notes) |
| A12 | `r = c ? 1 : 2` | `SyntaxError: invalid syntax` | `r = 1 if c else 2` | GPT, DS |
| A13 | `if x = 10:`, `while (x = next()):` | `SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?` | `==` to compare; `:=` to assign inside a condition | GPT, Kimi, Gem, DS |
| A14 | `x === 1`, `x !== 1`, `x <> 1` | `SyntaxError: invalid syntax` | `==`, `!=` | + (PHP, JS) |
| A15 | `y = (int)x` | `SyntaxError: invalid syntax` | `y = int(x)` | + (C, C++, Java, PHP) |
| A16 | `q->v`, `math::pi` | `SyntaxError: invalid syntax` | `q.v`, `math.pi` | + (C++, PHP) |
| A17 | `$x = 5` | `SyntaxError: invalid syntax` | `x = 5` | + (PHP) |
| A18 | `"x" . "y"` | `SyntaxError: invalid syntax` (with variables: see B14) | `"x" + "y"` or an f-string | + (PHP) |

### A.3 Statements and keywords

| ID | You write | Python's response | Write instead | Seen in |
|---|---|---|---|---|
| A19 | `else if x == 0:` | `SyntaxError: expected ':'` | `elif x == 0:` | GPT |
| A20 | `elseif x == 0:`, `elsif` | `SyntaxError: invalid syntax` | `elif` | + (PHP) |
| A21 | `for (int i = 0; i < 5; i++):` | `SyntaxError: invalid syntax. Perhaps you forgot a comma?` | `for i in range(5):` | GPT, Kimi, Gem |
| A22 | `foreach (a as x):` | `SyntaxError: invalid syntax` | `for x in a:` | + (PHP) |
| A23 | `switch (day):` | `SyntaxError: invalid syntax` | `if` / `elif`, or `match` / `case` (3.10+) | GPT, DS |
| A24 | `do: ... while (cond)` | `SyntaxError: invalid syntax` | `while True:` with `if not cond: break` at the end | GPT |
| A25 | `try: ... catch ValueError:` | `SyntaxError: expected 'except' or 'finally' block` | `except ValueError:` | GPT |
| A26 | `except (ValueError e):` | `SyntaxError: invalid syntax. Perhaps you forgot a comma?` | `except ValueError as e:` | + |
| A27 | `throw ValueError('x')`, `raise new ValueError('x')` | `SyntaxError: invalid syntax` | `raise ValueError('x')` | + |
| A28 | `q = new Q()` | `SyntaxError: invalid syntax` | `q = Q()` | + |
| A29 | `print "Hello"`, `echo "hi"` | `SyntaxError: Missing parentheses in call to 'print'. Did you mean print(...)?` (`echo`: `invalid syntax`) | `print("Hello")` | GPT |
| A30 | A misspelt keyword, e.g. `if non values:` | `SyntaxError: invalid syntax`, with no hint | `not`. Read the caret position, the message will not help | **You** |

### A.4 Declarations

| ID | You write | Python's response | Write instead | Seen in |
|---|---|---|---|---|
| A31 | `int x = 10`, `int x` | `SyntaxError: invalid syntax` | `x = 10` (optional hint: `x: int = 10`) | GPT, Gem |
| A32 | `int add(int a, int b):`, `void f():`, `function add(a, b):` | `SyntaxError: invalid syntax` | `def add(a, b):` | GPT |
| A33 | `const N = 10`, `final N = 10`, `static x = 1`, `public x = 1` | `SyntaxError: invalid syntax` | No such keywords. `N = 10` by convention; `_x` for "internal" | + |
| A34 | `int a[10]` | `SyntaxError: invalid syntax` | `a = [0] * 10` | + |
| A35 | `class B extends A:`, `interface Shape:` | `SyntaxError: invalid syntax` | `class B(A):` | + (Java, PHP) |
| A36 | A reserved word as a name: `from = 0`, `in = 5`, `class = 'A'`, `lambda = 0.5`, `is = 1`, `pass = True` | `SyntaxError: invalid syntax` (`None = 0`: `cannot assign to None`) | Rename: `src`, `inp`, `cls`, `lam` | + |

A36 bites in algorithm code in particular, where `from`/`to`, `in`/`out` and `lambda` are natural variable names.

### A.5 Comments, strings and line structure

| ID | You write | Python's response | Write instead | Seen in |
|---|---|---|---|---|
| A37 | `// This is a comment` | `SyntaxError: invalid syntax` | `# This is a comment` | GPT |
| A38 | `/* comment */` | `SyntaxError: invalid syntax` | `#` on each line | + |
| A39 | `print((1 + 2)` then more code | `SyntaxError: '(' was never closed` | Close the bracket. The error can point lines away from where you were typing | + |
| A40 | `s = 'it's'` | `SyntaxError: unterminated string literal (detected at line N)` | `"it's"` | + |
| A41 | A statement split after an operator: `total = a +` then `b` on the next line | `SyntaxError: invalid syntax` | Wrap in parentheses: `total = (a +` / `b)` | + |
| A42 | The same split with the next line indented: `total = a` then `    + b` | `IndentationError: unexpected indent` | Parentheses, as in A41 (unindented, it is silent: see C23) | + |
| A43 | `import 07-01-merge`, `import merge-lists` | `SyntaxError: leading zeros in decimal integer literals are not permitted...` / `invalid syntax` | Module file names must be valid identifiers: `merge_lists.py` | **You** |
| A44 | A trailing condition with no `else`: `q.append(node.left) if node.left` | `SyntaxError: expected 'else' after 'if' expression` | `if node.left:` on its own line, then the call indented under it | **You** (Ruby, Perl; also the C habit of `cond && call()`) |

---

## Part B: Python starts, then fails when the line runs

These all pass the parser. A C/C++/Java compiler would have rejected most of them up front; Python finds them only if execution reaches the line. Code in an untested branch can carry one of these indefinitely.

### B.1 Names that do not exist

| ID | You write | Python's response | Write instead | Seen in |
|---|---|---|---|---|
| B1 | `result = null`, `p = NULL` | `NameError: name 'null' is not defined` | `None` | GPT, Gem |
| B2 | `flag = true`, `while true:` | `NameError: name 'true' is not defined` | `True`, `False` | GPT, Kimi |
| B3 | `name = "Sam"` then `print(Name)` | `NameError: name 'Name' is not defined` | Names are case-sensitive, functions included (PHP's are not) | GPT |
| B4 | A wrong or misspelt name inside a branch that rarely runs | Nothing, until that branch runs: then `NameError` | Exercise every branch at least once | **You** |
| B5 | `total += 1` or `seen[w] = 1` with no earlier assignment | `NameError: name 'seen' is not defined` (inside a function: `UnboundLocalError`) | Initialise first: `total = 0`, `seen = {}` | + (PHP auto-creates) |
| B6 | Declaring without a value: `x` on its own, or `x: int` then using `x` | `NameError: name 'x' is not defined` | A name exists only once something is assigned to it | + |
| B7 | Calling a function above its `def` at module level | `NameError: name 'f' is not defined` | `def` is an executed statement; put driver code at the bottom | **You** |
| B8 | Assigning to a module-level variable inside a function: `count += 1` | `UnboundLocalError: cannot access local variable 'count' where it is not associated with a value` | `global count`, or pass it in and return it | + |
| B9 | `printf("%d", x)`, `sizeof(a)`, `count(items)`, `length(items)`, `array(1, 2)` | `NameError: name 'printf' is not defined` | `print(f"{x}")`, `len(items)`, `[1, 2]` | GPT, + |
| B10 | `this.items = []` | `NameError: name 'this' is not defined` | `self.items = []` | + |
| B11 | Inside a method, `items` instead of `self.items` | `NameError: name 'items' is not defined` | There is no implicit `this`; always write `self.` | + (C++, Java) |

### B.2 Attributes and methods that do not exist

| ID | You write | Python's response | Write instead | Seen in |
|---|---|---|---|---|
| B12 | `items.length()`, `items.size()` | `AttributeError: 'list' object has no attribute 'length'` | `len(items)` | GPT, **You** (own notes) |
| B13 | An attribute that was renamed or never created: `self.top` | `AttributeError: 'S' object has no attribute 'top'` | Attributes exist only after `self.x = ...` has run | **You** ×2 |
| B14 | `a . b` meaning concatenation | `AttributeError: 'str' object has no attribute 'b'` | `a + b` | + (PHP) |
| B15 | `d.x` on a dict | `AttributeError: 'dict' object has no attribute 'x'` | `d["x"]` | + (JS, PHP objects) |
| B16 | A constructor named after the class, or `_init_` with single underscores | `TypeError: Stack() takes no arguments` (with no arguments it is silently never called) | `def __init__(self, ...)` with two underscores each side | + (C++, Java) |
| B17 | A subclass `__init__` that never calls the parent's | `AttributeError: 'B' object has no attribute 'x'` | `super().__init__()` (C++/Java call the base constructor for you) | + |

### B.3 Types that do not mix

| ID | You write | Python's response | Write instead | Seen in |
|---|---|---|---|---|
| B18 | `"Age: " + age` | `TypeError: can only concatenate str (not "int") to str` | `f"Age: {age}"` or `str(age)` | GPT, Kimi |
| B19 | `'a' + 1` | Same `TypeError` | `chr(ord('a') + 1)`; a character is a string, not a number | + (C, C++, Java) |
| B20 | `s[0] = 'b'` | `TypeError: 'str' object does not support item assignment` | Build a new string, or work on `list(s)` | + (C, C++) |
| B21 | `a[len(a) / 2]`, `range(n / 2)` | `TypeError: list indices must be integers or slices, not float` / `'float' object cannot be interpreted as an integer` | `//` for integer division | Kimi |
| B22 | `'10' < 9`, or arithmetic on `input()` | `TypeError: '<' not supported between instances of 'str' and 'int'` | Convert explicitly: `int(s)` | + (PHP juggles types) |
| B23 | A method defined without `self`: `def __len__():` | `TypeError: Q.__len__() takes 0 positional arguments but 1 was given` | `def __len__(self):` | Gem, **You** |
| B24 | `raise` or `except` with a class that does not inherit from `Exception` | `TypeError: exceptions must derive from BaseException`; with a message: `TypeError: EmptyQueueError() takes no arguments` | `class EmptyQueueError(Exception):` | **You** ×2 |
| B25 | `a \| b` between two objects, meaning "a or else b" | `TypeError: unsupported operand type(s) for \|: 'N' and 'NoneType'` | `a or b` | **You** (asked) |
| B26 | Two functions with the same name and different parameters | The second silently replaces the first; calling the old form: `TypeError: area() missing 1 required positional argument: 'h'` | Default arguments; there is no overloading | + (C++, Java) |
| B27 | A variable named like a built-in: `list = [1, 2]`, `len = 3`, `max = 0` | Later: `TypeError: 'list' object is not callable` | Do not reuse `list`, `str`, `len`, `max`, `min`, `sum`, `id`, `type`, `input` | Kimi |
| B28 | A function with no `return`, whose result is then used | `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'` | `return` the value explicitly | Gem |

### B.4 Containers

| ID | You write | Python's response | Write instead | Seen in |
|---|---|---|---|---|
| B29 | `values[0] = 5` on an empty list | `IndexError: list assignment index out of range` | `values.append(5)`, or pre-size with `[0] * n` | **You** |
| B30 | `values[] = 5` | `SyntaxError: invalid syntax` (parse time) | `values.append(5)` | + (PHP) |
| B31 | `d['x']` or `d['x'] += 1` for a missing key | `KeyError: 'x'` | `d.get('x', 0)`, `defaultdict`, `Counter` | + (PHP gives null, C++ `map` inserts) |
| B32 | `for k, v in d:` | `ValueError: not enough values to unpack (expected 2, got 1)` | `for k, v in d.items():` | + (PHP `foreach ... as $k => $v`) |
| B33 | `a = ['x' => 1]` | `SyntaxError: invalid syntax` (parse time) | `a = {'x': 1}` | + (PHP) |
| B34 | `import os.py` | `ModuleNotFoundError: No module named 'os.py'; 'os' is not a package` | `import os`: a module name, not a file path | + (`#include`, `require`) |
| B35 | Using a name from a module after a bare `import module`, or after no import at all: `q = deque()` | `NameError: name 'deque' is not defined` | `from collections import deque`, or `collections.deque()`. `import` binds the module name only; it does not paste the contents in | **You** (`#include`, PHP `require`) |
| B36 | A method name from another language's container: `q.empty()` | `AttributeError: 'collections.deque' object has no attribute 'empty'` | `while q:` (an empty container is false) | **You** (C++ `std::queue::empty()`) |
| B37 | camelCase for a standard-library method: `q.popLeft()` | `AttributeError: 'collections.deque' object has no attribute 'popLeft'` | `q.popleft()`: the standard library uses lowercase and snake_case | **You** (Java, PHP) |
| B38 | A type hint naming a class that is not defined yet: `def f(root: TreeNode):` | Python 3.12: `NameError: name 'TreeNode' is not defined`, when the `def` runs. Python 3.14: no error | Import or define the class first | **You** |
| B39 | A dataclass field without a default placed after fields that have one | `TypeError: non-default argument 'value' follows default argument 'right'`, when the class is created | Required fields first. The same rule as default parameters in C++ and PHP, applied to the generated constructor | **You** |

---

## Part C: no error at all

The program runs and produces the wrong result, or silently does nothing. These are the expensive ones.

| ID | You write | What actually happens | Write instead | Seen in |
|---|---|---|---|---|
| C1 | `++i`, `--i`, even `j = i++ + 1` | Valid: unary plus or minus applied twice. `i` does not change | `i += 1` | Gem, **You** (own notes) |
| C2 | `if __name__ == "main":` | The condition is always false, so the block never runs. No output, no error | `"__main__"`. A function called `main` is not run automatically either | **You** |
| C3 | A line one indent level off, still legal | It joins or leaves the loop: runs once instead of every pass, or returns on the first iteration | Check the indent of the line after every loop and `if` | Kimi, Gem, DS |
| C4 | `#include <stdio.h>`, `#define N 10` | They are comments. `N` is never defined | `import ...`, `N = 10` | + |
| C5 | `&` and `\|` where you meant `and` / `or` | Valid bitwise operators with tighter binding: with `x = 2, y = 9`, `x > 1 & y < 5` is `True` while `x > 1 and y < 5` is `False` | `and`, `or` | +, **You** (asked) |
| C6 | `/` expecting integer division | `5 / 2` is `2.5` | `5 // 2` | Kimi |
| C7 | `//` and `%` with negatives, expecting C behaviour | `-5 // 2` is `-3` (C gives `-2`); `-5 % 3` is `1` (C gives `-2`) | `int(a / b)` to truncate like C | + |
| C8 | `range(1, 5)` expecting 5 to be included; `a[1:3]` likewise | The end is excluded: `1, 2, 3, 4` | `range(1, 6)` | GPT, Kimi, Gem |
| C9 | `range(5, 0)` to count down | Empty: the loop body never runs | `range(4, -1, -1)` or `reversed(range(5))` | + |
| C10 | `i += 2` inside `for i in range(6):` to skip ahead | No effect on the next pass: still visits `0, 1, 2, 3, 4, 5` | A `while` loop, or `range(0, 6, 3)` | + |
| C11 | `a[i - 1]` when `i` is 0 | Index `-1` is the last element, so you get a value where C would misbehave and you would notice | Guard the boundary explicitly | + |
| C12 | `0 <= x <= 3` ported from C logic | Means `0 <= x and x <= 3` (C evaluates `(0 <= x) <= 3`) | Usually what you want; know that it differs | Gem |
| C13 | `x = (10)` for a one-element tuple | An `int` | `x = (10,)` | GPT |
| C14 | A stray trailing comma: `x = 10,` | A tuple `(10,)` | Remove the comma | + |
| C15 | `b = a` to copy a list | Both names point at the same list; `b.append(3)` changes `a` | `b = a.copy()` or `a[:]` | + (PHP arrays and C++ vectors copy) |
| C16 | `A = []` inside a function to empty the caller's list | Rebinds the local name only; the caller's list is untouched | `A[:] = []` or `A.clear()` | **You** (own notes) |
| C17 | Changing an `int` parameter, expecting the caller to see it | The caller's value is unchanged; there is no `int &x` | Return the new value | + |
| C18 | `def f(items=[]):` | One list shared by every call: a second call returns `[1, 1]` | `items=None`, then `if items is None: items = []` | Kimi |
| C19 | `g = [[0] * 2] * 2` for a 2D array | Both rows are the same list: setting `g[0][0]` gives `[[1, 0], [1, 0]]` | `[[0] * 2 for _ in range(2)]` | + |
| C20 | Fields declared in the class body, Java/C++ style: `values = []` | One list shared by every instance | Assign in `__init__`: `self.values = []` | + |
| C21 | A method named without parentheses: `q.empty`, `stack.pop` | Nothing is called. `if q.empty:` is always true | `q.empty()` | + |
| C22 | A function that computes but does not `return`; `a = a.sort()` | The result is `None` | `return` it; `a.sort()` alone, or `a = sorted(a)` | Gem, + |
| C23 | A statement continued on the next line: `total = a` then `+ b` | Two statements: `total` is `a`. `return` followed by the value on the next line returns `None` | Parentheses around the whole expression | + |
| C24 | Expecting a loop variable to disappear after the loop | It survives with its last value; `if` and `for` create no scope | Do not rely on block scope | + |
| C25 | `"Hello $name"` | Prints `Hello $name` literally | `f"Hello {name}"` | + (PHP) |
| C26 | `assert(x == 1, "x must be 1")` | Always passes: the parentheses make a non-empty tuple (`SyntaxWarning: assertion is always true`) | `assert x == 1, "x must be 1"` | + |
| C27 | `x is 5`, `x is []` | `is` compares identity, not value. `x is []` is always `False` | `==` for values; `is` only for `None` | Kimi |
| C28 | `if x == None:` to test for an empty list | `[] == None` is `False`: empty and `None` are different states | `if not x:` for empty, `if x is None:` for `None` | Kimi, **You** (asked) |
| C29 | Removing items from a list while looping over it | Elements are skipped: `[1, 2, 2, 3]` minus the 2s gives `[1, 2, 3]` | Build a new list: `[x for x in a if x != 2]` | Kimi |
| C30 | `'10' == 10`, `'10' < '9'` | `False` (PHP says true); `True`, because strings compare character by character | Convert with `int()` first | + (PHP) |

---

## Part D: often listed as errors, but they are not

Corrections to the source lists, worth getting right in a video because viewers will test them.

| Claim | Reality |
|---|---|
| A trailing semicolon "causes a `SyntaxError` in Python" (Gemini) | False. `x = 10;` runs normally. It is an empty statement separator: harmless, just unnecessary. **You** did this in two files and nothing broke. |
| Parentheses around a condition are a mistake (ChatGPT #5) | `if (x > 10):` is fully valid. The one place parentheses do change meaning is `assert(...)`: see C26. |
| "Python doesn't have `++`" (several lists) | True for `i++` (A11), but `++i` is accepted and does nothing (C1). The silent form is the dangerous one. |
| `except ValueError, TypeError:` without parentheses is an error | It ran without error on Python 3.14.4. Older versions reject it (I did not test one here), so write `except (ValueError, TypeError):` to be safe everywhere. |
| `print "Hello"` is a C/Java habit (ChatGPT #14) | It is mostly a Python 2 habit. It is a real carry-over for PHP, where `print "Hello";` and `echo` are valid. |
| ChatGPT items #1 and #9 | The same mistake listed twice (braces for blocks). Merged here as A2 and A3. |
| `null`, `true`, `NULL` give a syntax error | They give a `NameError`, at run time, and only if the line executes (B1, B2). |

---

## Part E: the ones you made

From the four EPI files reviewed on 2026-11-19 and 2026-11-21. Line numbers refer to the version of the file at the time of review.

| Where | What you wrote | Result | ID |
|---|---|---|---|
| `08-01-min-stack.py`, first version, line 14 | `if self.top <= -1` with no colon | `SyntaxError`, file did not run | A1 |
| `08-09-01-queue.py`, line 19 | `def __len__()` with no colon | `SyntaxError`, file did not run | A1 |
| `08-01-min-stack.py`, second version, line 24 | `if non self._values:` | `SyntaxError`, file did not run | A30 |
| `08-09-01-queue.py`, line 19 | `def __len__()` with no `self` | `TypeError` on `len(q)` | B23 |
| `08-01-min-stack.py`, first version, line 1 | `class EmptyStack: pass` then `raise EmptyStack` | `TypeError: exceptions must derive from BaseException` | B24 |
| `08-09-01-queue.py`, line 1 | `class EmptyQueueError:` then raised with a message | `TypeError: EmptyQueueError() takes no arguments` | B24 |
| `08-01-min-stack.py`, first version, line 11 | `self.values[ self.top ] = value` on an empty list | `IndexError: list assignment index out of range` | B29 |
| `08-01-min-stack.py`, first version, line 30 | `except EmptyStack as e: print( a )` | `NameError`, only if that branch runs | B4 |
| `08-01-min-stack.py`, second version, lines 17 and 37 | `return self.top + 1` after `top` was removed | `AttributeError`, only if `len()` is called | B13 |
| `07-01-merge-sorted-linked-lists.py` | `print_ll(...)` called above `def print_ll` | `NameError` | B7 |
| `08-01-min-stack.py`, first version, line 22 | `if __name__ == "main":` | Block never runs, silently | C2 |
| `07-01-merge-sorted-linked-lists.py`, `08-09-01-queue.py` | Tabs and spaces mixed in one file | No error in these places; one line away from a `TabError` | A7 |
| All EPI files | File names with leading digits and hyphens | No error until you try to `import` one | A43 |
| `06-01-dutch-natinoal-flag.py` (your notes) | No `++` / `--`; `A = x` vs `A[:] = x`; `len()` instead of a method | You caught these yourself | A11, C1, C16, B12 |
| `07-01-...`, `06-01-...` | Trailing semicolons | Not an error (Part D) | D |
| Question, 2026-11-19 | Why `a \| b` fails where `a or b` works | `TypeError` between two objects | B25, C5 |
| Question, 2026-11-21 | Is `if not x:` the same as `if x == None:`? | No | C28 |
| `08-09-printing-a-binary-tree-in-level-order.py`, lines 1 and 2 | `import tree-node`, `import 01-test-utils` | `SyntaxError`; Python reports line 2 first (leading zero), then line 1 (hyphen) | A43 |
| same file, lines 13 and 14 | `q.append(node.left) if node.left` | `SyntaxError: expected 'else' after 'if' expression` | A44 |
| same file, line 7 | `deque()` with no import of it | `NameError` | B35 |
| same file, line 6 | `root: TreeNode` with `TreeNode` never brought into scope | `NameError` on 3.12, nothing on 3.14 | B38 |
| same file, line 10 | `while not q.empty():` | `AttributeError` | B36 |
| same file, line 11 | `q.popLeft()` | `AttributeError` | B37 |
| same file, line 12 | `print(node.value + " ")` | `TypeError`: number plus string | B18 |
| same file | Tabs for indentation, as in the queue file | No error | A7 |
| `src/test-utils/01_test_utils.py`, line 1 | `import tree-node.py` | `SyntaxError: invalid syntax` (hyphen), and a file extension in an import | A43, B34 |
| `src/test-utils/01_test_utils.py` (its name and folder) | A module name starting with a digit, in a folder with a hyphen | `import 01_test_utils`: `SyntaxError: invalid decimal literal`; `from test-utils import ...`: `SyntaxError: invalid syntax` | A43 |
| `src/tree_node.py`, line 1 | `@dataclass` with no import of it | `NameError: name 'dataclass' is not defined` | B35 |
| `src/tree_node.py`, lines 3 to 5 | Fields with defaults (`left`, `right`) listed before one without (`value`) | `TypeError: non-default argument 'value' follows default argument 'right'` | B39 |

**Review of 2026-11-23.** The level-order file repeats the pattern: three Part A errors stop it, and five Part B errors sit behind them. Two are repeats of items already in the "Python Won't Tell You" video (number plus string, and an error that only appears once the line runs), and the file-name problem predicted under A43 has now happened.

**The pattern in your own list.** All three reviews on 2026-11-21 (min-stack twice, queue once) were stopped by a one-token Part A error (two missing colons, one `non`), which then hid Part B errors sitting behind it. In the min-stack file, fixing the colon would have revealed five more problems one at a time. That "error behind the error" sequence is the most useful thing in this document for a video.
