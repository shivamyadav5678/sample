from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import joblib
import nltk

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, async_mode ='eventlet')

# Load the spam classifier and TF-IDF vectorizer
spam_classifier = joblib.load('./models/spam_classifier.pkl')
tfidf_vectorizer = joblib.load('./models/tfidf_vectorizer.pkl')

# Preprocessing function
def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    return ' '.join(tokens)

# Spam classification function
def classify_message(message):
    preprocessed_message = preprocess_text(message)
    vectorized_message = tfidf_vectorizer.transform([preprocessed_message])
    is_spam = spam_classifier.predict(vectorized_message)[0]
    return "spam" if is_spam else "ham"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# SocketIO events

@socketio.on('user_joined')
def handle_user_joined(data):
    username = data['username']
    # Broadcast to all users that the new user has joined
    emit('user_joined', {'username': username}, broadcast=True)

    
@socketio.on('send_message')
def handle_send_message(data):
    username = data['username']
    message = data['message']
    classification = classify_message(message)
    emit('receive_message', {
        'username': username,
        'message': message,
        'classification': classification
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
