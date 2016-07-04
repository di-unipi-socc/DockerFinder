// Dependencies
var express = require('express')
var router = express.Router();

// Models
var Image = require('../models/image')

// record all the methods
Image.methods(['get','put','post','delete']);

Image.register(router,'/images');

// Return router
module.exports = router;
