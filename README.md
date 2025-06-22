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

![Insights Page](https://github.com/user-attachments/assets/053c2c38-ab79-4617-84a0-2c1cb9dd651c)
![Filter Log Page](https://github.com/user-attachments/assets/7ce2d377-da47-4094-8bf1-7a5c450fe3e3)
![Mood Chart Summary 2](https://github.com/user-attachments/assets/921e09ac-1e9a-4b31-9d06-cdb81d16b1e8)
![Mood Chart Summary 1](https://github.com/user-attachments/assets/edb74638-b543-4987-aa46-0313a49d4400)
![Log Mood Page](https://github.com/user-attachments/assets/a20e0601-0981-4caa-a141-00ae58a29f5a)


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
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# To use seed data(optional)
python manage.py seed_moods
