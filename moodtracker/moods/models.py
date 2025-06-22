from django.db import models

# Create your models here.
class MoodEntry(models.Model):
    date = models.DateField()
    mood = models.CharField(max_length=20)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.mood}"