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

def get_count_tags(repo_name):
    url_tags = DOCKER_HUB + "/v2/repositories/library/" + repo_name + "/tags/"
    res = requests.get(url_tags)
    if res.status_code == requests.codes.ok:
        return res.json()['count']
    else:
        print(str(res.status_code) + ": " + str(res.json()))
        raise Exception("Error code {}".format(res.status_code))

def get_all_tags(repo_name, is_official=True):
    """
    GEt  all the tags associated with the repository name.
    :param repo_name: the name of the repository.
    :return: a list of (string) tags name.
    """
    count_tags = 0
    url_tags = DOCKER_HUB + "/v2/repositories/library/" + repo_name + "/tags/"
    try:
        print(url_tags)
        res = requests.get(url_tags)
        if res.status_code == requests.codes.ok:
            json_response = res.json()
            count = json_response['count']
            count_tags += count
            # get the tags in the current page
            # list_tags = [res['name'] for res in json_response['results']]
            # next_page = json_response['next']
            # while next_page:       # pagination of the tags
            #     res = requests.get(next_page)
            #     json_response = res.json()
            #     list_tags += [res['name'] for res in json_response['results']]
            #     next_page = json_response['next']
            # print("[{}] {} tags found ".format(repo_name, len(list_tags)))
            # return list_tags
        else:
            print(str(res.status_code) + ": " + str(res.json()))

    except requests.exceptions.ConnectionError as e:
        print("ConnectionError: ")
        raise e
    except:
        print("Unexpected error:")
        raise


def dump_officials():
    names = pull_officials()
    with open(FILE_SAVE, 'w') as fout:
        json.dump({"officials": names}, fout)
        print("{} repo ufficiali".format(len(names)))


def count_all_tags():
    count_total = 0
    for name in pull_officials():
        count = get_count_tags(name)
        print("{} tags {}".format(name, count))
        count_total += count
    print("{} total tags".format(count_total))

count_all_tags()
