from django.test import TestCase
from .models import MoodEntry
from datetime import date
from .forms import MoodEntryForm
from django.urls import reverse

# Create your tests here.
class MoodEntryModelTest(TestCase):
    def test_mood_entry_creation(self):
        entry = MoodEntry.objects.create(date=date.today(), mood='happy', note='Felt great!')
        self.assertEqual(str(entry), f"{entry.date} - happy")

class MoodEntryFormTest(TestCase):
    def test_valid_form(self):
        form = MoodEntryForm(data={
            'date': date.today(),
            'mood': 'happy',
            'note': 'All good!'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = MoodEntryForm(data={
            'date': '',  # missing required
            'mood': 'happy'
        })
        self.assertFalse(form.is_valid())


class MoodViewTest(TestCase):
    def test_log_mood_get(self):
        response = self.client.get(reverse('log_mood'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Save Mood')