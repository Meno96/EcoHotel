from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# Classe per la creazione di utenti
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    # Definimo i placeholders
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username..',
        })

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email..',
        })

        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password..',
        })

        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Enter the Password again..',
        })

        # Ciclo for per attribuire le classi
        for field in self.fields:

            self.fields[field].widget.attrs.update({
                'class': 'text w3lpass',
                'required': 'required',
            })
            self.fields[field].widget.attrs.pop(
                'autofocus', None
            )