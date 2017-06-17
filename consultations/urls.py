from django.conf.urls import patterns, url
from consultations import views

urlpatterns = patterns('',
	# /consultations/
        url(r'^$',views.IndexView.as_view(), name='index'),
        url(r'^(?P<slug>[-_\w]+)/$', views.ConsultationPageView.as_view(), name='consultationPage'),
)

