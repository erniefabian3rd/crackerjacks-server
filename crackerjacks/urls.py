"""
URL configuration for crackerjacks project.

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
from django.conf.urls import include
from django.contrib import admin
from rest_framework import routers
from django.urls import path
from crackerjacksapi.views import register_user, login_user, TeamView, ParkView, TripView, PostView, CrackerjacksUserView, CommentView, LeagueNewsView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'teams', TeamView, 'team')
router.register(r'parks', ParkView, 'park')
router.register(r'trips', TripView, 'trip')
router.register(r'posts', PostView, 'post')
router.register(r'comments', CommentView, 'comment')
router.register(r'users', CrackerjacksUserView, 'user')
router.register(r'articles', LeagueNewsView, 'article')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
