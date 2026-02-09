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
        return jsonify({"error": "Username, Password, and URL are required!"}), 400

    try:
        session = requests.Session()
        # লগইন করে সেশন আইডি বের করার প্রসেস
        res = session.get('https://www.instagram.com/')
        csrf = res.cookies['csrftoken']
        
        login_data = {'username': user, 'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1612345678:{pw}'}
        headers = {'X-CSRFToken': csrf, 'Referer': 'https://www.instagram.com/'}
        
        login_res = session.post('https://www.instagram.com/accounts/login/ajax/', data=login_data, headers=headers)
        
        if 'authenticated":true' in login_res.text:
            # লাইক দেওয়ার প্রসেস
            shortcode = post_url.split('/')[-2]
            like_url = f"https://www.instagram.com/api/v1/web/likes/{shortcode}/like/"
            session.post(like_url, headers={'X-CSRFToken': session.cookies['csrftoken']})
            return jsonify({"status": "success", "message": f"Liked by {user}!"})
        else:
            return jsonify({"status": "failed", "message": "Login failed! Wrong password or 2FA on."})

    except Exception as e:
        return jsonify({"error": str(e)})

def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)
