// dependencies
var express = require('express')
var mongoose = require('mongoose')
var bodyParser = require('body-parser')

var db_path = 'mongodb://172.17.0.3/images';
var port = 3000;



var app = express();
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


app.get('/', function (req, res) {
    res.json({message: 'use /search/?python=3.4  or /api/'});
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
app.listen(port);
console.log('API is running on port ' + port);
