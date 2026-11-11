from flask import Blueprint, jsonify, request
from services.difficultyEngine import generateCombinedChallenge

gameBp = Blueprint("game", __name__)

@gameBp.route("/roud", methods = ["GET"])
def getRound():
    """Generate a combined survival mode round with a randomly assigned traversal."""
    stage = request.args.get("stage", default=1, type=int)
    stage = max(1, min(10, stage))

    challenge = generateCombinedChallenge(stage=stage)
    return jsonify(challenge)

@gameBp.route("/calculate-score", methods = ["POST"])
def calculateScore():
    """Calculate points based on sateg cleared, remaining time and active combo streak."""

    data = request.get_json() or {}
    stage = max(1, int(data.get("stage",1)))
    timeLeft = max(0, float(data.get("timeLeft", 0)))
    streak = max(0, int(data.get("streak", 0)))

    #Scoring formula

    basePoints = stage * 100
    timeBonus = int(timeLeft * 15)
    multiplier = min(3.0, 1.0 + (streak * 0.2))
    totalEarned = int((basePoints + timeBonus) * multiplier)

    return jsonify({
        "basePoints": basePoints,
        "timeBonus": timeBonus,
        "multiplier": round(multiplier, 2),
        "totalEarned": totalEarned
    })