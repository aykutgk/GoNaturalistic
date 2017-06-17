from django.db import models
from django.contrib.auth.models import User
import urllib2
from decimal import Decimal
from users.geoData import COUNTRIES

#User's Account##################
class User_Account(models.Model):

	user = models.ForeignKey(User, verbose_name="User Model")
	user_full_name = models.CharField("User Full Name", max_length=50)
	user_address = models.CharField("Address", max_length=100,blank=True)
	user_city = models.CharField("City", max_length=20,blank=True)
	COUNTRY_CHOICES = (('US', 'United States'), ('CA', 'Canada'))
	user_country = models.CharField("State", max_length=3,choices=COUNTRIES,default='US',blank=True)
	STATE_CHOICES = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))
	user_state = models.CharField("State", max_length=2,choices=STATE_CHOICES,blank=True)
	user_zipcode = models.CharField("Zip Code", max_length=5,blank=True)
	user_phone = models.CharField("Phone Number", max_length=16,blank=True)
	user_registration_date = models.DateField("Registration Date",auto_now_add=True)
        TYPE_CHOICES = (
                ('s', 'Staff'),
                ('m', 'Member'),
        )
        user_type = models.CharField("Type",max_length=1,choices=TYPE_CHOICES,default="m",help_text="Staff, Member")
        STATUS_CHOICES = (
                ('e', 'Enable'),
                ('d', 'Disable'),
        )
	user_status = models.CharField("User Status?",max_length=1,choices=STATUS_CHOICES,default="e") 

        class Meta:
                verbose_name = "User's Account"

        def __unicode__(self):
                return self.user.email
###############################################

#User's Consultation Wish List#################
class User_Consultation_Wishlist(models.Model):
        user = models.ForeignKey(User, verbose_name="User Model")
	consultation = models.ForeignKey("consultations.Consultation", verbose_name="Consultation Model")
        wishlist_added_date = models.DateField("wishlist Date",auto_now_add=True)

        class Meta:
                verbose_name = "User's Consultation Wish List"
                unique_together = ("user", "consultation")
#########################################################################################################

#User's Consultation Orders#################
class User_Consultation_Purchase(models.Model):
        user = models.ForeignKey(User, verbose_name="User")
        STATUS_CHOICES = (
                ('u', 'upcoming'),
                ('s','completed'),
		('c','canceled'),
        )
        consultation_status = models.CharField("consultation time status",max_length=1,choices=STATUS_CHOICES,default='u')
	consultation_note = models.TextField("Consultation Notes by Professional")
	professional_purchased_consultation = models.OneToOneField("professionals.Professional_Purchased_Consultation", blank=True, null=True,on_delete=models.SET_NULL)
	consultation_order_detail = models.OneToOneField("professionals.Consultation_Order_Detail", blank=True, null=True,on_delete=models.SET_NULL)
        purchase_date = models.DateTimeField("Purchase Date",auto_now_add=True)
	order = models.IntegerField(verbose_name="Slide Order",default=1)
        class Meta:
                verbose_name = "User's Consultation Purchases"
##########################################


