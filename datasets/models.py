from django.db import models

class Dataset(models.Model):
	title = models.CharField(max_length=200)
	organisation = models.CharField(max_length=200)
	contact_name = models.CharField(max_length=200)
	contact_email = models.EmailField()
	pmh_url = models.CharField(max_length=2000)
	metadata_prefix = models.CharField(max_length=200)

