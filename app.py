from flask import Flask, request, jsonify
import requests
import base64
import hashlib
import hmac
import time

app = Flask(__name__)

# 👉 改成你自己的讯飞信息
APPID = "c3da867f"
APIKey = "5b816a73013339b4b8c54a44b1c9a672"
APISecret = "ZjY3MTRkMjA0ZDE4ZjQxODEyMDBlNWJl"

def get_auth_header():
    date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
    signature_origin = f"host: api.xfyun.cn\ndate: {date}\nGET /v2/ise HTTP/1.1"
    signature_sha = hmac.new(APISecret.encode(), signature_origin.encode(), digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(signature_sha).decode()
    authorization_origin = f'api_key="{APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    authorization = base64.b64encode(authorization_origin.encode()).decode()
    return {
        "Authorization": authorization,
        "Date": date,
        "Host": "api.xfyun.cn"
    }

@app.route('/evaluate', methods=['POST'])
def evaluate():
    audio_file = request.files['audio']
    ref_text = request.form.get('ref_text', 'Hello')
    audio_base64 = base64.b64encode(audio_file.read()).decode()

    params = {
        "app_id": APPID,
        "language": "en",
        "accent": "mandarin",
        "text": ref_text,
        "audio": audio_base64,
        "audio_type": "wav",
        "level": "sentence"
    }

    url = "https://api.xfyun.cn/v2/ise"
    headers = get_auth_header()
    response = requests.post(url, headers=headers, json=params)
    return jsonify(response.json())

@app.route('/')
def index():
    return "语音打分后端已运行！"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
