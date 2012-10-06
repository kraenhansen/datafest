from lxml import etree
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, MetadataReader
from itertools import *

def parse_transforms(txt):
    errorneous_lines = []
    transforms = []
    prefixes = [(0, '')]
    lines = txt.split('\n')
    next_prefix = None
    for line in lines:
        if not line.strip() or line.strip().startswith('#'):
            continue
        indent = len(line) - len(line.lstrip())
        for j in xrange(len(prefixes) - 1, -1, -1):
            if prefixes[j][0] < indent:
                break
        prefixes = prefixes[:j + 1]
        if '->' not in line:
            prefixes.append((indent, prefixes[j][1] + '/' + line.strip()))
        else:
            path, field  = (x.strip() for x in line.split('->', 1))
            path = prefixes[-1][1] + '/' + path
            path = path.lstrip('/')

            transforms.append({'path': path, 'field': field})
    return transforms


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
    print namespaces,fields
    registry.registerReader(namespace, MetadataReader(fields=fields, namespaces=namespaces))
    return c, namespace

def list_records(url, transforms):
    client, ns = get_client(url, transforms)
    return client.listRecords(metadataPrefix=ns)

def get_record(url, transforms, identifier):
    client, ns = get_client(url, transforms)
    return client.getRecord(identifier=identifier, metadataPrefix=ns)

def get_key_values(url, transform_sheet, identifier):
    transforms = parse_transforms(transform_sheet)
    record = get_record(url, transforms, identifier)
    metadata = record[1]
    return dict((k, v[0]) for k,v in metadata.getMap().iteritems())
