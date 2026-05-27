
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # 允许所有来源的跨域请求，生产环境应限制特定域名

WISHES_FILE = 'wishes.json'

def load_wishes():
    if not os.path.exists(WISHES_FILE):
        return []
    with open(WISHES_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_wishes(wishes):
    with open(WISHES_FILE, 'w', encoding='utf-8') as f:
        json.dump(wishes, f, ensure_ascii=False, indent=4)

@app.route('/wish', methods=['POST'])
def submit_wish():
    data = request.get_json()
    wish_text = data.get('wish')
    if not wish_text:
        return jsonify({'error': 'Wish text is required'}), 400

    wishes = load_wishes()
    new_wish = {
        'id': len(wishes) + 1,
        'text': wish_text,
        'timestamp': datetime.now().isoformat()
    }
    wishes.append(new_wish)
    save_wishes(wishes)
    return jsonify({'message': 'Wish submitted successfully', 'wish': new_wish}), 201

@app.route('/wishes', methods=['GET'])
def get_wishes():
    wishes = load_wishes()
    return jsonify(wishes), 200

if __name__ == '__main__':
    port = int(os.environ.get(\'PORT\', 5000))
    app.run(host=\'0.0.0.0\', port=port)
