// dependencies
//"use strict";
var express = require('express');
var mongoose = require('mongoose');
var path = require('path');
var bodyParser = require('body-parser');

//var db_path = 'mongodb://172.17.0.2/images';

var app = express();

// Environment configurations
app.set('port', process.env.PORT || 80);


app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(bodyParser.json());
app.use(bodyParser.json({
  type: 'application/vnd.api+json'
}));
app.use(express.static(path.join(process.cwd(), 'public')));

var http = require('http');

app.get('/images',function(req, res) {
  // res.send("Imgaes api is working");
  var path = "/api/images"+ (req._parsedUrl.search || '');
  console.log("\n Redirect to images_server: " + path);
  var reqApi = http.request({
      //host: '127.0.0.1',
      host: 'images_server',
      path: path,
      //since we are listening on a custom port, we need to specify it by hand
      port: '3000',
      //This is what changes the request to a POST request
      method: 'GET'
    },
    function(resApi) {
      // res.writeHead(resApi.statusCode, resApi.headers);
      res.writeHead(resApi.statusCode,resApi.headers);
      resApi.pipe(res);
    }
  );
  reqApi.end();
});

app.get('/search', function(req, res) { //  /api
  var path = '/search' + (req._parsedUrl.search || '');
  console.log("\n Redirect to images_server: " + path);

  var reqApi = http.request({
      //host: '127.0.0.1',
      host: 'images_server',
      path: path,
      //since we are listening on a custom port, we need to specify it by hand
      port: '3000',
      //This is what changes the request to a POST request
      method: 'GET'
    },
    function(resApi) {

      // res.writeHead(resApi.statusCode, resApi.headers);
      res.writeHead(resApi.statusCode);
      resApi.pipe(res);
      console.log("Response received from images_server");
    }
  );
  reqApi.end();

});

// TODO: return all the routes in GET, -> return only a blacklist of route , and configure angular to redirect to "/"
app.get('*', function(req, res) {
  res.sendFile(path.join(process.cwd(), 'public/index.html'));
});

app.use(function(err, req, res, next) {
  // logic
  res.status(err.status || 500);
  res.json({
    message: err.message,
    error: {}
  });
});

// Start server
var server = app.listen(app.get('port'), function() {
  var host = server.address().address;
  var port = server.address().port;
  console.log('Web app is listening on port:' + port);
});
