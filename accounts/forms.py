from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username..',
        })

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email..',
        })

        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Inserisci la Password..',
        })

        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Inserisci nuovamente la Password..',
        })

        for field in self.fields:

            self.fields[field].widget.attrs.update({
                'class': 'text w3lpass',
                'required': 'required',
            })
            self.fields[field].widget.attrs.pop(
                'autofocus', None
            )