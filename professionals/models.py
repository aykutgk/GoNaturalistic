from django.db import models
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User
import datetime

#Professional Model##############
class Professional(models.Model):
        TYPE_CHOICES = (
                ('a', 'Author'),
                ('p', 'Professional'),
                ('ap', 'Author and Professional'),
        )
        professional_type = models.CharField("Type",max_length=2,choices=TYPE_CHOICES,default="a",help_text="Author, Practitioner, Company.")
        professional_full_name = models.CharField(max_length=100, verbose_name="Full Name",help_text="Allison R. Ramsey")
        SEX_CHOICES = (
                ('f', 'Female'),
                ('m', 'Male'),
        )
	professional_sex = models.CharField("Sex",max_length=1,choices=SEX_CHOICES,default="f") 
        professional_email = models.EmailField("Main E-Mail")
        professional_gn_email = models.EmailField("Gonaturalistic E-Mail")
        professional_address = models.CharField("Address", max_length=120,blank=True)
        professional_phone = models.CharField("Phone Number", max_length=16,blank=True)
        T_Z_CHOICES = (
                ('pst', 'Pacific Time Zone (UTC-08:00)'),
                ('mst', 'Mountain Time Zone (UTC-07:00)'),
                ('cst', 'Central Time Zone (UTC-06:00)'),
                ('est', 'Eastern Time Zone (UTC-05:00)'),
                ('cest', 'Central European Time Zone (UTC+01:00)'),
                ('gmtz', 'Greenwich Mean Time Zone (UTC+00:00)'),
                ('eest', 'Eastern European Time Zone (UTC+02:00)'),
        )
        professional_time_zone = models.CharField("Time Zone",max_length=4,choices=T_Z_CHOICES,default="ctz")
        professional_member_date = models.DateField("Professional Member Date",auto_now_add=True)
        slug = models.SlugField("Url",max_length=100,help_text="Allison-Ramsey",unique=True)
        #Professional Main Page
        professional_main_page_description = models.TextField("Professional Page Description")
        professional_main_page_meta_description = models.TextField("Professional Page Meta Description")
        professional_main_page_content = models.TextField("Professional Page Content", help_text="HTML Content.")
        #Professional Consultation Page and Pruchase Email
        professional_consultation_page_content = models.TextField("Consultation Page Content",blank=True, help_text="HTML Content.")
	professional_consultation_purchase_email_message = models.TextField("Consultation Purchase Email Message",blank=True, help_text="HTML Content.")
	professional_consultation_purchase_email_subject = models.CharField("Consultation Purchase Email Subject", max_length=100,blank=True)
	professional_consultation_purchase_email_from = models.EmailField("Consultation Purchase Email sent From?",blank=True)
        #Professional Pictures
        professional_small_picture_url =  models.CharField("Small Picture Url",max_length=50,help_text="allison_small.jpg",default="default1_pro_small.jpeg")
        professional_medium_picture_url =  models.CharField("Medium Picture Url",max_length=50,help_text="allison_medium.jpg",blank=True,default="default1_pro_medium.jpeg")
        professional_large_picture_url =  models.CharField("Large (For Slide) Picture Url",max_length=50,help_text="allison_large.jpg",blank=True,default="default1_pro_large.jpeg")
        professional_hits = models.PositiveIntegerField("Hits",default=0)
        SG_CHOICES = (
                ('y', 'Yes'),
                ('n', 'No'),
        )
        s_article = models.CharField("is Suggested Article Allowed?",max_length=1,choices=SG_CHOICES,default="n")
        s_consultation = models.CharField("is Suggested Consultation Allowed?",max_length=1,choices=SG_CHOICES,default="n")
        s_ads = models.CharField("is Suggested Ads by Google Allowed?",max_length=1,choices=SG_CHOICES,default="n")
        STATUS_CHOICES = (
                ('e', 'Enable'),
                ('d', 'Disable'),
        )
	#Professional Prices
        hour_price = models.DecimalField("Hour Price",max_digits=6,decimal_places=2,default=0)
        half_hour_price = models.DecimalField("Half Hour Price",max_digits=6,decimal_places=2,default=0)
        quarter_hour_price = models.DecimalField("Quarter Hour Price",max_digits=6,decimal_places=2,default=0)

	professional_status = models.CharField("Professional Status?",max_length=1,choices=STATUS_CHOICES,default="d")
        consultation_service_status = models.CharField("consultation service status?",max_length=1,choices=STATUS_CHOICES,default="d")

        def hit(self):
                self.professional_hits = self.professional_hits + 1
                self.save()

        def __unicode__(self):
                return self.professional_full_name

##################################################

#Consultation Method####################
class Consultation_Method(models.Model):
        METHOD_CHOICES = (
                ('s', 'Skype'),
                ('ft', 'FaceTime'),
                ('ph', 'Phone Call'),
                ('o', 'Face to Face'),
        )
        professional = models.ForeignKey(Professional)
        consultation_method_name = models.CharField("Method",max_length=2,choices=METHOD_CHOICES,default="s")
	consultation_method_description = models.CharField("Description", max_length=200,blank=True)
        consultation_method_username = models.CharField("Username", max_length=30,blank=True)
        consultation_method_email = models.EmailField("E-Mail",blank=True)
        consultation_method_target_link = models.URLField("Target Link",blank=True)
        consultation_method_phone_number = models.CharField("Mobile Phone Number", max_length=16,blank=True)
        consultation_method_address = models.CharField("Address", max_length=120,blank=True)
        consultation_method_order = models.PositiveSmallIntegerField("Order?",default=1)
        S_CHOICES = (
                ('y', 'Yes'),
                ('n', 'No'),
        )
        consultation_method_status = models.CharField("is this method enabled?",max_length=1,choices=S_CHOICES,default="n")
        consultation_method_hour_allowed = models.CharField("can this method give one hour consultation?",max_length=1,choices=S_CHOICES,default="n")
        consultation_method_half_hour_allowed = models.CharField("can this method give half hour consultation?",max_length=1,choices=S_CHOICES,default="n")
        consultation_method_quarter_hour_allowed = models.CharField("can this method give quarter hour consultation?",max_length=1,choices=S_CHOICES,default="n")

        class Meta:
                ordering = ('consultation_method_order',)
                verbose_name = "Consultation Method"

        def __unicode__(self):
                return self.consultation_method_name
#################################################### 

#Consultation Available Time####################
class Professional_Available_Time(models.Model):

        T_P_CHOICES = (
                ('h', '60 Mins'),
                ('hh', '30 Mins'),
                ('qh', '15 Mins'),
        )
        professional = models.ForeignKey(Professional)
        consultation_duration = models.CharField("Duration",max_length=2,choices=T_P_CHOICES,default="h")
        consultation_start_time = models.CharField("Start Time",max_length=8,help_text="1:00 PM, 2:30 PM, 3:15 PM")
        consultation_end_time = models.CharField("End Time",max_length=8,blank=True)
        consultation_time_period = models.CharField("Time Period",max_length=20)
        consultation_24hour_start_time = models.TimeField("24 Hour Format Start Time")
        consultation_24hour_end_time = models.TimeField("24 Hour Format End Time")
        def clean(self):
                type = self.consultation_duration
                #validate start time field
                if type == "h":
                        match = re.search(r'^([1-9]|10|11|12):00 (AM|PM)$',self.consultation_start_time)
                elif type == "hh":
                        match = re.search(r'^([1-9]|10|11|12):(00|30) (AM|PM)$',self.consultation_start_time)
                elif type == "qh":
                        match = re.search(r'^([1-9]|10|11|12):(00|15|30|45) (AM|PM)$',self.consultation_start_time)
                if not match:
                        raise ValidationError('Start Time Format is Wrong.')
                #Automatic Value for Time Period and Time And, this is made after validation of field
                splited_str = self.consultation_start_time.split(':')
                hour = int(splited_str[0])
                splited_str = splited_str[1].split(' ')
                minute = splited_str[0]
                period = splited_str[1]

                if type == "h":
                        if hour > 0 and hour < 11:
                                hour+=1
                        elif hour == 11:
                                hour+=1
                                if period == "AM":
                                        period = "PM"
                                elif period == "PM":
                                        period = "AM"
                        elif hour == 12:
                                hour = 1
                elif type == "hh":
                        if hour > 0 and hour < 11:
                                if minute == "00":
                                        minute = "30"
                                elif minute == "30":
                                        minute = "00"
                                        hour+=1
                        elif hour == 11:
                                if minute == "00":
                                        minute = "30"
                                elif minute == "30":
                                        hour+=1
                                        minute = "00"
                                        if period == "AM":
                                                period = "PM"
                                        elif period == "PM":
                                                period = "AM"
                        elif hour == 12:
                                if minute == "00":
                                        minute = "30"
                                elif minute == "30":
                                        hour = 1
                                        minute = "00"
                elif type == "qh":
                        if hour > 0 and hour < 11:
                                if minute == "00":
                                        minute = "15"
                                elif minute == "15":
                                        minute = "30"
                                elif minute == "30":
                                        minute = "45"
                                elif minute == "45":
                                        hour+=1
                                        minute = "00"
                        elif hour == 11:
                                if minute == "00":
                                        minute = "15"
                                elif minute == "15":
                                        minute = "30"
                                elif minute == "30":
                                        minute = "45"
                                elif minute == "45":
					hour+=1
                                        minute = "00"
                                        if period == "AM":
                                                period = "PM"
                                        elif period == "PM":
                                                period = "AM"
                        elif hour == 12:
                                if minute == "00":
                                        minute = "15"
                                elif minute == "15":
                                        minute = "30"
                                elif minute == "30":
                                        minute = "45"
                                elif minute == "45":
                                        hour = 1
                                        minute = "00"

                self.consultation_end_time = str(hour)+":"+minute+" "+period
                self.consultation_time_period = self.consultation_start_time+" to "+self.consultation_end_time

        class Meta:
                ordering = ('consultation_duration','consultation_24hour_start_time')
                verbose_name = "Professional default available time"
                unique_together = ("professional", "consultation_start_time")

        def __unicode__(self):
                return self.consultation_time_period
####################################################

#Professional Available Day and Times########################
class Professional_Available_Day_Time(models.Model):
        professional = models.ForeignKey(Professional)
        professional_available_time = models.ManyToManyField(Professional_Available_Time, db_table="professional_available_day_time_m2m")
        available_day = models.DateField("Available Day")

        class Meta:
                ordering = ('available_day',)
                verbose_name = "Professional Available Date"
                unique_together = ("professional", "available_day")

	def __unicode__(self):
		return str(self.available_day)
##############################################

##Professional Promo Code#############
class Professional_Promo_Code(models.Model):

        professional = models.ForeignKey(Professional)
        promo_code = models.CharField("Promo Code",max_length=12)
        promo_code_percent = models.PositiveIntegerField("Promo Code Percentage")
        promo_code_start_date = models.DateField("Promo Code Start Date")
        promo_code_end_date = models.DateField("Promo Code End Date")

        class Meta:
                ordering = ('promo_code_start_date',)
                verbose_name = "Professional Promo Code"
                unique_together = (("professional", "promo_code"),("professional", "promo_code_percent"))

        def clean(self):
                today = datetime.datetime.today().date()

                if self.promo_code_start_date > self.promo_code_end_date:
                        raise ValidationError("Promotion Code End Date Cannot be less than Start Date")

        def __unicode__(self):
                return self.promo_code_percent
########################################

#Professional's Purchased Consultation by Users############
class Professional_Purchased_Consultation(models.Model):
        professional = models.ForeignKey(Professional, blank=True, null=True,on_delete=models.SET_NULL)
        user = models.ForeignKey(User, blank=True, null=True,on_delete=models.SET_NULL)
	stripe_charge = models.CharField("Stripe Charge",max_length=50)
        consultation = models.ForeignKey("consultations.Consultation", blank=True, null=True,on_delete=models.SET_NULL)
        consultation_method = models.ForeignKey(Consultation_Method, blank=True, null=True,on_delete=models.SET_NULL)
        consultation_day = models.ForeignKey(Professional_Available_Day_Time, blank=True, null=True,on_delete=models.SET_NULL)
        consultation_time = models.ForeignKey(Professional_Available_Time, blank=True, null=True,on_delete=models.SET_NULL)
        STATUS_CHOICES = (
                ('s', 'sold'),
                ('h','hold'),
		('c','canceled'),
        )
        consultation_time_status = models.CharField("consultation time status",max_length=1,choices=STATUS_CHOICES,default='h')
        payment = models.DecimalField("Payment Amount",max_digits=6,decimal_places=2,default=0)
        date = models.DateTimeField("Payment Date", auto_now_add=True)
	refunded_payment = models.DecimalField("Pefunded Amount",max_digits=6,decimal_places=2,default=0)
	after_refunded_payment = models.DecimalField("After Refunded Payment",max_digits=6,decimal_places=2,default=0) 
        class Meta:
                ordering = ('-date',)
                verbose_name = "Professional's Purchased Consultation"
                unique_together = ("professional", "consultation_day", "consultation_time")

        def __unicode__(self):
                return self.professional.professional_full_name

#################################

#################################################
class Consultation_Order_Detail(models.Model):
        professional_purchased_consultation = models.OneToOneField(Professional_Purchased_Consultation, blank=True, null=True,on_delete=models.SET_NULL)
        user_name = models.CharField("User Name",max_length=50, blank=True)
        professional_name = models.CharField("Professional Name",max_length=50, blank=True)
        consultation_name = models.CharField("Consultation Name",max_length=50, blank=True)
        METHOD_CHOICES = (
                ('s', 'Skype'),
                ('ft', 'FaceTime'),
                ('ph', 'Phone Call'),
                ('o', 'At Office'),
        )
        consultation_method_name = models.CharField("Consultation Method Name",max_length=2,choices=METHOD_CHOICES, blank=True)
        consultation_date = models.CharField("Consultation Date",max_length=30, blank=True)
        consultation_time_period = models.CharField("Consultation Time",max_length=30, blank=True)
        consultation_time_zone = models.CharField("TZ info",max_length=30, blank=True)
        D_CHOICES = (
                ('h', '60 Mins'),
                ('hh', '30 Mins'),
                ('qh', '15 Mins'),
        )
        consultation_duration = models.CharField("Duration",max_length=2,choices=D_CHOICES,default="h", blank=True)
        promo_code_discount = models.CharField("Promo Code Percent",max_length=30, blank=True)
        full_price = models.CharField("Full Price",max_length=30, blank=True)
        final_price = models.CharField("Final Price",max_length=30, blank=True)

