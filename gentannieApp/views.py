from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from django.core.files.base import File
from django.db import reset_queries
from django.db.models.expressions import F
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.core.mail import message, send_mail
from django.contrib import messages
from .models import *
from django.contrib.auth.forms import UserCreationForm
from gentannieReferal.models import user_referal
from gentannieReferal.form import referForm

from gent_marketering.models import *

from .form import *
from datetime import date, datetime, timedelta,date,timezone
from time import sleep,thread_time, time
import time
import threading

from django.db.models import Sum,Avg

comfirm_Supreme_plus__pack_details = Supreme_plus_UnLocked.objects.all()
super_pack_details = Supreme_plus_Locked.objects.all()
comfirm_Supreme_plus_Savings_pack_details = Supreme_plus_Savings.objects.all()

def countdown(request):
    return render(request,'gentannieReferal/countdown_lauch.html',None)        

def Referal_withdrawal_alert(get_user):
    EMAIL_HOST_USER = 'anthonix1759@gmail.com'
    subject =  'withdrawal of referral bonus is being requested by %s'%get_user
    message = 'Admin someone just made a request to withdraw referral bonus'
    # recepient = ['informaniac665@gmail.com']
    try:
        send_mail(subject,
            message, 'support@gentannie.com', ['support@gentannie.com'], fail_silently=False)
    except:
        print('MAIL not sent')

def dashboard(request):
    recom_profiles = user_referal.objects.get(user=request.user)
    my_recs = recom_profiles.get_recommended_profiles()

    recom_len =  len(my_recs)
    recomms_rewards = recom_len*1000

    # *******************  referral bonus request ******************
    if request.method=='POST':
        referal_req_form = referForm(request.POST)
        if referal_req_form.is_valid():
            request_mark = user_referal.objects.all().filter(numbers_refered__gte=3).filter(user=request.user)
            request_mark.update(request_bonus=True, requested_bonus=recomms_rewards,total_withdrawed_bonus=F('total_withdrawed_bonus')+recomms_rewards)
            # request_mark.update(request_bonus=True, requested_bonus=10000,total_withdrawed_bonus=F('total_withdrawed_bonus')+10000)

            request_marked = user_referal.objects.all().filter(recommended_by = request.user)
            request_marked.update(recommended_by= None)

            # ****** mailing Admin ****
            get_user = request.user
            Referal_withdrawal_alert(get_user)
            # / .****** mailing Admin *****
        return redirect('dashboard')
    else:
        referal_req_form = referForm()

    # ******************* / .referral bonus request ****************

    user_item_prog = users_investment_progress(user=request.user)
    user_progress_feed = users_investment_progress.objects.all().filter(user=request.user)
    
    users_data = users_investment_progress(user=request.user)
    
    smart_data = Supreme_plus_UnLocked.objects.all().filter(username=request.user)
    super_data = Supreme_plus_Locked.objects.all().filter(username=request.user)
    supreme_data = Supreme_plus_Savings.objects.all().filter(username=request.user)

    # ********** Referal Section ***********
    recom_profiles = user_referal.objects.get(user=request.user)
    my_recs = recom_profiles.get_recommended_profiles()

    recom_len =  len(my_recs)
    recomms_rewards = recom_len * 1000

    # referal_no_check = user_referal.objects.all().filter(user=request.user).filter(numbers_refered__gte=10).exists()
    referal_no_check = user_referal.objects.all().filter(user=request.user).filter(numbers_refered=10).exists()
    referal_no = user_referal.objects.all().filter(user=request.user)
    referal_no.update(numbers_refered=recom_len, Referal_bonus=recomms_rewards)
    
    
    referal_trace = user_referal.objects.all().filter(user=request.user).values_list('recommended_by')
    

    Num_refered = user_referal.objects.all().filter(user=request.user)

    # ********** / .Referal Section ***********
    user_referal_profile = user_referal.objects.filter(user=request.user)
    pic = users_details.objects.all().filter(username=request.user)
    Supreme_plus_UnLocked_feed = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked')
    Supreme_plus_Locked_feed = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked')
    Supreme_plus_Savings_feed = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings')

    context = {
        'referal_trace':referal_trace,
        'users_data':users_data,
        'user_progress_feed':user_progress_feed,
        'recomms_rewards':recomms_rewards,
        'user_referal_profile':user_referal_profile,
        'recom_len':recom_len,
        'smart_data':smart_data,
        'super_data':super_data,
        'supreme_data':supreme_data,
        'pic':pic,
        'Supreme_plus_UnLocked_feed':Supreme_plus_UnLocked_feed,
        'Supreme_plus_Locked_feed':Supreme_plus_Locked_feed,
        'Supreme_plus_Savings_feed':Supreme_plus_Savings_feed,
        'referal_no_check':referal_no_check,
        'referal_req_form':referal_req_form,
        'Num_refered':Num_refered,
        
    }
    return render(request, 'gentannieReferal/dash/dash_index.html', context)

# ************** Referal section ******************
def referal_views(request,  *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profiles = Referal.objects.get(code=code)
        request.session['ref_profile'] = profiles.id
        print('id', profiles.id)
    except:
        pass
    print('site will espire in ', request.session.get_expiry_date())

    session = request.session.get_expiry_age()
    context = {
        'session':session
    }
    return render(request, 'gentannieApp/dash/Referal_page.html', context)

def my_recomms_views(request):
    recom_profiles = user_referal.objects.get(user=request.user)
    my_recs = recom_profiles.get_recommended_profiles()

    recom_len =  len(my_recs)
    recomms_rewards = recom_len*1000

    user_referal_profile = user_referal.objects.filter(user=request.user)

    context = {
        'recomms_rewards':recomms_rewards,
        'my_recs':my_recs,
        'user_referal_profile':user_referal_profile,
        'recom_len':recom_len,
    }
    return render (request, 'gentannieReferal/index2.html', context)

# ******** investment plans deposit Views *********
def deposit_page(request):
    user_Supreme_plus_Unlocked_details = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked')
    user_Supreme_plus_locked_details = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked')
    user_Supreme_plus_Savings_details = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings')

    Supreme_plus_Unlocked_pack_check = Supreme_plus_UnLocked.objects.all().filter(username=request.user)
    Supreme_plus_Unlocked_pack_close = Supreme_plus_Unlocked_pack_check.values().exists()

    Supreme_plus_locked_pack_check = Supreme_plus_Locked.objects.all().filter(username=request.user)
    Supreme_plus_locked_pack_close = Supreme_plus_locked_pack_check.values().exists()

    Supreme_plus_Savings_pack_check = Supreme_plus_Savings.objects.all().filter(username=request.user)
    Supreme_plus_Savings_pack_close = Supreme_plus_Savings_pack_check.values().exists()

    context={
        "user_Supreme_plus_Unlocked_details":user_Supreme_plus_Unlocked_details,
        'Supreme_plus_Unlocked_pack_check':Supreme_plus_Unlocked_pack_check,
        'Supreme_plus_locked_pack_check':Supreme_plus_locked_pack_check,
        'Supreme_plus_Savings_pack_check':Supreme_plus_Savings_pack_check,
        'Supreme_plus_locked_pack_close':Supreme_plus_locked_pack_close,
        'Supreme_plus_Unlocked_pack_close':Supreme_plus_Unlocked_pack_close,
        'Supreme_plus_Savings_pack_close':Supreme_plus_Savings_pack_close,
        
    }
    return render(request, 'gentannieApp/dash/dash_deposit.html',context)

def Supreme_plus_Unlocked_pack(request):
    user_pack = Supreme_plus_UnLocked(username=request.user)
    if request.method == 'POST':
        packform = Supreme_plus_Unlocked_form(request.POST, request.FILES, instance=user_pack)
        if packform.is_valid():
            users_investment_progress.objects.filter(user=request.user)

            users_investment_progress.objects.filter(user=request.user)
            users_data = users_investment_progress(user=request.user)

            # acc_type = user_pack.account_type #***********Re-editings
            acc_plan = user_pack.plan_name
            uploaded_proof = user_pack.payment_proof
            pack = user_pack.plan

            span = '6 months'

            if acc_plan ==  basic:
                amount_deposit = 60000
            elif acc_plan == standard:
                amount_deposit = 100000
            elif acc_plan == premium:
                amount_deposit = 160000
            elif acc_plan ==  bronze:
                amount_deposit = 200000
            elif acc_plan == super_bronze:
                amount_deposit = 360000
            elif acc_plan == silver:
                amount_deposit = 500000
            elif acc_plan == super_silver:
                amount_deposit = 1000000
            elif acc_plan == Gold:
                amount_deposit = 2000000
            elif acc_plan == Diamond:
                amount_deposit = 3000000

            # ******** Acc type Logics *******
            interest = int(amount_deposit) * 0.25
            time_stamp = timedelta(days = 30)

            future_time = datetime.now() + time_stamp
            Supreme_plus_UnLocked.objects.update_or_create(username=request.user, amount_deposited=amount_deposit, ROI=interest, plan_name=pack, plan=acc_plan, payment_proof=uploaded_proof, )
            users_investment_progress.objects.all().filter(user=request.user).update_or_create(user=request.user, amount_deposited = amount_deposit, ROI=interest, proof=uploaded_proof, plan=acc_plan, package=pack, life_span=span )

            deposit = str(amount_deposit)
            get_user = request.user
            deposit_sending(str(deposit), get_user)# sending Admin email for deposit alert
            
            
            # *******************************************
            # plans = Supreme_plus_UnLocked.all().filter(plan_name)
            # print('*******************>',plans)
            # *******************************************

            return redirect('dashboard')
    else:
        packform = Supreme_plus_Unlocked_form()
    context = {
        'packform':packform,
    }   
    return render(request, 'gentannieApp/dash/make_supremePlus_Unlocked_deposit.html', context)

def Supreme_plus_Locked_pack(request):
    user_pack = Supreme_plus_Locked(username=request.user)
    if request.method == 'POST':
        packform = Supreme_plus_Locked_form(request.POST, request.FILES, instance=user_pack)
        if packform.is_valid():
            users_investment_progress.objects.filter(user=request.user)

            acc_plan = user_pack.plan_name
            # acc_type = user_pack.account_type
            uploaded_proof = user_pack.payment_proof
            pack = user_pack.plan

            span = '6 months'
            # if pack ==  'Supreme_plus_Locked':
            #     span = '6 months'

            if acc_plan ==  basic:
                amount_deposit = 60000
            elif acc_plan == standard:
                amount_deposit = 100000
            elif acc_plan == premium:
                amount_deposit = 160000
            elif acc_plan ==  bronze:
                amount_deposit = 200000
            elif acc_plan == super_bronze:
                amount_deposit = 360000
            elif acc_plan == silver:
                amount_deposit = 500000
            elif acc_plan == super_silver:
                amount_deposit = 1000000
            elif acc_plan == Gold:
                amount_deposit = 2000000
            elif acc_plan == Diamond:
                amount_deposit = 3000000

            # ******** Acc type Logics *******
            interest = amount_deposit * 0.80
            time_stamp = timedelta(days = 30 )
            
            future_time = datetime.now() + time_stamp
            Supreme_plus_Locked.objects.update_or_create(username=request.user, amount_deposited=amount_deposit, ROI=interest, plan_name=pack, plan=acc_plan, payment_proof=uploaded_proof, )
            users_investment_progress.objects.all().filter(user=request.user).update_or_create(user=request.user, amount_deposited = amount_deposit, ROI=interest, proof=uploaded_proof, plan=acc_plan, package=pack, life_span=span)

            deposit = str(amount_deposit)
            get_user = request.user
            deposit_sending(deposit, get_user)# sending Admin email for deposit alert

            return redirect('dashboard')
    else:
        packform = Supreme_plus_Locked_form()

    context = {
        'packform':packform,
    }   
    # return render(request, 'gentannieApp/dash/dash_make_deposit.html', context)
    return render(request, 'gentannieApp/dash/make_SupremePlus_Locked_deposit.html', context)

def Supreme_plus_Savings_pack(request):
    user_pack = Supreme_plus_Savings(username=request.user)
    
    if request.method == 'POST':
        packform = Supreme_plus_Savings_form(request.POST, request.FILES, instance=user_pack)
        if packform.is_valid():
            users_investment_progress.objects.filter(user=request.user)

            acc_plan = user_pack.plan_name
            pack = user_pack.plan
            uploaded_proof = user_pack.payment_proof

            span = '6 months'

            if acc_plan ==  basic:
                amount_deposit = 60000
            elif acc_plan == standard:
                amount_deposit = 100000
            elif acc_plan == premium:
                amount_deposit = 160000
            elif acc_plan ==  bronze:
                amount_deposit = 200000
            elif acc_plan == super_bronze:
                amount_deposit = 360000
            elif acc_plan == silver:
                amount_deposit = 500000
            elif acc_plan == super_silver:
                amount_deposit = 1000000
            elif acc_plan == Gold:
                amount_deposit = 2000000
            elif acc_plan == Diamond:
                amount_deposit = 3000000

            interest = amount_deposit * 0.165
            future_time = datetime.now() + timedelta(days = 30)

            Supreme_plus_Savings.objects.update_or_create(username=request.user, amount_deposited=amount_deposit, ROI=interest, plan_name=pack, plan=acc_plan, payment_proof=uploaded_proof, )
            users_investment_progress.objects.all().filter(user=request.user).update_or_create(user=request.user, amount_deposited = amount_deposit, ROI=interest, proof=uploaded_proof, plan=acc_plan, package=pack, life_span=span )

            deposit = str(amount_deposit)
            get_user = request.user
            deposit_sending(deposit, get_user)# sending Admin email for deposit alert

            return redirect('dashboard')
    else:
        packform = Supreme_plus_Savings_form()

    context = {
        'packform':packform,
    }   
    
    return render(request, 'gentannieApp/dash/make_SupremePlus_Savings_deposit.html', context)
    # return render(request, 'gentannieReferal/dash/dash_profile.html', context)


# ************ withdrawal request **************
def user_withdrawal_page(request):
    user_progress_feed = users_investment_progress.objects.all().filter(user=request.user)

    Supreme_plus_Unlocked_data = Supreme_plus_UnLocked.objects.all().filter(username=request.user)
    Supreme_plus_Locked_data = Supreme_plus_Locked.objects.all().filter(username=request.user)
    Supreme_plus_Savings_data = Supreme_plus_Savings.objects.all().filter(username=request.user)

    context = {
        'user_progress_feed':user_progress_feed,
        'Supreme_plus_Unlocked':Supreme_plus_Unlocked,
        'Supreme_plus_Locked':Supreme_plus_Locked,
        'Supreme_plus_Savings':Supreme_plus_Savings
        }
    return render(request,'gentannieApp/dash/withdrawal_page.html',context)


# ******************************
def UnLocked_basic_withdrawal(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='basic')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="basic").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    user_progress_update_basic = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='basic')
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='basic').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_basic = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='basic').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_basic':user_progress_update_basic,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Unlocked_basic_withdrawal_page.html',context)
def UnLocked_basicPlan_cashOut(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='basic')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="basic").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='basic').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_basic = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='basic').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_basic':user_progress_update_basic,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/basicPlan_Unlocked_cash_out_page.html',context)

def UnLocked_standard_withdrawal(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='standard')
            req_user_option.update(request=True)
            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="standard").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='standard').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_standard = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='standard').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_standard':user_progress_update_standard,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Unlocked_standard_withdrawal_page.html',context)
def UnLocked_standardPlan_cashOut(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='standard')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="standard").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='standard').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_standard = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='standard').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_standard':user_progress_update_standard,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/standardPlan_Unlocked_cash_out_page.html',context)

def UnLocked_premium_withdrawal(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='premium')
            req_user_option.update(request=True)
            
            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="premium").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='premium').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_premium = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='premium').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        # 'Unlocked_premium_withdraw_form':Unlocked_premium_withdraw_form,
        'user_progress_update_premium':user_progress_update_premium,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Unlocked_premium_withdrawal_page.html',context)
def UnLocked_premiumPlan_cashOut(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='premium')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="premium").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='premium').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_premium = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='premium').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_premium':user_progress_update_premium,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/premiumPlan_Unlocked_cash_out_page.html',context)

def UnLocked_bronze_withdrawal(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='bronze')
            req_user_option.update(request=True)
            
            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="bronze").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='bronze').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_bronze = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='bronze').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_bronze':user_progress_update_bronze,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Unlocked_bronze_withdrawal_page.html',context)
def UnLocked_bronzePlan_cashOut(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='bronze')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="bronze").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='bronze').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_bronze = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='bronze').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_bronze':user_progress_update_bronze,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/bronzePlan_Unlocked_cash_out_page.html',context)

def UnLocked_super_bronze_withdrawal(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='super_bronze')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="super_bronze").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='super_bronze').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_super_bronze = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='super_bronze').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_super_bronze':user_progress_update_super_bronze,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Unlocked_super_bronze_withdrawal_page.html',context)
def UnLocked_super_bronzePlan_cashOut(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='super_bronze')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="super_bronze").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='super_bronze').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_super_bronze = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='super_bronze').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_super_bronze':user_progress_update_super_bronze,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/super_bronzePlan_Unlocked_cash_out_page.html',context)

def UnLocked_silver_withdrawal(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='silver')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="silver").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='silver').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_silver = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='silver').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        # 'Unlocked_silver_withdraw_form':Unlocked_silver_withdraw_form,
        'user_progress_update_silver':user_progress_update_silver,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Unlocked_silver_withdrawal_page.html',context)
def UnLocked_silverPlan_cashOut(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='silver')
            req_user_option.update(request=True)
            
            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="silver").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='silver').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_silver = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='silver').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        # 'Unlocked_silver_withdraw_form':Unlocked_silver_withdraw_form,
        'user_progress_update_silver':user_progress_update_silver,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/silverPlan_Unlocked_cash_out_page.html',context)

def Unlocked_gold_withdrawal(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='gold').filter(hault=True)
            req_user_option.update(request=True)

            user_progress_update_gold = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='gold')

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="gold").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)
            
            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    user_progress_update_gold = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='Gold') 
    

    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='gold').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
        
    user_progress_update_gold_filtered = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='gold').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')

    context = {
        'user_progress_update_gold_filtered':user_progress_update_gold_filtered,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Unlocked_gold_withdrawal_page.html',context)
def Unlocked_GoldPlan_cashOut(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='gold').filter(hault=True)
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)
            
            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="gold").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()    
       
        
        user_progress_update_gold = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='Gold') 
          
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='gold').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_gold_filtered = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='gold').filter(Due_date__lte=datetime.isoformat(current_date))
    # user_progress_update_gold_filtered = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='gold').filter(Due_date__lte=datetime.isoformat(current_date)).values('id','Due_date','date_created')
    
    context = {
        'user_progress_update_gold_filtered':user_progress_update_gold_filtered,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/GoldPlan_cash_out_page.html',context)

def UnLocked_super_silver_withdrawal(request):
    
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='super_silver')
            req_user_option.update(request=True)
            
            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="super_silver").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='super_silver').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_super_silver = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='super_silver').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        # 'Unlocked_super_silver_withdraw_form':Unlocked_super_silver_withdraw_form,
        'user_progress_update_super_silver':user_progress_update_super_silver,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Unlocked_super_silver_withdrawal_page.html',context)
def UnLocked_super_silverPlan_cashOut(request):
    
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='super_silver')
            req_user_option.update(request=True)
            
            current_date = datetime.now()
            today = date.isoformat(current_date)
            
            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="super_silver").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='super_silver').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_super_silver = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='super_silver').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_super_silver':user_progress_update_super_silver,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/super_silverPlan_Unlocked_cash_out_page.html',context)

def UnLocked_diamond_withdrawal(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='diamond')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="diamond").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='diamond').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_diamond = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='diamond').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        # 'Unlocked_diamond_withdraw_form':Unlocked_diamond_withdraw_form,
        'user_progress_update_diamond':user_progress_update_diamond,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Unlocked_diamond_withdrawal_page.html',context)
def UnLocked_diamondPlan_cashOut(request):
    if request.method == 'POST':
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Unlocked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='diamond')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="diamond").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='diamond').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_diamond = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='diamond').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_diamond':user_progress_update_diamond,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/diamondPlan_Unlocked_cash_out_page.html',context)

# ****************** Locked packages withdrawal ********************

def Locked_basic_withdrawal(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='basic')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)
            
            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="basic").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='basic').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_basic = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='basic').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_basic':user_progress_update_basic,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Locked_basic_withdrawal_page.html',context)
def Locked_basicPlan_cashOut(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='basic')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="basic").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='basic').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_basic = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='basic').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_basic':user_progress_update_basic,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/basicPlan_Locked_cash_out_page.html',context)

def Locked_standard_withdrawal(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='standard')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="standard").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='standard').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_standard = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='standard').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_standard':user_progress_update_standard,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Locked_standard_withdrawal_page.html',context)
def Locked_standardPlan_cashOut(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='standard')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="standard").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='standard').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_standard = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='standard').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_standard':user_progress_update_standard,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/standardPlan_Locked_cash_out_page.html',context)

def Locked_premium_withdrawal(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='premium')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="premium").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='premium').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_premium = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='premium').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_premium':user_progress_update_premium,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Locked_premium_withdrawal_page.html',context)
def Locked_premiumPlan_cashOut(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='premium')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="premium").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='premium').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_premium = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='premium').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        # 'Locked_premium_withdraw_form':Locked_premium_withdraw_form,
        'user_progress_update_premium':user_progress_update_premium,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/premiumPlan_Locked_cash_out_page.html',context)

def Locked_bronze_withdrawal(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='bronze')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="bronze").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='bronze').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_bronze = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='bronze').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_bronze':user_progress_update_bronze,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Locked_bronze_withdrawal_page.html',context)
def Locked_bronzePlan_cashOut(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='bronze')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="bronze").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='bronze').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_bronze = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='bronze').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_bronze':user_progress_update_bronze,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/bronzePlan_Locked_cash_out_page.html',context)

def Locked_super_bronze_withdrawal_page(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='super_bronze')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)
        
            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="super_bronze").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='super_bronze').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists().filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    user_progress_update_super_bronze = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='super_bronze')
    
    context = {
        'user_progress_update_super_bronze':user_progress_update_super_bronze,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Locked_super_bronze_withdrawal_page.html',context)
def Locked_super_bronzePlan_cashOut(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='super_bronze')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)
        
            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="super_bronze").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='super_bronze').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists().filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    user_progress_update_super_bronze = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='super_bronze')
    
    context = {
        'user_progress_update_super_bronze':user_progress_update_super_bronze,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/super_bronzePlan_Locked_cash_out_page.html',context)

# def Locked_silver_withdrawal(request):
#     if request.method == 'POST':
#         Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
#         if Locked_withdraw_form.is_valid():
#             messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
#             req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='silver')
#             req_user_option.update(request=True)

#             Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="silver")
#             Supreme_plus_Locked_pull_request.update(withdraw_request=True)

#             get_user = request.user
#             mail_sending(get_user)#sends Admin alert for user withdrawal request 

#             return redirect('dashboard')
#     else:
#         Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
#     user_progress_update_silver = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='silver')
    
#     current_date = datetime.now()
#     today = date.isoformat(current_date)

#     date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='silver').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
#     context = {
#         # 'Locked_silver_withdraw_form':Locked_silver_withdraw_form,
#         'user_progress_update_silver':user_progress_update_silver,
#         'today':today,
#         'date_check':date_check,
#     }
#     return render(request, 'gentannieApp/dash/Locked_silver_withdrawal_page.html',context)

def Locked_silver_withdrawal(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='silver')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="silver").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='silver').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_silver = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='silver').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        # 'Locked_silver_withdraw_form':Locked_silver_withdraw_form,
        'user_progress_update_silver':user_progress_update_silver,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Locked_silver_withdrawal_page.html',context)
def Locked_silverPlan_cashOut(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='silver')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="silver").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='silver').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_silver = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='silver').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_silver':user_progress_update_silver,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/silverPlan_Locked_cash_out_page.html',context)

def Supreme_plus_Locked_gold_withdrawal_page(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='gold')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="gold").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='gold').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_gold = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='gold').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_gold':user_progress_update_gold,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Locked_gold_withdrawal_page.html',context)
def Plan_Locked_goldPlan_cashOut(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='gold')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="gold").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='gold').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_gold = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='gold').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_gold':user_progress_update_gold,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/GoldPlan_Locked_cash_out_page.html',context)

def Locked_super_silver_withdrawal_page(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='super_silver')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="super_silver").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='super_silver').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_super_silver = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='super_silver').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_super_silver':user_progress_update_super_silver,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Locked_super_silver_withdrawal_page.html',context)
def Locked_super_silverPlan_cashOut(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='super_silver')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="super_silver").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='super_silver').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_super_silver = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='super_silver').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_super_silver':user_progress_update_super_silver,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/super_silverPlan_Locked_cash_out_page.html',context)

def Locked_diamond_withdrawal(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='diamond')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="diamond").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='diamond').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_diamond = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='diamond').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_diamond':user_progress_update_diamond,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Locked_diamond_withdrawal_page.html',context)
def Locked_diamondPlan_cashOut(request):
    if request.method == 'POST':
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST)
        if Locked_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user).filter(plan_name='diamond')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Locked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan="diamond").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Locked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='diamond').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_diamond = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(plan='diamond').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_diamond':user_progress_update_diamond,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/diamondPlan_Locked_cash_out_page.html',context)

# ****************** Savings packages withdrawal ********************

def Savings_basic_withdrawal(request):
    if request.method == 'POST':
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST)
        if Savings_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user).filter(plan_name='basic')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan="basic").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='basic').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_basic = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='basic').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_basic':user_progress_update_basic,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Savings_basic_withdrawal_page.html',context)
def Savings_basicPlan_cashtOut(request):
    if request.method == 'POST':
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST)
        if Savings_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user).filter(plan_name='basic')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan="basic").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='basic').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_basic = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='basic').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_basic':user_progress_update_basic,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/basicPlan_Savings_cashOut_page.html',context)

def Savings_standard_withdrawal(request):
    if request.method == 'POST':
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST)
        if Savings_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user).filter(plan_name='standard')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan="standard").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='standard').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_standard = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='standard').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        'user_progress_update_standard':user_progress_update_standard,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Savings_standard_withdrawal_page.html',context)
def Savings_standardPlan_cashtOut(request):
    if request.method == 'POST':
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST)
        if Savings_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user).filter(plan_name='standard')
            req_user_option.update(request=True)

            current_date = datetime.now()
            today = date.isoformat(current_date)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan="standard").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='standard').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_standard = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='standard').filter(Due_date__lte=datetime.isoformat(current_date))
    
    context = {
        'user_progress_update_standard':user_progress_update_standard,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/standardPlan_Savings_cashOut_page.html',context)

def Savings_premium_withdrawal(request):
    if request.method == 'POST':
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST)
        if Savings_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user).filter(plan_name='premium')
            req_user_option.update(request=True)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan="premium").filter(Due_date__lte=datetime.isoformat(current_date))
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
        
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='premium').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    user_progress_update_premium = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='premium').filter(Due_date__gt=datetime.isoformat(current_date)).values('id','Due_date','date_created','package','plan')
    
    context = {
        # 'Savings_premium_withdraw_form':Savings_premium_withdraw_form,
        'user_progress_update_premium':user_progress_update_premium,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Savings_premium_withdrawal_page.html',context)
def Savings_bronze_withdrawal_page(request):
    if request.method == 'POST':
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST)
        if Savings_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user).filter(plan_name='bronze')
            req_user_option.update(request=True)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan="bronze")
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
        
    user_progress_update_bronze = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='bronze')
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='bronze').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    context = {
        'user_progress_update_bronze':user_progress_update_bronze,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Savings_bronze_withdrawal_page.html',context)

def Savings_super_bronze_withdrawal(request):
    if request.method == 'POST':
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST)
        if Savings_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user).filter(plan_name='super_bronze')
            req_user_option.update(request=True)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan="super_bronze")
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
        
    user_progress_update_super_bronze = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='super_bronze')
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='super_bronze').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    context = {
        'user_progress_update_super_bronze':user_progress_update_super_bronze,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Savings_super_bronze_withdrawal_page.html',context)

def Savings_silver_withdrawal(request):
    if request.method == 'POST':
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST)
        if Savings_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user).filter(plan_name='silver')
            req_user_option.update(request=True)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan="silver")
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
        
    user_progress_update_silver = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='silver')
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='silver').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    context = {
        # 'Savings_silver_withdraw_form':Savings_silver_withdraw_form,
        'user_progress_update_silver':user_progress_update_silver,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Savings_silver_withdrawal_page.html',context)

def Savings_silver_withdrawal(request):
    if request.method == 'POST':
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST)
        if Savings_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user).filter(plan_name='silver')
            req_user_option.update(request=True)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan="silver")
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
        
    user_progress_update_silver = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='silver')
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='silver').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    context = {
        # 'Savings_silver_withdraw_form':Savings_silver_withdraw_form,
        'user_progress_update_silver':user_progress_update_silver,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Savings_silver_withdrawal_page.html',context)

def Supreme_plus_Savings_gold_withdrawal_page(request):
    if request.method == 'POST':
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST)
        if Savings_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user).filter(plan_name='gold')
            req_user_option.update(request=True)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan="gold")
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
        
    user_progress_update_gold = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='gold')
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='gold').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    context = {
        # 'Savings_gold_withdraw_form':Savings_gold_withdraw_form,
        'user_progress_update_gold':user_progress_update_gold,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Savings_gold_withdrawal_page.html',context)

def Savings_super_silver_withdrawal(request):
    if request.method == 'POST':
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST)
        if Savings_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user).filter(plan_name='super_silver')
            req_user_option.update(request=True)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan="super_silver")
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
        
    user_progress_update_super_silver = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='super_silver')
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='super_silver').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    context = {
        # 'Savings_super_silver_withdraw_form':Savings_super_silver_withdraw_form,
        'user_progress_update_super_silver':user_progress_update_super_silver,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Savings_super_silver_withdrawal_page.html',context)

def Savings_diamond_withdrawal(request):
    if request.method == 'POST':
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST)
        if Savings_withdraw_form.is_valid():
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user).filter(plan_name='diamond')
            req_user_option.update(request=True)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan="diamond")
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
        
    user_progress_update_diamond = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='diamond')
    
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(plan='diamond').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    context = {
        'user_progress_update_diamond':user_progress_update_diamond,
        'today':today,
        'date_check':date_check,
    }
    return render(request, 'gentannieApp/dash/Savings_diamond_withdrawal_page.html',context)

# *******************************************

def Supreme_plus_UnLocked_withdrawal(request):
    smart_opt = Supreme_plus_UnLocked(username=request.user)
    if request.method == 'POST':
        Supreme_plus_Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm(request.POST)
        if Supreme_plus_Unlocked_withdraw_form.is_valid():
            
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name='Gold')
            # req_user_option = Supreme_plus_UnLocked.objects.filter(username=request.user).filter(plan_name=get_plan_name)
            req_user_option.update(request=True)

            Supreme_plus_Unlocked_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan="Gold")
            Supreme_plus_Unlocked_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        Supreme_plus_Unlocked_withdraw_form = Supreme_plus_Unlocked_withdrawalForm()
            
    user_progress_update_Gold = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(plan='Gold')

    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(Due_date__lt=datetime.isoformat(current_date)).values().exists()
    context = {
        'Supreme_plus_Unlocked_withdraw_form':Supreme_plus_Unlocked_withdraw_form,
        'user_progress_update_Gold':user_progress_update_Gold,
        'today':today,
        'date_check':date_check,

    }
    return render(request, 'gentannieApp/dash/Supreme_plus_Unlocked_withdrawal_page.html',context)

def Supreme_plus_Locked_withdrawal(request):
    super_opt = Supreme_plus_Locked(username=request.user)
    if request.method == 'POST':
        Supreme_plus_Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm(request.POST, instance=super_opt)
        if Supreme_plus_Locked_withdraw_form.is_valid:
            req_user_option = Supreme_plus_Locked.objects.filter(username=request.user)
            req_user_option.update(request=True)

            super_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked')
            super_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#Alerts Admin for withdrawal request

            return redirect('dashboard')
    else:
        Supreme_plus_Locked_withdraw_form = Supreme_plus_Locked_withdrawalForm()
    user_progress_update = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Locked')
    for invested_items in user_progress_update.iterator():
        invested_items

    current_date = datetime.now()
    today = date.isoformat(current_date)
    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(Due_date__lte=datetime.isoformat(current_date)).values().exists()
    context = {
        'Supreme_plus_Locked_withdraw_form':Supreme_plus_Locked_withdraw_form,
        'user_progress_update':user_progress_update,
        'today':today,
        'date_check':date_check
    }
    return render(request, 'gentannieApp/dash/Supreme_plus_Locked_withdrawal_page.html',context)

def Supreme_plus_Savings_withdrawal_page(request):
    Supreme_plus_Savings_opt = Supreme_plus_Savings(username=request.user)
    if request.method == 'POST':
        Supreme_plus_Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm(request.POST, instance=Supreme_plus_Savings_opt)
        if Supreme_plus_Savings_withdraw_form.is_valid:
            req_user_option = Supreme_plus_Savings.objects.filter(username=request.user)
            req_user_option.update(request=True)

            Supreme_plus_Savings_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings')
            Supreme_plus_Savings_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#Alerts Admin for withdrawal request

            return redirect('dashboard')
    else:
        Supreme_plus_Savings_withdraw_form = Supreme_plus_Savings_withdrawalForm()
    user_progress_update = users_investment_progress.objects.filter(user=request.user).filter(package='Supreme_plus_Savings')
    current_date = datetime.now()
    today = date.isoformat(current_date)
    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings').filter(Due_date__lte=datetime.isoformat(current_date)).values().exists()
    context = {
        'Supreme_plus_Savings_withdraw_form':Supreme_plus_Savings_withdraw_form,
        'user_progress_update':user_progress_update,
        'today':today,
        'date_check':date_check
    }
    return render(request, 'gentannieApp/dash/Supreme_plus_Savings_withdrawal_page.html',context)
# **************** / .withdrawal request *****************

def notification(request):
    notice = notify_user.objects.all().filter(username=request.user)
    notice2 = notify_all_user.objects.all()

    context={
        'notice':notice,
        'notice2':notice2
    }
    return render(request,'gentannieApp/dash/dash_notification.html', context)

def account_detail_profile(request):
    user_prof = users_details(username=request.user)
    if request.method == 'POST':
        profile_form = users_detailsForm(request.POST, request.FILES, instance=user_prof)
        if profile_form.is_valid():
            # profile_form.cl
            user_details = profile_form.save(commit=False)
            user_details.save()
 
        return redirect('dashboard')
    else:
        profile_form = users_detailsForm()

    details = users_details.objects.all().filter(username=request.user)
    profile_check = users_details.objects.all().filter(username=request.user).values()
    profile_list = users_details.objects.all().values_list

    print(profile_list)
    rendered_form = ''
    button_diabler = ''
    Display_btn = ''
    if profile_check.exists():
        button_diabler = 'hidden'
        Display_btn = 'Profile updated'
        print('am present sir')
    else:
        rendered_form = users_detailsForm()
        Display_btn = 'submit'
        print('not in list')

    profile_context={
        'rendered_form':rendered_form,
        'details':details,
        'button_diabler':button_diabler,
        'Display_btn':Display_btn
    }
    return render(request,'gentannieApp/dash/dash_profile.html',profile_context)

def mail_check():
    dateDue = users_investment_progress.objects.all()
    # due_date = dateDue.get()
    due_date = date.today
    filtered_date = users_investment_progress.objects.filter(Due_date = str(due_date))

    print (filtered_date.user )
# ******** / .investment plans Views *********

def logoutUser(request):
    logout(request)
    messages.info(request, "You have logged Out!!!")
    return redirect("login")

def deposit_sending(deposit, get_user):
    EMAIL_HOST_USER = 'anthonix1759@gmail.com'
    subject =  'Deposit made, plan has been paid for by %s'%get_user
    message = 'Admin Someone just made a deposit and needs comfirmation'
    # recepient = ['informaniac665@gmail.com']
    try:
        send_mail(subject,
            message, 'support@gentannie.com', ['support@gentannie.com'], fail_silently=False)
    except:
        print('MAIL not sent')

def mail_sending(get_user):
    EMAIL_HOST_USER = 'anthonix1759@gmail.com'
    subject =  'Withdrawal is being requested for by %s'%get_user
    message = 'Admin someone just made a request for Withdrawal '
    # recepient = ['informaniac665@gmail.com']
    try:
        send_mail(subject,
            # message, 'informaniac665@gmail.com', ['anthonix1759@gmail.com'], fail_silently=False)
            message, 'informaniac665@gmail.com', ['support@gentannie.com'], fail_silently=False)
    except:
        print('MAIL not sent')

def scheduled_withdrawal():
    filtered_data = users_investment_progress.objects.all().filter(deposit_status=comfirmed, hault=False, plan=Supreme_plus_Locked)
    super_filtered_data = users_investment_progress.objects.all().filter(deposit_status=comfirmed, hault=False, plan=Supreme_plus_Unlocked)
    supreme_filtered_data = users_investment_progress.objects.all().filter(deposit_status=comfirmed, hault=False, plan=Supreme_plus_Savings)
    
    # filtered_data = users_investment_progress.objects.all().filter(deposit_status=comfirmed).filter(hault=False).filter(account_type=locked)
    # super_filtered_data = users_investment_progress.objects.all().filter(deposit_status=comfirmed).filter(hault=False).filter(account_type=unlocked)
    # supreme_filtered_data = users_investment_progress.objects.all().filter(deposit_status=comfirmed).filter(hault=False).filter(account_type='NONE')

    filtered_data.update(Due_date=datetime.now()+ timedelta(days= (30*3)),hault=True )
    super_filtered_data.update(Due_date=datetime.now()+ timedelta(days=30),hault=True)
    supreme_filtered_data.update(Due_date=datetime.now()+ timedelta(days=30),hault=True)

    # current_date = datetime.now()
    current_date = date.today()
    payment_filters = users_investment_progress.objects.all().filter(deposit_status=comfirmed).filter(Due_date__lte=date.isoformat(current_date))

    payment_filters.update(payment_status=payment_declined)

def life_span_cheker():
    Supreme_plus_Unlocked_pay_out_checker = Supreme_plus_UnLocked.objects.all().filter(payment_count=6)
    Supreme_plus_Locked_pay_out_checker = Supreme_plus_Locked.objects.all().filter(payment_count=6)
    Supreme_plus_Savings_pay_out_checker = Supreme_plus_Savings.objects.all().filter(payment_count=6)
    pay_out_checker = users_investment_progress.objects.all().filter(count=6)

    Supreme_plus_Unlocked_pay_out_checker.all().delete()
    Supreme_plus_Locked_pay_out_checker.all().delete()
    Supreme_plus_Savings_pay_out_checker.all().delete()
    pay_out_checker.all().delete()

def transact_history(request):
    user_history = users_investment_progress.objects.all().filter(user=request.user)
    # get_ROI = user_history.values_list('ROI')
    # get_count = user_history.values_list('count')
    # total_gained = get_ROI * get_count
    # for count_check in user_history:
    #     total_gained = count_check.ROI * count_check.count
    # withdrawal_amount_count = user_history.filter()
    # print(withdrawal_amount_count.values())
    context={
        'user_history':user_history,
        # "total_gained":total_gained,
    }
    return render(request, 'gentannieApp/dash/dash_trans_history.html', context)

# ************* payment comfirmations  ********************
def comfirm_Supreme_plus_Unlocked_payment_page(request):
    if request.method=='POST':
        comfirmed_form = Supreme_plus_Unlocked_pay_comfirmForm(request.POST)
        if comfirmed_form.is_valid():

            # ********** keeping count of users life span **********
            Supreme_plus_Unlocked_count = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked')
            Supreme_plus_Unlocked_count_life_span = Supreme_plus_UnLocked.objects.all().filter(username=request.user)
            # Supreme_plus_Unlocked_count_locked = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(account_type=locked)
            # Supreme_plus_Unlocked_count_life_span = Supreme_plus_UnLocked.objects.all().filter(username=request.user).filter(account_type=locked)

            # Supreme_plus_Unlocked_count.update(count=F('count')+3)
            # Supreme_plus_Unlocked_count_life_span.update(payment_count=F('payment_count')+3)

            # Supreme_plus_Unlocked_count_unlockd = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(account_type=unlocked)
            # Supreme_plus_Unlocked_count_life_span_unlocked = Supreme_plus_UnLocked.objects.all().filter(username=request.user).filter(account_type=unlocked)

            Supreme_plus_Unlocked_count.update(count=F('count')+1)
            Supreme_plus_Unlocked_count_life_span.update(payment_count=F('payment_count')+1)
            # ********** / .keeping count of users life span **********

            #*************** withdrawal History ******************
            withdrawal_history = withdrawal_tabel.objects.all().filter(username=request.user)
            withdrawal_history.update()
            #*************** / .withdrawal History ******************

            Supreme_plus_Unlocked_comfirm_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked').filter(withdraw_request=True )
            Supreme_plus_Unlocked_comfirm_check.update(hault=False,withdraw_request=False)

        return redirect('dashboard')
    else:
        comfirmed_form = Supreme_plus_Unlocked_pay_comfirmForm()

    Supreme_plus_Unlocked_progress_feed = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Unlocked')
    context = {
        'comfirmed_form':comfirmed_form,
        "Supreme_plus_Unlocked_progress_feed":Supreme_plus_Unlocked_progress_feed
    }
    return render(request,'gentannieApp/dash/Supreme_plus_Unlocked_pay_comfirm.html', context)

def comfirm_Supreme_plus_Locked_payment_page(request):
    if request.method=='POST':
        comfirmed_form = Supreme_plus_Locked_pay_comfirmForm(request.POST)
        if comfirmed_form.is_valid():

            # ********** keeping count of users life span **********
            Supreme_plus_Locked_count = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked')
            Supreme_plus_Locked_count_life_span = Supreme_plus_Locked.objects.all().filter(username=request.user)
            # Supreme_plus_Locked_count_locked = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(account_type=locked)
            # Supreme_plus_Locked_count_life_span_locked = Supreme_plus_Locked.objects.all().filter(username=request.user).filter(account_type=locked)

            Supreme_plus_Locked_count.update(count=F('count')+3)
            Supreme_plus_Locked_count_life_span.update(payment_count=F('payment_count')+3)

            # Supreme_plus_Locked_count_unlocked = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(account_type=unlocked)
            # Supreme_plus_Locked_count_life_span_unlocked = Supreme_plus_Locked.objects.all().filter(username=request.user).filter(account_type=unlocked)

            # Supreme_plus_Locked_count_unlocked.update(count=F('count')+1)
            # Supreme_plus_Locked_count_life_span_unlocked.update(payment_count=F('payment_count')+1)
            # ********** / .keeping count of users life span **********

            Supreme_plus_Locked_comfirm_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked').filter(withdraw_request=True )
            Supreme_plus_Locked_comfirm_check.update(hault=False,withdraw_request=False)

        return redirect('dashboard')
    else:
        comfirmed_form = Supreme_plus_Locked_pay_comfirmForm()

    Supreme_plus_Locked_progress_feed = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Locked')
    context = {
        'comfirmed_form':comfirmed_form,
        'Supreme_plus_Locked_progress_feed':Supreme_plus_Locked_progress_feed
    }
    return render(request,'gentannieApp/dash/Supreme_plus_Locked_pay_comfirm.html', context)

def comfirm_Supreme_plus_Savings_payment_page(request):
    if request.method=='POST':
        comfirmed_form = Supreme_plus_Savings_pay_comfirmForm(request.POST)
        if comfirmed_form.is_valid():

            # ********* keeping count of users life span *************
            Supreme_plus_Savings_count = users_investment_progress.objects.all().filter(user=request.user).filter(package='Supreme_plus_Savings')
            Supreme_plus_Savings_count.update(count=F('count')+6)

            Supreme_plus_Savings_count_life_span = Supreme_plus_Savings.objects.all().filter(username=request.user)
            Supreme_plus_Savings_count_life_span.update(payment_count=F('payment_count')+6)
            # ********* / .keeping count of users life span *************

            Supreme_plus_Savings_comfirm_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='supreme').filter(withdraw_request=True )
            Supreme_plus_Savings_comfirm_check.update(hault=False,withdraw_request=False)

        return redirect('dashboard')
    else:
        comfirmed_form = Supreme_plus_Savings_pay_comfirmForm()
    
    Supreme_plus_Savings_progress_feed = users_investment_progress.objects.all().filter(user=request.user).filter(package='supreme')
    context = {
        'comfirmed_form':comfirmed_form,
        "Supreme_plus_Savings_progress_feed":Supreme_plus_Savings_progress_feed
    }
    return render(request,'gentannieA.pp/dash/Supreme_plus_Savings_pay_comfirm.html', context)
# ************ / .payment comfirmations ***************

def referal_scheduler():
    referal_bonus_reset = user_referal.objects.all().filter(payment_status='Payment_made')
    referal_bonus_reset.update(Referal_bonus=F('Referal_bonus')-10000, numbers_refered=F('numbers_refered')-10, payment_status='NONE', request_bonus=False, requested_bonus=0)


def statistics(request):
    investment_prog_details = users_investment_progress.objects.all()

    users_detail = users_details.objects.all().order_by('-username')
     
    Supreme_plus_Unlocked_plan_stats = Supreme_plus_UnLocked.objects.all()
    Supreme_plus_Locked_plan_stats = Supreme_plus_Locked.objects.all()
    Supreme_plus_Savings_plan_stats = Supreme_plus_Savings.objects.all()

    summed_Supreme_plus_Unlocked = 0
    summed_Supreme_plus_Locked = 0
    summed_Supreme_plus_Savings = 0

    # for Supreme_plus_Unlocked_x in Supreme_plus_Unlocked_plan_stats.iterator():
    #     gotted_val = Supreme_plus_Unlocked_x.amount_deposited
    #     summed_Supreme_plus_Unlocked = int(gotted_val) + summed_Supreme_plus_Unlocked
    
    amount_details = investment_prog_details.values_list('amount_deposited')
    total_amount_deposited = 0
    for total_amount in amount_details:
        amount_listed = list(total_amount)
        for gotten_sum in amount_listed:
            gotten_sum_int = int(gotten_sum)
            total_amount_deposited = gotten_sum_int + total_amount_deposited

    for Supreme_plus_Unlocked_x in Supreme_plus_Locked_plan_stats.iterator():
        gotted_val = Supreme_plus_Unlocked_x.amount_deposited
        summed_Supreme_plus_Unlocked = int(gotted_val) + summed_Supreme_plus_Unlocked

    summed_Supreme_plus_locked = 0
    for Supreme_plus_Locked_x in Supreme_plus_Locked_plan_stats.iterator():
        gotted_val = Supreme_plus_Locked_x.amount_deposited
        summed_Supreme_plus_locked = int(gotted_val) + summed_Supreme_plus_locked

    for Supreme_plus_Savings_x in Supreme_plus_Savings_plan_stats.iterator():
        gotted_val = Supreme_plus_Savings_x.amount_deposited
        summed_Supreme_plus_Savings = int(gotted_val) + summed_Supreme_plus_Savings

    pack =None

    for invest_prog_details in  investment_prog_details.iterator():
        pack = invest_prog_details.plan
            
    # ************* Sum of Supreme_plus_Unlocked total ROI For Investors *****************
    # ******** total basic Supreme_plus_Unlocked ROI********
    unlocked_basic_count = users_investment_progress.objects.filter(package='Supreme_plus_Unlocked').filter(plan='basic').values_list('count')
    basic_ROI = 0
    total_unlocked_basic_ROI = 0
    for unlocked_basic_ROI_count in unlocked_basic_count.iterator():
        for ROI_count in unlocked_basic_ROI_count:
            basic_ROI = ROI_count + basic_ROI
            total_unlocked_basic_ROI = basic_ROI * 15000

    # ******** total standard Supreme_plus_Unlocked ROI********
    unlocked_standard_count = users_investment_progress.objects.filter(package='Supreme_plus_Unlocked').filter(plan='standard').values_list('count')
    standard_ROI = 0
    total_unlocked_standard_ROI = 0
    for standard_ROI_count in unlocked_standard_count.iterator():
        for ROI_count in standard_ROI_count:
            standard_ROI = ROI_count + standard_ROI
            total_unlocked_standard_ROI = standard_ROI * 25000

    # ******** total premium Supreme_plus_Unlocked ROI********
    unlocked_premium_count = users_investment_progress.objects.filter(package='Supreme_plus_Unlocked').filter(plan='premium').values_list('count')
    premium_ROI = 0
    total_unlock_premium_ROI = 0
    for premium_ROI_count in unlocked_premium_count.iterator():
        for ROI_count in premium_ROI_count:
            premium_ROI = ROI_count + premium_ROI
            total_unlock_premium_ROI = premium_ROI * 40000

    # ******** total bronze Supreme_plus_Unlocked ROI********
    unlocked_bronze_count = users_investment_progress.objects.filter(package='Supreme_plus_Unlocked').filter(plan='bronze').values_list('count')
    bronze_ROI = 0
    total_unlock_bronze_ROI = 0
    for bronze_ROI_count in unlocked_bronze_count.iterator():
        for ROI_count in bronze_ROI_count:
            bronze_ROI = ROI_count + bronze_ROI
            total_unlock_bronze_ROI = bronze_ROI * 50000

    # ******** total super_bronze Supreme_plus_Unlocked ROI********
    unlocked_super_bronze_count = users_investment_progress.objects.filter(package='Supreme_plus_Unlocked').filter(plan='super_bronze').values_list('count')
    super_bronze_ROI = 0
    total_unlock_super_bronze_ROI = 0
    for super_bronze_ROI_count in unlocked_super_bronze_count.iterator():
        for ROI_count in super_bronze_ROI_count:
            super_bronze_ROI = ROI_count + super_bronze_ROI
            total_unlock_super_bronze_ROI = super_bronze_ROI * 90000

    # ******** total silver Supreme_plus_Unlocked ROI********
    unlocked_silver_count = users_investment_progress.objects.filter(package='Supreme_plus_Unlocked').filter(plan='silver').values_list('count')
    silver_ROI = 0
    total_unlock_silver_ROI = 0
    for silver_ROI_count in unlocked_silver_count.iterator():
        for ROI_count in silver_ROI_count:
            silver_ROI = ROI_count + silver_ROI
            total_unlock_silver_ROI = silver_ROI * 125000

    # ******** total super_silver Supreme_plus_Unlocked ROI********
    unlocked_super_silver_count = users_investment_progress.objects.filter(package='Supreme_plus_Unlocked').filter(plan='super_silver').values_list('count')
    super_silver_ROI = 0
    total_unlock_super_silver_ROI = 0
    for super_silver_ROI_count in unlocked_super_silver_count.iterator():
        for ROI_count in super_silver_ROI_count:
            super_silver_ROI = ROI_count + super_silver_ROI
            total_unlock_super_silver_ROI = super_silver_ROI * 250000

    # ******** total ROI Supreme_plus_Unlocked Gold ********
    unlocked_Gold_count = users_investment_progress.objects.filter(package='Supreme_plus_Unlocked').filter(plan='Gold').values_list('count')
    Gold_ROI = 0
    total_unlock_Gold_ROI = 0
    for Gold_ROI_count in unlocked_Gold_count.iterator():
        for ROI_count in Gold_ROI_count:
            Gold_ROI = ROI_count + Gold_ROI
            total_unlock_Gold_ROI = Gold_ROI * 500000

    # ******** total ROI Supreme_plus_Unlocked Diamond ********
    unlocked_Diamond_count = users_investment_progress.objects.filter(package='Supreme_plus_Unlocked').filter(plan='Diamond').values_list('count')
    Diamond_ROI = 0
    total_unlock_Diamond_ROI = 0
    for Diamond_ROI_count in unlocked_Diamond_count.iterator():
        for ROI_count in Diamond_ROI_count:
            Diamond_ROI = ROI_count + Diamond_ROI
            total_unlock_Diamond_ROI = Diamond_ROI * 750000

    # **************************** Sum of Supreme_plus_Locked total ROI For Investors *****************
    # ******** total basic Supreme_plus_Locked ROI********
    basic_count = users_investment_progress.objects.filter(package='Supreme_plus_Locked').filter(plan='basic').values_list('count')
    basic_ROI = 0
    total_locked_basic_ROI = 0
    for basic_ROI_count in basic_count.iterator():
        for ROI_count in basic_ROI_count:
            basic_ROI = ROI_count + basic_ROI
            total_locked_basic_ROI = basic_ROI * 48000

    # ******** total standard Supreme_plus_Locked ROI********
    standard_count = users_investment_progress.objects.filter(package='Supreme_plus_Locked').filter(plan='standard').values_list('count')
    standard_ROI = 0
    total_locked_standard_ROI = 0
    for standard_ROI_count in standard_count.iterator():
        for ROI_count in standard_ROI_count:
            standard_ROI = ROI_count + standard_ROI
            total_locked_standard_ROI = standard_ROI * 80000

    # ******** total premium Supreme_plus_Locked ROI********
    premium_count = users_investment_progress.objects.filter(package='Supreme_plus_Locked').filter(plan='premium').values_list('count')
    premium_ROI = 0
    total_lock_premium_ROI = 0
    for premium_ROI_count in premium_count.iterator():
        for ROI_count in premium_ROI_count:
            premium_ROI = ROI_count + premium_ROI
            total_lock_premium_ROI = premium_ROI * 128000

    # ******** total bronze Supreme_plus_Locked ROI********
    bronze_count = users_investment_progress.objects.filter(package='Supreme_plus_Locked').filter(plan='bronze').values_list('count')
    bronze_ROI = 0
    total_lock_bronze_ROI = 0
    for bronze_ROI_count in bronze_count.iterator():
        for ROI_count in bronze_ROI_count:
            bronze_ROI = ROI_count + bronze_ROI
            total_lock_bronze_ROI = bronze_ROI * 160000

    # ******** total super_bronze Supreme_plus_Locked ROI********
    super_bronze_count = users_investment_progress.objects.filter(package='Supreme_plus_Locked').filter(plan='super_bronze').values_list('count')
    super_bronze_ROI = 0
    total_lock_super_bronze_ROI = 0
    for bronze_ROI_count in super_bronze_count.iterator():
        for ROI_count in bronze_ROI_count:
            super_bronze_ROI = ROI_count + super_bronze_ROI
            total_lock_super_bronze_ROI = super_bronze_ROI * 288000

    # ******** total silver Supreme_plus_Locked ROI********
    silver_count = users_investment_progress.objects.filter(package='Supreme_plus_Locked').filter(plan='silver').values_list('count')
    silver_ROI = 0
    total_lock_silver_ROI = 0
    for silver_ROI_count in silver_count.iterator():
        for ROI_count in silver_ROI_count:
            silver_ROI = ROI_count + silver_ROI
            total_lock_silver_ROI = silver_ROI * 400000

    # ******** total super_silver Supreme_plus_Locked ROI********
    super_silver_count = users_investment_progress.objects.filter(package='Supreme_plus_Locked').filter(plan='super_silver').values_list('count')
    super_silver_ROI = 0
    total_lock_super_silver_ROI = 0
    for super_silver_ROI_count in super_silver_count.iterator():
        for ROI_count in super_silver_ROI_count:
            super_silver_ROI = ROI_count + super_silver_ROI
            total_lock_super_silver_ROI = super_silver_ROI * 800000

    # ******** total Gold Supreme_plus_Locked ROI********
    Gold_count = users_investment_progress.objects.filter(package='Supreme_plus_Locked').filter(plan='Gold').values_list('count')
    Gold_ROI = 0
    total_lock_Gold_ROI = 0
    for Gold_ROI_count in Gold_count.iterator():
        for ROI_count in Gold_ROI_count:
            Gold_ROI = ROI_count + Gold_ROI
            total_lock_Gold_ROI = Gold_ROI * 1600000

    # ******** total Diamond Supreme_plus_Locked ROI********
    Diamond_count = users_investment_progress.objects.filter(package='Supreme_plus_Locked').filter(plan='Diamond').values_list('count')
    Diamond_ROI = 0
    total_lock_Diamond_ROI = 0
    for Diamond_ROI_count in Diamond_count.iterator():
        for ROI_count in Diamond_ROI_count:
            Diamond_ROI = ROI_count + Diamond_ROI
            total_lock_Diamond_ROI = Diamond_ROI * 2400000

    # **************************** Sum of Supreme_plus_Savings total ROI For Investors *****************
    # ******** total basic Supreme_plus_Savings ROI********
    basic_count = users_investment_progress.objects.filter(package='Supreme_plus_Savings').filter(plan='basic').values_list('count')
    basic_ROI = 0
    total_Savings_basic_ROI = 0
    for basic_ROI_count in basic_count.iterator():
        for ROI_count in basic_ROI_count:
            basic_ROI = ROI_count + basic_ROI
            total_Savings_basic_ROI = basic_ROI * 99000

    # ******** total standard Supreme_plus_Savings ROI********
    Savings_standard_count = users_investment_progress.objects.filter(package='Supreme_plus_Savings').filter(plan='standard').values_list('count')
    standard_ROI = 0
    total_Savings_standard_ROI = 0
    for standard_ROI_count in Savings_standard_count.iterator():
        for ROI_count in standard_ROI_count:
            standard_ROI = ROI_count + standard_ROI
            total_Savings_standard_ROI = standard_ROI * 165000

    # ******** total premium Supreme_plus_Savings ROI********
    Supreme_plus_Savings_premium_count = users_investment_progress.objects.filter(package='Supreme_plus_Savings').filter(plan='premium').values_list('count')
    premium_ROI = 0
    total_Savings_premium_ROI = 0
    for premium_ROI_count in Supreme_plus_Savings_premium_count.iterator():
        for ROI_count in premium_ROI_count:
            premium_ROI = ROI_count + premium_ROI
            total_Savings_premium_ROI = premium_ROI * 264000

    # ******** total bronze Supreme_plus_Savings ROI********
    bronze_count = users_investment_progress.objects.filter(package='Supreme_plus_Savings').filter(plan='bronze').values_list('count')
    bronze_ROI = 0
    total_Savings_bronze_ROI = 0
    for bronze_ROI_count in bronze_count.iterator():
        for ROI_count in bronze_ROI_count:
            bronze_ROI = ROI_count + bronze_ROI
            total_Savings_bronze_ROI = bronze_ROI * 330000

    # ******** total super_bronze Supreme_plus_Savings ROI********
    super_bronze_count = users_investment_progress.objects.filter(package='Supreme_plus_Savings').filter(plan='super_bronze').values_list('count')
    super_bronze_ROI = 0
    total_Savings_super_bronze_ROI = 0
    for bronze_ROI_count in super_bronze_count.iterator():
        for ROI_count in bronze_ROI_count:
            super_bronze_ROI = ROI_count + super_bronze_ROI
            total_Savings_super_bronze_ROI = super_bronze_ROI * 594000

    # ******** total silver Supreme_plus_Savings ROI********
    silver_count = users_investment_progress.objects.filter(package='Supreme_plus_Savings').filter(plan='silver').values_list('count')
    silver_ROI = 0
    total_Savings_silver_ROI = 0
    for silver_ROI_count in silver_count.iterator():
        for ROI_count in silver_ROI_count:
            silver_ROI = ROI_count + silver_ROI
            total_Savings_silver_ROI = silver_ROI * 825000

    # ******** total super_silver Supreme_plus_Savings ROI********
    super_silver_count = users_investment_progress.objects.filter(package='Supreme_plus_Savings').filter(plan='super_silver').values_list('count')
    super_silver_ROI = 0
    total_Savings_super_silver_ROI = 0
    for super_silver_ROI_count in super_silver_count.iterator():
        for ROI_count in super_silver_ROI_count:
            super_silver_ROI = ROI_count + super_silver_ROI
            total_Savings_super_silver_ROI = super_silver_ROI * 1650000

    # ******** total Gold Supreme_plus_Savings ROI********
    Gold_count = users_investment_progress.objects.filter(package='Supreme_plus_Savings').filter(plan='Gold').values_list('count')
    Gold_ROI = 0
    total_Savings_Gold_ROI = 0
    for Gold_ROI_count in Gold_count.iterator():
        for ROI_count in Gold_ROI_count:
            Gold_ROI = ROI_count + Gold_ROI
            total_Savings_Gold_ROI = Gold_ROI * 3300000

    # ******** total Diamond Supreme_plus_Savings ROI********
    Diamond_count = users_investment_progress.objects.filter(package='Supreme_plus_Savings').filter(plan='Diamond').values_list('count')
    Diamond_ROI = 0
    total_Savings_Diamond_ROI = 0
    for Diamond_ROI_count in Diamond_count.iterator():
        for ROI_count in Diamond_ROI_count:
            Diamond_ROI = ROI_count + Diamond_ROI
            total_Savings_Diamond_ROI = Diamond_ROI * 4950000

    # count of Supreme_plus_Locked_plan packages
    basic_Supreme_plus_Locked_count = Supreme_plus_Locked_plan_stats.filter(plan='basic').values_list('plan').count()
    standard_Supreme_plus_Locked_count = Supreme_plus_Locked_plan_stats.filter(plan='standard').values_list('plan').count()
    premium_Supreme_plus_Locked_count = Supreme_plus_Locked_plan_stats.filter(plan='premium').values_list('plan').count()
    bronze_Supreme_plus_Locked_count = Supreme_plus_Locked_plan_stats.filter(plan='bronze').values_list('plan').count()
    super_bronze_Supreme_plus_Locked_count = Supreme_plus_Locked_plan_stats.filter(plan='super_bronze').values_list('plan').count()
    silver_Supreme_plus_Locked_count = Supreme_plus_Locked_plan_stats.filter(plan='silver').values_list('plan').count()
    super_silver_Supreme_plus_Locked_count = Supreme_plus_Locked_plan_stats.filter(plan='super_silver').values_list('plan').count()
    Gold_Supreme_plus_Locked_count = Supreme_plus_Locked_plan_stats.filter(plan='Gold').values_list('plan').count()
    diamond_Supreme_plus_Locked_count = Supreme_plus_Locked_plan_stats.filter(plan='Diamond').values_list('plan').count()    

    # count of Supreme_plus_Unlocked_plan packages
    basic_Supreme_plus_Unlocked_count = Supreme_plus_Unlocked_plan_stats.filter(plan='basic').values_list('plan').count()
    standard_Supreme_plus_Unlocked_count = Supreme_plus_Unlocked_plan_stats.filter(plan='standard').values_list('plan').count()
    premium_Supreme_plus_Unlocked_count = Supreme_plus_Unlocked_plan_stats.filter(plan='premium').values_list('plan').count()
    bronze_Supreme_plus_Unlocked_count = Supreme_plus_Unlocked_plan_stats.filter(plan='bronze').values_list('plan').count()
    super_bronze_Supreme_plus_Unlocked_count = Supreme_plus_Unlocked_plan_stats.filter(plan='super_bronze').values_list('plan').count()
    silver_Supreme_plus_Unlocked_count = Supreme_plus_Unlocked_plan_stats.filter(plan='silver').values_list('plan').count()
    super_silver_Supreme_plus_Unlocked_count = Supreme_plus_Unlocked_plan_stats.filter(plan='super_silver').values_list('plan').count()
    Gold_Supreme_plus_Unlocked_count = Supreme_plus_Unlocked_plan_stats.filter(plan='Gold').values_list('plan').count()
    diamond_Supreme_plus_Unlocked_count = Supreme_plus_Unlocked_plan_stats.filter(plan='Diamond').values_list('plan').count()    
    
    # count of Supreme_plus_Savings_plan packages
    basic_Supreme_plus_Savings_count = Supreme_plus_Savings_plan_stats.filter(plan='basic').values_list('plan').count()
    standard_Supreme_plus_Savings_count = Supreme_plus_Savings_plan_stats.filter(plan='standard').values_list('plan').count()
    premium_Supreme_plus_Savings_count = Supreme_plus_Savings_plan_stats.filter(plan='premium').values_list('plan').count()
    bronze_Supreme_plus_Savings_count = Supreme_plus_Savings_plan_stats.filter(plan='bronze').values_list('plan').count()
    super_bronze_Supreme_plus_Savings_count = Supreme_plus_Savings_plan_stats.filter(plan='super_bronze').values_list('plan').count()
    silver_Supreme_plus_Savings_count = Supreme_plus_Savings_plan_stats.filter(plan='silver').values_list('plan').count()
    super_silver_Supreme_plus_Savings_count = Supreme_plus_Savings_plan_stats.filter(plan='super_silver').values_list('plan').count()
    Gold_Supreme_plus_Savings_count = Supreme_plus_Savings_plan_stats.filter(plan='Gold').values_list('plan').count()
    diamond_Supreme_plus_Savings_count = Supreme_plus_Savings_plan_stats.filter(plan='Diamond').values_list('plan').count()    

    # **************
    total_Supreme_plus_Unlocked_depo = Supreme_plus_Unlocked_plan_stats.count()
    total_Supreme_plus_Locked_depo = Supreme_plus_Locked_plan_stats.count()
    total_Supreme_plus_Savings_depo = Supreme_plus_Savings_plan_stats.count()

    total_unlocked_ROI = {  
        total_unlocked_basic_ROI,
        total_unlocked_standard_ROI,
        total_unlock_premium_ROI,
        total_unlock_bronze_ROI,
        total_unlock_super_bronze_ROI,
        total_unlock_silver_ROI,
        total_unlock_super_silver_ROI,
        total_unlock_Gold_ROI,
        total_unlock_Diamond_ROI,
    }

    summed_unlocked_ROI = sum(total_unlocked_ROI)

    total_locked_ROI = {    
        total_locked_basic_ROI,
        total_locked_standard_ROI,
        total_lock_premium_ROI,
        total_lock_bronze_ROI,
        total_lock_super_bronze_ROI,
        total_lock_silver_ROI,
        total_lock_super_silver_ROI,
        total_lock_Gold_ROI,
        total_lock_Diamond_ROI,
    }

    summed_locked_ROI = sum(total_locked_ROI)

    total_savings_ROI = {  
        total_Savings_basic_ROI,
        total_Savings_standard_ROI,
        total_Savings_premium_ROI,
        total_Savings_bronze_ROI,
        total_Savings_super_bronze_ROI,
        total_Savings_silver_ROI,
        total_Savings_super_silver_ROI,
        total_Savings_Gold_ROI,
        total_Savings_Diamond_ROI,
    }

    summed_savings_ROI = sum(total_savings_ROI)

    total_ROI = {summed_savings_ROI,
        summed_locked_ROI,
        summed_unlocked_ROI
        }
    summed_ROI = sum(total_ROI)

    total_basic_ROI = sum({
        total_unlocked_basic_ROI,
        total_locked_basic_ROI,
        total_Savings_basic_ROI,
    })

    total_stantard_ROI = sum({
        total_unlocked_standard_ROI,
        total_locked_standard_ROI,
        total_Savings_standard_ROI,
    })
    total_premium_ROI = sum({
        total_unlock_premium_ROI,
        total_lock_premium_ROI,
        total_Savings_premium_ROI,
    })
    total_bronze_ROI = sum({
        total_unlock_bronze_ROI,
        total_lock_bronze_ROI,
        total_Savings_bronze_ROI,
    })
    total_super_bronze_ROI = sum({
        total_unlock_super_bronze_ROI,
        total_lock_super_bronze_ROI,
        total_Savings_super_bronze_ROI,
        })

    total_silver_ROI = sum({
        total_unlock_silver_ROI,
        total_lock_silver_ROI,
        total_Savings_silver_ROI,
        })

    total_super_silver_ROI = sum({
        total_unlock_super_silver_ROI,
        total_lock_super_silver_ROI,
        total_Savings_super_silver_ROI,
        })
    
    total_Gold_ROI = sum({
        total_unlock_Gold_ROI,
        total_lock_Gold_ROI,
        total_Savings_Gold_ROI,
        })

    total_Diamond_ROI = sum({
        total_unlock_Diamond_ROI,
        total_lock_Diamond_ROI,
        total_Savings_Diamond_ROI,
        })

    sum_total_ROI_payed = sum({
        total_basic_ROI,
        total_stantard_ROI,
        total_premium_ROI,
        total_bronze_ROI,
        total_super_bronze_ROI,
        total_silver_ROI,
        total_super_silver_ROI,
        total_Gold_ROI,
        total_Diamond_ROI,
        })

    context= {
        "sum_total_ROI_payed":sum_total_ROI_payed,

        "total_basic_ROI":total_basic_ROI,
        "total_stantard_ROI":total_stantard_ROI,
        "total_premium_ROI":total_premium_ROI,
        "total_bronze_ROI":total_bronze_ROI,
        "total_super_bronze_ROI":total_super_bronze_ROI,
        "total_silver_ROI":total_silver_ROI,
        "total_super_silver_ROI":total_super_silver_ROI,
        "total_Gold_ROI":total_Gold_ROI,
        "total_Diamond_ROI":total_Diamond_ROI,

        "summed_ROI":summed_ROI,

        'summed_unlocked_ROI':summed_unlocked_ROI,
        'summed_locked_ROI':summed_locked_ROI,
        'summed_savings_ROI':summed_savings_ROI,

        'total_unlocked_basic_ROI':total_unlocked_basic_ROI,
        'total_locked_basic_ROI':total_locked_basic_ROI,
        'total_Savings_basic_ROI':total_Savings_basic_ROI,
        
        'total_unlocked_standard_ROI':total_unlocked_standard_ROI,
        'total_locked_standard_ROI':total_locked_standard_ROI,
        'total_Savings_standard_ROI':total_Savings_standard_ROI,

        'total_unlock_premium_ROI':total_unlock_premium_ROI,
        'total_lock_premium_ROI':total_lock_premium_ROI,
        'total_Savings_premium_ROI':total_Savings_premium_ROI,

        'total_unlock_bronze_ROI':total_unlock_bronze_ROI,
        'total_lock_bronze_ROI':total_lock_bronze_ROI,
        'total_Savings_bronze_ROI':total_Savings_bronze_ROI,

        'total_unlock_super_bronze_ROI':total_unlock_super_bronze_ROI,
        'total_lock_super_bronze_ROI':total_lock_super_bronze_ROI,
        'total_Savings_super_bronze_ROI':total_Savings_super_bronze_ROI,

        'total_unlock_silver_ROI':total_unlock_silver_ROI,
        'total_lock_silver_ROI':total_lock_silver_ROI,
        'total_Savings_silver_ROI':total_Savings_silver_ROI,

        'total_unlock_super_silver_ROI':total_unlock_super_silver_ROI,
        'total_lock_super_silver_ROI':total_lock_super_silver_ROI,
        'total_Savings_super_silver_ROI':total_Savings_super_silver_ROI,

        'total_unlock_Gold_ROI':total_unlock_Gold_ROI,
        'total_lock_Gold_ROI':total_lock_Gold_ROI,
        'total_Savings_Gold_ROI':total_Savings_Gold_ROI,

        'total_unlock_Diamond_ROI':total_unlock_Diamond_ROI,
        'total_lock_Diamond_ROI':total_lock_Diamond_ROI,
        'total_Savings_Diamond_ROI':total_Savings_Diamond_ROI,

        "pack":pack,

        "total_amount_deposited":total_amount_deposited,
        
        "investment_prog_details":investment_prog_details,

        "users_detail":users_detail,

        "Supreme_plus_Unlocked_plan_stats":Supreme_plus_Unlocked_plan_stats,
        "Supreme_plus_Locked_plan_stats":Supreme_plus_Locked_plan_stats,
        # "Supreme_plus_Savings_stats":Supreme_plus_Savings_stats,

        "total_Supreme_plus_Unlocked_depo":total_Supreme_plus_Unlocked_depo,
        "total_Supreme_plus_Locked_depo":total_Supreme_plus_Locked_depo,
        "total_Supreme_plus_Savings_depo":total_Supreme_plus_Savings_depo,

        "summed_Supreme_plus_Unlocked":summed_Supreme_plus_Unlocked,
        "summed_Supreme_plus_Unlocked":summed_Supreme_plus_Unlocked,
        "summed_Supreme_plus_Savings":summed_Supreme_plus_Savings,
        
        "basic_count" :basic_count,
        "standard_count":standard_count,
        "premium_count":premium_count,
        "bronze_count":bronze_count,
        "super_bronze_count":super_bronze_count,
        "silver_count":silver_count,
        "super_silver_count":super_silver_count,
        "Gold_count":Gold_count,

        # Count of Supreme_plus_Unlocked plan
        "basic_Supreme_plus_Unlocked_count":basic_Supreme_plus_Unlocked_count,
        "standard_Supreme_plus_Unlocked_count":standard_Supreme_plus_Unlocked_count,
        "premium_Supreme_plus_Unlocked_count":premium_Supreme_plus_Unlocked_count,
        "bronze_Supreme_plus_Unlocked_count":bronze_Supreme_plus_Unlocked_count,
        "super_bronze_Supreme_plus_Unlocked_count":super_bronze_Supreme_plus_Unlocked_count,
        "silver_Supreme_plus_Unlocked_count":silver_Supreme_plus_Unlocked_count,
        "super_silver_Supreme_plus_Unlocked_count":super_silver_Supreme_plus_Unlocked_count,
        "Gold_Supreme_plus_Unlocked_count":Gold_Supreme_plus_Unlocked_count,
        "diamond_Supreme_plus_Unlocked_count":diamond_Supreme_plus_Unlocked_count,

        # Count of Supreme_plus_Locked plan
        "basic_Supreme_plus_Locked_count":basic_Supreme_plus_Locked_count,
        "standard_Supreme_plus_Locked_count":standard_Supreme_plus_Locked_count,
        "premium_Supreme_plus_Locked_count":premium_Supreme_plus_Locked_count,
        "bronze_Supreme_plus_Locked_count":bronze_Supreme_plus_Locked_count,
        "super_bronze_Supreme_plus_Locked_count":super_bronze_Supreme_plus_Locked_count,
        "silver_Supreme_plus_Locked_count":silver_Supreme_plus_Locked_count,
        "super_silver_Supreme_plus_Locked_count":super_silver_Supreme_plus_Locked_count,
        "Gold_Supreme_plus_Locked_count":Gold_Supreme_plus_Locked_count,
        "diamond_Supreme_plus_Locked_count":diamond_Supreme_plus_Locked_count,
        
        # Count of Supreme_plus_Savings plan
        "basic_Supreme_plus_Savings_count":basic_Supreme_plus_Savings_count,
        "standard_Supreme_plus_Savings_count":standard_Supreme_plus_Savings_count,
        "premium_Supreme_plus_Savings_count":premium_Supreme_plus_Savings_count,
        "bronze_Supreme_plus_Savings_count":bronze_Supreme_plus_Savings_count,
        "super_bronze_Supreme_plus_Savings_count":super_bronze_Supreme_plus_Savings_count,
        "silver_Supreme_plus_Savings_count":silver_Supreme_plus_Savings_count,
        "super_silver_Supreme_plus_Savings_count":super_silver_Supreme_plus_Savings_count,
        "Gold_Supreme_plus_Savings_count":Gold_Supreme_plus_Savings_count,
        "diamond_Supreme_plus_Savings_count":diamond_Supreme_plus_Savings_count,

    }
    return render(request, 'gentannie_stats/gentannie_stats.html', context)

def user_stats(request):
    users_stats = users_details.objects.all().order_by('-username')

    context = {
        "users_stats":users_stats,
    }
    return render(request, 'gentannie_stats/user_stats.html',context)

def marketing_stats(request):

    # marketer's summary
    mark_001_details = Gem001_client.objects.all()
    mark_001_summed_total = 0
    for market_sum in mark_001_details.iterator():
        gotted_val = market_sum.amount
        mark_001_summed_total = int(gotted_val) + mark_001_summed_total

    mark001_percent_earned = mark_001_summed_total * 0.05
    # client_count = mark_001_details.filter('client').count()

    mark_002_details = Gem002_client.objects.all()
    mark_002_summed_total = 0
    for market_sum in mark_002_details.iterator():
        gotted_val = market_sum.amount
        mark_002_summed_total = int(gotted_val) + mark_002_summed_total

    mark002_percent_earned = mark_002_summed_total * 0.05
    # client_count = mark_00_details.count()

    mark_003_summed_total = 0
    mark_003_details = Gem003_client.objects.all()
    for market_sum in mark_003_details.iterator():
        gotted_val = market_sum.amount
        mark_003_summed_total = int(gotted_val) + mark_003_summed_total

    mark003_percent_earned = mark_003_summed_total * 0.05
    # client_count = mark_00_details.count()

    mark_004_details = Gem004_client.objects.all()
    mark_004_summed_total = 0
    for market_sum in mark_004_details.iterator():
        gotted_val = market_sum.amount
        mark_004_summed_total = int(gotted_val) + mark_004_summed_total

    mark004_percent_earned = mark_004_summed_total * 0.05
    # client_count = mark_00_details.count()

    mark_005_summed_total = 0
    mark_005_details = Gem005_client.objects.all()
    for market_sum in mark_005_details.iterator():
        gotted_val = market_sum.amount
        mark_005_summed_total = int(gotted_val) + mark_005_summed_total

    mark005_percent_earned = mark_005_summed_total * 0.05
    # client_count = mark_00_details.count()

    mark_006_summed_total = 0
    mark_006_details = Gem006_client.objects.all()
    for market_sum in mark_006_details.iterator():
        gotted_val = market_sum.amount
        mark_006_summed_total = int(gotted_val) + mark_006_summed_total

    mark006_percent_earned = mark_006_summed_total * 0.05
    # client_count = mark_00_details.count()

    context = {
        "mark_001_summed_total":mark_001_summed_total,
        "mark001_percent_earned":mark001_percent_earned,
        
        "mark_002_summed_total":mark_002_summed_total,
        "mark002percent_earned":mark002_percent_earned,

        "mark_003_summed_total":mark_003_summed_total,
        "mark003_percent_earned":mark003_percent_earned,

        "mark_004_summed_total":mark_004_summed_total,
        "mark004_percent_earned":mark004_percent_earned,

        "mark_005_summed_total":mark_005_summed_total,
        "mark005_percent_earned":mark005_percent_earned,

        "mark_006_summed_total":mark_006_summed_total,
        "mark006_percent_earned":mark006_percent_earned,

    }
    return render(request, 'gentannie_stats/marketing_stats.html',context)
