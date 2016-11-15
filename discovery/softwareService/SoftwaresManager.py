import json
import requests
from docopt import docopt


def upload_softwares(file_json, url="http://127.0.0.1:3001/api/software", ):

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

def delete_all_Softwares(url="http://127.0.0.1:3001/api/software"):
    list_softwares = get_all_softwares(url)
    _delete_softwares(url, list_softwares)

def get_all_softwares(url="http://127.0.0.1:3001/api/software"):
    try:
        res = requests.get(url)
        if res.status_code == requests.codes.ok:
            json_response = res.json()
            print(str(json_response['count']) + " softwares to delete")
            software_list = json_response['software']  # list of object
            return software_list
    except requests.exceptions.ConnectionError:
        raise


def _delete_softwares(url, list_software):
    deleted_sw=0
    for sw in list_software:
        url_delete= url+"/"+sw['_id']
        requests.delete(url_delete)
        deleted_sw+=1
        print("removed: " + url_delete)
    print(str(deleted_sw)+" Tot deleted softwares")

__doc__= """SoftwareManager

Usage:
  SoftwareManager.py upload [--file=<softwares.json>] [--software-url=<http://127.0.0.1:3001/api/software>]
  SoftwareManager.py rm    [--software-url=<http://127.0.0.1:3001/api/software>]
  SoftwareManager.py (-h | --help)
  SoftwareManager.py --version

Options:
  -h --help                         Show this screen.
  --file=FILE                       File JSON with all the softwares   [default: softwares.json]
  --software-url=SOWTWARESERVICE    Url software service [default: http://127.0.0.1:3001/api/software].
  --version                         Show version.
"""

if __name__=="__main__":
    args = docopt(__doc__, version='SoftwareManger 0.0.1')
    if args['upload']:
        upload_softwares(args['--file'], args['--software-url'])

    if args['rm']:
        delete_all_Softwares(args['--software-url'])
