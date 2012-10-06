from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from datasets.api import DatasetResource, RecordResource
admin.autodiscover()

dataset_resource = DatasetResource()
record_resource = RecordResource()

urlpatterns = patterns('',
    url(r'^$', 'datasets.views.overview', name='overview'),
    url(r'^test$', 'datasets.views.test', name='test'),
    url(r'^populate$', 'datasets.views.populate_db', name='populate_db'),
    url(r'^save_change$', 'datasets.views.save_change', name='save_change'),
    (r'^api/%s/(?P<dataset_pk>\w+)/' % dataset_resource._meta.resource_name, 
       include(record_resource.urls)),
    (r'^api/', include(dataset_resource.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
