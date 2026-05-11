from flask import Flask, jsonify, request
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)

API_KEYS = ["SABBIR"]

DB_FILE = "likes_db.json"


# -------------------------
# Load DB
# -------------------------
def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)


# -------------------------
# Save DB
# -------------------------
def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -------------------------
# Home Route
# -------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "developer": "Jihad X Codex"
    })


# -------------------------
# LIKE API
# -------------------------
@app.route("/like")
def like():
    uid = request.args.get("uid")
    server = request.args.get("server_name", "bd")
    key = request.args.get("key")

    # KEY CHECK
    if key not in API_KEYS:
        return jsonify({"status": "error", "message": "Invalid API Key"})

    # UID CHECK
    if not uid:
        return jsonify({"status": "error", "message": "UID Missing"})

    try:
        # -------------------------
        # ORIGINAL API CALL
        # -------------------------
        api_url = f"https://silent-vip-like-api.up.railway.app/like?uid={uid}&server_name={server}&key=MR19"
        response = requests.get(api_url, timeout=10)
        data = response.json()

        # -------------------------
        # Player Info
        # -------------------------
        player_name = data.get("PlayerNickname", "UNKNOWN")
        api_like = int(data.get("LikesGivenByAPI", 0))

        # -------------------------
        # Load DB (before like)
        # -------------------------
        db = load_db()
        before_like = db.get(uid, 0)

        # -------------------------
        # Extra Like System
        # -------------------------
        extra_like = 100
        total_like_added = api_like + extra_like

        # -------------------------
        # After Like
        # -------------------------
        after_like = before_like + total_like_added

        # -------------------------
        # Save new value
        # -------------------------
        db[uid] = after_like
        save_db(db)

        # -------------------------
        # Response
        # -------------------------
        return jsonify({
            "player_name": player_name,
            "uid": uid,
            "before_like": before_like,
            "api_like": api_like,
            "extra_like": extra_like,
            "like_added": total_like_added,
            "after_like": after_like,
            "server": server.upper(),
            "status": "success",
            "developer": "Jihad X Codex",
            "time": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)