
from django.contrib import admin
from django.urls import path
from BankApp import views, tamirviews, buykaviews, davaaviews, husleeviews, tumeeviews, erhmeeviews, nomioviews, updateuserviews

urlpatterns = [
    path('api/number/', tamirviews.dt_statement),
    # path('api/transaction/', buykaviews.dt_transaction),
    path('api/qr/', husleeviews.dt_qr),
    path('api/account/', davaaviews.dt_account),
    # path('api/user/', tumeeviews.dt_user),
    path('api/login/', erhmeeviews.dt_login),
    path('api/register/', nomioviews.dt_register),
    path('api/updateuser/', updateuserviews.dt_update_user),



]
