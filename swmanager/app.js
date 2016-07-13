'use strict'

var express = require('express');
var path = require('path');
var logger = require('morgan');
var mongoose = require('mongoose');
var methodOverride = require('method-override');
var bodyParser = require('body-parser');

var db_path = 'mongodb://172.17.0.2/software';

var app = express();

app.set('port', process.env.PORT || 3001);

app.use(logger('dev'));

app.use(bodyParser.urlencoded({'extended':'true'}));
app.use(bodyParser.json());
app.use(bodyParser.json({type:'application/vnd.api+json'}));
app.use(methodOverride());

//###################################################################################
//                                 CONNECTION DATABASE
// #################################################################################


// Connect to the database before starting the application server.
mongoose.connect(db_path, function (err, database) {
    console.log("Try to connect "+ db_path);
    if (err) {
        console.log(err);
        //return next(err);
        process.exit(1);

    }
    // Save database object from the callback for reuse.
    console.log("Database connection ready");
});



//###################################################################################
//                                 ROUTES
// ################################################################################


app.get('/', function (req, res) {
    res.json({message: 'use /api/software'});
});

app.use('/api', require('./routes/software'));   //api/software

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
    res.json({"message": err.message,
      "error": err
    });
});


//module.exports = app;
// Start server
var server = app.listen(app.get('port'), function () {
    var host = server.address().address;
    console.log(server.address())
    var port = server.address().port;
    console.log('Software manger is listening on :' + host + ":" + port);
});
