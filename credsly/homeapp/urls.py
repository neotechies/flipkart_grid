from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('privacypolicy', views.privacy, name='Privacy-Policy'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register, name='Register'),
    path('login', views.loginuser, name='login'),

]