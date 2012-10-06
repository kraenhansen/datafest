from django.db import models, connection

default_transformation = """
fbb:buildingWrap/fbb:building
   fbb:id -> ID
   fbb:BBR/fbb:primaryAddress/fbb:streetName -> Vejnavn
"""

class Dataset(models.Model):
    title = models.CharField(max_length=200)
    organisation = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    pmh_url = models.CharField(max_length=2000)
    metadata_prefix = models.CharField(max_length=200)
    transformation = models.TextField()
    
    @classmethod
    def get_default(cls):
            dataset, _ = cls.objects.get_or_create(
                    title="titel", 
                    organisation="hello",
                    contact_name="hey",
                    contact_email="hey@hey.com",
                    pmh_url="https://www.kulturarv.dk/repox/OAIHandler",
                    metadata_prefix="fbb",
                    transformation=default_transformation)
            return dataset
        
class Resource(object):
    title = ""

class FieldChange(models.Model):
    identifier = models.CharField(max_length=1024, db_index=True)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    fieldname = models.CharField(max_length=765, db_index=True)
    value = models.TextField()
    
    class Meta:
        get_latest_by = "datetime"
    
    @classmethod
    def latest_values(cls, identifier):
        query = """
        select id, fieldname, value, datetime from 
              %s
        where 
               identifier=%%s
        group by (fieldname)
        having (datetime=max(datetime))""" % cls._meta.db_table
        return cls.objects.raw(query, [identifier])
        
        
