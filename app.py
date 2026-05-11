from flask import Flask, jsonify, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

API_KEYS = ["MR19"]


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "developer": "Jihad X Codex"
    })


@app.route("/like")
def like():
    uid = request.args.get("uid")
    server = request.args.get("server_name", "bd")
    key = request.args.get("key")

    if key not in API_KEYS:
        return jsonify({"status": "error", "message": "Invalid API Key"})

    if not uid:
        return jsonify({"status": "error", "message": "UID Missing"})

    try:
        # ORIGINAL API CALL
        api_url = f"https://silent-vip-like-api.up.railway.app/like?uid={uid}&server_name={server}&key=MR19"
        response = requests.get(api_url, timeout=10)
        data = response.json()

        # BEFORE LIKE (original API)
        before_like = int(data.get("LikesbeforeCommand", 0))

        # API LIKE (original)
        api_like = int(data.get("LikesGivenByAPI", 0))

        # AFTER LIKE (calculated)
        after_like = before_like + api_like

        return jsonify({
            "status": "success",
            "uid": uid,
            "server": server.upper(),
            "player_name": data.get("PlayerNickname", "UNKNOWN"),

            "before_like": before_like,
            "api_like": api_like,
            "after_like": after_like,

            "developer": "Jihad X Codex",
            "time": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
