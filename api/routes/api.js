// Dependencies
var express = require('express')
var router = express.Router();

// Models
var Image = require('../models/image')



router.get('/imagesv2', function(req, res) {
 res.send('api is working for images')
});

// Routes
// without register the routes
//router.get('/images', function(req, res){
//  res.send('api is working for images')
//})


Image.methods(['get','put','post','delete']);
Image.register(router,'/images');




// Return router
module.exports = router;
