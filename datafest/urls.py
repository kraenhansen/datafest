from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from datasets.api import DatasetResource
admin.autodiscover()

dataset_resource = DatasetResource()

urlpatterns = patterns('',
    url(r'^$', 'datasets.views.overview', name='overview'),
    url(r'^test$', 'datasets.views.test', name='test'),
    (r'^api/', include(dataset_resource.urls)),
    # Examples:
    # url(r'^datafest/', include('datafest.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)