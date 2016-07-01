// dependencies
var express = require('express')
var mongoose = require('mongoose')
var bodyParser = require('body-parser')

// MongoDb
mongoose.connect('mongodb://172.17.0.2/images')

// Express
var app = express();

app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());


// =============================================================================
var router = express.Router();              // get an instance of the express Router

// middleware to use for all requests
router.use(function(req, res, next) {
    // do logging
    console.log('Something is happening.');
    next(); // make sure we go to the next routes and don't stop here
});

// test route to make sure everything is working (accessed at GET http://localhost:8080/api)
router.get('/', function(req, res) {
    console.log("ofiwfhoib");
    res.json({ message: 'hooray! welcome to our api v2!' });
});

app.use(router)
// Routes
app.use('/api', require('./routes/api'));

// Start server
var port = 3000
app.listen(port);
console.log('API is running on port '+port);
