from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'creation_datetime',
            'start_datetime',
            'finish_datetime',
            'dependencies',
        ]

