from flask import Flask, request, jsonify
from instagrapi import Client

app = Flask(__name__)

@app.route('/')
def home():
    return "Instagram Like API is Online!"

@app.route('/mass_like')
def mass_like():
    post_url = request.args.get('url')
    accounts_str = request.args.get('accounts')

    if not post_url or not accounts_str:
        return jsonify({"error": "Missing parameters"}), 400

    results = {"success": 0, "failed": 0}
    # accounts format: user:pass,user2:pass2
    account_list = accounts_str.split(',')

    for acc in account_list:
        try:
            u, p = acc.split(':')
            cl = Client()
            cl.login(u, p)
            media_id = cl.media_id(cl.media_pk_from_url(post_url))
            cl.media_like(media_id)
            results["success"] += 1
        except Exception as e:
            results["failed"] += 1
            print(f"Error for {acc}: {e}")

    return jsonify(results)

# Vercel handler
def handler(event, context):
    return app(event, context)
