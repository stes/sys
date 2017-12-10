# !/bin/env python

''' Convert rosbag logging files to json

$ ./convert_bag.py infile.bag outfile.json /first/topic [/second/topic ...]
'''

import rosbag
import sys
import json

if __name__ == '__main__':
	bag_dict = {}
	bag = rosbag.Bag(sys.argv[1])
        for msg_name in sys.argv[3:]:
            bag_dict[msg_name] = {}
            for topic, msg, t in bag.read_messages(msg_name):
                msg_dict = '{'
                for line in str(msg).split("\n"):
                        fmt_line = '"' + line.replace(":", '":')
                        msg_dict += fmt_line + ","
                msg_dict += '"timestamp": {}'.format(t)
                msg_dict += "}"
                msg_dict = json.loads(msg_dict)	
                bag_dict[msg_name][str(t)] = msg_dict
	bag.close()
	with open(sys.argv[2], "w") as fp:
            json.dump(bag_dict, fp)

