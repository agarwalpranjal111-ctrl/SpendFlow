from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Below this confidence, we don't trust the prediction enough to use it
CONFIDENCE_THRESHOLD = 0.4

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    message = (data.get('message') or '').strip()

    if not message:
        return jsonify({'category': 'uncategorized', 'confidence': 0.0})

    X_vec = vectorizer.transform([message])
    probabilities = model.predict_proba(X_vec)[0]
    best_index = probabilities.argmax()
    confidence = float(probabilities[best_index])
    predicted_category = model.classes_[best_index]

    if confidence < CONFIDENCE_THRESHOLD:
        return jsonify({'category': 'uncategorized', 'confidence': confidence})

    return jsonify({'category': predicted_category, 'confidence': confidence})

if __name__ == '__main__':
    app.run(port=6000)