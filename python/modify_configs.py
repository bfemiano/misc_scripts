import os
import json
import sys
from collections import OrderedDict

def copy_data_in_order(path, data):
    updated_data = OrderedDict()
    updated_data['name'] = data['name']
    updated_data['description'] = data['description']
    if 'owner' in data:
        updated_data['owner'] = data['owner']
    updated_data['cluster'] = data['cluster']
    if 'type' in data:
        updated_data['type'] = data['type']
    updated_data['command'] = data['command']
    if 'instances' in data:
        updated_data['instances'] = data['instances']
    if 'onepernode' in data:
        updated_data['onepernode'] = data['onepernode']
    if 'retries' in data:
        updated_data['retries'] = data['retries']
    if 'runas' in data:
        updated_data['runas'] = data['runas']
    if 'rack' in data:
        updated_data['rack'] = data['rack']
    if 'cpus' in data:
        updated_data['cpus'] = data['cpus']
    if 'memory' in data:
        updated_data['memory'] = data['memory']
    if 'disk' in data:
        updated_data['disk'] = data['disk']
    if 'kerberos' in data:
        updated_data['kerberos'] = data['kerberos']
    if 'schedule' in data:
        updated_data['schedule'] = data['schedule']
    updated_data['enabled'] = data['enabled']
    if 'restart' in data:
        updated_data['restart'] = data['restart']
    if 'parents' in data:
        updated_data['parents'] = data['parents']
    if 'action' in data:
        updated_data['action'] = data['action']
    if 'nagios' in data:
        updated_data['nagios'] = data['nagios']
    if 'environment' in data:
        updated_data['environment'] = data['environment']
    missing_props = set(data.keys()).difference(updated_data.keys())
    if len(missing_props) > 0:
        raise Exception("missing %s for %s" % (' '.join(list(missing_props)), path))
    return updated_data


def list_dirs(files):
    for f in files:
        if os.path.isdir(f):
            list_dirs([os.path.join(f, path) for path in os.listdir(f)])
        else:
            if f.endswith("config.json") and 'template' not in f:
                with open(f, 'r') as data:
                    try:
                        json_data = json.load(data)
                        print f, json_data['name']
                        if json_data['cluster'] == 'nbs-dc1-prod':
                            with open(f, 'w') as out_data:
                                json_data['cluster'] = 'default'
                                updated_data = copy_data_in_order(f, json_data)
                                out_data.write(json.dumps(updated_data, indent=2, separators=(',', ': ')))
                    except ValueError as e:

                        print "error on %s" % f
                        raise e


start_path = sys.argv[1]
print "Listing config paths at %s " % start_path
list_dirs([os.path.join(start_path, path) for path in os.listdir(start_path)])
