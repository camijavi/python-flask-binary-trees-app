from flask import Blueprint, jsonify, request
from services.difficultyEngine import generateQuizStage

quizBp = Blueprint("quiz", __name__)

VALID_MODES = {"preorder", "inorder", "postorder"}

@quizBp.route("/challenge", methods = ["GET"])
def getChallenge():
    """Fecth a stage challenge with generated tree and target sequence"""
    mode = request.args.get("mode", default="inorder").lower()
    stage = request.args.get("stage", default=1, type=int)

    if mode not in VALID_MODES:
        return jsonify({"error":f"Invalid mode. Choose from {list(VALID_MODES)}"}), 400

    stage = max(1, min(10, stage))

    challenge = generateQuizStage(mode=mode, stage=stage)
    return jsonify(challenge)

@quizBp.route("/validate", methods=["POST"])
def validateSequence():
    """Validate a submitted sequence against expected traversal order."""

    data = request.get_json() or {}
    expected = data.get("expected", [])
    userSequence = data.get("userSequence", [])

    isCorrect = (expected == userSequence)
    matchedCount = sum(1 for e, u in zip(expected, userSequence) if e == u)

    return jsonify({
        "isCorrect": isCorrect,
        "matchedCount": matchedCount,
        "totalExpected": len(expected)
    })