from flask import Flask, jsonify
from views.pageRoutes import Pages

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello, Binary Trees! wow </h1>"

@app.route("/api/status")
def status():
    return jsonify({"status":"running", "framework":"Flask"})

if __name__ == "__main__":
    app.run(debug=True)