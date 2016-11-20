FROM node:alpine
# node.js and npm already installed

# Create app directory
RUN mkdir -p /code
WORKDIR /code

# Install app dependencies
COPY package.json /code
RUN npm install

# Bundle app source
# COPY . /code

# replace this with your application's default port
#EXPOSE 8080
EXPOSE 80

#commnand to run the app
CMD [ "npm", "start" ]
