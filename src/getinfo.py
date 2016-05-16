import json
import os.path
from pprint import pprint

from src import Container

image = "ubuntu"

scriptpath = os.path.dirname(__file__)
filename = os.path.join(scriptpath, 'images.json')

with open(filename) as data_file:
    data = json.load(data_file)
    pprint(data[image]['os'])
    pprint(data[image]['kernel'])
    pprint(data[image]['apps'])

    with Container(image, volumes=['/home/dido/getInfo.sh:/my/info.sh', '/home/dido/out.txt:/my/out.txt']) as c:
        for output_line in c.run('bash /my/info.sh >> /my/out.txt'):  # && bash  /my/info.sh > /my/out.txt && cat /my/out.txt"):
            print(output_line)

# for output_line in c.run(data['ubuntu']['app']):
#    print(output_line)
# for output_line in c.run(data['fedora']['os']):
#   print(output_line)
