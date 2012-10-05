from django.http import HttpResponse
from django.template import Context, loader
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

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
	
