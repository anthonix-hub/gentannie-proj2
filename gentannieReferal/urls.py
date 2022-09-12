from django.contrib.auth import views as auth_views
from django.urls import path
# from .views import signupview
from . import views
from .views import *


urlpatterns = [
    path('', views.index, name='index'),
    path('<str:ref_code>/', referal_views, name='referal_views'),
    # path('<str:ref_code>/', signup_view, name='signup_view'),
    path('referal_profile', my_recomms_views, name='my_recomms_views'),
    path('signup_view', signup_view, name='signup_view'),        
    path('terms_n_conditions',views.terms_n_condition, name='terms_n_condition'),


    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
    name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(),
    name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
    name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
    name='password_reset_complete'),
]
