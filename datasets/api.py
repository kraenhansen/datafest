from tastypie.resources import ModelResource
from datasets.models import Dataset

class DatasetResource(ModelResource):
	class Meta:
		queryset = Dataset.objects.all()
		resource_name = 'entry'
