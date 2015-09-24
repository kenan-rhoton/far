from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^noticia/(?P<noticia_id>[0-9]+)/$', views.detall_noticia, name='detall noticia'),
	url(r'^font/(?P<font_id>[0-9]+)/$', views.detall_font, name='detall font'),
	url(r'^actualitza/(?P<font_id>[0-9]+)/$', views.actualitza_font, name='actualitza font'),
]