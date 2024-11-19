from django import forms
from .models import Order 
from django.core.validators import RegexValidator
phone_validator = RegexValidator(
    r"((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))","Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx!")

from django import forms
from .models import Order  # Đảm bảo bạn đã import model Order

class OrderCreateForm(forms.ModelForm):  # Thay đổi thành ModelForm
    last_name = forms.CharField(max_length=150, label='Họ', widget=forms.TextInput(attrs={
        'placeholder': 'Nhập họ', 'class': 'form-control fh5co_contact_text_box'
    }))
    first_name = forms.CharField(max_length=150, label='Tên', widget=forms.TextInput(attrs={
        'placeholder': 'Nhập tên', 'class': 'form-control fh5co_contact_text_box'
    }))
    phone = forms.CharField(max_length=20, label='Phone', widget=forms.TextInput(
        attrs={'pattern': '((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))',
               'title': 'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'form-control fh5co_contact_text_box'}))
    
    address = forms.CharField(max_length=500, label='Địa chỉ', widget=forms.TextInput(attrs={
        'placeholder': 'Nhập địa chỉ', 'class': 'form-control fh5co_contact_text_box'
    }))
    
    class Meta:
        model = Order  # Chỉ định model
        fields = '__all__' 