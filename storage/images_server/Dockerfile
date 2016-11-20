FROM node:alpine
# node.js and npm already installed

# Create  directory that store the source code
RUN mkdir -p /code
WORKDIR /code

# Install server dependencies
COPY package.json /code
RUN npm install -save

COPY . /code

ENTRYPOINT  ["npm","start"]
