import os
from pathlib import Path
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / "todo.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path.as_posix()}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SNo}-{self.title}"

@app.route("/", methods=['GET', "POST"])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo(title=title, desc = desc)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    allTodo = ToDo.query.all()
    return render_template("index.html", allTodo=allTodo)

@app.route("/show")
def products():
    allTodo = ToDo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route("/update/<int:SNo>", methods=["GET", "POST"])
def update(SNo):
    todo = ToDo.query.get_or_404(SNo)
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:SNo>")
def delete(SNo):
    allTodo = ToDo.query.filter_by(SNo=SNo).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
