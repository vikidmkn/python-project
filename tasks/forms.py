from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Task


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'forge-input'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'forge-input'})


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'forge-input'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'deadline', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'forge-input', 'placeholder': 'Task title...'}),
            'description': forms.Textarea(attrs={'class': 'forge-input', 'rows': 3, 'placeholder': 'Description (optional)...'}),
            'priority': forms.Select(attrs={'class': 'forge-input'}),
            'status': forms.Select(attrs={'class': 'forge-input'}),
        }