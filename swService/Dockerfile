FROM node:argon

#node.js and npm already installed

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install app dependencies
COPY package.json /usr/src/app/
RUN npm install

# Bundle app source
COPY . /usr/src/app


# replace this with your application's default port
EXPOSE 3001

#commnand to run the app
CMD [ "npm", "start" ]