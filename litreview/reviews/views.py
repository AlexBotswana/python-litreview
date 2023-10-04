from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user
from django.conf import settings
from . import forms, models
from .models import Ticket, Review
from itertools import chain

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
    tickets = models.Ticket.objects.all()
    posts = sorted(
        tickets,
        key=lambda post: post.time_created,
        reverse=True
        )
    return render(request, 'reviews/feed.html', context={'posts': posts})


def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'reviews/view_ticket.html', context={'ticket': ticket})

def create_ticket(request):

    form = forms.TicketForm()

    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect(settings.REDIRECT_FEED)
    return render(request, 'reviews/create_ticket.html', context={'form': form})

def posts(request):
    current_user = request.user
    tickets = models.Ticket.objects.filter(user=current_user.id)
    # tickets = models.Ticket.objects.all()
    posts = sorted(
        tickets,
        key=lambda post: post.time_created,
        reverse=True
        )
    
    return render(request, "reviews/posts.html", context={'posts': posts})

def create_review_ticket(request):
    review_form = forms.ReviewForm()

def create_review_wo_ticket(request):
    
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()

    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.has_review = True
            ticket.save()
            
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect(settings.REDIRECT_FEED)
        
        else:
            context_review = {
                'ticket_form': ticket_form,
                'review_form': review_form,
        }
        
        return render(request, 'reviews/review_wo_ticket_create.html', context=context_review)
