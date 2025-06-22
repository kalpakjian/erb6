# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label='電子郵件')  # 使 email 可選
    password1 = forms.CharField(widget=forms.PasswordInput, label='密碼')
    password2 = forms.CharField(widget=forms.PasswordInput, label='確認密碼')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('此電子郵件已被使用。')
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }