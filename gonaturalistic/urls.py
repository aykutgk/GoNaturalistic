from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('home.urls', namespace="home")),
    url(r'^user/', include('users.urls', namespace="users")),
    url(r'^articles/', include('articles.urls', namespace="articles")),
    url(r'^consultations/', include('consultations.urls', namespace="consultations")),
    url(r'^categories/', include('categories.urls', namespace="categories")),
    url(r'^professionals/', include('professionals.urls', namespace="professionals")),
    url(r'^user/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    url(r'^user/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^user/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^user/reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    url(r'^user/password_change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^user/password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^gnAdmin2014_GoNatural/', include(admin.site.urls)),
)
