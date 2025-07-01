from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

import os
import random
import requests

# Load environment variables from .env file
load_dotenv()



# Setup Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Allow up to 2MB form data


# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///generations.db'
db = SQLAlchemy(app)

# Define supported genres
GENRES = ['Fantasy', 'Sci-Fi', 'Romance', 'Horror', 'Mystery', 'Adventure', 'Historical','Dark Romance']

# Define database model
class Generation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50))
    word_count = db.Column(db.Integer)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def get_prompt(genre, word_count):
    if genre == "Dark Romance":
        return (
            f"A passage from a forgotten gothic romance novel, written in the 1800s. "
            f"Include themes of heartbreak, obsession, and forbidden love. Keep it exactly {word_count} words:\n"
        )

    elif genre == "Fantasy":
        return (
            f"An excerpt from a published fantasy novel set in a magical realm. "
            f"Use immersive world-building, myth, and magic. Exactly {word_count} words:\n"
        )

    elif genre == "Sci-Fi":
        return (
            f"A passage from a futuristic science fiction novel once featured in a sci-fi anthology. "
            f"Focus on technology, mystery, or space. Keep it exactly {word_count} words:\n"
        )

    elif genre == "Romance":
        return (
            f"A passage from a classic romantic novel. Center it on love, longing, or a quiet emotional moment. "
            f"Exactly {word_count} words:\n"
        )

    elif genre == "Horror":
        return (
            f"A chilling excerpt from a published horror anthology. Use suspense, psychological fear, or the supernatural. "
            f"Exactly {word_count} words:\n"
        )

    elif genre == "Mystery":
        return (
            f"A mysterious scene from an old detective novel. Someone disappears, something is hidden, or a secret is revealed. "
            f"Exactly {word_count} words:\n"
        )

    elif genre == "Adventure":
        return (
            f"A published adventure tale from a classic pulp fiction magazine. Use fast pace and high stakes. "
            f"Exactly {word_count} words:\n"
        )

    elif genre == "Historical":
        return (
            f"A dramatic passage from a published historical novel. Set in a vivid historical era. "
            f"Exactly {word_count} words:\n"
        )

    else:
        return (
            f"An excerpt from a published {genre.lower()} work. Keep it refined, evocative, and exactly {word_count} words:\n"
        )


def generate_text(genre, word_count):
    prompt = get_prompt(genre, word_count) 
    try:
        buffer_words = int(word_count * 1.5)
        result = generator(
            prompt,
            max_new_tokens=buffer_words + 40,
            do_sample=True,
            temperature=0.9,
            pad_token_id=50256
        )

        generated = result[0]['generated_text'][len(prompt):].strip()
        words = generated.split()

        if len(words) < word_count:
            return ' '.join(words)

        # Try to truncate to sentence end
        text = ' '.join(words[:buffer_words])
        end_punct = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
        if end_punct != -1:
            sentence = text[:end_punct + 1]
            if len(sentence.split()) >= word_count:
                return sentence.strip()

        return ' '.join(words[:word_count]) + "..."

    except Exception as e:
        return f"Error generating text: {e}"
    
@app.route('/')
def index():
    return render_template('index.html')

# Route: Generate book text
@app.route('/generate', methods=['POST'])
def generate():
    try:
        count = int(request.form['word_count'])
        if count < 5 or count > 500:
            return redirect('/')
    except:
        return redirect('/')

    genre = request.form.get("genre")

    text = generate_text(genre, count)

    generation = Generation(genre=genre, word_count=count, content=text)
    db.session.add(generation)
    db.session.commit()

    return render_template('result.html', genre=genre, word_count=count, text=text)

# Route: Optional history
@app.route('/history')
def history():
    gens = Generation.query.order_by(Generation.timestamp.desc()).limit(10).all()
    return render_template('history.html', generations=gens)

# Start the server
if __name__ == '__main__':
    app.run(debug=True)
