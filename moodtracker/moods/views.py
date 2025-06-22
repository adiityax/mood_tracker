from django.shortcuts import render, redirect
from django.db.models import Count
from django.http import JsonResponse
from django.contrib import messages
from .models import MoodEntry
from .forms import MoodEntryForm
from datetime import date, timedelta, datetime
from collections import Counter, defaultdict

# Create your views here.
def log_mood(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Mood saved successfully!")
            except Exception as e:
                messages.error(request, f"Failed to save mood: {e}")
            return redirect('log_mood')
        else:
            messages.error(request, "Form validation failed.")
    else:
        form = MoodEntryForm()

    return render(request, 'moods/log_mood.html', {
        'form': form,
        'today': date.today().isoformat()  # e.g., '2025-06-21'
    })

def mood_summary(request):
    today = date.today()
    entries = MoodEntry.objects.all()

    short_term = entries.filter(date__gte = today - timedelta(days=7))
    long_term = entries.filter(date__gte = today - timedelta(days=30))

    def count_moods(qs):
        return dict(Counter(qs.values_list('mood', flat = True)))
    
    context = {
        'short_term_summary': count_moods(short_term),
        'long_term_summary': count_moods(long_term),
        'all_entries': entries.order_by('-date'),
    }
    return render(request, 'moods/summary.html', context)

def filter_logs(request):
    date = request.GET.get('date')
    mood = request.GET.get('mood')

    logs = MoodEntry.objects.all().order_by('-date')

    if date:
        logs = logs.filter(date=date)
    if mood:
        logs = logs.filter(mood__icontains=mood)

    return render(request, 'moods/filter_logs.html', {'logs':logs, 'date':date, 'mood':mood})

def mood_chart_data(request):
    today = datetime.today().date()
    short_term_days = 7
    long_term_days = 30

    short_term_cutoff = today - timedelta(days=short_term_days)
    long_term_cutoff = today - timedelta(days=long_term_days)

    short_term_logs = MoodEntry.objects.filter(date__gte=short_term_cutoff)
    long_term_logs = MoodEntry.objects.filter(date__gte=long_term_cutoff)

    def count_moods(logs):
        mood_counts = logs.values('mood').annotate(count=Count('mood')).order_by('-count')
        return {item['mood']: item['count'] for item in mood_counts}

    data = {
        'short_term': count_moods(short_term_logs),
        'long_term': count_moods(long_term_logs),
    }

    return JsonResponse(data)

def calculate_streaks(logs):

    sorted_logs = sorted(logs, key=lambda log: log.date)

    streaks = defaultdict(int)
    current_mood = None
    current_streak = 0
    previous_date = None

    for entry in sorted_logs:
        if previous_date and entry.date == previous_date + timedelta(days=1) and entry.mood == current_mood:
            current_streak += 1
        else:
            if current_mood:
                streaks[current_mood] = max(streaks[current_mood], current_streak)
            # Reset streak
            current_streak = 1
            current_mood = entry.mood

        previous_date = entry.date

    # Final check
    if current_mood:
        streaks[current_mood] = max(streaks[current_mood], current_streak)

    return dict(streaks)

def advanced_insights(request):
    try:
        logs = MoodEntry.objects.all()
        if not logs.exists():
            return render(request, 'moods/insights.html', {'summary': "No data available."})

        total_entries = logs.count()
        mood_counts = logs.values('mood').annotate(count=Count('mood')).order_by('-count')
        most_common_mood = mood_counts[0]['mood'] if mood_counts else None
        streaks = calculate_streaks(logs)
        swing_info = calculate_mood_swings(logs)

        summary = {
            'total_entries': total_entries,
            'most_common_mood': most_common_mood,
            'mood_counts': mood_counts,
            'streaks': streaks,
            'swing_info': swing_info,
        }

        return render(request, 'moods/insights.html', {'summary': summary})

    except Exception as e:
        return render(request, 'moods/insights.html', {'summary': f"Error generating insights: {e}"})
    
def calculate_mood_swings(logs):
    logs = sorted(logs, key=lambda log: log.date)
    changes = 0
    prev_mood = None

    for log in logs:
        if prev_mood and log.mood != prev_mood:
            changes += 1
        prev_mood = log.mood

    swing_score = round(changes / max(1, len(logs)), 2)  # Normalize
    return {
        'total_changes': changes,
        'swing_score': swing_score,
        'swing_level': (
            "Stable" if swing_score < 0.2 else
            "Moderate Swings" if swing_score < 0.5 else
            "High Mood Swings"
        )
    }

def swing_chart_data(request):
    logs = MoodEntry.objects.all().order_by('date')

    # Define mood scores
    mood_scores = {
        'excited':3,
        'happy': 2,
        'content': 1,
        'neutral': 0,
        'anxious': -1,
        'sad': -2,
        'angry': -3,
    }

    date_score_map = {}
    for log in logs:
        mood = log.mood.lower()
        score = mood_scores.get(mood)
        if score is not None:
            date_str = log.date.strftime('%Y-%m-%d')
            date_score_map[date_str] = score  # only latest entry per day

    sorted_dates = sorted(date_score_map.keys())
    mood_values = [date_score_map[date] for date in sorted_dates]

    return JsonResponse({
        'dates': sorted_dates,
        'moods': mood_values
    })