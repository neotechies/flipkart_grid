from django.urls import path
from django.contrib import admin
from . import views

admin.site.site_header="CredSly Admin"
admin.site.site_title="CredSly Admin Panel"
admin.site.index_title="Welcome to CredSly Admin Panel"

urlpatterns = [
    path('', views.index, name='index'),
    path('privacypolicy', views.privacy, name='Privacy-Policy'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register, name='register'),
    path('login', views.loginuser, name='login'),
    path('logout', views.logoutuser, name='logout'),
    path('fbzipupload', views.uploadFacebookZip, name='fbzipupload'),
    path('linkedinzipupload', views.uploadLinkedinZip, name='linkedinzipupload'),
    path('twitterusernameupload', views.uploadTwitterUsername, name='twitterusernameupload'),


]