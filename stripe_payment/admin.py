from django.contrib import admin
from stripe_payment.models import Stripe_Error

admin.site.register(Stripe_Error)
