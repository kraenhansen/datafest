from django.http import HttpResponse
from django.template import Context, loader
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from datasets.models import Dataset
import json

def populate_db(self):
        Dataset.get_default()
        return HttpResponse("Quite OK")

def overview(request):
	t = loader.get_template('datasets/overview.html')
	c = Context({
		'datasets_list': 0,
	})
	return HttpResponse(t.render(c))

def test(request):
	URL = 'http://www.kulturarv.dk/ffrepox/OAIHandler'
	registry = MetadataRegistry()
	registry.registerReader('oai_dc', oai_dc_reader)
	client = Client(URL, registry)
	identifyResponse = client.identify()

	print dir(identifyResponse)
	#for record in client.listRecords(metadataPrefix='oai_dc'):
	#	result += record
	return HttpResponse(identifyResponse.repositoryName())

def save_change(request):
        data = json.loads(request.POST.get('data', {}))
        identifier = data.get('identifier')
        fieldname = data.get('fieldname')
        value = data.get('name')

        if identifier:
                FieldChange.objects.create(identifier=identifier,
                                           fieldname=fieldname,
                                           value=value)
        return HttpResponse("OK!")
