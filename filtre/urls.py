from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^avis/(?P<avis_id>[0-9]+)/$', views.detall_avis, name='detall avis'),
	url(r'^font/(?P<font_id>[0-9]+)/$', views.detall_font, name='detall font'),
	url(r'^comprova/(?P<font_id>[0-9]+)/$', views.comprova_font, name='comprova font'),
	url(r'^files/', include('db_file_storage.urls')),
]
