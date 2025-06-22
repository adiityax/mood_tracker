from django import forms
from .models import MoodEntry

class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['date', 'mood', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'note': forms.Textarea(attrs={'rows':2}),
        }