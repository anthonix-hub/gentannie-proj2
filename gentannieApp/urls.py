from os import name
from django.contrib.auth import views as auth_views
from django.urls import path,include
# from .views import signupview, update_view
from . import views
from gentannieReferal.views import *

urlpatterns = [
    path('countdown', views.countdown, name='countdown'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('transaction_history_page', views.transact_history, name='transact_history'),
    path('notification_page', views.notification, name='notification'),
    path('profile_page', views.account_detail_profile, name='account_detail_profile'),
    path('referal_views', views.Referal_views, name='Referal_views'),
    # path('<user_id>/update_view', update_view),

    # ******** deposits urls *********
    path('deposit_page', views.deposit_page, name='deposit_page'),
    path('Supreme_plus_Unlocked_pack', views.Supreme_plus_Unlocked_pack, name='Supreme_plus_Unlocked_pack'),
    path('Supreme_plus_Locked_pack', views.Supreme_plus_Locked_pack, name='Supreme_plus_Locked_pack'),
    path('Supreme_plus_Savings_pack', views.Supreme_plus_Savings_pack, name='Supreme_plus_Savings_pack'),
    # ******** / .deposits urls *********

    path('user_withdrawal', views.user_withdrawal_page, name='user_withdrawal_page'),
    path('Supreme_plus_Unlocked_withdrawal_page', views.Supreme_plus_UnLocked_withdrawal, name='Supreme_plus_Unlocked_withdrawal_page'),
    path('Supreme_plus_Locked_withdrawal_page', views.Supreme_plus_Locked_withdrawal, name='Supreme_plus_Locked_withdrawal_Locked_page'),
    path('Supreme_plus_Savings_withdrawal_page', views.Supreme_plus_Savings_withdrawal_page, name='Supreme_plus_Savings_withdrawal_page'),
    
    # ************* Unlocked withdrawal pakacge pages url
    path('basicSupreme_plus_Unlocked_page', views.UnLocked_basic_withdrawal, name='basic_withdrawal_Supreme_plus_Unlocked_page'),
    path('standardSupreme_plus_Unlocked_page', views.UnLocked_standard_withdrawal, name='standardSupreme_plus_Unlocked_page'),
    path('premiumSupreme_plus_Unlocked_page', views.UnLocked_premium_withdrawal, name='premiumSupreme_plus_Unlocked_page'),
    path('bronzeSupreme_plus_Unlocked_page', views.UnLocked_bronze_withdrawal, name='bronzeSupreme_plus_Unlocked_page'),
    path('super_bronzeSupreme_plus_Unlocked_page', views.UnLocked_super_bronze_withdrawal, name='super_bronzeSupreme_plus_Unlocked_page'),
    path('silverSupreme_plus_Unlocked_page', views.UnLocked_silver_withdrawal, name='silverSupreme_plus_Unlocked_page'),
    path('super_silverSupreme_plus_Unlocked_page', views.UnLocked_super_silver_withdrawal, name='super_silverSupreme_plus_Unlocked_page'),
    path('GoldSupreme_plus_Unlocked_page', views.Unlocked_gold_withdrawal, name='GoldSupreme_plus_Unlocked_page'),
    path('diamondSupreme_plus_Unlocked_page', views.UnLocked_diamond_withdrawal, name='diamondSupreme_plus_Unlocked_page'),
    
    # ************* Unlocked cash out page url
    path('basicPlan_Unlocked_cash_out_page', views.UnLocked_basicPlan_cashOut, name='basicPlan_Unlocked_cash_out_page'),
    path('standardPlan_Unlocked_cash_out_page', views.UnLocked_standardPlan_cashOut, name='standardPlan_Unlocked_cash_out_page'),
    path('premiumPlan_Unlocked_cash_out_page', views.UnLocked_premiumPlan_cashOut, name='premiumPlan_Unlocked_cash_out_page'),
    path('bronzePlan_Unlocked_cash_out_page', views.UnLocked_bronzePlan_cashOut, name='bronzePlan_Unlocked_cash_out_page'),
    path('super_bronzePlan_Unlocked_cash_out_page', views.UnLocked_super_bronzePlan_cashOut, name='super_bronzePlan_Unlocked_cash_out_page'),
    path('silverPlan_Unlocked_cash_out_page', views.UnLocked_silverPlan_cashOut, name='silverPlan_Unlocked_cash_out_page'),
    path('super_silverPlan_Unlocked_cash_out_page', views.UnLocked_super_silverPlan_cashOut, name='super_silverPlan_Unlocked_cash_out_page'),
    path('GoldPlan_Unlocked_cash_out_page', views.Unlocked_GoldPlan_cashOut, name='GoldPlan_Unlocked_cash_out_page'),
    path('diamondPlan_Unlocked_cash_out_page', views.UnLocked_diamondPlan_cashOut, name='diamondPlan_Unlocked_cash_out_page'),
    
    
    
    # ************* Locked withdrawal pakage pages url
    path('basicSupreme_plus_Locked_page', views.Locked_basic_withdrawal, name='basicSupreme_plus_Locked'),
    path('standardSupreme_plus_Locked_page', views.Locked_standard_withdrawal, name='standardSupreme_plus_Locked'),
    path('premiumSupreme_plus_Locked_page', views.Locked_premium_withdrawal, name='premiumSupreme_plus_Locked'),
    path('bronzeSupreme_plus_Locked_page', views.Locked_bronze_withdrawal, name='bronzeSupreme_plus_Locked_page'),
    path('super_bronzeSupreme_plus_Locked_page', views.Locked_super_bronze_withdrawal_page, name='Locked_super_bronze_withdrawal'),
    path('silverSupreme_plus_Locked_page', views.Locked_silver_withdrawal, name='Supreme_plus_Locked_silver_withdrawal_page'),
    path('super_silverSupreme_plus_Locked_page', views.Locked_super_silver_withdrawal_page, name='Supreme_plus_Locked_super_silver_withdrawal_page'),
    path('GoldSupreme_plus_Locked_page', views.Supreme_plus_Locked_gold_withdrawal_page, name='Supreme_plus_Locked_Gold_withdrawal_page'),
    path('diamondSupreme_plus_Locked_page', views.Locked_diamond_withdrawal, name='Supreme_plus_Locked_diamond_withdrawal_page'),
    
    # ************* Locked cash out pages url
    path('basicPlan_Locked_cash_out_page', views.Locked_basicPlan_cashOut, name='basicPlan_Locked_cash_out_page'),
    path('standardPlan_Locked_cash_out_page', views.Locked_standardPlan_cashOut, name='standardPlan_Locked_cash_out_page'),
    path('premiumPlan_Locked_cash_out_page', views.Locked_premiumPlan_cashOut, name='premiumPlan_Locked_cash_out_page'),
    path('bronzePlan_Locked_cash_out_page', views.Locked_bronzePlan_cashOut, name='bronzePlan_Locked_cash_out_page'),
    path('super_bronzePlan_Locked_cash_out_page', views.Locked_super_bronzePlan_cashOut, name='super_bronzePlan_Locked_cash_out_page'),
    path('silverPlan_Locked_cash_out_page', views.Locked_silverPlan_cashOut, name='silverPlan_Locked_cash_out_page'),
    path('super_silverPlan_Locked_cash_out_page', views.Locked_super_silverPlan_cashOut, name='super_silverPlan_Locked_page'),
    path('GoldPlan_Locked_cash_out_page', views.Plan_Locked_goldPlan_cashOut, name='GoldPlan_Locked_cash_out_page'),
    path('diamondPlan_Locked_cash_out_page', views.Locked_diamondPlan_cashOut, name='diamondPlan_Locked_cash_out_page'),
    
    # ************* Savings withdrawal package pages url
    path('basicSupreme_plus_Savings_page', views.Savings_basic_withdrawal, name='basicSupreme_plus_Savings_page'),
    path('standardSupreme_plus_Savings_page', views.Savings_standard_withdrawal, name='standardSupreme_plus_Savings_page'),
    path('premiumSupreme_plus_Savings_page', views.Savings_premium_withdrawal, name='premiumSupreme_plus_Savings_page'),
    path('bronzeSupreme_plus_Savings_page', views.Savings_bronze_withdrawal_page, name='bronzeSupreme_plus_Savings_page'),
    path('super_bronzeSupreme_plus_Savings_page', views.Savings_super_bronze_withdrawal, name='super_bronzeSupreme_plus_Savings_page'),
    path('silverSupreme_plus_Savings_page', views.Savings_silver_withdrawal, name='silverSupreme_plus_Savings_page'),
    path('super_silverSupreme_plus_Savings_page', views.Savings_super_silver_withdrawal, name='super_silverSupreme_plus_Savings_page'),
    path('GoldSupreme_plus_Savings_page', views.Supreme_plus_Savings_gold_withdrawal_page, name='GoldSupreme_plus_Savings_page'),
    path('diamondSupreme_plus_Savings_page', views.Savings_diamond_withdrawal, name='diamondSupreme_plus_Savings_page'),

    # ************* Savings cash Out pakage pages url
    path('basicPlan_Savings_cashOut_page', views.Savings_basicPlan_cashtOut, name='basicPlan_Savings_cashOut_page'),
    path('standardPlan_Savings_cashOut_page', views.Savings_standardPlan_cashtOut, name='standardPlan_Savings_cashOut_page'),
    path('premiumPlan_Savings_cashOut_page', views.Savings_premiumPlan_cashtOut, name='premiumPlan_Savings_cashOut_page'),
    path('bronzePlan_Savings_cashOut_page', views.Savings_bronzePlan_cashtOut, name='bronzePlan_Savings_cashOut_page'),
    path('super_bronzePlan_Savings_cashOut_page', views.Savings_super_bronzePlan_cashtOut, name='super_bronzePlan_Savings_cashOut_page'),
    path('silverPlan_Savings_cashOut_page', views.Savings_silverPlan_cashtOut, name='silverPlan_Savings_cashOut_page'),
    path('super_silverPlan_Savings_cashOut_page', views.Savings_super_silverPlan_cashtOut, name='super_silverPlan_Savings_cashOut_page'),
    path('GoldPlan_Savings_cashOut_page', views.Savings_goldPlan_cashtOut, name='GoldPlan_Savings_cashOut_page'),
    path('diamondPlan_Savings_cashOut_page', views.Savings_diamondPlan_cashtOut, name='diamondPlan_Savings_cashOut_page'),

    # ********** payment confirmation_page ************
    path('comfirm_Supreme_plus_Unlocked_payment/', views.comfirm_Supreme_plus_Unlocked_payment_page, name='comfirm_Supreme_plus_Unlocked_payment_page'),
    path('comfirm_Supreme_plus_Locked_payment_payment', views.comfirm_Supreme_plus_Locked_payment_page, name='comfirm_Supreme_plus_Locked_payment_page'),
    path('comfirm_Supreme_plus_Savings_payment', views.comfirm_Supreme_plus_Savings_payment_page, name='comfirm_Supreme_plus_Savings_payment_page'),
    # ********** / .payment confirmation_page ************

    path('', include('django.contrib.auth.urls')),
    path('signup', signup_view, name='signup_view'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),
    
    path('statistics', views.statistics, name='statistics'),
    path('marketing_stat', views.marketing_stats, name='marketing_stats'),
    path('user_statistics', views.user_stats, name="user_stats")
    
]