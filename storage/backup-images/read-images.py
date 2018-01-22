import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file", help="The name of the JSON file to read.")
args = parser.parse_args()

if (args.file):
    f  = args.file
    print("Reading JSON: {} ...".format(f))
    with open(f,encoding="utf8") as json_data:
       	data = json.load(json_data)
	# number of images stored into the JSOn file
        total_images = data['count']
        print( "{} total images in the file".format(total_images))
        # array of images descriptions
        images = data['images']
        #for i in images:
        #    print("Name: {}".format(i['name']))

