# AJIBADE — macOS-style Portfolio (HTML + CSS + JS + Python)

## Run locally
1. Create a virtual environment (optional).
2. `pip install flask`
3. `python app.py`
4. Visit http://127.0.0.1:5000

## Structure
- `templates/index.html` — UI
- `static/css/style.css` — Styling
- `static/js/script.js` — Interactivity
- `data/projects.json` — Project data
- `app.py` — Flask backend (projects API, contact endpoint)

## Features
- Top bar with Wi‑Fi, battery, date/time
- Dock with magnification
- Draggable windows (About, Projects, Contact)
- Dark/Light theme toggle (persisted)
- Spotlight search (Cmd/Ctrl + Space)
- Notifications sheet
- Projects loaded from Flask JSON
- Contact form posting to `/api/contact`
