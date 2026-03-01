from flask import Flask, request, jsonify
from datetime import datetime
from routes.events import events_bp
from db.mongo import collection

app = Flask(__name__)

# Register Blueprint
app.register_blueprint(events_bp)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON payload received"}), 400

        # GitHub event header
        event = request.headers.get("X-GitHub-Event")

        # If testing from Postman (no header), allow manual event in body
        if not event:
            event = data.get("event_type")

        # Handle ping (GitHub sends automatically)
        if event == "ping":
            return jsonify({"msg": "Ping received"}), 200

        if event == "push":
            author = data["pusher"]["name"]
            to_branch = data["ref"].split("/")[-1]
            request_id = data["after"]

            doc = {
                "request_id": request_id,
                "author": author,
                "action": "PUSH",
                "from_branch": None,
                "to_branch": to_branch,
                "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
            }

        elif event == "pull_request":
            action = data.get("action")
            pr = data.get("pull_request", {})

            if action == "opened":
                doc = {
                    "request_id": str(pr.get("id")),
                    "author": pr.get("user", {}).get("login"),
                    "action": "PULL_REQUEST",
                    "from_branch": pr.get("head", {}).get("ref"),
                    "to_branch": pr.get("base", {}).get("ref"),
                    "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
                }

            elif action == "closed" and pr.get("merged"):
                doc = {
                    "request_id": str(pr.get("id")) + "_merge",
                    "author": pr.get("user", {}).get("login"),
                    "action": "MERGE",
                    "from_branch": pr.get("head", {}).get("ref"),
                    "to_branch": pr.get("base", {}).get("ref"),
                    "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
                }
            else:
                return jsonify({"msg": "Pull request action ignored"}), 200

        else:
            return jsonify({"msg": "Unsupported event"}), 200

        # Insert into MongoDB safely
        collection.insert_one(doc)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500