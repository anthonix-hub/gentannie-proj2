from django.contrib import admin
from .models import *


class user_referalAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommended_by', 'created', 'code', 'date_refered', 'Referal_bonus', 'numbers_refered', 'request_bonus', 'requested_bonus' , 'total_withdrawed_bonus' ,'payment_status')


admin.site.register(user_referal, user_referalAdmin)