# ⚒ FORGE — Task Manager


---

## Overview

**Forge** is a productivity-focused web application for creating, managing, and tracking personal tasks. It ships with a polished, responsive interface powered by Django Templates and a fully compliant REST API layer — making it usable both as a standalone web app and as a backend for any external client.


## Features

### Task Management
- Create, edit, and delete tasks with title, description, priority, deadline, and status
- Three priority levels — **High**, **Medium**, **Low** — with visual colour coding
- Automatic overdue detection — tasks past their deadline are flagged instantly
- **Instant status toggle** via AJAX — no page reload required
- Real-time search with debounce, and filter by status, priority, or sort order
- Stats bar updates automatically whenever a task is completed or reopened

### Pomodoro Timer
- Full-width Pomodoro timer at the top of the dashboard (lemon-yellow section)
- Custom duration input — set any session length you like
- Four dot indicators track completed focus sessions
- Click ▶ on any task card to load it as the current focus target
- Automatic 5-minute break mode after each session completes
- Pause and reset controls

### Weekly Calendar View
- Toggle between Grid and Week views
- Navigate weeks with Prev / Next / Today buttons
- Tasks appear as colour-coded pills on their deadline day

### Sticker Badge System
Playful, rotated pill badges on each task card:
- 🔥 **High** — Raspberry pink
- ⚡ **Medium** — Lemon lime
- 🌿 **Low** — Kale green
- ⚠️ **Overdue** — Red
- ✓ **Done** / ● **Pending** — single status badge, no duplicates


Full **light / dark mode** with localStorage persistence.

### REST API
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sign-up/` | Register — returns 201 |
| POST | `/sign-in/` | Login — returns 200 |
| POST | `/logout/` | Logout — returns 204 |
| GET | `/tasks/` | List all tasks + stats — returns 200 |
| POST | `/tasks/` | Create a task — returns 201 |
| GET | `/tasks/<id>/` | Get one task — returns 200 |
| PUT | `/tasks/<id>/` | Full update — returns 200 |
| PATCH | `/tasks/<id>/` | Partial update — returns 200 |
| DELETE | `/tasks/<id>/` | Delete task — returns 204 |
| GET | `/stats/` | Stats only — returns 200 |

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13, Django 6.0 |
| REST API | Django REST Framework 3.x |
| Database | SQLite via Django ORM |
| Frontend | Django Templates, Vanilla JS |
| Typography | Inter (Google Fonts) |
| Charts | Chart.js |
| Version Control | Git + GitHub |

---

## Usage

### Getting Started
1. Go to `/sign-up/` and create an account
2. Sign in at `/sign-in/`
3. You land on the dashboard — hit **+ New Task** to begin

### Pomodoro Timer
1. Set your session duration in the input field (default 25 min)
2. Click ▶ on any task card to load it as your focus target
3. Hit **▶ Start** — the timer counts down in real time
4. After it ends, a 5-minute break starts automatically
5. Four dots track how many sessions you have completed

### Week View
1. Click the **Week** tab next to the Grid tab
2. Tasks appear on their deadline day as colour-coded pills
3. Use **← Prev**, **Next →**, and **Today** to navigate


## Project Structure

```
python-project/
├── python_project/        # Django config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/                 # Main app
│   ├── templates/tasks/
│   │   ├── base.html              # Layout, nav, CSS, dark mode
│   │   ├── dashboard.html         # Dashboard, Pomodoro, week view
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── task_form.html
│   │   └── task_confirm_delete.html
│   ├── models.py          # Task model
│   ├── views.py           # HTML views
│   ├── forms.py           # Django forms
│   ├── urls.py            # URL routing
│   ├── serializers.py     # DRF serializers
│   └── api_views.py       # REST API endpoints
├── requirements.txt
├── README.md
└── manage.py
```


*Built with ❤️ and Django — coursework project by vikidmkn*
