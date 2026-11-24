from tree_node import TreeNode
from test_utils.utils import build_test_tree
from collections import deque 

def print_level_order( root: TreeNode):
	if not root:
		return
	q = deque()
	q.append(root)

	while q:
		node = q.popleft()
		print(node.value, end=" ")
		if node.left:
			q.append(node.left) 
		
		if node.right:
			q.append(node.right)
	print()

if __name__ == "__main__":
	root = build_test_tree()
	print_level_order(root)