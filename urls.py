from django.conf.urls.defaults import patterns, include, url
from webshop import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import os

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'webshop.views.home', name='home'),
	# url(r'^webshop/', include('webshop.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
	(r'^', include('catalog.urls')),

	# enable language choice
	url(r'^i18n/', include('django.conf.urls.i18n')),
	url(r'^set_language/$', 'django.views.i18n.set_language', name='set_language'),

)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve',\
		   {'document_root' : settings.STATIC_ROOT }),
		# if work then show 404 Directory indexes are not allowed here.
	)

handler404 = 'webshop.views.file_not_found_404'