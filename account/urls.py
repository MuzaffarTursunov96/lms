from django.urls import path
from . import views





urlpatterns = [

    path('login',views.login, name='login'),
    path('register',views.registerUser, name='register'),
    path('logout',views.logout, name='logout'),

    path('my-courses',views.my_courses, name='my-courses'),
    ]