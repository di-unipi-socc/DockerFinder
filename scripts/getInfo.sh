#! /bin/bash

echo "Docker image description is started"


ARCH=$(uname -m | sed 's/x86_//;s/i[3-6]86/32/')

if [ -f /etc/lsb-release ]; then
    . /etc/lsb-release
    OS=$DISTRIB_ID
    VER=$DISTRIB_RELEASE
elif [ -f /etc/debian_version ]; then
    OS=Debian  # XXX or Ubuntu??
    VER=$(cat /etc/debian_version)
elif [ -f /etc/redhat-release ]; then
    OS=RedHat
    # TODO add code for Red Hat and CentOS here
else
    OS=$(uname -s)
    VER=$(uname -r)
fi

echo $OS
echo $VER
echo $ARCH