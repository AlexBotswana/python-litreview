from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=63,
        label="Nom d'utilisateur",
        help_text="Saisir votre nom d'utilisateur"
        )
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput,
        label="Mot de passe",
        help_text="Saisir votre mot de passe"
        )


class SignupForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'field-box',
                'placeholder': "Nom d'utilisateur"
                }
            )
        )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'field-box',
                'placeholder': "Mot de passe"
                }
            )
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'field-box',
                'placeholder': "Confirmer mot de passe"
                }
            )
        )

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username',)
