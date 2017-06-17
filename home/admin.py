from django.contrib import admin
from home.models import Gonaturalistic, Activity, Slides, Popular_Articles, Popular_Consultations
from articles.models import Article
from consultations.models import Consultation
class GonaturalisticAdmin(admin.ModelAdmin):
	fieldsets = [
		('Gonaturalistic General Info', {'fields': ['title','description','email','phone','address', 'logo_icon','logo_small_url','logo_medium_url','logo_large_url','page_status','hits'], 'classes': ['wide']}),
		('Gonaturalistic Meta Info', {'fields': ['meta_title','meta_description','meta_keywords'],'classes': ['wide',]}),
		('Footer Info',{'fields': ['terms','privacy_policy','policies', 'help_center','about_us','contact_us_member_to','contact_us_guest_to','contact_us_content'], 'classes': ['wide',]}),
 		('Home Page Popup', {'fields': ['home_page_popup_title','home_page_popup_content','home_page_popup_footer','home_page_popup_status'],'classes': ['wide',]}),
	]
	readonly_fields = ('hits',)
class ActivityAdmin(admin.ModelAdmin):
        fieldsets = [
                ('GoNaturalistic Activity Emails', {'fields': ['activity_email','activity_registration','activity_purchase','activity_cancel_purchase'],'classes': ['wide',]}),
                ('Gonaturalistic Registration Email', {'fields': ['registration_email_subject','registration_email_from','registration_email_message'],'classes': ['wide',]}),
                ('Gonaturalistic Purchase Email', {'fields': ['consultation_purchase_email_subject','consultation_purchase_email_from','consultation_purchase_email_message_to_user','consultation_purchase_email_message_to_professional'],'classes': ['wide',]}),
                ('Gonaturalistic Change Consultation Method Email', {'fields': ['consultation_change_method_email_subject','consultation_change_method_from','consultation_change_method_email_message_to_user','consultation_change_method_email_message_to_professional'],'classes': ['wide',]}),
                ('Gonaturalistic Cancel Consultation Email', {'fields': ['consultation_cancel_purchase_email_subject','consultation_cancel_purchase_from','consultation_cancel_purchase_email_message_to_user','consultation_cancel_purchase_email_message_to_professional'],'classes': ['wide',]}),
        ]

class Popular_Consultations_Admin(admin.ModelAdmin):

        def formfield_for_foreignkey(self, db_field, request, **kwargs):
                kwargs["queryset"] = Consultation.objects.filter(consultation_status="p")
                return super(Popular_Consultations_Admin, self).formfield_for_foreignkey(db_field, request, **kwargs)
 
        def consultation_status(self,obj):
                return obj.consultation.consultation_status

	list_display = ['consultation','consultation_order','consultation_status']

class Popular_Articles_Admin(admin.ModelAdmin):

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
            	kwargs["queryset"] = Article.objects.filter(article_status="p")
        	return super(Popular_Articles_Admin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def article_status(self,obj):
		return obj.article.article_status
	list_display = ['article', 'article_order','article_status']

class SlidesAdmin(admin.ModelAdmin):
	list_display = ['order','article', 'consultation','custom_title']

admin.site.register(Gonaturalistic,GonaturalisticAdmin)
admin.site.register(Activity,ActivityAdmin)
admin.site.register(Slides, SlidesAdmin)
admin.site.register(Popular_Articles,Popular_Articles_Admin)
admin.site.register(Popular_Consultations,Popular_Consultations_Admin)
