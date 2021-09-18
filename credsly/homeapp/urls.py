from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('privacypolicy', views.privacy, name='Privacy-Policy'),
    path('signin', views.sigin, name='sigin'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
]