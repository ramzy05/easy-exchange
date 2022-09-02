from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Account, Country


CHOICES_COUNTRY = [
    ('', 'Choose the country'),
    ('Cameroon', 'Cameroon'),
    ('USA', 'USA'),
    ('Canada', 'Canada'),
    ('France', 'France'),
]


class CreateAccountForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CreateAccountForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='Username', required=False, widget=forms.TextInput(
        attrs={
            'maxlength': 100,
            'placeholder': 'username',

        }
    ))
    first_name = forms.CharField(label='First Name', required=False, widget=forms.TextInput(
        attrs={
            'maxlength': 50,
            'placeholder': 'John',
        }
    ))
    last_name = forms.CharField(label='Last Name', required=False, widget=forms.TextInput(
        attrs={
            'maxlength': 50,
            'placeholder': 'Doe',
        }
    ))
    country = forms.CharField(label='Country', required=False, widget=forms.Select(
        choices=CHOICES_COUNTRY,
        attrs={
            'maxlength': 100,
            'placeholder': 'Choose your country',
        }
    ))

    password1 = forms.CharField(label='Password', required=False, widget=forms.PasswordInput(
        attrs={
            'maxlength': 400,
            'placeholder': '',
        }
    ))
    password2 = forms.CharField(label='Confirm Password', required=False, widget=forms.PasswordInput(
        attrs={
            'maxlength': 400,
            'placeholder': '',
        }
    ))

    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name',
                  'country', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == '':
            raise forms.ValidationError("Username field cannot be blank")
        if Account.objects.filter(username=str(username)).exists():
            raise forms.ValidationError(
                "This username is unavailable, please enter another one")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name == '':
            raise forms.ValidationError("First name field cannot be blank")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name == '':
            raise forms.ValidationError("Last name field cannot be blank")

        return last_name

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if country == '':
            raise forms.ValidationError("Country field cannot be blank")
        if not country in ['Cameroon', 'USA', 'Canada', 'France']:
            raise forms.ValidationError("Please choose a valid country")
        return country

    def clean_password1(self):
        import re
        password1 = self.cleaned_data.get('password1')
        if password1 == '':
            raise forms.ValidationError("Password field cannot be blank")
        if len(password1) < 7:
            raise forms.ValidationError(
                "The password must contain at least 8 character")

        if str(password1).isdecimal():
            raise forms.ValidationError("password cannot be entire numeric")

        # if re.match(r'[]',(str(password1))):
        #     raise forms.ValidationError("password cannot be entire numeric")

        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password1 = self.cleaned_data.get('password1')
        if password2 != password1:
            raise forms.ValidationError("The password doesn't match")

        return password2
