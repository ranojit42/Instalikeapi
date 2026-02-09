from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Insta Liker is Active! Use /auto?user=USERNAME&pass=PASSWORD&url=POST_URL"

@app.route('/auto')
def auto_like():
    user = request.args.get('user')
    pw = request.args.get('pass')
    post_url = request.args.get('url')

    if not all([user, pw, post_url]):
        return jsonify({"error": "Missing params"}), 400

    try:
        session = requests.Session()
        # CSRF হ্যান্ডেল করার নিরাপদ উপায়
        res = session.get('https://www.instagram.com/')
        csrf = session.cookies.get('csrftoken', 'en') 
        
        login_url = 'https://www.instagram.com/accounts/login/ajax/'
        login_data = {
            'username': user, 
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1720000000:{pw}',
            'queryParams': "{}",
            'optIntoOneTap': 'false'
        }
        headers = {
            'X-CSRFToken': csrf, 
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        login_res = session.post(login_url, data=login_data, headers=headers)
        
        if login_res.status_code == 200 and login_res.json().get('authenticated'):
            # শর্টকোড বের করা
            shortcode = post_url.split('/')[-2] if post_url.endswith('/') else post_url.split('/')[-1]
            like_url = f"https://www.instagram.com/api/v1/web/likes/{shortcode}/like/"
            
            # নতুন CSRF দিয়ে লাইক দেওয়া
            headers['X-CSRFToken'] = session.cookies.get('csrftoken', csrf)
            headers['X-IG-App-ID'] = "936619743392459"
            
            like_res = session.post(like_url, headers=headers)
            return jsonify({"status": "success", "message": f"Liked by {user}"})
        else:
            return jsonify({"status": "failed", "message": "Login Failed. Check User/Pass or 2FA."})

    except Exception as e:
        return jsonify({"error": str(e)})

# Vercel-এর জন্য বাড়তি হ্যান্ডলার দরকার নেই যদি vercel.json ঠিক থাকে
