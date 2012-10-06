from lxml import etree
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, MetadataReader
from itertools import *

def parse_transforms(txt):
    errorneous_lines = []
    transforms = []

    for line in txt.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if not '->' in line:
            errorneous_lines.append({
                'line': line,
                'reason': 'Missing ->'
            })
            continue

        path, field  = (x.strip() for x in line.split('->', 2))
        transforms.append({'path': path, 'field': field})
    return transforms, errorneous_lines


def read_fields(record, transforms):
    for path, field in transforms:
        parts = filter(None, (part.strip() for part in path.split('/')))
    
        data = record
        for part in parts:
            ns = None
            if ':' in part:
                short_ns, part = part.split(':', 2)
                ns = data.nsmap.get(short_ns)
            original_part = part
            if ns:
                part = "{%s}%s" % (ns, part)
            new_data = getattr(data, part, None)
            if not new_data:
                for child in data.iterchildren():
                    ns = child.nsmap.get(short_ns)
                    other_part = "{%s}%s" % (ns, part)
                    if child.tag == other_part or child.tag == part:
                        new_data = child
                        break
            data = new_data
            if not new_data:
                raise Exception("failed to find: %s" % original_part)
        yield (field, unicode(data))

def fix_transforms(transforms):
    res = []
    for transform in transforms:
        new_transform = transform.copy()
        if not new_transform['path'].endswith('/'):
            new_transform['path'] += '/'
        new_transform['path'] += 'text()'
        res.append(new_transform)
    return res

def get_client(url, transforms):
    transforms = fix_transforms(transforms)
    registry = MetadataRegistry()
    c = Client(url, registry)
    metadata = c.listMetadataFormats()
    metadata[0] = [
        'fbb', 'http://www.kulturarv.dk/fbb/fbb.xsd', 'http://www.kulturarv.dk/fbb']
    namespaces = dict((x[0], x[2]) for x in metadata)
    fields = dict((transform['field'], ('textList', transform['path']))
                  for transform in transforms)
    namespace = metadata[0][0]
    registry.registerReader(namespace, MetadataReader(fields=fields, namespaces=namespaces))
    return c, namespace

def list_records(url, transforms):
    client, ns = get_client(url, transforms)
    return client.listRecords(metadataPrefix=ns)

def get_record(url, transforms, identifier):
    client, ns = get_client(url, transforms)
    return client.getRecord(identifier=identifier, metadataPrefix=ns)

def get_key_values(url, transform_sheet, identifier):
    transforms, errors = parse_transforms(transform_sheet)
    if errors:
        print errors
    return get_record(url, transforms, identifier)
    
