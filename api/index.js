// dependencies
"use strict"

var express = require('express')
var mongoose = require('mongoose')
var bodyParser = require('body-parser')

var db_path = 'mongodb://172.17.0.2/images';
//var port = 8081;

var app = express();

// Environment configurations

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
    console.log("Try to connect "+ db_path)
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

var images = [{
        "_id": "577",
        "distro": "Description:\tUbuntu 14.04.4 LTS",
        "last_scan": "2016-07-04T20:22:07.092Z",
        "description": "description java",
        "full_size": 289459071,
        "repo_name": "java",
        "star_count": 8,
        "last_updated": "2016-07-01T14:56:07.236Z",
        "pull_count": 5,
        "__v": 0,
        "bins": [
                {
                    "bin": "python",
                    "ver": "2.7.6"
                },
                {
                    "bin": "python3",
                    "ver": "3.4.3"
                },
                {
                    "bin": "python2",
                    "ver": "2.7.6"
                },
                {
                    "bin": "curl",
                    "ver": "7.35.0"
                }
            ]

    },
    {
        "_id": "574",
        "distro": "Ubuntu 14.04.4 LTS",
        "last_scan": "2016-07-04T20:22:07.092Z",
        "description": "other description python",
        "full_size": 289459071,
        "repo_name": "python",
        "star_count": 4,
        "last_updated": "2016-07-01T14:56:07.236Z",
        "pull_count": 5,
        "__v": 0,
        "bins": [
            {
                "bin": "python",
                "ver": "2.7.6"
            },
            {
                "bin": "python3",
                "ver": "3.4.3"
            },
            {
                "bin": "python2",
                "ver": "2.7.6"
            },
            {
                "bin": "curl",
                "ver": "7.35.0"
            }
        ]
    },
     {
        "_id": "579",
        "distro": "Ubuntu 14.04.4 LTS",
        "last_scan": "2016-07-04T20:22:07.092Z",
        "description": "something ",
        "full_size": 289459071,
        "repo_name": "fedora",
        "star_count": 4,
        "last_updated": "2016-07-01T14:56:07.236Z",
        "pull_count": 5,
        "__v": 0,
         "bins": [
            {
                "bin": "python",
                "ver": "2.7.6"
            },
            {
                "bin": "python3",
                "ver": "3.4.3"
            },
            {
                "bin": "python2",
                "ver": "2.7.6"
            },
            {
                "bin": "curl",
                "ver": "7.35.0"
            }
        ]
    }
    ];

//
// app.get('/api/images', function(req, res){
//     res.setHeader('Content-Type', 'application/json');
//     res.send(images)
// });


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
