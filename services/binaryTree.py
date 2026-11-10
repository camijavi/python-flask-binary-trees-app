"""Bianry Tree & Binary Search Tree Core Data Structures and layout algorithms"""

from typing import Optional, List, Dict, Any

class TreeNode:
    """Represents a signle node in Binary Tree"""

    def __init__(self, val:int):
        self.val: int = val
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None

        #Normalized coordinates for SVG rendering (0.0 to 100%)
        self.x: float = 50.0
        self.y: float = 0.0
        self.depth: int = 0

    def toDict(self) -> Dict[str, Any]:
        """Convert the node and its subtree into a serializable dictionary"""
        return{
            "val": self.val,
            "x": round(self.x,2),
            "y": round(self.y, 2),
            "depth": self.depth,
            "left": self.left.toDict() if self.left else None,
            "right": self.right
        }

class BinarySearchTree:
    """Binary Search Tree implementation with visual layout calculation"""

    def __init__(self):
        self.root: Optional [TreeNode] = None

    def insert(self, val: int) -> TreeNode:
        """Insert a unique value the BST following standard BST rules."""
        if self.root is None:
            self.root = TreeNode(val)
            self.calculateLayout()
            return self.root
        
        current = self.root
        while True:
            if val == current.val:
                #Value already exists: return existing node
                return current
            elif val < current.val:
                if current.left is None:
                    current.left = TreeNode(val)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = TreeNode(val)
                    break
                current = current.right
        
        self.calculateLayout()
        return current

    def search(self, val: int) -> Dict[str, Any]:
        """
        Search for a value in the BST.
        Return whether it was found and the full path of visited nodes.
        Useful for step-by-step search animations in the simulator. :0
        """

        path = []
        current = self.root

        while current:
            path.append(current.val)
            if val == current.val:
                return {"found":True, "path": path}
            elif val < current.val:
                current = current.left
            else:
                current = current.right

        return {"found": False, "path": path}

    @classmethod
    def fromList(cls, values: List[int]) -> "BinarySearchTree":
        """Convenience factory method to build a tree from a list of integers."""

        bst = cls()
        for v in values:
            bst.insert(v)
        return bst

    def calculateLayout(self) -> None:
        """
        Calculate (x,y) coordinates for all nodes in the three.
        Uses In-Order traversal ranking for the X-axis:
        - Every left child is strictly to the left of its parent
        - Every right child is strictly to the right of its parent
        - Guaranteed zero node collisions regardless of tree balance
        """

        #Step 1: Assign depth (Y level)
        def assignDepth(node: Optional[TreeNode], currentDepth: int):
            if not node:
                return
            node.depth = currentDepth
            assignDepth(node.left, currentDepth + 1)
            assignDepth(node.right, currentDepth + 1)

        assignDepth(self.root, 0)

        #Step 2: In-Order traversal to determine X rank(1 to N)
        orderedNodes: List[TreeNode] = []

        def inOrderCollect(node: Optional[TreeNode]):
            if not node:
                return
            inOrderCollect(node.left)
            orderedNodes.append(node)
            inOrderCollect(node.right)

        inOrderCollect(self.root)
        totalNodes = len(orderedNodes)

        # Step 3: Compute percentage-based coordinates (0 to 100)
        # Y: 15% padding from top + 18% per depth level
        # X: Evenly distributed percentage from left to right

        for rank, node in enumerate(orderedNodes, start=1):
            if totalNodes == 1:
                node.x = 50.0
            else:
                #Leaves 10% margin on left and right borders
                node.x = 15.0 + (rank - 1) * (80.0 / (totalNodes - 1))

            node.y = 15.0 + node.depth * 18.0

    def toDict(self) -> Optional[Dict[str,Any]]:
        """Return full JSON-serializable tree structure."""

        return self.root.toDict() if self.root else None

    def getNodeCount(self) -> int:
        """Return the total number of nodes in the tree"""

        count = 0

        def traverse(node: Optional[TreeNode]):
            nonlocal count
            if not node:
                return
            count += 1
            traverse(node.left)
            traverse(node.right)

        traverse(self.root)
        return count
    