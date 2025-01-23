from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput,PasswordInput, ModelForm
from django import forms
from django.contrib.auth.hashers import make_password
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email', 'first_name', 'last_name','phone','address','profile_pic', 'role',"job_title","department",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom classes and IDs to fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f'id_{field_name}',
                'placeholder': f'{field.label}',
            })


class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'id_password',
            'placeholder': 'Enter new password (leave blank to keep current password)',
        }),
        help_text="Leave blank if you don't want to change the password."
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name','phone','address','profile_pic', 'role',"job_title","department", 'password', 'is_active', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom classes and IDs to other fields
        for field_name, field in self.fields.items():
            if field_name != 'password':  # Skip the custom password field
                field.widget.attrs.update({
                    'class': 'form-control',
                    'id': f'id_{field_name}',
                    'placeholder': f'{field.label}'
                })

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('password')
        if new_password:  # Only set the password if it's not blank
            user.set_password(new_password)
        if commit:
            user.save()
        return user


from .models import  Attendance, Messages_to_employees, PublicMessages, FeedBack
class MessagesToEmployeesForm(forms.ModelForm):
    class Meta:
        model = Messages_to_employees
        fields = ['employee', 'message', 'approve']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'approve': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = [ 'feedback']
        widgets = {
          
            'feedback': forms.Textarea(attrs={'class': 'form-control', }),
      
        }

from .models import Salaries
from .models import Leave

class SalariesForm(forms.ModelForm):
    class Meta:
        model = Salaries
        fields = ['employee', 'salary', 'month', 'year']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = [ 'leave_type', 'start_date', 'end_date', 'reason', 'status']
        widgets = {
            
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            
        }