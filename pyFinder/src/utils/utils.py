import json


def dictToJson(file, dictionary):
    with open(file, 'a') as fp:
        json.dump(dictionary, fp, indent=4)