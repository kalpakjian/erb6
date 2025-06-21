from django import forms
from .models import CustomerProfile

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['phone', 'address', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'avatar': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 動態生成頭像選項
        avatar_choices = [
            ('icons/default_avatar.png', '預設頭像'),
            ('icons/avatar1.png', '頭像 1'),
            ('icons/avatar2.png', '頭像 2'),
            # 可根據實際文件新增更多選項
        ]
        self.fields['avatar'].choices = avatar_choices