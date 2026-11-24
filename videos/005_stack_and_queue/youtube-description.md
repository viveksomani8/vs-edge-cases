# YouTube upload notes: Stack and queue in Python (Short)

Video file: `stack-and-queue-short.mp4` (1:08, 1080x1920)
Subtitles: `stack-and-queue-short.en.srt`
Playlist: Python for Programmers Who Already Code

## Title (pick one)

1. Stop Writing a Stack Class in Python #shorts
2. Python Already Has a Stack and a Queue #shorts
3. Your Python Queue Is 500x Slower Than It Needs to Be #shorts

## Description (paste everything between the lines)

---

Coming from C++ or PHP, you write a Stack class and a Queue class in Python. You do not need either.

Stack: a list. append pushes, pop takes the last item, [-1] peeks at the top. Everything happens at the end of the list, so nothing else moves.

Queue: collections.deque. popleft takes the front item and nothing else moves. A list works as a queue too, and gives the right answer, but pop(0) shifts every remaining item one place left.

Measured for this video: draining a queue of 200,000 items from the front took 5.3 seconds with list.pop(0) and 9 milliseconds with deque.popleft(). That is one machine and one run of Python 3.12, not a benchmark, but the gap grows with the size of the queue.

When a class is worth writing:
- to limit what callers can do, for example only push and pop
- to add behaviour, for example a stack that also knows its minimum

queue.Queue is a different tool: it is for passing work between threads.

Full video on what Python does with habits from C, C++, Java and PHP: (paste the main video's link here)

Narration is a synthetic voice.

#python #shorts #programming #learnpython

---

## Tags

python stack, python queue, python deque, collections deque, list pop 0 slow, python list as stack, python for c++ programmers, python for php developers, python data structures, python tips, python shorts, learn python

## Upload checklist

- Add it to the playlist "Python for Programmers Who Already Code".
- Set "Python Won't Tell You" as the Related video so the link shows on the Shorts player, and paste its link into the description above.
- It runs 1:08. YouTube accepts Shorts up to three minutes, so it still publishes as a Short.
- Category: Education. Language: English.
- Check YouTube's altered/synthetic content question in the upload flow for the AI narration.
- Title 3 says "500x": the measured ratio was about 575 for 200,000 items (185 for 100,000, 680 for 500,000). Use that title only if you are comfortable with a figure that depends on queue size and machine.
- The timing figures and how they were measured are recorded at the top of `narration.py`.
