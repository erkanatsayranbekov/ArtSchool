from django import forms
from django.forms import ModelForm
from .models import Customer, Group, Attendance
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Пароль')
    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 20}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 20}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
        }
        

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'resize': 'none'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_permanent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'weekdays': forms.TextInput(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'