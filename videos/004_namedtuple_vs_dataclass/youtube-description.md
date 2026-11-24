# YouTube upload notes: NamedTuple or @dataclass? (Short)

Video file: `namedtuple-or-dataclass-short.mp4` (1:09, 1080x1920)
Subtitles: `namedtuple-or-dataclass-short.en.srt`
Playlist: Python for Programmers Who Already Code

## Title (pick one)

1. NamedTuple or @dataclass? Python's Two Structs #shorts
2. Python Has Two Structs. Which One Do You Need? #shorts
3. NamedTuple vs dataclass in 60 Seconds #shorts

## Description (paste everything between the lines)

---

In C you would write a struct. Python has two ways to do it: NamedTuple and @dataclass.

NamedTuple: a tuple whose fields have names. Read a field by name or by position. It cannot be changed after it is created.

@dataclass: an ordinary class where Python writes the constructor, the printout and the equality check for you. Its fields can be changed.

The differences that decide it:
- assign to a field: error on a NamedTuple, fine on a dataclass
- unpack into two names: works on a NamedTuple, error on a dataclass
- use as a dict key: works on a NamedTuple, error on a dataclass

Rule: never changes after it is created, use NamedTuple. Its fields get reassigned, use @dataclass.

Neither needs installing: NamedTuple is in the typing module and dataclass is in dataclasses, both part of Python itself.

Full video on what Python does with habits from C, C++, Java and PHP: (paste the main video's link here)

Narration is a synthetic voice.

#python #shorts #programming #learnpython

---

## Tags

python namedtuple, python dataclass, namedtuple vs dataclass, python struct, python for c++ programmers, python for php developers, typing NamedTuple, dataclasses, python tips, python shorts, learn python

## Upload checklist

- Add it to the playlist "Python for Programmers Who Already Code", after the main video.
- Set "Python Won't Tell You" as the Related video so the link shows on the Shorts player, and paste its link into the description above.
- It runs 1:09. YouTube accepts Shorts up to three minutes, so it still publishes as a Short.
- Category: Education. Language: English.
- Check YouTube's altered/synthetic content question in the upload flow for the AI narration.
- The error messages on screen are from Python 3.12. On Python 3.14 the dict-key error is worded differently ("cannot use 'Node' as a dict key (unhashable type: 'Node')").
- A frozen dataclass can be used as a dict key and cannot be changed; the Short leaves that out to keep the rule simple. Expect it in the comments.
