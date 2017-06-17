from django.contrib import admin
from professionals.models import Professional, Consultation_Method, Professional_Available_Time,Professional_Available_Day_Time, Professional_Promo_Code, Professional_Purchased_Consultation, Consultation_Order_Detail
from django import forms

#########################################
class Professional_Form(forms.ModelForm):
        class Meta:
                model = Professional
                fields = ['professional_main_page_meta_description', 'professional_main_page_content', 'professional_consultation_page_content',]
                widgets = {
                        'professional_main_page_meta_description': forms.Textarea(attrs={'cols':70,'rows':5}),
                        'professional_main_page_content': forms.Textarea(attrs={'cols':100,'rows':30}),
                        'professional_consultation_page_content': forms.Textarea(attrs={'cols':100,'rows':30}),
                }
#################
class Professional_Promo_Code_Inline(admin.TabularInline):
	model = Professional_Promo_Code
        extra = 1
        fk_name = "professional"
#################################################################
######################################################
class Consultation_Method_Inline(admin.StackedInline):
        model = Consultation_Method
        extra = 1
        fk_name = "professional"
################################

######################################################
class Professional_Available_Time_Inline(admin.TabularInline):
        model = Professional_Available_Time
        extra = 1
        fk_name = "professional"
	readonly_fields = ('consultation_end_time','consultation_time_period',)
################################################################################

######################################################
class Professional_Available_Day_Time_Inline(admin.StackedInline):
        model = Professional_Available_Day_Time
        extra = 1	
        filter_horizontal = ('professional_available_time',)
	fk_name = "professional"
        fieldsets = [
                (None, {'fields': ['available_day'], 'classes': ['wide',]}),
 		(None, {'fields': ['professional_available_time']}),
        ]
	def get_formset(self, request, obj=None, **kwargs):
        	self.parent_obj = obj
        	return super(Professional_Available_Day_Time_Inline, self).get_formset(request, obj, **kwargs)

    	def formfield_for_manytomany(self, db_field, request, **kwargs):
        	if db_field.name == "professional_available_time":
				kwargs["queryset"] = Professional_Available_Time.objects.filter(professional = self.parent_obj)
        	return super(Professional_Available_Day_Time_Inline, self).formfield_for_manytomany(db_field, request, **kwargs)
################################

#Professional Admin######################
class Professional_Admin(admin.ModelAdmin):
	fieldsets = [
                ('Professional Information', {'fields': ['professional_type', 'professional_full_name', 'professional_sex', 'professional_email', 'professional_gn_email', 'professional_address', 'professional_phone','professional_time_zone', 'slug', 'professional_status'], 'classes': ['wide']}),
		('Professional Consultation Prices', {'fields': ['hour_price','half_hour_price','quarter_hour_price'], 'classes': ['wide',]}),
                ('Professional Pictures', {'fields': ['professional_small_picture_url', 'professional_medium_picture_url', 'professional_large_picture_url'], 'classes': ['wide']}),
                ('Professional Main Page', {'fields': ['professional_main_page_description', 'professional_main_page_meta_description', 'professional_main_page_content']}),
                ('Professional Consultation', {'fields': ['professional_consultation_page_content','professional_consultation_purchase_email_message','professional_consultation_purchase_email_subject','professional_consultation_purchase_email_from'], 'classes': ['collapse',]}),
                ('Professional Configuration', {'fields': ['consultation_service_status', 's_article', 's_consultation', 's_ads', 'professional_hits'], 'classes': ['wide','collapse']}),
	]
	inlines = [Consultation_Method_Inline, Professional_Promo_Code_Inline,Professional_Available_Time_Inline,Professional_Available_Day_Time_Inline]
        form = Professional_Form
	readonly_fields = ('professional_hits',)
        search_fields = ['professional_full_name']
	save_on_top = True	
        def get_formsets(self, request, obj=None):
                for inline in self.get_inline_instances(request, obj):
                        # hide MyInline in the add view
                        if isinstance(inline, Professional_Available_Day_Time_Inline) and obj is None:
                                continue
                        if isinstance(inline, Professional_Available_Time_Inline) and obj is None:
                                continue
                        if isinstance(inline, Consultation_Method_Inline) and obj is None:
                                continue
                        if isinstance(inline, Professional_Promo_Code_Inline) and obj is None:
                                continue
                        yield inline.get_formset(request, obj)
##################################################

######################################################
class Consultation_Order_Detail_Inline(admin.StackedInline):
        model = Consultation_Order_Detail
################################

class Professional_Purchased_Consultation_Admin(admin.ModelAdmin):
        inlines = [Consultation_Order_Detail_Inline,]
	list_display = ['professional','date','payment']
#Admin Register###################################
admin.site.register(Professional,Professional_Admin)
admin.site.register(Professional_Purchased_Consultation, Professional_Purchased_Consultation_Admin)
###################################################

