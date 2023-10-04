from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from . import models

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

class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=True
    )
    title = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'class': "xl-field"})
    )
    description = forms.CharField(
        max_length=2048,
        widget=forms.Textarea(attrs={'class':"xl-field"})
    )
    image = forms.ImageField(
        required=True,
        widget=forms.FileInput
    )
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

class ReviewForm(forms.ModelForm):
    CHOICES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    headline = forms.CharField(
        max_length=128,
        label='Titre',
        widget=forms.TextInput(attrs={'class': "xl-field"})
    )
    body = forms.CharField(
        max_length=2048,
        label='Commentaire',
        widget=forms.Textarea(attrs={'class': "xl-field"})
    )
    rating = forms.CharField(
        label='Note',
        widget=forms.RadioSelect(
            choices=CHOICES,
            attrs={'class': 'radio-block'}
            )
        )
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
