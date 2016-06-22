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

// Routes
app.use('/api', require('./routes/api'));

// Start server
var port = 3000
app.listen(port);
console.log('API is running on port '+port);
