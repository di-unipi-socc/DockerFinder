// dependencies
"use strict"

var express = require('express')
var mongoose = require('mongoose')
var bodyParser = require('body-parser')

var db_path = 'mongodb://172.17.0.2/images';
//var port = 8081;

var app = express();

// Environment configurations

app.set('port', process.env.PORT_API || 3000);
console.log()

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());


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
    console.log(req.originalUrl);
    next();
})
app.get('/', function (req, res) {
    res.json({message: 'use /api/images'});
});

var images = [{
        "_id": "577ac56f0ecbc24b284e2526",
        "distro": "Description:\tUbuntu 14.04.4 LTS",
        "last_scan": "2016-07-04T20:22:07.092Z",
        "description": "",
        "full_size": 289459071,
        "repo_name": "editoo/utils",
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
        "_id": "577ac56f0ecbc24b284e2568",
        "distro": "Ubuntu 14.04.4 LTS",
        "last_scan": "2016-07-04T20:22:07.092Z",
        "description": "",
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
    }
    ];

app.get('/api/images', function(req, res){
    res.setHeader('Content-Type', 'application/json');
    res.send(images)
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
app.listen(app.get('port') );
console.log('API is running on port ' + app.get('port') );
