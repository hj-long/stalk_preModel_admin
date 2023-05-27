from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login),
    path('test/', views.test),
    path('logout/', views.user_logout),
    path('register/', views.user_register),
    path('userList/', views.user_list),
    path('getUser/', views.getUser),
    path('updateUser/', views.user_update),
    path('deleteUser/', views.user_delete),
    path('addUser/', views.user_add),
]