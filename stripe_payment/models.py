from django.db import models
from django.contrib.auth.models import User

#Stripe###########################
class Stripe_Error(models.Model):
        user = models.ForeignKey(User, verbose_name="User", blank=True, null=True,on_delete=models.SET_NULL)
        date = models.DateTimeField("Error Date and Time", auto_now_add=True)
        json_data = models.TextField("Json Data",blank=True)
        status = models.CharField("Http Status",max_length=255,blank=True)
        type = models.CharField("Error type",max_length=255,blank=True)
        code = models.CharField("Error code",max_length=255,blank=True)
        param = models.CharField("Error param",max_length=255,blank=True)
        message = models.CharField("Error message",max_length=255,blank=True)

        class Meta:
                ordering = ('-date',)
                verbose_name = "Stripe Error"

        def __unicode__(self):
                return str(self.date)
