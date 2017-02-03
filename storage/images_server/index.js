"use strict";

var express = require('express');
var mongoose = require('mongoose');
var bodyParser = require('body-parser');

var Image = require('./models/image')
//var db_path = 'mongodb://172.17.0.2/images';
//var port = 8081;

var app = express();
var readline = require('readline'); //read the input from the users
var path = require('path');



// Environment configurations
app.set('port', process.env.PORT || 3000);
app.set('env',process.env.NODE_ENV || 'production');

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(bodyParser.json({type:'application/vnd.api+json'}));

///var env = process.env.NODE_ENV || 'development';
//var env = process.env.NODE_ENV || 'production';
//table name of the mongo database
var table ="/images";
var linkname_docker_compose = 'images_db' ; //link to database, resolved IP by DNS of bridge/overlay network



//###################################################################################
//                                 ROUTES
// ################################################################################

app.use(function (req, res, next) {
    console.log(req.method +" "+req.originalUrl);
    next();
});

app.all('*', function(req, res,next) {
    /**
     * Response settings
     * @type {Object}
     */
    var responseSettings = {
        "AccessControlAllowOrigin": req.headers.origin,
        "AccessControlAllowHeaders": "Content-Type,X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5,  Date, X-Api-Version, X-File-Name",
        "AccessControlAllowMethods": "POST, GET, PUT, DELETE, OPTIONS",
        "AccessControlAllowCredentials": true
    };
    /**
     * Headers
     */
    res.header("Access-Control-Allow-Credentials", responseSettings.AccessControlAllowCredentials);
    res.header("Access-Control-Allow-Origin", responseSettings.AccessControlAllowOrigin);
    res.header("Access-Control-Allow-Headers", (req.headers['access-control-request-headers']) ? req.headers['access-control-request-headers'] : "x-requested-with");
    res.header("Access-Control-Allow-Methods", (req.headers['access-control-request-method']) ? req.headers['access-control-request-method'] : responseSettings.AccessControlAllowMethods);

    if ('OPTIONS' == req.method) {
        res.send(200);
    }
    else {
        next();
    }
});

app.use(function(err, req, res, next) {
    // logic
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});

// development only
if ('development' == app.get('env')) {
   console.log("Development mode \n");
   app.set('db_path', '172.17.0.2');

}

// production only
if ('production' == app.get('env')) {
  console.log("Production mode \n ");
  app.set('db_path', linkname_docker_compose);   //images_db is set in docker-compose link
}


// CONNECTION DATABASE

// Connect to the database before starting the application server.
var mongo_path = 'mongodb://'+app.get('db_path') + table;

var connectWithRetry = function() {
  return mongoose.connect(mongo_path, function (err, database) {
      console.log("\nTry to connect "+ mongo_path);
      if (err) {
        console.error(err.message+ '- retrying in 5 sec' );
        setTimeout(connectWithRetry, 5000);

      }else{
      // Save database object from the callback for reuse.
      console.log("Succesful Connection to database "+ mongo_path );
    //  load_images()
    }
  });
};
//
// function load_images(){
//   //read THE JSON software and store them into database
//   var json = require(path.resolve(__dirname, 'images.json'));
//   Image.count({}, function( err, count){
//     console.log( count + ": images into local database" );
//     var rl = readline.createInterface({
//       input: process.stdin,
//       output: process.stdout
//     });
//     //if(count == 0){
//     rl.question("What do you think of node.js? ", function(answer) {
//          if(answer=="y"){
//              console.log("Thank you for your valuable feedback:", answer);
//          }
//
//
//         rl.close();
//       });
//     // console.log("No images, Inserting :  "+ json);
//     //     Image.collection.insertMany(json, function(err,r) {
//     //              assert.equal(Object.keys(json).length, r.insertedCount);
//     //              console.log(r.insertedCount + ": image inserted into database")
//     //   });
//     // }else {
//     //    console.log(count + ": images already present into database")
//     // }
//
//   });
//
// }

connectWithRetry();

/*
 ROUTES
 */

app.get('/', function (req, res) {
    res.json({message: 'use /api/images'});
});


app.use('/search', require('./routes/search'))
//app.use('/search', require('./routes/search-paginated'))
app.use('/api', require('./routes/api'));

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {

    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.json({"message": err.message,
          "error": err
        });
      });
}

// production error handler

// no stacktraces leaked to user
app.use(function(err, req, res, next) {
      res.status(err.status || 500);
        res.json({
              "message": err.message,
              "error": err
          });
});

// Start server
var server = app.listen(app.get('port'), function(){
    var port = server.address().port;
    console.log('Images Server is listening port: '+ port +"\n");
});
