from django import forms
from . import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    r"((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))","Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx!")


class FormContact(forms.ModelForm):
    name = forms.CharField(max_length=150, label='Họ tên', widget=forms.TextInput(attrs={
                           'placeholder':'Nhập họ tên','class':'form-control fh5co_contact_text_box'}))
    phone_number = forms.CharField(max_length=20, label='Điện thoại',validators=[phone_validator], widget=forms.TextInput(
        attrs={'placeholder':'Số điện thoại',
               'class':'form-control fh5co_contact_text_box',
               'pattern':'((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))',
               'title':'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx!'}))
    email = forms.EmailField(label='Email',widget=forms.TextInput(
        attrs={'placeholder':'Email','class':'form-control fh5co_contact_text_box'}))
    subject = forms.CharField(label='Subject', widget=forms.TextInput(
        attrs={'placeholder':'Subject','class':'form-control fh5co_contact_text_box'}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':'Message','class':'form-control fh5co_contacts_message'}))
    
    class Meta:
        model = models.Lienhe
        fields = '__all__'

class FormSearch(forms.ModelForm):
    name = forms.CharField()
    category_id= forms.IntegerField()

    class Meta:
        model = models.Sanpham
        fields = ('name', 'category_id')



class UserForm(forms.ModelForm):
    password = forms.CharField(
        max_length=150, label='Password', widget=forms.PasswordInput())
    confirm = forms.CharField(
        max_length=150, label='Confirm', widget=forms.PasswordInput())

    class Meta():
        model = models.User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserProfileInfoForm(forms.ModelForm):
    address = forms.CharField(max_length=500, widget=forms.TextInput())
    phone = forms.CharField(max_length=20, label='Phone', widget=forms.TextInput(
        attrs={'pattern': '((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))',
               'title': 'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx'}))
    image = forms.ImageField(required=False)

    class Meta():
        model = models.UserProfileInfo
        exclude = ('user', )

