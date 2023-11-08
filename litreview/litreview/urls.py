"""
URL configuration for litreview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import reviews.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', reviews.views.login_page, name='login'),
    path('signup/', reviews.views.signup_page, name='signup'),
    path('logout/', reviews.views.logout_user, name='logout'),
    path('feed/', reviews.views.feed, name='feed'),
    path('create_ticket/', reviews.views.create_ticket, name='create_ticket'),
    path('posts/', reviews.views.posts, name='posts'),
    path('create_review_ticket/<int:ticket_id>/', reviews.views.create_review_ticket, name='create_review_ticket'),
    path('create_review_wo_ticket/', reviews.views.create_review_wo_ticket, name='create_review_wo_ticket'),
    path('ticket/<int:ticket_id>/edit', reviews.views.edit_post, name='edit_post'),
    path('ticket/<int:ticket_id>/delete', reviews.views.delete_post, name='delete_post'),
    path('subscription/', reviews.views.subscription, name='subscription'),
    path("unfollow/<user_follows_id>", reviews.views.unfollow, name="unfollow"),
]
