from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ API is Ready! Use /like?sid=SESSION_ID&url=POST_URL"

@app.route('/like')
def like_post():
    # ইউজার থেকে ডাটা নেওয়া
    sid = request.args.get('sid')
    post_url = request.args.get('url')

    # যদি ডাটা মিসিং থাকে
    if not sid or not post_url:
        return jsonify({
            "status": "error",
            "message": "Please provide both 'sid' (Session ID) and 'url' (Post Link)"
        }), 400

    try:
        # লিঙ্ক থেকে পোস্টের আইডি (Shortcode) বের করা
        if 'reels/' in post_url:
            shortcode = post_url.split('reels/')[1].split('/')[0]
        elif 'p/' in post_url:
            shortcode = post_url.split('p/')[1].split('/')[0]
        else:
            shortcode = post_url.split('/')[-2] if post_url.endswith('/') else post_url.split('/')[-1]

        like_url = f"https://www.instagram.com/api/v1/web/likes/{shortcode}/like/"
        
        # ইনস্টাগ্রামের জন্য রিকোয়েস্ট হেডাস
        headers = {
            "cookie": f"sessionid={sid}",
            "x-csrftoken": "en",
            "x-ig-app-id": "936619743392459",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15",
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://www.instagram.com/"
        }
        
        # লাইক পাঠানোর কমান্ড
        response = requests.post(like_url, headers=headers)
        
        return jsonify({
            "status": "success",
            "instagram_response": response.json()
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Vercel এর জন্য রান করার নিয়ম
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)
