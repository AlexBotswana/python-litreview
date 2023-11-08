from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user
from django.contrib.auth.models import User
from django.conf import settings
from . import forms, models
from .forms import ReviewForm, TicketForm, DeletePostForm
from .models import Ticket, Review, UserFollows
from itertools import chain
from django.db.models import CharField, Value, Q
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

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
    user = request.user
    followed_users = models.UserFollows.objects.filter(user=user).values_list('followed_user_id', flat=True)
    tickets = models.Ticket.objects.filter(Q(user=user) | Q(user__in=followed_users)) # to exclude ticket if already a critic on it : .exclude(review__isnull=False)
    reviews = models.Review.objects.filter(Q(user=user) | Q(user__in=followed_users))

    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
        )
    stars_values= [1,2,3,4,5]
    return render(request, 'reviews/feed.html', context={'posts': posts, 'stars_values': stars_values})


def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'reviews/view_ticket.html', context={'ticket': ticket})

def create_ticket(request):

    form = forms.TicketForm()

    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        print(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect(settings.REDIRECT_FEED)
    return render(request, 'reviews/create_ticket.html', context={'form': form})

def posts(request):
    current_user = request.user
    tickets = models.Ticket.objects.filter(user=current_user.id)
    reviews = models.Review.objects.filter(user=current_user.id)

    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
        )
    
    stars_values= [1,2,3,4,5]
    return render(request, "reviews/posts.html", context={'posts': posts, 'stars_values': stars_values})

def create_review_ticket(request, ticket_id):
    review_form = ReviewForm()
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False) 
            review.ticket = ticket
            ticket.save()
            review.user = request.user  
            review.save()  

            return redirect(settings.REDIRECT_FEED)  
    
    context = {
        "review_form": review_form,
        "ticket": ticket,
    }

    return render(request, 'reviews/create_review_ticket.html', context=context)

def create_review_wo_ticket(request):
    
    form_ticket = TicketForm()
    form_review = ReviewForm()
    if request.method == "POST":
        form_ticket_post = TicketForm(request.POST, request.FILES)
        form_review_post = ReviewForm(request.POST)
        if form_ticket_post.is_valid() and form_review_post.is_valid():
            review_form = form_review_post.save(commit=False)
            ticket_form = form_ticket_post.save(commit=False)
            ticket = Ticket.objects.create(
                title=ticket_form.title,
                description=ticket_form.description,
                user=request.user,
                image=ticket_form.image,
                time_created=ticket_form.time_created,
            )
            review_form.ticket = ticket
            review_form.user = request.user

            ticket.save()
            review_form.save()
            return redirect(settings.REDIRECT_FEED)
    context = {
        "form_ticket": form_ticket,
        "form_review": form_review,
    }
    return render(request, 'reviews/create_review_wo_ticket.html', context=context)

def delete_post(request, ticket_id):
    # get post id and delete if ticket or review
    try:
        obj = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        obj = Review.objects.get(id=ticket_id)
    delete_form = DeletePostForm()
    if request.method == "POST":
        delete_form = DeletePostForm(request.POST)
        if delete_form.is_valid():
            if isinstance(obj, Review):
                obj.ticket.save()
            obj.delete()
            return redirect(settings.REDIRECT_POSTS)
    context = {"delete_form": delete_form}
    return render(request, 'reviews/delete_post.html', context=context)

def edit_post (request, ticket_id):
    """ get post_id and edit post (try ticket, else review)"""
    try:
        obj = Ticket.objects.get(id=ticket_id)
        form = TicketForm
        html = "reviews/edit_ticket.html"
    except Ticket.DoesNotExist:
        obj = Review.objects.get(id=ticket_id)
        form = ReviewForm
        html = "reviews/edit_review.html"
    edit_form = form(instance=obj)
    if request.method == 'POST':
        edit_form = form(request.POST or None, request.FILES or None, instance=obj)
        # form = forms.TicketForm(request.POST, request.FILES, instance=obj)
        if edit_form.is_valid():
            # ticket = form.save(commit=False)
            # ticket.user = request.user
            # ticket.save()
            edit_form.save()
            return redirect("posts")
        # else: 
            # print(form.errors.as_data())
    context = {"edit_form": edit_form, "post": obj}
    return render(request, html, context=context)
    
def subscription(request):
    users_followed = UserFollows.objects.filter(user=request.user)
    users_followers = UserFollows.objects.filter(followed_user=request.user)
    if request.method == "POST":
        follow = request.POST["name"]  # get input name's user from html page.
        username = request.user
        try:
            to_follow = User.objects.get(username=follow)
            if to_follow != username:
                if (
                    UserFollows.objects.get_or_create(
                        user=request.user, followed_user=to_follow
                    )
                    is False
                ):
                    UserFollows.objects.create(
                        user=request.user, followed_user=to_follow
                    )
                else:
                    messages.add_message(
                        request,
                        messages.INFO,
                        f"Vous êtes abonné à {to_follow}.",
                    )
            else:
                messages.add_message(
                    request, messages.INFO, f"Vous êtes {request.user} !"
                )
        except ObjectDoesNotExist:
            messages.add_message(
                request, messages.INFO, "Cet utilisateur n'existe pas."
            )

    return render(
        request,
        "reviews/subscription.html",
        context={
            "users_followed": users_followed,
            "users_followers": users_followers,
        },
    )

def unfollow(request, user_follows_id):
    """
    get user followed id
    delete subscription and redirect to 'subscription'
    """
    if request.method == "GET":
        subscription = UserFollows.objects.filter(pk=user_follows_id)
        subscription.delete()
    return redirect("subscription")


