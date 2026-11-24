from dataclasses import dataclass

@dataclass
class TreeNode:
	value: int
	left: TreeNode | None = None
	right: TreeNode | None = None
