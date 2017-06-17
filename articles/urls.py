from django.conf.urls import patterns, url
from articles import views

urlpatterns = patterns('',
        # /articles/
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^(?P<slug>[-_\w]+)/$', views.ArticlePageView.as_view(), name='articlePage'),
)
