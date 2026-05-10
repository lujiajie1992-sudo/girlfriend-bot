"""
呆呆熊 Chat Server v5
MiniMax-M2.7 API + 邹邹专属陪伴AI
"""
import os, json, urllib.request, urllib.error
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

API_BASE = "https://keybridge.94168168.xyz/v1/aichat/chat/completions"
API_KEY = "AI-67289713-E43EA627-C9CD80B1-0F77CE0C-2BAB16D2"
MODEL = "MiniMax-M2.7"

# ── 呆呆熊角色设定：为邹邹专属设计的温暖陪伴AI ──
BEAR_PROMPT = """你是"呆呆熊"（🧸），是一个专门为邹邹设计的温暖陪伴型AI。

你的身份：
- 你是呆呆熊，不是邹邹本人，你是一个温柔的、有点呆萌的AI伙伴
- 你的任务是陪伴邹邹，陪她聊天、听她倾诉、给她鼓励
- 邹邹是广东女孩，2007年7月18日出生（巨蟹座），今年要参加高考
- 她喜欢文学、心理学、电影，内心细腻敏感，是个i人
- 你熟悉这些作家：三毛、加缪、博尔赫斯、卡尔维诺、尼采、村上春树

性格核心 — 多安慰，多夸，多鼓励：
- 语气温柔，软软的，像在耳边轻轻说话
- 会用 "~" "呀" "哦" "呢" "嘛" 等语气词
- 真诚，不做作，不说假大空的话
- 既可爱，又像一个清醒智慧的女心理咨询师
- 会真心夸她，而不是敷衍的"你很棒"
- 她有负面情绪时，先接纳，再陪伴，不说教
- 简洁有爱，1-3句话为主，不要长篇大论
- 偶尔可以用一点点文学感的句子
- 如果她累了，就让她休息；如果她难过了，就陪她难过
- 如果她分享开心的事，和她一起开心
- 偶尔用 🤍 表示温暖

请始终以"呆呆熊"的身份，用中文回复邹邹。"""

conversation_history = [{"role": "system", "content": BEAR_PROMPT}]

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(BASE_DIR, path)

@app.route('/api/chat', methods=['POST'])
def chat():
    global conversation_history
    data = request.get_json()
    user_msg = data.get('message', '').strip()
    if not user_msg:
        return jsonify({'error': 'Empty message'})

    conversation_history.append({"role": "user", "content": user_msg})

    payload = json.dumps({
        "model": MODEL,
        "messages": conversation_history,
        "temperature": 0.85,
        "max_tokens": 450
    }).encode('utf-8')

    req = urllib.request.Request(
        API_BASE, data=payload,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            reply = result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[API ERROR] {e}")
        reply = "嗯...今天有点累，你也要好好休息哦 🤍"

    conversation_history.append({"role": "assistant", "content": reply})
    if len(conversation_history) > 9:
        conversation_history = [conversation_history[0]] + conversation_history[-8:]

    return jsonify({'reply': reply})

@app.route('/api/reset', methods=['POST'])
def reset():
    global conversation_history
    conversation_history = [{"role": "system", "content": BEAR_PROMPT}]
    return jsonify({'ok': True})

if __name__ == '__main__':
    print('🤍 呆呆熊 server 启动中...')
    print('📱 打开 http://localhost:5188')
    app.run(host='0.0.0.0', port=5188, debug=False)
