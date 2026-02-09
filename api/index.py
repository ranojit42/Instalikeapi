from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# সুন্দর ওয়েবসাইট ডিজাইন (HTML)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Insta Liker Pro</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #fafafa; display: flex; justify-content: center; padding: 20px; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
        h2 { color: #e1306c; text-align: center; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #e1306c; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        #status { margin-top: 15px; font-size: 14px; text-align: center; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Insta Liker Pro</h2>
        <input type="text" id="user" placeholder="Username">
        <input type="password" id="pass" placeholder="Password">
        <input type="text" id="url" placeholder="Post URL">
        <button onclick="sendLike()">Send Like Now</button>
        <div id="status"></div>
    </div>

    <script>
        async function sendLike() {
            const status = document.getElementById('status');
            status.innerHTML = "Processing... please wait.";
            const user = document.getElementById('user').value;
            const pass = document.getElementById('pass').value;
            const url = document.getElementById('url').value;

            try {
                const res = await fetch(`/process?user=${user}&pass=${pass}&url=${url}`);
                const data = await res.json();
                status.innerHTML = data.message || data.error;
                status.style.color = data.status === 'success' ? 'green' : 'red';
            } catch (e) {
                status.innerHTML = "Error connecting to API";
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/process')
def process():
    user = request.args.get('user')
    password = request.args.get('pass')
    post_url = request.args.get('url')

    if not all([user, password, post_url]):
        return jsonify({"status": "error", "message": "All fields required!"})

    try:
        session = requests.Session()
        # Login Logic
        login_url = 'https://www.instagram.com/accounts/login/ajax/'
        time = int(requests.get('https://www.instagram.com').timestamp())
        payload = {'username': user, 'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}', 'queryParams': {}, 'optIntoOneTap': 'false'}
        headers = {'X-CSRFToken': 'en', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://www.instagram.com/'}
        
        login_res = session.post(login_url, data=payload, headers=headers)
        if 'authenticated":true' not in login_res.text:
            return jsonify({"status": "error", "message": "Login Failed! Check credentials."})

        # Like Logic
        shortcode = post_url.split('/')[-2]
        like_url = f"https://www.instagram.com/api/v1/web/likes/{shortcode}/like/"
        headers.update({"X-Instagram-AJAX": "1", "X-IG-App-ID": "936619743392459"})
        
        like_res = session.post(like_url, headers=headers)
        return jsonify({"status": "success", "message": "✅ Post Liked Successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def handler(event, context):
    return app(event, context)
