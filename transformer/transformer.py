from lxml import etree

def parse_transformations(txt):
    errorneous_lines = []
    transforms = []

    for line in txt:
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


