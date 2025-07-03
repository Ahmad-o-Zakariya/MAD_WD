import os
from pathlib import Path
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from collections import defaultdict


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
    is_done = db.Column(db.Boolean, default=False)

class CompletedLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    desc = db.Column(db.String(500))
    completed_on = db.Column(db.Date)
    xp_awarded = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"{self.id}-{self.title}"

# Home page
@app.route("/", methods=['GET', "POST"])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    allTodo = ToDo.query.all()  # needed for active list + inbox zero achievement
    logs = CompletedLog.query.all()

    total_tasks = len(logs)
    xp = sum(log.xp_awarded for log in logs)
    level = xp // 100 + 1
    progress = xp % 100

    # Streak and task_dates from CompletedLog
    completed_dates = sorted({log.completed_on for log in logs}, reverse=True)
    task_dates = [d.isoformat() for d in completed_dates]

    streak = 0
    today = datetime.utcnow().date()
    for i in range(len(completed_dates)):
        expected_day = today - timedelta(days=i)
        if completed_dates[i] == expected_day:
            streak += 1
        else:
            break

    # Achievements
    achievements = []
    if total_tasks >= 1:
        achievements.append("🐣 First Quest Complete")
    if streak >= 3:
        achievements.append("🔥 3-Day Streak")
    if total_tasks >= 10:
        achievements.append("💪 Task Warrior")
    if len(allTodo) == 0:
        achievements.append("🧹 Inbox Zero")

    # XP per day
    xp_per_day = defaultdict(int)
    for log in logs:
        day = log.completed_on.isoformat()
        xp_per_day[day] += log.xp_awarded

    xp_chart_data = sorted(xp_per_day.items())
    labels = [item[0] for item in xp_chart_data]
    values = [item[1] for item in xp_chart_data]

    return render_template(
        "index.html",
        allTodo=allTodo,
        xp=xp,
        level=level,
        progress=progress,
        streak=streak,
        achievements=achievements,
        labels=labels,
        values=values,
        task_dates=task_dates
    )

# Update a task
@app.route("/update/<int:SNo>", methods=["GET", "POST"])
def update(SNo):
    todo = ToDo.query.get_or_404(SNo)
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)

# Delete a task (only from ToDo)
@app.route("/delete/<int:SNo>")
def delete(SNo):
    todo = ToDo.query.get_or_404(SNo)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# Complete a task and log it
@app.route("/complete/<int:SNo>")
def complete(SNo):
    todo = ToDo.query.get_or_404(SNo)
    if not todo.is_done:
        log = CompletedLog(
            title=todo.title,
            desc=todo.desc,
            completed_on=datetime.utcnow().date(),
            xp_awarded=10
        )
        db.session.add(log)
        db.session.commit()

        todo.is_done = True
        db.session.commit()

    return redirect("/")

# Show calendar view
@app.route("/calendar")
def calendar():
    logs = CompletedLog.query.order_by(CompletedLog.completed_on).all()
    task_dates = [log.completed_on.isoformat() for log in logs]
    return render_template("calendar.html", task_dates=task_dates)

# Show all completed tasks
@app.route("/completed")
def show_completed():
    completed_tasks = CompletedLog.query.order_by(CompletedLog.completed_on.desc()).all()
    return render_template("completed.html", tasks=completed_tasks)

@app.route("/search")
def search():
    query = request.args.get('query', '').strip()
    if not query:
        return redirect("/")

    results = ToDo.query.filter(
        (ToDo.title.ilike(f"%{query}%")) | (ToDo.desc.ilike(f"%{query}%"))
    ).all()

    return render_template("search.html", query=query, results=results)

if __name__ == "__main__":
   with app.app_context():
      db.create_all()
app.run(debug=True, port=8000)
    
