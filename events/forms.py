from django import forms
from .models import Event, Participant, Category
from django.core.exceptions import ValidationError
from django.utils import timezone

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'HH:MM'}),
            'name': forms.TextInput(attrs={'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Event Description .....'}),
            'category': forms.Select(attrs={'class': 'p-2 border rounded'}),
        }
        labels = {
            'date': 'Event Date',
            'time': 'Event Time',
            'category': 'Event Category',
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise ValidationError("Event date cannot be in the past.")
        return date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['value'] = timezone.now().date()
        self.fields['time'].widget.attrs['value'] = timezone.now().strftime('%H:%M')

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'events': forms.SelectMultiple(attrs={'class': 'p-2 border rounded'}),  # Better UI for multiple selections
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'events': 'Select Events',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = { 
            'name': forms.TextInput(attrs={'placeholder': 'Category Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Category Description .....'}),
        }
        labels = {
            'name': 'Category Name',
        }
