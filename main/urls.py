from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home, name='home'),
    path('room/<str:n>', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name='register'),
    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),
]