from django.conf.urls import patterns, url
from django.contrib.sitemaps import GenericSitemap
from articles.models import Article
from home import views
from django.contrib import sitemaps
from django.core.urlresolvers import reverse

class ViewSitemap(sitemaps.Sitemap):
	priority = 0.5
	changefreq = 'daily'
	def items(self):
		return Article.objects.all()

	def location(self,item):
		appName = item._meta.app_label
		slug = item.slug 
		mainUrl = appName+':articlePage'
		return reverse(mainUrl, args=[slug])

sitemaps = {
    'news': ViewSitemap,
}

urlpatterns = patterns('',
        url(r'^$',views.HomePageView.as_view(), name='index'),
	url(r'^terms/$', views.TermsPageView.as_view(), name='terms'),
        url(r'^privacy/$', views.PrivacyPageView.as_view(), name='privacy'),
        url(r'^policies/$', views.PoliciesPageView.as_view(), name='policies'),
        url(r'^aboutus/$', views.AboutusPageView.as_view(), name='aboutus'),
        url(r'^contactus/$', views.ContactusPageView.as_view(), name='contactus'),
	url(r'^helpcenter/$', views.HelpcenterPageView.as_view(), name='helpcenter'),
	url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
)

