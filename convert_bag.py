# !/bin/env python

''' Convert rosbag logging files to json

$ ./convert_bag.py infile.bag outfile.json
'''

import rosbag
import sys
import json
import yaml
import re

if __name__ == '__main__':
	bag_dict = {}
	bag = rosbag.Bag(sys.argv[1])

        regex = re.compile(r'[ ]*(.*)[:] (.*)')
        
        n_messages =  bag.get_message_count()
        for n, (topic, msg, t) in enumerate(bag.read_messages()):
            msg_dict = {}
            for line in str(msg).split("\n"):
                match = regex.search(line)
                if match is not None:
                    groups = match.groups()
                    if len(groups) == 2:
                        key, data = groups
                        if len(data) > 0 and data != '' and data != "''":
                            msg_dict[key] = json.loads(data)

            #msg_dict['timestamp'] = int(str(t))
            
            if not str(topic) in bag_dict.keys():
                bag_dict[str(topic)] = {}
                print('New topic {}'.format(str(topic)))

            bag_dict[str(topic)][int(str(t))] = msg_dict
            
            if n % (n_messages // 100) == 0:
                print('Processing Message {}/{}'.format(n, n_messages))

	bag.close()
	with open(sys.argv[2], "w") as fp:
            json.dump(bag_dict, fp)

