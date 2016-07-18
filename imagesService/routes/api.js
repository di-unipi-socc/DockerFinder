// Dependencies
var express = require('express')
var router = express.Router();
// Modelskkk
var Image = require('../models/image')

// record all the methods
Image.methods(['get','put','post','delete']).updateOptions({ new: true });

Image.register(router,'/images');

// Return router
module.exports = router;
