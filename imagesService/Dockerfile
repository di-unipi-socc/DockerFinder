FROM node:argon
#node.js and npm already installed

# Create app directory
RUN mkdir -p /code
WORKDIR /code

# Install app dependencies
COPY package.json /code
RUN npm install

# Bundle app source
#COPY . /usr/src/imagesServer

# replace this with your application's default port
EXPOSE 3000

#commnand to run the app
CMD [ "npm", "start" ]