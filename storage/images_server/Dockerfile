FROM node:alpine
# node.js and npm already installed

# Create  directory that store the source code
RUN mkdir -p /code

#install git because it is needed otinstall node-restful lates release
RUN apk add --update  git
WORKDIR /code

# Install server dependencies
COPY package.json /code
RUN npm install -save

COPY . /code


ENTRYPOINT  ["npm","start"]
