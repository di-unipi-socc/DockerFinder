// Dependencies
var express = require('express')
var router = express.Router();
// Modelskkk
var Image = require('../models/image')

// record all the methods
Image.methods(['get','put','post','delete']).updateOptions({ new: true });

// GET /api/images
Image.after('get', function(req, res, next) {
  //var tmp = res.locals.bundle.title; // Lets swap the title and year fields because we're funny!
  //res.locals.bundle.title = res.locals.bundle.year;
  //res.locals.bundle.year = tmp;
    //console.log(res.locals);
    var count = res.locals.bundle.length;
    res.json({"count": count, "images": res.locals.bundle});
    console.log("Results " + count);
    next(); // Don't forget to call next!
});

Image.register(router,'/images');

// Return router
module.exports = router;
