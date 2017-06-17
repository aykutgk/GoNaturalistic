from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
        url(r'^login/$',views.UserLoginView.as_view(), name='login'),
        url(r'^logout/$',views.UserLogoutView, name='logout'),
        url(r'^signup/$',views.UserSignupView.as_view(), name='signup'),
        url(r'^search/$',views.UserSearchView.as_view(), name='search'),
	url(r'^account/(?P<pk>\d+)/$', views.UserAccountView.as_view(), name='account'),
        url(r'^wishlist/(?P<pk>\d+)/$', views.UserWishlistView.as_view(), name='wishlist'),	
        url(r'^consultations/(?P<pk>\d+)/$', views.UserConsultationView.as_view(), name='consultations'),
        url(r'^consultations/notes/(?P<pk>\d+)/$', views.UserConsultationNotesView.as_view(), name='consultationNotes'),
        url(r'^consultations/method-details/(?P<pk>\d+)/$', views.UserConsultationMethodDetailsView.as_view(), name='consultationMethodDetails'),
        url(r'^consultations/method-change/(?P<pk>\d+)/$', views.UserConsultationMethodChangeView.as_view(), name='consultationMethodChange'),
        url(r'^consultations/cancel/(?P<pk>\d+)/$', views.UserConsultationCancelView.as_view(), name='consultationCancel'),
)



