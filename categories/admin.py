from django.contrib import admin
from categories.models import Category

class CategoryAdmin(admin.ModelAdmin):
        fieldsets = [
                ('Category Information', {'fields': ['category_name', 'category_description', 'category_style', 'slug', 'category_hits'], 'classes': ['wide']}),
        ]
	list_display = ['category_name', 'category_style','category_hits']
        readonly_fields = ('category_hits',)
        search_fields = ['category_name']

admin.site.register(Category,CategoryAdmin)
