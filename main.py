from flask import Flask, request, jsonify
from instagrapi import Client
import os

app = Flask(__name__)

@app.route('/mass_like', methods=['GET'])
def mass_like():
    # URL format: /mass_like?url=POST_URL&accounts=USER1:PASS1,USER2:PASS2
    post_url = request.args.get('url')
    accounts_str = request.args.get('accounts')

    if not post_url or not accounts_str:
        return jsonify({"status": "error", "message": "Missing URL or accounts (format: user:pass,user:pass)"}), 400

    results = {"success": 0, "failed": 0}
    accounts = accounts_str.split(',')

    for acc in accounts:
        if ':' not in acc: continue
        user, pwd = acc.split(':')
        cl = Client()
        try:
            cl.login(user, pwd)
            media_id = cl.media_id(cl.media_pk_from_url(post_url))
            cl.media_like(media_id)
            results["success"] += 1
        except Exception:
            results["failed"] += 1

    return jsonify({
        "status": "completed",
        "total_success": results["success"],
        "total_failed": results["failed"]
    })

# Vercel handler
def handler(event, context):
    return app(event, context)