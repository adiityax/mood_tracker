from django.core.management.base import BaseCommand
from moods.models import MoodEntry
from datetime import timedelta, date
import random

class Command(BaseCommand):
    help = 'Seed the database with mood entries'

    def handle(self, *args, **kwargs):
        moods = ['excited', 'happy', 'content', 'neutral', 'anxious', 'sad', 'angry']
        MoodEntry.objects.all().delete()
        for i in range(30):
            MoodEntry.objects.create(
                date=date.today() - timedelta(days=i),
                mood=random.choice(moods),
                note=f"Day {i} mood"
            )
        self.stdout.write(self.style.SUCCESS("Seeded 30 mood entries."))