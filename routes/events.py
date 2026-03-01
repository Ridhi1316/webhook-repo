from flask import Blueprint, jsonify
from db.mongo import collection
from datetime import datetime

events_bp = Blueprint("events_bp", __name__)

@events_bp.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find().sort("_id", -1).limit(20))

    formatted_events = []

    for e in events:
        action = e.get("action")
        author = e.get("author")
        from_branch = e.get("from_branch")
        to_branch = e.get("to_branch")
        timestamp = e.get("timestamp")

        # timestamp
        if isinstance(timestamp, datetime):
            timestamp = timestamp.strftime("%d %B %Y - %I:%M %p UTC")

        if action == "PUSH":
            message = f'{author} pushed to {to_branch} on {timestamp}'
        elif action == "PULL_REQUEST":
            message = f'{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}'
        elif action == "MERGE":
            message = f'{author} merged branch {from_branch} to {to_branch} on {timestamp}'
        else:
            continue

        formatted_events.append({
            "id": str(e["_id"]),
            "message": message
        })

    return jsonify(formatted_events)

