"""Level order traversal of a binary tree: the code shown in the video.

Run it to check the function against the trees used on screen:
    python videos/006_level_order/level_order.py
"""

from collections import deque
from dataclasses import dataclass


@dataclass
class TreeNode:
    value: int
    left: "TreeNode | None" = None   # quoted: the scene is rendered with Python 3.12,
    right: "TreeNode | None" = None  # which evaluates annotations when the class is built


def level_order(root):
    result = []
    if root is None:
        return result
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.value)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        result.append(level)
    return result


def walk(root, from_front):
    """The loop from the hook: visit order when taking from the front (a queue)
    or from the back (a stack) of the same deque."""
    order = []
    todo = deque([root])
    while todo:
        node = todo.popleft() if from_front else todo.pop()
        order.append(node.value)
        if node.left:
            todo.append(node.left)
        if node.right:
            todo.append(node.right)
    return order


def brute_force(root):
    """One full walk of the tree per depth; `visits` counts the nodes touched."""
    def collect(node, depth, wanted, out):
        nonlocal visits
        if node is None:
            return
        visits += 1
        if depth == wanted:
            out.append(node.value)
        collect(node.left, depth + 1, wanted, out)
        collect(node.right, depth + 1, wanted, out)

    visits, result = 0, []
    while True:
        level = []
        collect(root, 0, len(result), level)
        if not level:
            return result, visits
        result.append(level)


def example_tree():
    """The tree drawn in the video: four levels, deliberately lopsided."""
    return TreeNode(
        3,
        TreeNode(9, TreeNode(4), TreeNode(7, TreeNode(1))),
        TreeNode(20, None, TreeNode(15, None, TreeNode(8))),
    )


def chain(n):
    """A tree that is one long chain of right children: 1 -> 2 -> ... -> n."""
    root = node = TreeNode(1)
    for value in range(2, n + 1):
        node.right = TreeNode(value)
        node = node.right
    return root


if __name__ == "__main__":
    tree = example_tree()
    assert level_order(tree) == [[3], [9, 20], [4, 7, 15], [1, 8]]
    assert level_order(None) == []
    assert level_order(TreeNode(5)) == [[5]]
    assert level_order(chain(3)) == [[1], [2], [3]]
    assert walk(tree, from_front=True) == [3, 9, 20, 4, 7, 15, 1, 8]
    assert walk(tree, from_front=False) == [3, 20, 15, 8, 9, 7, 1, 4]
    assert brute_force(tree)[0] == level_order(tree)
    print("level order:", level_order(tree))
    print("stack order:", walk(tree, from_front=False))
    print("brute force visits:", brute_force(tree)[1], "for", 8, "nodes")
    print("brute force visits on a chain of 100:", brute_force(chain(100))[1])
    print("all checks passed")
