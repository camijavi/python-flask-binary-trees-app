import random
from typing import Dict, Any, List
from services.binaryTree import BinarySearchTree
from services.traversals import getPreorder, getInorder, getPostOrder

#Stage configu rules: (nodeCount, timeLimitSeconds)
STAGE_DIFFICULTY_TABLE = {
    1: {"nodes": 3, "timeLimit": 30},
    2: {"nodes": 5, "timeLimit": 25},
    3: {"nodes": 7, "timeLimit": 20},
    4: {"nodes": 8, "timeLimit": 18},
    5: {"nodes": 9, "timeLimit": 15},
}

def generateBalancedValues(count: int) -> List[int]:
    """
    Generate unique 2-digit integers arranged to produce a well-balanced tree
    with interesting left and right branches (avoiding degenerate linear lines).
    """

    # Pick random distinct 2-digit numbers
    pool = sorted(random.sample(range(10,99), count))

    #Helper to insert median first (recursively creates a balanced BST)
    def pickBalancedOrder(arr: List[int]) -> List[int]:
        if not arr:
            return[]

        mid = len(arr) // 2
        root = arr[mid]
        leftPart = arr[:mid]
        righPart = arr[mid + 1 :]
        return [root] + pickBalancedOrder(leftPart) + pickBalancedOrder(righPart)

    insertionOrder = pickBalancedOrder(pool)

    # For stages > 3, introduce slight asymmetry so the student experiences real-world trees
    if count > 5 and random.random() > 0.4:
        #Swap two non-root elements slightly
        swapIdx = random.randint(1, len(insertionOrder) - 1)
        insertionOrder[1], insertionOrder[swapIdx] = (
            insertionOrder[swapIdx],
            insertionOrder[1],
        )
    return insertionOrder

def generateTreeByCount(nodeCount: int) -> BinarySearchTree:
    """Creates a BinarySearchTree with the requested number of unique nodes."""
    values = generateBalancedValues(nodeCount)
    return BinarySearchTree.fromList(values)

def generateQuizStage(mode: str, stage: int = 1) -> Dict[str, Any]:
    """
    Generate a quiz stage for a specific traversal mode ('preorder', 'inorder', 'postorder')
    Returns the serialized tree, time limit, and expected node sequence.
    """

    mode = mode.lower()
    config = STAGE_DIFFICULTY_TABLE.get(stage, {"nodes":10, "timeLimit":15})
    nodeCount = config["nodes"]
    timeLimit = config["timeLimit"]

    tree = generateTreeByCount(nodeCount)

    #Compute expected traversal sequence

    if mode == "preorder":
        expectedSequence = getPreorder(tree.root)
        modeTitle = "Pre-Order"
        ruleDescription = "Root -> Left -> Right"
    elif mode == "inorder":
        expectedSequence = getInorder(tree.root)
        modeTitle = "In-Order"
        ruleDescription = "Left -> Root -> Right"
    elif mode == "postorder":
        expectedSequence = getPostOrder(tree.root)
        modeTitle = "Post-Order"
        ruleDescription = "Left -> Right -> Root"
    else:
        raise ValueError(f"Unknown traversal mode: {mode}")

    return {
        "stage": stage,
        "mode": mode,
        "modeTitle": modeTitle,
        "ruleDescription": ruleDescription,
        "timeLimit": timeLimit,
        "nodeCount": nodeCount,
        "tree": tree.toDict(),
        "expectedSequence": expectedSequence,
    }

def generateCombinedChallenge(stage: int = 1) -> Dict [str, Any]:
    """
    generate a challenge for Combined Survival Mode.
    Randomly selects one of the 3 traversal types and applies fast timers.
    """

    modes = ["preorder", "inorder", "postorder"]
    chosenMode = random.choice(modes)

    challenge = generateQuizStage(chosenMode, stage)

    # Slightly tighter time limit for combined survival mode
    challenge ["timeLimit"] = max(10, challenge["timeLimit"] - 3)
    challenge["isSurvival"] = True

    return challenge 
