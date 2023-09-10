from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user
from django.conf import settings
from . import forms, models

# def login(request):
    # locals() will collect all variables that you created inside function.
    # return render(request, 'template.html', locals())
    # return render(request, 'login.html')

def logout_user(request):

    logout(request)
    return redirect('login')


def login_page(request):

    form = forms.LoginForm()
    message = ""
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
        message = "Identifiants Invalides."
    return render(
        request, 'reviews/login.html',
        context={'form': form, 'message': message}
    )

def signup_page(request):

    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_URL)
    return render(request, 'reviews/signup.html', context={'form': form})

def feed(request):
    user = get_user(request)
    reviews = models.Review.objects.filter(user=user.id)
    tickets = models.Ticket.objects.filter(user=user.id)


    return render(request, 'reviews/feed.html')

def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'reviews/view_ticket.html', context={'ticket': ticket})

