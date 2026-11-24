# YouTube upload notes: Merge Two Sorted Linked Lists

## Main video

Video file: `merge-sorted-lists-narrated.mp4` (4:00)
Thumbnail: `thumbnail.png` (1280x720)
Subtitles: `merge-sorted-lists-narrated.en.srt`

### Title (pick one)

1. Merge Two Sorted Linked Lists in Python, Visualised (In Place, O(1) Space)
2. No New Nodes: Merging Two Sorted Linked Lists by Re-aiming the Arrows
3. Merge Two Sorted Lists Without Copying a Single Node | Python, Step by Step

### Description (paste everything between the lines)

---

Merge two sorted linked lists into one, without creating a single new node. The only thing that changes is where each node's next pointer aims. This video starts from the brute force that copies every node, then walks through the in-place merge step by step, with the code highlighted line by line.

You will learn:
- the brute-force merge, and why it is already linear time but still costs O(n + m) extra space
- the in-place idea: the same walk, but re-aim a next pointer instead of copying
- the invariant: everything from dummy to tail is merged and sorted
- why the comparison uses "less than or equal" (it keeps the merge stable)
- why the leftover list is attached with one assignment, not a loop
- where this is used: merge sort on linked lists, and merging k sorted lists

Chapters
0:00 The problem
0:32 Brute force
1:01 The in-place idea and the dummy node
1:34 Step-by-step walkthrough
3:03 Time and space complexity
3:23 Where it is used

Time: O(n + m). Extra space: O(1). The full Python code is on screen from 1:34.

Why a dummy node at all? That has its own Short: (paste the Short's link here)

Related problems to try next: Merge Two Sorted Lists (LeetCode 21), Merge k Sorted Lists (LeetCode 23), Sort List (LeetCode 148).

The problem is 7.1 in "Elements of Programming Interviews in Python" by Aziz, Lee and Prakash.

Animation made with Manim Community Edition. Narration is a synthetic voice.

#python #algorithms #datastructures #codinginterview #linkedlist

---

### Tags

merge two sorted lists, merge sorted linked lists, merge two sorted linked lists python, linked list, in place merge, dummy node, dummy head, sentinel node, merge sort linked list, merge k sorted lists, python algorithms, data structures and algorithms, coding interview, elements of programming interviews, EPI, leetcode 21, stable merge

## Short: The Dummy Head Trick

Video file: `dummy-head-short.mp4` (0:59, 1080x1920)
Subtitles: `dummy-head-short.en.srt`

### Title (pick one)

1. The Dummy Head Trick for Linked Lists #shorts
2. One Extra Node That Deletes Your Linked List Edge Cases #shorts

### Description

---

Without a dummy node, merging two linked lists needs the head picked by hand before the loop: the same comparison written twice, plus an extra check for an empty list. Put one placeholder node in front and the first node stops being special.

Rule of thumb: use a dummy whenever the head of the result is not known up front, or might change.

Same trick: Remove Nth Node From End of List (LeetCode 19), Partition List (LeetCode 86), Add Two Numbers (LeetCode 2).

Full merge walkthrough: (paste the main video's link here)

#python #linkedlist #codinginterview #algorithms

---

## Upload checklist

- Upload the main video first, then the Short, then paste each link into the other's description.
- On the Short, set the main video as the "Related video" so the link shows on the Shorts player.
- Category: Education. Language: English.
- Add the main video to the series playlist with the Dutch flag video.
- End screen: the last 10 seconds (from 3:50) is the channel card; place the subscribe element and a "next video" element over it.
- Check YouTube's altered/synthetic content question in the upload flow for the AI narration.
- LeetCode numbers and the book credit above are from memory; confirm them before publishing.
- YouTube rejects the characters < and > in descriptions, so the code is not pasted here (it contains "<="). To share it, host it on GitHub and add a line "Code: (link)".
