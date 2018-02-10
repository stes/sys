# !/bin/env python

''' Convert rosbag logging files to json

$ ./convert_bag.py infile.bag outfile.json
'''

import rosbag
import sys
import json
import yaml
import re
import collections


def flatten(d, parent_key='', sep='/'):
    """
    https://stackoverflow.com/questions/6027558/flatten-nested-python-dictionaries-compressing-keys
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, list):
            v = {str(i) : x for i,x in enumerate(v)}
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


if __name__ == '__main__':
	bag_dict = {}
	bag = rosbag.Bag(sys.argv[1])

        #regex = re.compile(r'[ ]*(.*)[:] (.*)')
        
        n_messages =  bag.get_message_count()
        for n, (topic, msg, t) in enumerate(bag.read_messages()):
            msg_dict = yaml.load(str(msg))
            #print(topic)
            #print(msg_dict)
            #print('-'*80)

            #msg_dict = {}
            #for line in str(msg).split("\n"):
            #    match = regex.search(line)
            #    if match is not None:
            #        groups = match.groups()
            #        if len(groups) == 2:
            #            key, data = groups
            #            if len(data) > 0 and data != '' and data != "''":
            #                msg_dict[key] = json.loads(data)

            #msg_dict['timestamp'] = int(str(t))
            
            for k, v in flatten(msg_dict, parent_key=str(topic)).items():

                if not k in bag_dict.keys():
                    bag_dict[k] = {}
                    print('New topic {}'.format(k))
                    print(v)

                bag_dict[k][int(str(t))] = v
            
            if n % (n_messages // 100) == 0:
                print('Processing Message {}/{}'.format(n, n_messages))

            
            #if n > 100:
            #    break

	bag.close()
	with open(sys.argv[2], "w") as fp:
            json.dump(bag_dict, fp)

