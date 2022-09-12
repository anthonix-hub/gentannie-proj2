from gentannieProj.gentannieApp.views import Due_checker
from .models import *
from datetime import date, datetime, time,timedelta

def mail_check():
    dateDue = users_investment_progress.objects.all()
    # dateDue.get(Due_date)
    filtered_date = users_investment_progress.objects.filter(Due_date = str(datetime.now()))

    if filtered_date:
        print (filtered_date.user )