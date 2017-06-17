from django.contrib import admin
from categories.models import Category
from articles.models import Article, Article_Suggested_Article,Article_Category, Article_Suggested_Consultation
from django import forms
from django.utils.html import format_html
from django.core.urlresolvers import reverse

class Article_Form(forms.ModelForm):
        class Meta:
                model = Article
                fields = ['article_description', 'article_meta_description', 'article_content']
                widgets = {
                        'article_description': forms.Textarea(attrs={'cols':70,'rows':5}),
                        'article_meta_description': forms.Textarea(attrs={'cols':70,'rows':5}),
                        'article_content': forms.Textarea(attrs={'cols':100,'rows':30}),
                }
class Article_Category_Form(forms.ModelForm):
	
	def clean_article_category_order(self):
		data = self.cleaned_data['article_category_order']
		return 1

class Article_Category_Inline(admin.StackedInline):
        model = Article_Category
        extra = 1
	max_num = 4
        fk_name = "article"

class Article_Suggested_Article_Inline(admin.StackedInline):
        model = Article_Suggested_Article
        extra = 1
        fk_name = "article"
class Article_Suggested_Consultation_Inline(admin.StackedInline):
        model = Article_Suggested_Consultation
        extra = 1
        fk_name = "article"
class ArticleAdmin(admin.ModelAdmin):
        fieldsets = [
                ('Article Introduction', {'fields': ['article_title', 'article_author', 'article_description', 'article_meta_description','article_keywords', 'slug'], 'classes': ['wide']}),
                ('Article Body', {'fields': ['article_content']}),
                ('Article Sources and References',{'fields': ['article_sources_references']}),
                ('Article Pictures',{'fields': ['article_small_picture_url','article_medium_picture_url','article_large_picture_url']}),
                ('Article Configuration',{'fields': ['article_pubdate', 'article_status', 's_article', 's_consultation', 's_ads', 'article_hits']}),
	]
        inlines = [Article_Category_Inline, Article_Suggested_Article_Inline,Article_Suggested_Consultation_Inline]
	form = Article_Form
        list_filter = ['article_pubdate','article_status']

	def article_link(self, obj):
		return format_html("<a href='{0}' target='_blank'>Click Here</a>", reverse('articles:articlePage', args=[obj.slug]))

        readonly_fields = ('article_hits',)
        list_display = ['article_title', 'article_hits','article_link', 'article_status']
        search_fields = ['article_title']

admin.site.register(Article,ArticleAdmin)

