'use strict';

var express = require('express');
var path = require('path');
var logger = require('morgan');
var mongoose = require('mongoose');
var methodOverride = require('method-override');
var bodyParser = require('body-parser');
var fs = require("fs")
var assert = require('assert')

var Software = require('./models/software')  // return the model of the Run


var app = express();

app.set('port', process.env.PORT || 3001);
app.set('db_path', 'software_db');

app.use(logger('dev'));
app.use(bodyParser.urlencoded({'extended':'true'}));
app.use(bodyParser.json());
app.use(bodyParser.json({type:'application/vnd.api+json'}));
app.use(methodOverride());


var env = process.env.NODE_ENV || 'development';
//table name of the mongo database
var table ="/software";
var jsonPath = "/code/software.json"


app.use('/api', require('./routes/software'));   //api/software
app.use('/api', require('./routes/system'));   //api/system

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    console.log("Development mode \n");

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
  console.log("Production mode \n");

  res.status(err.status || 500);
    res.json({"message": err.message,
      "error": err
    });
});


//###################################################################################
//                                 CONNECTION DATABASE
// #################################################################################

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
      load_softwares()

    }
  });
};

function load_softwares(){
  //read THE JSON software and store them into database

  //var json = require(path.resolve(__dirname, 'softwares.json'));
  var json = require(path.resolve(__dirname, 'command.json'));
/
 // console.log( "Read json file: " +  path.resolve(__dirname, 'softwares.json'))
  //var json = require(path.resolve(__dirname, 'softwares.json'));
/
  Software.count({}, function( err, count){
    console.log( count + ": read softwares" );
    if(count == 0){
      console.log(json)
      //   var cmd = new Software ({
      //     run : json.run
      //   })
      //   cmd.save( function(err, document) {
      //     if (err) console.log(err)
      //     console.log(document)
      //
      //   }
      // )
      Software.collection.insertMany(json, function(err,r) {
          //assert.equal(Object.keys(json).length, r.insertedCount);
          console.log(r)
        console.log(r.getInsertedIds())// + ": software inserted into database")
          //console.log(r.insertedCount + ": software inserted into database")

      });
    }else {

       console.log(count + ": software are already present into database")

    }
  });
}

connectWithRetry();


// Start server
var server = app.listen(app.get('port'), function () {
    var host = server.address().address;
    var port = server.address().port;
    console.log('\nSoftware manger is listening port '+ port +"\n");
});
