import pickle
import re

from flask import Flask, request, jsonify

model_file = 'model_spam.bin'

with open(model_file, 'rb') as f_in:
    vectorizer, model = pickle.load(f_in)

app = Flask('spam-detector')

THRESHOLD = 0.4

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})
    

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    text = data.get('text', '')
    cleaned = clean_text(text)

    X = vectorizer.transform([cleaned])
    y_pred = model.predict_proba(X)[0, 1]
    is_scam = y_pred >= THRESHOLD

    return jsonify({
        'is_scam': bool(is_scam),
        'probability': float(y_pred)
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)