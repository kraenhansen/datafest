from tastypie.resources import ModelResource, Resource
from tastypie import fields
from datasets.models import Dataset
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from oaipmh.common import Header
from django.conf.urls import url
from transformer.transformer import get_key_values
from itertools import * 

class DatasetResource(ModelResource):
	class Meta:
		queryset = Dataset.objects.all()
		resource_name = 'dataset'

class RecordResource(Resource):
	identifier = fields.CharField(readonly=True)
	metadata = fields.ListField(readonly=True)

	class Meta:
		resource_name = 'record'
		list_allowed_methods = ['get']
		max_limit = 100

	def _client(self, dataset):
		registry = MetadataRegistry()
		registry.registerReader(dataset.metadata_prefix, oai_dc_reader)
		return Client(dataset.pmh_url, registry)

	def override_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w.:/]*)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
		]

	def detail_uri_kwargs(self, bundle_or_obj):
		kwargs = {}
		if isinstance(bundle_or_obj, Bundle):
			kwargs['pk'] = bundle_or_obj.obj.id
		else:
			kwargs['pk'] = bundle_or_obj.id
		return kwargs

	def get_object_list(self, request, dataset):
		client = self._client(dataset)
		limit = int(request.GET.get('limit', self._meta.limit))
		offset = int(request.GET.get('offset', 0))
		result = client.listIdentifiers(metadataPrefix=dataset.metadata_prefix)
		return list(islice(result, offset, limit))

	def obj_get_list(self, request=None, **kwargs):
		dataset = Dataset.objects.get(pk=kwargs.get('dataset_pk'))
		return self.get_object_list(request, dataset)

	def obj_get(self, request=None, **kwargs):
		dataset = Dataset.objects.get(pk=kwargs['dataset_pk'])
		metadata_values = get_key_values(url=dataset.pmh_url, transform_sheet=dataset.transformation, identifier=kwargs['pk'])
		return dict(metadata = metadata_values, identifier=kwargs['pk'])

	def dehydrate_identifier(self, bundle):
		if isinstance(bundle.obj, Header):
			return bundle.obj.identifier()
		elif isinstance(bundle.obj, dict):
			return bundle.obj.get('identifier')
		else:
			raise Exception("Trouble dehydrating the record identifier, got %s" % type(bundle.obj))

	def dehydrate_metadata(self, bundle):
		if isinstance(bundle.obj, Header):
			return None
		elif isinstance(bundle.obj, dict):
			return bundle.obj.get('metadata', [])
