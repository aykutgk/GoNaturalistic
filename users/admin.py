from django.contrib import admin
from django.core.urlresolvers import reverse
from users.models import User_Consultation_Purchase, User_Account
from django.utils.html import format_html

class User_Consultation_Purchase_Admin(admin.ModelAdmin):

	fields = ('user','consultation_status','consultation_note','order','p_link')
        readonly_fields = ('p_link',)
	def p_link(self,obj):
		return format_html("<a href='{0}' target='_blank'>Click Here</a>", reverse('admin:professionals_professional_purchased_consultation_change', args=[obj.professional_purchased_consultation.pk]))

	p_link.short_description = "Purchase Details"
	p_link.allow_tags = True
	list_display = ['user','consultation_status']
admin.site.register(User_Account)
admin.site.register(User_Consultation_Purchase,User_Consultation_Purchase_Admin)
