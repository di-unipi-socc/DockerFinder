// dependencies
//"use strict";
var express = require('express');
var mongoose = require('mongoose');
var path = require('path');
var bodyParser = require('body-parser');
var db_path = 'mongodb://172.17.0.2/images';
var app = express();

// Environment configurations
app.set('port', process.env.PORT || 3000);


app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(bodyParser.json({type: 'application/vnd.api+json'}));
app.use(express.static(path.join(__dirname, 'public')));

//##################################################################################
//                                 CONNECTION DATABASE
// #################################################################################
// Connect to the database before starting the application server.

mongoose.connect(db_path, function (err, database) {
    console.log("Try to connect " + db_path);
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

app.use(function (req, res, next) {
    console.log(req.method + " " + req.originalUrl);
    next();
});

var http = require('http');

app.get('/api/search', function (req, res) {
    console.log(req._parsedUrl.search);

    var reqApi = http.request({
            host: '127.0.0.1',
            path: '/search' + req._parsedUrl.search,
            //since we are listening on a custom port, we need to specify it by hand
            port: '8000',
            //This is what changes the request to a POST request
            method: 'GET'
        },
        function (resApi) {
            console.log("Called Callaback ServerApi");
            // res.writeHead(resApi.statusCode, resApi.headers);
            res.writeHead(resApi.statusCode);
            resApi.pipe(res);
        }

        // function (resApi) {
        //     var str = ''
        //     resApi.on('data', function (chunk) {
        //         str += chunk;
        //     });
        //
        //     resApi.on('end', function () {
        //         res.write(str);
        //     });
        // }
    );
    reqApi.end();

    //  var resApi = http.get('http://127.0.0.1:8000/search'+req._parsedUrl.search, function (resApi) {
    //         res.writeHead(resApi.statusCode, resApi.headers);
    //         resApi.pipe(res);
    //  });
    //
    // resApi.end();
});

// TODO: return all the routes in GET, -> return only a blacklist of route , and configure angular to redirect to "/"
app.get('*', function (req, res) {
    res.sendFile(__dirname + '/public/index.html');
});

app.use(function (err, req, res, next) {
    // logic
    res.status(err.status || 500);
    res.json({
        message: err.message,
        error: {}
    });
});

// Start server
var server = app.listen(app.get('port'), function () {
    var host = server.address().address;
    var port = server.address().port;
    console.log('Web app is listening on :' + host + ":" + port);
});
