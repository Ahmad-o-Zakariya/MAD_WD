# 🎮 Gamified Flask ToDo App

A sleek, gamified task management web application built with **Flask**, designed to make productivity fun and engaging.  
Track your tasks, earn XP, level up, and maintain streaks with a retro-inspired interface.

---
## 🚀 Features

- **Task Management**
  - Add, update, delete, and mark tasks as complete
  - Separate completed tasks page with history

- **Gamification**
  - Earn XP for each completed task
  - Level progression and XP progress bar
  - Daily streak tracking and achievements
  - Calendar highlighting completed task days

- **Visual Style**
  - Pixel-inspired, dark theme UI
  - **Fira Code** font for a developer/gamified feel
  - Golden glow effects and subtle animations

---

## 🛠 Tech Stack

- **Backend:** Python 3, Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** Bootstrap 4, HTML5, CSS3
- **Extras:** Chart.js (optional for XP trends), Custom CSS

---
### Achievements

The application tracks and rewards key productivity milestones:

- **First Quest Complete** – Earned by completing the first task.  
- **Streak Hunter** – Achieved after maintaining a 3‑day completion streak.  
- **Task Warrior** – Awarded for completing 10 tasks.  
- **Inbox Zero** – Granted when all active tasks are cleared.

---

### Calendar and XP

- The **CompletedLog** model ensures XP and streak data remain even if tasks are deleted.  
- The calendar view highlights all days with completed tasks, with the current day emphasized.  
- XP is calculated dynamically based on logged task completions.

---

### Contributing

Contributions are welcome. To propose improvements or new features:

1. Fork the repository.  
2. Create a feature branch (e.g., `feature/new-achievement`).  
3. Commit and push your changes.  
4. Submit a Pull Request.

---

### License

This project is licensed under the **MIT License**.  
You are free to modify and distribute with proper attribution.
