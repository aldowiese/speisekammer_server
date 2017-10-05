from django.conf.urls import url

from . import views

app_name = 'speisekammer_server'
urlpatterns = [
    url(r'^$', views.SpeisekammerView.as_view(), name='speisekammer_server'),
    url(r'^(?P<pk>[0-9]+)$', views.SpeisekammerProductView.as_view(), name='product_detail'),
    url(r'^(?P<pk>[0-9]+)/(?P<barcode>[0-9]+)$', views.SpeisekammerProductView.as_view(), name='product_manipulate'),

    # api urls
    url(r'^products/(?P<pk>[0-9]+)$', views.ProductView.as_view()),
    url(r'^products', views.ProductListView.as_view()),
    url(r'^instances/(?P<barcode>[0-9]+)/item_count', views.ItemCountView.as_view()),
    url(r'^instances/(?P<barcode>[0-9]+)$', views.InstanceView.as_view()),
    url(r'^instances', views.InstanceListView.as_view()),
]
