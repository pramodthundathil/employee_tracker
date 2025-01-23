from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['employee', 'title', 'description']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter task description'}),
        }


from .models import TaskUpdate

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = TaskUpdate
        fields = [ 'update_text', 'files']
        widgets = {
           
            'update_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter update details'}),
            'files': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
