from tree_node import TreeNode

def build_test_tree():
	node = TreeNode(314)

	node.left = TreeNode(6) 
	node.right = TreeNode(6)

	node.left.left = TreeNode(271)
	node.left.right = TreeNode(561)

	node.left.left.left = TreeNode(28)
	node.left.left.right = TreeNode(0)

	node.left.right.right = TreeNode(3)
	node.left.right.left = TreeNode(17)

	node.right.left = TreeNode(2)
	node.right.right = TreeNode(271)

	node.right.left.right = TreeNode(1)
	node.right.left.right.left = TreeNode(401)
	node.right.left.right.right = TreeNode(257)

	node.right.left.right.left.right = TreeNode(641)

	return node
