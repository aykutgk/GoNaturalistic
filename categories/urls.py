from django.conf.urls import patterns, url
from categories import views

urlpatterns = patterns('',
        # /categories/
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^(?P<slug>[-_\w]+)/$', views.CategoryPageView.as_view(), name='categoryPage'),
)
