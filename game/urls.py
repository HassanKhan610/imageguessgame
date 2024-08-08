from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('guess/', views.guess, name='guess'),
    path('logout/', views.logout, name='logout'),
    path('statistics/', views.statistics, name='statistics'),

]
