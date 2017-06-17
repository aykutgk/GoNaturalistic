from django.db import models

class Gonaturalistic(models.Model):
	#Genaral##############
	title = models.CharField("Title", max_length=100)
	description = models.TextField("Description")
	email = models.EmailField("Main Email")
	phone = models.CharField("Phone Number", max_length=16,blank=True)
	address = models.CharField("Address", max_length=120,blank=True)
	logo_icon = models.URLField("Logo Icon URL",blank=True)
	logo_small_url = models.URLField("Logo Small URL",blank=True)
	logo_medium_url = models.URLField("Logo Medium URL",blank=True)
	logo_large_url = models.URLField("Logo Large URL",blank=True)
	hits = models.PositiveIntegerField("Hits",default=0)

	#Meta####################
	meta_title = models.CharField("Meta Title", max_length=100)
	meta_description = models.TextField(" Meta Description")
	meta_keywords = models.CharField("Meta Keywords",max_length=100,blank=True)

	#Footer################
	terms = models.TextField("Terms",help_text="HTML")
	privacy_policy = models.TextField("Privacy Policy",help_text="HTML")
	policies = models.TextField("Gonaturalistic Policies",help_text="HTML")
	about_us = models.TextField("About Us",help_text="HTML")
	contact_us_member_to = models.EmailField("Contact Us Member Email goes to")
        contact_us_guest_to = models.EmailField("Contact Us Guest Email goes to")
	contact_us_content = models.TextField("Contact Us Content",help_text="HTML")
	help_center = models.TextField("Help Center",help_text="HTML")

	#Social Media Urls##############
	facebook_url = models.URLField("Facebook URL",blank=True)
	google_plus = models.URLField("Google Plus URL",blank=True)
	twitter = models.URLField("Twitter URL",blank=True)
	linkedin = models.URLField("Linkedin URL",blank=True)
	pinterest = models.URLField("Pinterest URL",blank=True)
	youtube = models.URLField("Youtube URL",blank=True)
	vimeo = models.URLField("Vimeo URL",blank=True)
	blogger = models.URLField("Blogger URL",blank=True)
	reddit = models.URLField("Reddit URL",blank=True)
	digg = models.URLField("Digg URL",blank=True)
	tumblr = models.URLField("Tumblr URL",blank=True)
	live_journal = models.URLField("Live Journal URL",blank=True) 
	stumble_upon = models.URLField("StumbleUpon URL",blank=True)
	######################################

	#Home Page Popup
	home_page_popup_title = models.CharField("Title", max_length=100,blank=True)
        home_page_popup_content =models.TextField("Home Page Popup Content", help_text="Home Page Popup HTML Content.",blank=True)
        home_page_popup_footer = models.TextField("Home Page Popup Footer", help_text="Home Page Popup HTML Content.",blank=True)  
        STATUS_CHOICES = (
                ('e', 'Enable'),
                ('d', 'Disable'),
        )
	home_page_popup_status = models.CharField("Popup Status?",max_length=1,choices=STATUS_CHOICES,default="d")
	#Whole Page Status for under construction
	page_status = models.CharField("Page Status?",max_length=1,choices=STATUS_CHOICES,default="d")

        def hit(self):
                self.hits = self.hits + 1
                self.save()

	class Meta:
		verbose_name = "GoNaturalistic Settings and Content"

        def __unicode__(self):
                return self.title

class Activity(models.Model):
        #Activity Emails Goes to GoNaturalistic
        activity_email = models.EmailField("Activity Email Sent to?")
        activity_registration = models.TextField("Activity Registration Email Message",help_text="HTML")
        activity_purchase = models.TextField("Activity Purchase Email Message",help_text="HTML")
        activity_cancel_purchase = models.TextField("Activity Cancel Purchase Email Message",help_text="HTML")

        #Registration Email########################
        registration_email_subject = models.CharField("Registration Email Subject", max_length=100)
        registration_email_from = models.EmailField("Email sent From?")
        registration_email_message = models.TextField("Registration Email Message",help_text="HTML")

        #Consultation Purchase Email########################
        consultation_purchase_email_subject = models.CharField("Consultation Purchase Email Subject", max_length=100)
        consultation_purchase_email_from = models.EmailField("Consultation Purchase Email sent From?")
        consultation_purchase_email_message_to_user = models.TextField("Consultation Purchase Email Message To User",help_text="HTML")
        consultation_purchase_email_message_to_professional = models.TextField("Consultation Purchase Email Message To Professional",help_text="HTML")

	#Consultation Cancel Email
        consultation_cancel_purchase_email_subject = models.CharField("Consultation Cancel Purchase Email Subject", max_length=100)
        consultation_cancel_purchase_from = models.EmailField("Consultation Cancel Purchase sent From?")
        consultation_cancel_purchase_email_message_to_user = models.TextField("Consultation Cancel Purchase Email Message to User",help_text="HTML")
        consultation_cancel_purchase_email_message_to_professional = models.TextField("Consultation Cancel Purchase Email Message to Professional",help_text="HTML")

	#Consultation Change Method
	consultation_change_method_email_subject = models.CharField("Consultation Change Method Email Subject", max_length=100)
        consultation_change_method_from = models.EmailField("Consultation Change Method Email sent From?")	
        consultation_change_method_email_message_to_user = models.TextField("Consultation Change Method Email Message to User",help_text="HTML")
        consultation_change_method_email_message_to_professional = models.TextField("Consultation Change Method Email Message to Professional",help_text="HTML")

        class Meta:
                verbose_name = "GoNaturalistic Activities' Email"

	def __unicode__(self):
                return self.activity_email

class Slides(models.Model):
        T_CHOICES = (
                ('a', 'Article'),
                ('c', 'Consultation'),
		('m', 'Custom'),
        )
	type = models.CharField("is Selecyed Article or Consultation?",max_length=1,choices=T_CHOICES,default="a")
        article = models.ForeignKey('articles.Article', verbose_name="Popular Article",blank=True,null=True)
        C_CHOICES = (
                ('e', 'Everybody'),
                ('m', 'Members'),
                ('g', 'Guests'),
        )
        consultation = models.ForeignKey('consultations.Consultation', verbose_name="Popular Consultation",blank=True,null=True)
	custom_only_for = models.CharField("Who can see this custom slide?",max_length=1,choices=C_CHOICES,default="e",blank=True)
	custom_large_picture_url = models.CharField("Custom Slide Picture Url",max_length=50,help_text="a_large.jpg",blank=True)
	custom_title = models.CharField("Custom Title", max_length=50,blank=True)
	custom_description = models.CharField("Custom Description", max_length=200,blank=True)
	custom_url = models.CharField("Url",max_length=50,blank=True,help_text="/user/signup/")
	custom_button_content = models.TextField("Custom Button Html Content",blank=True)
	order = models.IntegerField(verbose_name="Slide Order")	
        class Meta:
                ordering = ["order",]
		verbose_name = "Slide"

class Popular_Articles(models.Model):
        article = models.ForeignKey('articles.Article', verbose_name="Popular Article")
        article_order = models.IntegerField(verbose_name="Popular Article Order")

    	class Meta:
        	ordering = ["article_order",]
		verbose_name = "Popular Article"


class Popular_Consultations(models.Model):
	consultation = models.ForeignKey('consultations.Consultation', verbose_name="Popular Consultation")
	consultation_order = models.IntegerField(verbose_name="Popular Consultation Order")
        class Meta:
                ordering = ["consultation_order",]
		verbose_name = "Popular Consultation"
