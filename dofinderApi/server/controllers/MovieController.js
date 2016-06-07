// convert into rest API from the module definition
var restful = require('node-restful');

module.exports = function(app, route){

  //setup the controller for REST
  var rest = restful.model(
    'movie',
    app.models.movie
  ).methods(['get','put','post','delete']);

  //Register this end point with applications
  rest.register(app,route);

  //Return moddilewar
  return function(req, res, next){
    next();
  };
};
