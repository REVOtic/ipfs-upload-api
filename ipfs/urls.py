from django.conf.urls import url
from . import views
app_name = 'ipfs'
urlpatterns = [
    url(r'^$', views.input, name= 'input'),
    url(r'^result_upload$',views.result_upload, name='result_upload'),
    url(r'^result_delete$',views.result_delete, name='result_delete'),
    url(r'^hash_upload$',views.hash_upload, name='hash_upload'),
    url(r'^node_status$',views.node_status, name='node_status'),
    ]
