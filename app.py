from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# 从环境变量读取 OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        # 1. 获取前端上传的音频和参考文本
        audio_file = request.files['audio']
        ref_text = request.form.get('ref_text', 'Hello, this is a test.')

        # 2. 调用 Whisper 进行英文语音转文字
        transcript = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            language="en"  # 指定英文，识别更精准
        )
        recognized_text = transcript['text'].strip()

        # 3. 简易发音评分：对比识别结果与参考文本
        ref_words = ref_text.lower().split()
        rec_words = recognized_text.lower().split()
        match_count = sum(1 for w in rec_words if w in ref_words)
        score = int((match_count / len(ref_words)) * 100) if ref_words else 0

        return jsonify({
            "code": 0,
            "message": "success",
            "data": {
                "reference_text": ref_text,
                "recognized_text": recognized_text,
                "pronunciation_score": score
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def index():
    return "Whisper 口语评测后端已运行！"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
