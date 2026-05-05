
from django.contrib import admin
from django.urls import path
from BankApp import views, tamirviews, buykaviews, davaaviews, husleeviews, tumeeviews, erhmeeviews, nomioviews, updateuserviews, forgotpasswordviews, LoginView, statusview, changepasswordviews

urlpatterns = [
    path('api/number/', tamirviews.dt_statement),
    # path('api/transaction/', buykaviews.dt_transaction),
    path('api/qr/', husleeviews.dt_qr),
    path('api/account/', davaaviews.dt_account),
    # path('api/user/', tumeeviews.dt_user),
    path('api/login/', erhmeeviews.dt_login),
    path('api/register/', nomioviews.dt_register),
    path('api/updateuser/', updateuserviews.dt_update_user),
    path('api/forgotpassword/', forgotpasswordviews.dt_forgotpassword),
    path('api/verifyuser/', forgotpasswordviews.dt_verifyuser),
    path('api/newpassword/', forgotpasswordviews.dt_newpassword),
    path('api/logins/', LoginView.dt_login),
    path('api/userstatus/', statusview.dt_status),
    path('api/getusername/', buykaviews.dt_username),
    path('api/changepassword/', changepasswordviews.dt_changepassword),


]
