import requests
import json

DOCKER_HUB = "https://hub.docker.com"

FILE_SAVE_TAGS="officials_images_tags.json"
FILE_SAVE="officials_images.json"

def pull_officials():
    payload = {'page': 1, 'page_size': 100}
    count = 0
    try:
        res = requests.get(DOCKER_HUB+"/v2/repositories/library",params=payload)
        if res.status_code == requests.codes.ok:
            json_response = res.json()
            list_images = [res['name'] for res in json_response['results']]
            count += json_response['count']
            next_page = json_response['next']
            while next_page:
                # print(next_page)
                res = requests.get(next_page)
                json_response = res.json()
                list_images += [res['name']
                                for res in json_response['results']]
                next_page = json_response['next']
            return list_images
        else:
            print(str(res.status_code) +
                              " error response: " + res.text)
            return []
    except requests.exceptions.ConnectionError as e:
        print("ConnectionError: " + str(e))
        raise e

def get_all_tags(repo_name, is_official=True):
    """
    GEt  all the tags associated with the repository name.
    :param repo_name: the name of the repository.
    :return: a list of (string) tags name.
    """
    if is_official:
        url_tags = DOCKER_HUB + "/v2/repositories/library/" + repo_name + "/tags/"
    else:
        url_tags = DOCKER_HUB + "/v2/repositories/" + repo_name + "/tags/"
    try:
        print(url_tags)
        res = requests.get(url_tags)
        # print("["+repo_name+"] Getting all the tags")
        if res.status_code == requests.codes.ok:
            json_response = res.json()
            count = json_response['count']
            # get the tags in the current page
            list_tags = [res['name'] for res in json_response['results']]
            next_page = json_response['next']
            while next_page:       # pagination of the tags
                res = requests.get(next_page)
                json_response = res.json()
                list_tags += [res['name'] for res in json_response['results']]
                next_page = json_response['next']
            print("[{}] {} tags found ".format(repo_name, len(list_tags)))
            return list_tags
        else:
            print(str(res.status_code) + ": " + res.text)
            return []

    except requests.exceptions.ConnectionError as e:
        print("ConnectionError: ")
        raise e
    except:
        print("Unexpected error:")
        raise

officials = {}
names = pull_officials()

with open(FILE_SAVE, 'w') as fout:
    json.dump({"officials": names}, fout)
    print("{} repo ufficiali".format(len(names)))

for name in names:
    tags =  get_all_tags(name)
    officials[name]  = tags
    print("{} saved {} tags".format(name,len(tags)))

with open(FILE_SAVE_TAGS, 'w') as fout:
    json.dump(officials, fout)
