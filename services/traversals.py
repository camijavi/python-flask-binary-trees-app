from typing import Optional, List, Dict, Any
from services.binaryTree import TreeNode

def getPreorder(root: Optional[TreeNode]) -> List[int]:
    """Pre-order Traversal: Root -> Left -> Right"""

    result: List[int] = []

    def traverse(node: Optional[TreeNode]):
        if not node:
            return
        result.append(node.val)
        traverse(node.left)
        traverse(node.right)

    traverse(root)
    return result

def getInorder(root: Optional[TreeNode]) -> List[int]:
    """In-order Traversal: Left -> Root -> Right (Sorted order in BST)"""

    result: List[int] = []

    def traverse(node: Optional[TreeNode]):
        if not node:
            return
        traverse(node.left)
        result.append(node.val)
        traverse(node.right)

    traverse(root)
    return result

def getPostOrder(root: Optional[TreeNode]) -> List[int]:
    """Post-order Traversal: Left -> Right -> Root"""
    result: List[int] = []

    def traverse(node: Optional[TreeNode]):
        if not node:
            return
        traverse(node.left)
        traverse(node.right)
        result.append(node.val)
    traverse(root)
    return result

def generateTraversalTrace(root: Optional[TreeNode], traversalType: str) -> List[Dict[str, Any]]:
    """
    Generate an animation tarce (frame-by-frame) for simulator
    Each frame contains the active node, explanation, pseudocode line and output state
    """

    if not root:
        return[]

    traversalType = traversalType.lower()
    frames: List[Dict[str,Any]] = []
    outputSoFar: List[int] = []

    def addFrame(node: TreeNode, action: str, explanation: str, codeLine: int):
       frames.append(
           {
               "step": len(frames) + 1,
               "activeNode": node.val,
               "action": action,
               "explanation": explanation,
               "codeLine": codeLine,
               "outputSoFar": list(outputSoFar),
           }
       )

    # --- Pre-order: Root -> Left -> Right ---

    if traversalType == "preorder":
        def tracePreorder(node: Optional[TreeNode]):
            if not node:
                return

            #1. Visit Root
            outputSoFar.append(node.val)
            addFrame(node, "visit", f"Visiting Root Node {node.val}. Added to Pre-order output.", codeLine=1)

            if node.left:
                addFrame(node, "stepLeft", f"From Node {node.val}, traversing into Right Subtree (Node {node.right.val}).", codeLine=3)
                tracePreorder(node.right)
        tracePreorder(root)

    # --- In-order: Left -> Root -> Right ---
    elif traversalType == "inorder":
        def traceInorder (node: Optional[TreeNode]):
            if not node:
                return

            #1. Recurse Left 
            if node.left:
                addFrame(
                    node,
                    "stepLeft",
                    f"Going left from Node {node.val} into Node {node.left.val}.",
                    codeLine= 11
                    )
                traceInorder(node.val)

            # 2. Visit Root
            outputSoFar.append(node.val)
            addFrame(
                node,
                "visit",
                f"Visiting Node {node.val} (Left subtree finished). Added to In-order output.",
                codeLine= 2
            )

            # 3.Recurse Right
            if node.right:
                addFrame(
                    node,
                    "stepRight",
                    f"Going Right from Node {node.val} into Node {node.right.val}.",
                    codeLine= 3,
                )

                traceInorder(node.right)

        traceInorder(root)


    # --- Post-order: Left -> Right -> Root
    elif traversalType == "postorder":
        def tracePostorder(node: Optional[TreeNode]):
            if not node:
                return

            #1. Recurse Left
            if node.left:
                addFrame(
                    node,
                    "stepLeft",
                    f"Traversing Left from Node {node.val} to Node {node.left.val}.",
                    codeLine= 1,
                )
                tracePostorder(node.left)

            # 2. Recurse Right
            if node.right:
                addFrame(
                    node,
                    "stepRight",
                    f"Traversing Right from Node {node.val} to Node {node.right.val}.",
                    codeLine= 2,
                )

                tracePostorder(node.right)

            # 3. Visit Root
            outputSoFar.append(node.val)
            addFrame(
                node,
                "Visit",
                f"Visit Node {node.val} (Both subtrees visited). Added to Post-order output.",
                codeLine= 3 
            )
            


