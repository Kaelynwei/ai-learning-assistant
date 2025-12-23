from flask import Flask, render_template, request
import json
from datetime import datetime

HISTORY_FILE = 'history.json'

def load_history():
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_history(item):
    history = load_history()
    history.append(item)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    history = load_history()  # 先把舊的歷史讀出來

    if request.method == 'POST':
        text = request.form['text']
        words = text.split()
        word_count = {w: words.count(w) for w in set(words)}
        result = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

        history_item = {
            "time": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "text_preview": text[:20],
            "top_word": result[0][0] if result else None
        }
        save_history(history_item)      # 把新的紀錄加進檔案
        history = load_history()        # 再讀一次，拿到更新後的全部

    # 傳「最近 5 筆」給前端
    return render_template('index.html', 
                           result=result, 
                           history=history[-5:])



if __name__ == '__main__':
    app.run(debug=True)
