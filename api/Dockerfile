FROM node:argon

#node.js and npm already installed

# Create app directory
RUN mkdir -p /usr/src/imagesServer
WORKDIR /usr/src/imagesServer

# Install app dependencies
COPY package.json /usr/src/imagesServer/
RUN npm install

# Bundle app source
COPY . /usr/src/imagesServer


# replace this with your application's default port
EXPOSE 3001

#commnand to run the app
CMD [ "npm", "start" ]