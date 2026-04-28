
from django.contrib import admin
from django.urls import path
from BankApp import views, tamirviews, buykaviews, davaaviews, husleeviews

urlpatterns = [
    path('api/number/', tamirviews.dt_statement),



]
