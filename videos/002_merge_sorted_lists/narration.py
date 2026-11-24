"""Narration script for the merge-sorted-lists video and the dummy-head Short.

One entry per audio clip: the key is the file stem under audio/ ("01" is
audio/01.mp3, "short/01" is audio/short/01.mp3). The scenes time every beat to
its clip, and subtitles.py builds the .srt files from the same text, so this
file is the single place to edit the wording.
"""

NARRATION = {
    # ------------------------------------------------------------ main video
    "hook": "Two sorted linked lists become one. No new nodes. No copying. Only the arrows change.",
    # The problem
    "01": "Merge two sorted linked lists. You are given the heads of two lists, a and b. Each one is already sorted.",
    "02": "Return a single sorted list that contains every node from both.",
    "03": "The catch: you must reuse the existing nodes. The only field you may change is next. So the extra space has to be constant.",
    # Brute force
    "04": "Both lists are sorted, so the smallest value that is left is always at the front of one of them. So the brute force way is: compare the two fronts, copy the smaller one into a brand new list, and repeat.",
    "05": "That is already linear time: big O of n plus m, for lists of length n and m. But every node gets copied, so the extra space is linear too. And that is exactly what the problem does not allow.",
    # The idea
    "06": "So here is the better idea. Keep exactly the same walk, but stop copying. Take the node itself, and link it into the result by changing a next pointer.",
    "07": "But which node becomes the head of the result? We do not know yet. So we start with a placeholder, called a dummy node, and build the result behind it.",
    "08": "A reference called tail always points at the last node of the merged list. Everything from dummy to tail is merged and sorted. That is the invariant.",
    # Walkthrough
    "09": "In code: dummy and tail start on the same new node. Then the loop runs while both lists still have nodes.",
    "10": "Compare the fronts: two and one. One is smaller. So tail's next is set to that node, and b moves forward.",
    "11": "Then tail steps onto the node we just linked. The merged list is now one node long.",
    "12": "Next: two against five. Two is smaller. Watch the arrow out of one. It used to point at five. Now it points at two. No node moved. Only next changed.",
    "13": "Five against five: a tie. The comparison is less than or equal, so the node from a goes first. That keeps the merge stable: equal values stay in their original order.",
    "14": "Now five, from b, against eight. Five is smaller. Link it, and advance.",
    "15": "Eight against nine. Eight is smaller. Link it. And now, list a has run out.",
    "16": "The loop stops as soon as one list is empty. The rest of the other list is still sorted, and still linked together. So a single assignment attaches all of it: tail's next becomes a or b, whichever one is left.",
    "17": "Finally, skip the placeholder. Return dummy's next. That is the real head. Drawn in a straight line, it is the same seven nodes, now in sorted order.",
    # Complexity
    "18": "Time: every pass of the loop links exactly one node. So the time is linear: big O of n plus m, the two lengths added together.",
    "19": "Space: one dummy node and a few references, whatever the size of the input. That is constant extra space.",
    # Where it is used
    "20": "Where is this used? It is the merge step of merge sort. And merge sort is the usual way to sort a linked list.",
    "21": "It is also the building block for merging k sorted lists: merge them in pairs, or use a heap.",
    "22": "And the dummy node? It removes edge cases far beyond this problem. That story has its own short video, linked in the description.",
    "outro": "Thanks for watching. Subscribe to Edge Cases for more Python, algorithms, and system design, explained visually.",

    # ------------------------------------------- Short: the dummy head trick
    "short/hook": "One extra node that makes linked list code simpler: the dummy head.",
    "short/01": "Merging two sorted linked lists. Before the loop can start, you need a head. So you compare the two fronts once, by hand, just to pick it.",
    "short/02": "Then the loop makes the same comparison again. And you still need an extra check, in case one list is empty.",
    "short/03": "Now put one placeholder node in front: a dummy. Tail starts on it.",
    "short/04": "The first node is no longer special. The loop links it like every other node. The duplicate code is gone, and empty lists just work.",
    "short/05": "At the end, return dummy's next. That is the real head.",
    "short/06": "Rule of thumb: use a dummy whenever the head of the result is not known up front, or might change.",
    "short/07": "You will see it again in remove the n-th node, partition list, and add two numbers. The full merge walkthrough is on the channel.",
}

MAIN_CLIPS = [name for name in NARRATION if not name.startswith("short/")]
SHORT_CLIPS = [name for name in NARRATION if name.startswith("short/")]
