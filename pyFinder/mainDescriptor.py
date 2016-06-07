import pyFinder
import sys

#path of directories that should be searched for Python packages,
sys.path.append('/home/dido/github/DockerFinder')



#def main():
#pyFinder.descriptor()
print("Connecting to database...")
#c = dbconnector.FinderMongoClient('mongodb://172.17.0.2:27017/'
print("Searching for image..")
pyFinder.imageDescriptor("java")
#c.insert_image(dict









"""
if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Download and describe Docker images')
    #parser.add_argument('--user', required=True, help='Username of the account used to make the request')
    #parser.add_argument('--password', required=True, help='Password of the account used to make the request')
    #parser.add_argument('--api_url', required=True, help='The API url that you want to access.')
    #args = parser.parse_args()

    main()
"""