import urllib.request
import json

url="https://hub.docker.com/v2/search/repositories/?page=3&query=*"


def crawl_all_images():

    response = urllib.request.urlopen("https://hub.docker.com/v2/search/repositories/?page="+i+"").read()
    print(json.loads(response.decode())['results'])
    #print(json.dumps(json.loads(response.decode()), indent=4))



'''

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def get_www_authenticate_header(api_url):
    try:
        resp = urllib.request.urlopen(api_url)
        response = resp.read()
    except urllib.error.HTTPError as error:
        response = error.info()['Www-Authenticate']
    return response

def get_token(user, password, service, scope, realm):
    data = {"scope":scope, "service":service, "account":user}
    r = requests.post(realm, auth=HTTPBasicAuth(user, password), data=data)
    token=find_between(str(r.content), 'token":"', '"')
    return token

def get_result(api_url, token):
    r = requests.get(api_url, headers={'Authorization':'Bearer ' + token})
    return r.content

def main():

    #get the Www-Authenticate header
    params=get_www_authenticate_header(args.api_url)
    #params=get_www_authenticate_header('https://registry-1.docker.io/v2/dido/webofficina/tags/list')

    #parse the params required for the token
    if params:
        realm=find_between(params, 'realm="', '"')
        service=find_between(params, 'service="', '"')
        scope=find_between(params, 'scope="', '"')

        # retrieve token
        #Bearer realm="https://auth.docker.io/token",service="registry.docker.io",scope="repository:dido/webofficina:pull"
        token = get_token(args.user, args.password, service, scope, realm)
        # retrieve token
        #token = get_token(args.user, args.password, service, scope, realm)

        # Do the API call as an authenticated user
        print("Response:")
        print(get_result(args.api_url, token))
    else:
        print("404 Not Found")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for making api calls to a private docker registry that requires authentication through a cesanta/docker_auth server.')
    parser.add_argument('--user', required=True, help='Username of the account used to make the request')
    parser.add_argument('--password', required=True, help='Password of the account used to make the request')
    parser.add_argument('--api_url', required=True, help='The API url that you want to access.')
    args = parser.parse_args()

    main()
    """
    python3 api-call.py --user davideneri18@gmail.com --password ***** --api_url  https://registry-1.docker.io/v2/dido/webofficina/tags/list
    """

#get_www_authenticate_header('https://auth.docker.io/token')
'''