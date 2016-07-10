// dependencies
"use strict";

var express = require('express');
var mongoose = require('mongoose');
var bodyParser = require('body-parser');

var db_path = 'mongodb://172.17.0.2/images';
//var port = 8081;

var app = express();

// Environment configurations
//app.set('view engine', 'ejs');
app.set('port', process.env.PORT || 8080);

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(bodyParser.json({type:'application/vnd.api+json'}));
// app.config(function($httpProvider) {
//     //Enable cross domain calls
//     $httpProvider.defaults.useXDomain = true;
// }



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

//authenttication for tha /api route
//app.all('/api/*', requireAuthentication);


app.use(function (req, res, next) {
    console.log(req.method +" "+req.originalUrl);
    next();
})

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

app.get('/', function (req, res) {
    res.json({message: 'use /api/images'});
});


app.use('/search', require('./routes/search'))
app.use('/api', require('./routes/api'));

app.use(function(err, req, res, next) {
    // logic
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});


// Start server
app.listen(app.get('port'));
console.log('API is running on ' + app.get('port') );//+app.get('domain')+":"
