var express = require('express');
var mongoose = require('mongoose');
var bodyParser = require('body-parser');
var methodOverride = require('method-override');
var _ = require('lodash');  //object _ : name of the varable is underscore


//Create teheapplicatin
var app = express();


//Add middleware (every request is intercepted by middleware) for REST API's
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(methodOverride('X-HTTP-Method-Override'));

//CORS support (allow to expose our api to all URL-public API)
app.use(function(req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

//Connect to the Mongo
mongoose.connect('mongodb://localhost/dofinder');  //meanapp is the database name
mongoose.connection.once('open', function(){
  //load the modules
  app.models = require('./models/index') //dependency inject into the controller all the modules.7

  //Load routes
  var routes = require('./routes.js');
  _.each(routes, function(controller,route){ // route=key'./movie', controller=function
      app.use(route, controller(app,route));
  });

  console.log("listening on port 3000");
  app.listen(3000);
});
