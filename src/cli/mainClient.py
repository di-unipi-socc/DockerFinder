from src.cli import *


if __name__=="__main__":

    image = "ubuntu"

    with container.Container(image) as c:
        '''
        for line in c.run("echo 'deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe1' >> /etc/apt/sources.list"):
            print(line)


        for line in c.run("apt-get update"):
            print(line)

        #apt-get install python-virtualenv

        for line in c.run("apt-get install -y python python-dev python-distribute python-pip"):
            print(line)
        '''
        for line in c.run("python -v"):
            print(line)

    # echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list


