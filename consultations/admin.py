from django.contrib import admin
from categories.models import Category
from consultations.models import Consultation, Consultation_Category, Consultation_Suggested_Consultation, Consultation_Suggested_Article
from django import forms
from django.utils.html import format_html
from django.core.urlresolvers import reverse

#############################
class Consultation_Form(forms.ModelForm):
        class Meta:
                model = Consultation
		fields = ['consultation_description','consultation_meta_description']
                widgets = {
                        'consultation_description': forms.Textarea(attrs={'cols':70,'rows':5}),
                        'consultation_meta_description': forms.Textarea(attrs={'cols':70,'rows':5}),
			'consultation_content': forms.Textarea(attrs={'cols':100,'rows':30}),
                }		
###############################

########################################################
class Consultation_Category_Inline(admin.StackedInline):
        model = Consultation_Category
        extra = 1
        max_num = 4
        fk_name = "consultation"
################################

########################################################
class Consultation_Suggested_Consultation_Inline(admin.StackedInline):
        model = Consultation_Suggested_Consultation
        extra = 1
        fk_name = "consultation"
################################

########################################################
class Consultation_Suggested_Article_Inline(admin.StackedInline):
        model = Consultation_Suggested_Article
        extra = 1
        fk_name = "consultation"
################################

##########################################
class ConsultationAdmin(admin.ModelAdmin):
	fieldsets = [
		('Consultation Information', {'fields': ['consultation_title','consultation_professional','slug','consultation_description','consultation_meta_description','consultation_keywords'], 'classes': ['wide']}),
		('Consultation Body', {'fields': ['consultation_content',]}),
		('Consultation Pictures', {'fields': ['consultation_small_picture_url','consultation_medium_picture_url','consultation_large_picture_url'], 'classes': ['wide']}),
		('Consultation Configuration', {'fields': ['consultation_status','s_article','s_consultation','s_ads','consultation_pubdate','consultation_hits'], 'classes': ['wide']})
	]
	form = Consultation_Form
	readonly_fields = ('consultation_hits',)
        search_fields = ['consultation_title']
        save_on_top = True
        def consultation_link(self, obj):
                return format_html("<a href='{0}' target='_blank'>Click Here</a>", reverse('consultations:consultationPage', args=[obj.slug]))
	list_filter = ['consultation_pubdate','consultation_status']
	list_display = ['consultation_title','consultation_hits', 'consultation_link', 'consultation_status']
	inlines = [Consultation_Category_Inline,Consultation_Suggested_Consultation_Inline,Consultation_Suggested_Article_Inline]

#################################################


##############################################################
admin.site.register(Consultation, ConsultationAdmin)

