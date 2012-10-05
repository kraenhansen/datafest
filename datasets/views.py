from django.http import HttpResponse
from django.template import Context, loader

from oaipmh.client import Client

def overview(request):
	t = loader.get_template('datasets/overview.html')
	c = Context({
		'datasets_list': 0,
	})
	return HttpResponse(t.render(c))

def test(request):
	return HttpResponse(" ... ")
	
