# GitHub Webhook Event Tracker

## Overview

This project captures GitHub repository events (Push, Pull Request, and Merge) using Webhooks, stores them in MongoDB, and displays them in a minimal UI that refreshes every 15 seconds.

The system consists of two repositories:

- **action-repo** → Dummy GitHub repository that triggers webhook events
- **webhook-repo** → Flask application that receives webhook payloads, stores data in MongoDB, and renders UI

---

## Architecture
GitHub (action-repo)
│
│ Webhook (Push / Pull Request / Merge)
▼
Flask Webhook Receiver (/webhook)
│
▼
MongoDB
│
▼
UI (Polling every 15 seconds via /events API)

---

## Features

- Capture **Push** events
- Capture **Pull Request** events
- Capture **Merge** events (Bonus)
- Store structured event data in MongoDB
- Clean minimal UI
- Auto refresh UI every 15 seconds
- Prevent duplicate entries using unique `request_id`

---

---

## Setup Instructions

### 1 Clone Repository
git clone <your-webhook-repo-url>
cd webhook-repo

---

### 2 Create Virtual Environment
python -m venv venv

Activate: venv\Scripts\activate

---

### 3 Install Dependencies
pip install -r requirements.txt

---

### 4 Setup Environment Variables
Create `.env` file:
MONGO_URI=mongodb://localhost:27017/
DB_NAME=github
COLLECTION_NAME=events

---

### 5 Run Flask App
flask run
Server runs on:
http://127.0.0.1:5000

---

---

## Repositories

- action-repo: https://github.com/Ridhi1316/action-repo
- webhook-repo: https://github.com/Ridhi1316/webhook-repo

---




