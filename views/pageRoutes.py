from flask import Blueprint, render_template, abort

pagesBp = Blueprint("pages", __name__)

VALID_QUIZ_MODES = {"preorder", "inorder", "postorder"}

@pagesBp.route("/")
def dashboard():
    """Main dashboard hub"""
    return render_template("dashboard.html")

@pagesBp.route("/simulator")
def simulator():
    return render_template("simulator.html")

@pagesBp.route("/quiz/<mode>")
def quiz(mode: str):
    """Specific order quiz mode (preorder, inorder, postorder)."""
    modeLower = mode.lower()
    if modeLower not in VALID_QUIZ_MODES:
        abort(404)
    return render_template("quiz.html", mode = modeLower)

@pagesBp.route("/game")
def game():
    return render_template("game.html")