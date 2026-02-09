from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Instagram Fast Like API is Running!"

@app.route('/like')
def fast_like():
    # সরাসরি সেশন আইডি ব্যবহার করলে লগইন এরর আসবে না
    # URL: /like?sessionid=XXXXX&url=POST_URL
    sessionid = request.args.get('sessionid')
    post_url = request.args.get('url')

    if not sessionid or not post_url:
        return jsonify({"error": "Missing sessionid or url"}), 400

    try:
        # শর্টকাট মেথড: সরাসরি ইন্সটাগ্রাম এপিআই হিট করা
        shortcode = post_url.split('/')[-2]
        like_url = f"https://www.instagram.com/api/v1/web/likes/{shortcode}/like/"
        
        headers = {
            "Cookie": f"sessionid={sessionid}",
            "X-Csrftoken": "en", # dummy token
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.instagram.com/"
        }
        
        response = requests.post(like_url, headers=headers)
        
        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Post Liked!"})
        else:
            return jsonify({"status": "failed", "response": response.text}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def handler(event, context):
    return app(event, context)
