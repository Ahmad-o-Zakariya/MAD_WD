# 🖋️ AI Story & Poetry Generator

A **Flask web application** that generates AI-written stories and poems based on **genre** and **word count**, with no external API required.  
It uses **Hugging Face GPT-2** locally via `transformers` and includes its **own Flask API** for generation and history tracking.

---

## ✨ Features

1. **Genre Selection**  
   - Fantasy, Sci-Fi, Romance, Horror, Mystery, Adventure, Historical, Poetry, Dark Romance

2. **Word Count Control**  
   - Enter any number between **5 and 500 words**  
   - Generates text that feels like a published literary excerpt

3. **Offline AI Text Generation**  
   - Uses **Hugging Face GPT-2** locally  
   - Prompts designed to simulate classic published works

4. **SQLite Database Storage**  
   - Stores generated texts with timestamps and metadata  
   - Easily accessible with Flask-SQLAlchemy

5. **Mini API Endpoints**  
   - `/generate` → Accepts form input and generates text  
   - `/history` → Shows the last 10 generated outputs

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python)  
- **AI Model**: Hugging Face `gpt2` via `transformers` (local)  
- **Database**: SQLite with SQLAlchemy ORM  
- **Frontend**: HTML, CSS (with optional dark themes)  

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ahmad-o-Zakariya/MAD_WD.git
   cd MAD_WD/Project_01
2. **Create virtual environment:**
  python -m venv venv
  source venv/Scripts/activate  # Windows
3. **Install dependencies:**
  pip install -r requirements.txt
4. **Initialize the database:**
  from app import app, db
  with app.app_context():
    db.create_all()
5. **Run the app:**
   python app.py

---

## 📚 What I Learned
- Building and structuring a **Flask web app** with its own mini API  
- Using **Hugging Face transformers** for offline AI text generation  
- **Prompt engineering** for genre-specific, literary-style outputs  
- Storing and retrieving data with **Flask-SQLAlchemy**  
- Running an **AI-powered project** locally without relying on external APIs

---

## 🖤 Future Enhancements
- Use **gpt2-medium** or **GPT-Neo** for higher quality  
- Genre-based theming (e.g., Dark mode for Horror/Dark Romance)  
- Option to **export or share** generated excerpts

