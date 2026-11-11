from flask import Blueprint, jsonify, request
from services.binaryTree import BinarySearchTree
from services.traversals import generateTraversalTrace
from services.difficultyEngine import generateTreeByCount

simulatorBp = Blueprint("simulator", __name__)

@simulatorBp.route("/build", methods = ["POST"])
def buildTreee():
    """Build a Binary Search Tree from a list of integer values."""
    data = request.get_json() or {}
    rawValues = data.get("values", [])

    # filter and parse integers
    values = []
    for item in rawValues:
        try:
            values.append(int(item))
        except(ValueError, TypeError):
            continue

    if not values:
        return jsonify({"error": "No valid numeric values provided"}), 400

    bst = BinarySearchTree.fromList(values)
    return jsonify({
        "tree": bst.toDict(),
        "count":bst.getNodeCount(),
        "values": values
    })


@simulatorBp.route("/random", methods = ["GET"])
def randomTree():
    """Generate a random balance tree for playground experimentation."""
    nodes = request.args.get("nodes", default=7, type= int)
    nodes = max(3, min(15, nodes)) #keep between 3 and 15 nodes for visual cleanliness

    bst = generateTreeByCount(nodes)
    return jsonify({
        "tree": bst.toDict(),
        "count": bst.getNodeCount()
    })


@simulatorBp.route("/search", methods=["POST"])
def searchNode():
    """Search for a value in the tree and return the step-by-step path visited"""
    data = request.get_json() or {}
    values = data.get("values", [])
    target = data.get("target")

    if target is None:
        return jsonify({"error": "Target value is required"}), 400

    try:
        target = int(target)
    except (ValueError, TypeError):
        return jsonify({"error": "Target must be an integer"}), 400

    bst = BinarySearchTree.fromList(values)
    searchResult = bst.search(target)
    return jsonify(searchResult)

@simulatorBp.route("/trace", methods = ["POST"])
def traversalTrace():
    """Generate the frame-by-frame animation script for the simulator"""
    data = request.get_json() or {}
    values = data.get("values", [])
    traversal = data.get("traversal", "inorder").lower()

    if traversal not in {"preorder","inorder", "postorder"}:
        return jsonify({"error": "Invalid travesal. Must be preorder, inorder, or postorder"}), 400

    bst = BinarySearchTree.fromList(values)
    frames = generateTraversalTrace(bst.root, traversal)

    return jsonify({
        "traversal": traversal,
        "frames": frames,
        "totalSteps": len(frames)
    })