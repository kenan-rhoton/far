from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^avis/(?P<avis_id>[0-9]+)/$', views.detall_avis, name='detall avis'),
	url(r'^font/(?P<font_id>[0-9]+)/$', views.detall_font, name='detall font'),
	url(r'^comprova/(?P<font_id>[0-9]+)/$', views.comprova_font, name='comprova font'),
	url(r'^analitza/(?P<font_id>[0-9]+)/$', views.analitza_font, name='analitza font'),
        url(r'^test/(?P<text>[^/]+)$', views.test_view, name='test'),
        url(r'^actualitza_tot/$', views.actualitza_tot, name='actualitza tot'),
]
