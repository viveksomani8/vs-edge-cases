"""Narration script for the level order traversal video.

One entry per audio clip, keyed by the file stem under audio/. The scene times
every beat to its clip, and subtitles.py builds the .srt file from the same
text, so this file is the single place to edit the wording.
"""

NARRATION = {
    "hook": "Here is a loop that walks a tree. It takes a node, visits it, and adds its children. Take from the same end you add to, and it dives down one branch. Change one word, to take from the other end, and it sweeps the tree level by level.",
    # The problem
    "01": "Level order traversal. You are given the root of a binary tree. Return its values grouped by depth: one list for each level, from the top down, and from left to right.",
    # Brute force
    "02": "The brute force way: for each depth, walk the whole tree, and collect the nodes at that depth. It is correct. But every pass starts from the root again, so the same nodes are visited over and over. On a tree that is one long chain, that is quadratic.",
    # The idea
    "03": "The better idea is to never go back. Keep a queue of nodes that have been found, but not visited yet. Take one from the front, visit it, and add its children at the back. Nodes come out in the order they went in: top to bottom, left to right.",
    "04": "One question is left. Where does one level end, and the next begin? Look at the queue just before a pass starts. It holds exactly one level, and nothing else. So its length tells you how many nodes to take.",
    # Walkthrough
    "05": "In code. The queue starts with the root. Its length is one, so the first pass takes one node: three. Its children, nine and twenty, go to the back. The first level is done.",
    "06": "Now the queue holds two nodes: the whole second level. Take nine, and add four and seven. Take twenty, and add fifteen. Two nodes were taken, so the pass ends. The second level is nine, twenty.",
    "07": "Three nodes are waiting, so this pass takes three. Four has no children. Seven adds one. Fifteen adds eight. That is the third level: four, seven, fifteen.",
    "08": "Two nodes are left: one and eight. Neither has children, so nothing is added. The queue is empty, the loop ends, and the result has one list for each level.",
    # Edge cases
    "09": "Now the edge cases. An empty tree: return an empty list, before touching the queue. A single node: one level. And a tree that is one long chain: every level holds exactly one node.",
    # Complexity
    "10": "Time: every node enters the queue once, and leaves it once. That is linear: big O of n. Space: the queue never holds more than two levels at a time, so the extra space is proportional to the widest level.",
    # Where it is used
    "11": "Where is this used? This is breadth first search. The same loop finds the shortest path in a maze or a graph. And it solves zigzag traversal, right side view, and the minimum depth of a tree.",
    "12": "And if you take from the other end instead, you get depth first search. Same loop. One word.",
    "outro": "Thanks for watching. Subscribe to Edge Cases for more Python, algorithms, and system design, explained visually.",
}

# Spoken form -> what the subtitle should show.
SUBTITLE_SPELLINGS = [
    ("big O of n", "O(n)"),
]
