import requests


class ClientSoftware(requests.Session):

    def __init__(self):
        super(ClientSoftware, self).__init__()

    def get_software(self):
        d = (("python", "--version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
             ("python3", "--version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
             ("python2", "--version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
             ("java", "-version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
             ("curl", "--version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
             ("nano", "-version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
             ("node", "--version", '[0-9]\.[0-9](\.[0-9])*[^\s]*'),
             ("ruby", "--version",'[0-9]\.[0-9](\.[0-9])*[^\s]*'),
             ("perl", "-version",'[0-9]\.[0-9](\.[0-9])'))
        for l in d:
            yield l[0], l[1], l[2]

    def get_system(self):
        # - {cmd: 'bash -c "cat /etc/*release"', re: '(?<=PRETTY_NAME=")[^"]*'}  # PRETTY_NAME=.*'
        # - {cmd: 'bash -c "lsb_release -a"', re: 'Description:.*'}

        d = (('bash -c "cat /etc/*release"', '(?<=PRETTY_NAME=")[^"]*'),
             ('bash -c "lsb_release -a"', 'Description:.*'))

        for l in d:
            yield l[0], l[1]