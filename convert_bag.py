import rosbag
import sys
import json

if __name__ == '__main__':
	bag_dict = {}
	bag = rosbag.Bag(sys.argv[1])
	for topic, msg, t in bag.read_messages(sys.argv[2]):
		msg_dict = '{'
		for line in str(msg).split("\n"):
			fmt_line = '"' + line.replace(":", '":')
			msg_dict += fmt_line + ","
		msg_dict += '"timestamp": {}'.format(t)
		msg_dict += "}"
		msg_dict = json.loads(msg_dict)	
		bag_dict[str(t)] = msg_dict
	bag.close()
	with open(sys.argv[3], "w") as fp:
		json.dump(bag_dict, fp)

