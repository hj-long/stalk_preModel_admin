from django.urls import path
from . import views

urlpatterns = [
    path('tableData/', views.tableData),
    path('search/', views.search),
    path('predict/', views.predict),
]