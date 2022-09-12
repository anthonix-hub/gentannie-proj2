from django.db import models
from django.contrib.auth import get_user_model
from django.http import request
from .utils import generate_ref_code

User = get_user_model()

NONE = 'None'
payment_pending = 'payment_pending'
Payment_made = "Payment_made"
payment_rejected = "payment_rejected"
bonu_status = [(NONE,'NONE'),(payment_pending,'payment_pending'), (Payment_made,'Payment_made') ,(payment_rejected,'payment_rejected')]

class user_referal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='ref_by')
    created = models.DateTimeField(auto_now_add=True)
    code = models.CharField (max_length=12, blank=True)
    date_refered = models.DateTimeField(auto_now_add=True)
    numbers_refered = models.IntegerField(null=True, blank=True, default=0)
    Referal_bonus = models.IntegerField(null=True, blank=True, default=0)
    request_bonus = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, default=NONE, choices=bonu_status)
    requested_bonus = models.IntegerField(null=True, blank=True, default=0)
    total_withdrawed_bonus = models.IntegerField(null=True, blank=True, default=0)

 
    def __str__(self):
        return  str(self.user) + str(self.code) + str(self.request_bonus)

    def recommend_tree(self):
        prof_items = user_referal.objects.get(self.recommended_by)

    def get_recommended_profiles(self):
        qs = user_referal.objects.all()
        # my_recomms = [p for p in qs if p.recommended_by == self.user] #shorter version of code below
        my_recomms = []
        for recom_prof in qs:
            if recom_prof.recommended_by == self.user:
                my_recomms.append(recom_prof)
        return my_recomms

    def save (self, *args, **kwargs):
        if self.code == '':
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)
