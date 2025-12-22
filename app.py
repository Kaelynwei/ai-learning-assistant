from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        text = request.form['text']
        words = text.split()
        word_count = {w: words.count(w) for w in set(words)}
        result = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
