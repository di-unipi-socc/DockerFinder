import json
import requests
from docopt import docopt


def upload_softwares(file_json, url="http://127.0.0.1:3001/api/images", ):

    with open(file_json) as json_data:
        softwares = json.load(json_data)
        print(str(len(softwares)) + " softwares read from "+file_json )
        tot_upload = 0
        for sw in softwares:
            res = requests.post(url, headers={'Content-type': 'application/json'}, json=sw)
            if res.status_code == requests.codes.created or res.status_code == requests.codes.ok:
                print("[" + sw['name'] + "] added into " + res.url)
                tot_upload+=1
            else:
                print(str(res.status_code) + " response: " + res.text)
        print(str(tot_upload) + " softwares uploaded")


def delete_all_images(url="http://127.0.0.1:3001/api/images"):
    list_images = get_all_softwares(url)
    _delete_images(url, list_images)


def get_all_softwares(url="http://127.0.0.1:3000/api/images"):
    try:
        res = requests.get(url)
        if res.status_code == requests.codes.ok:
            json_response = res.json()
            print(str(json_response['count']) + " images to delete")
            software_list = json_response['images']  # list of object
            return software_list
    except requests.exceptions.ConnectionError:
        raise


def _delete_images(url, list_images):
    deleted_im=0
    for image in list_images:
        url_delete= url+"/"+image['_id']
        requests.delete(url_delete)
        deleted_im+=1
        print("removed: " + url_delete)
    print(str(deleted_im)+" Tot deleted images")

__doc__= """Crawler

Usage:
  Tester.py upload [--file=<softwares.json>] [--software-url=<http://127.0.0.1:3000/api/images>]
  Tester.py rm    [--images-url=<http://127.0.0.1:3000/api/images>]
  Tester.py (-h | --help)
  Tester.py --version

Options:
  -h --help     Show this screen.
  --file=FILE        File JSON with all the softwares   [default: softwares.json]
  --images-url=IMAGESSERVICE  Url iamges service [default: http://127.0.0.1:3000/api/images].
  --version     Show version.
"""

if __name__=="__main__":
    args = docopt(__doc__, version='SoftwareManger 0.0.1')
    if args['upload']:
        upload_softwares(args['--file'], args['--images-url'])

    if args['rm']:
        delete_all_images(args['--images-url'])
