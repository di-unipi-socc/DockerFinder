// Dependencies
"use strict";
var express = require('express');
var router = express.Router();
var Image = require('../models/image');

// record all the methods
Image.methods(['get','put','post','delete']).updateOptions({ new: true });

// GET /api/images
Image.after('get', function(req, res, next) {
    var count = res.locals.bundle.length;
    var data = res.locals.bundle;
    res.locals.bundle = { "count":count, "images": data};
    console.log("Results " + count);
    next(); // Don't forget to call next!
});

Image.register(router,'/images');

// Return router
module.exports = router;
