from django.urls import path
from . import views


app_name = 'users'


urlpatterns = [
    path('', views.redirect_to_login, name='redirect_to_login'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    
]