from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import hashlib
import hmac
import time

app = Flask(__name__)
CORS(app)

# 你的讯飞信息（不用改）
APPID = "c3da867f"
APIKey = "5b816a733013339b4b8c54a44b1c9a672"
APISecret = "ZjY3MTRkMjA0ZDE4ZjQxODEyMDBINWJ1"

def get_auth_header():
    date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
    signature_origin = f"host: api.xfyun.cn\ndate: {date}\nGET /v2/iat HTTP/1.1"
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
    try:
        audio_file = request.files['audio']
        audio_base64 = base64.b64encode(audio_file.read()).decode()

        params = {
            "common": {"app_id": APPID},
            "business": {"aue": "raw", "engine_type": "sms16k_en", "sample_rate": 16000},
            "data": {"status": 2, "audio": audio_base64}
        }

        url = "https://api.xfyun.cn/v2/iat"  # 语音听写接口（你已开通）
        headers = get_auth_header()
        response = requests.post(url, headers=headers, json=params)
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def index():
    return "语音转文字后端已运行！"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
