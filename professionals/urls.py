from django.conf.urls import patterns, url
from professionals import views

urlpatterns = patterns('',
        # /professionals/
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^(?P<slug>[-_\w]+)/$', views.ProfessionalPageView.as_view(), name='professionalPage'),
)
