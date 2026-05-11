from flask import Flask, jsonify, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

API_KEY = "SABBIR"


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "developer": "Jihad X Codex"
    })


@app.route("/like")
def like():

    uid = request.args.get("uid")
    server = request.args.get("server_name", "BD")

    if not uid:
        return jsonify({
            "status": "error",
            "message": "UID Missing"
        })

    try:

        # ORIGINAL API
        api_url = (
            f"https://sabbir-codex-like.vercel.app/"
            f"like?uid={uid}&server_name={server}&key={API_KEY}"
        )

        response = requests.get(api_url, timeout=10)
        data = response.json()

        # ORIGINAL VALUES
        before_like = int(data.get("LikesbeforeCommand", 0))
        api_like = int(data.get("LikesGivenByAPI", 0))

        # EXTRA LIKE
        extra_like = 100

        # FINAL LIKE
        total_added = api_like + extra_like
        after_like = before_like + total_added

        return jsonify({

            "PlayerNickname": data.get("PlayerNickname", "UNKNOWN"),

            "UID": uid,

            "LikesbeforeCommand": before_like,

            "LikesGivenByAPI": total_added,

            "LikesafterCommand": after_like,

            "remains": data.get("remains", "(90/90)"),

            "status": data.get("status", 2),

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
