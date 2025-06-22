# Mood Tracker Web App

A Django-based web application that allows users to log daily moods, track emotional trends, and gain insights using interactive charts and summaries.

## Features

- Log your daily mood with optional notes
- Filter mood logs by date or mood type
- Visualize mood trends with bar and line charts (short and long term)
- Advanced insights: mood swings, streaks, averages
- Data stored securely with Django ORM
- Responsive UI powered by Bootstrap

## Screenshots


## Tech Stack

- Python
- Django
- SQLite (default, can be upgraded to PostgreSQL)
- Chart.js (for visualization)
- Bootstrap

## How to Run Locally

```bash
# Clone the repository
git clone https://github.com/adiityax/mood_tracker.git
cd moodtracker

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and start the server
python manage.py migrate
python manage.py runserver

# To use seed data(optional)
python manage.py seed_moods