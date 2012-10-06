from tastypie.resources import ModelResource, Resource
from datasets.models import Dataset
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

class DatasetResource(ModelResource):
	class Meta:
		queryset = Dataset.objects.all()
		resource_name = 'dataset'

class RecordResource(Resource):
	class Meta:
		resource_name = 'record'
		list_allowed_methods = ['get']

	def _client(self, dataset_pk = None):
		if 'dataset_pk' not in kwargs:
			return None
		metadata_prefix = 'ff'
		URL = 'https://www.kulturarv.dk/repox/OAIHandler'
		registry = MetadataRegistry()
		registry.registerReader(metadata_prefix, oai_dc_reader)
		return Client(URL, registry)

	def detail_uri_kwargs(self, bundle_or_obj):
		kwargs = {}
		if isinstance(bundle_or_obj, Bundle):
			kwargs['pk'] = bundle_or_obj.obj.id
		else:
			kwargs['pk'] = bundle_or_obj.id
		return kwargs

	def get_object_list(self, request):
		result = []
		return result

	def obj_get_list(self, request=None, **kwargs):
		# Filtering disabled for brevity...
		return self.get_object_list(request)

	def obj_get(self, request=None, **kwargs):
		
		#bucket = self._bucket()
		#message = bucket.get(kwargs['pk'])
		#return RiakObject(initial=message.get_data())
		return None
