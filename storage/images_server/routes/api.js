"use strict";
var express = require('express');
var router = express.Router();
var Image = require('../models/image');

// record all the methods
Image.methods(['get', 'put', 'post', 'delete']).updateOptions({
  new: true
});

// GET /api/images
Image.after('get', function(req, res, next) {
  res.setHeader('Content-Type', 'application/json');
  var count = res.locals.bundle.length;
  var data = res.locals.bundle;

  var total = req.query.total;
  //console.log("path" + req.query);
  // console.log("Results " + count);
  if (total === 'true') {
    console.log("Total="+count +" images")
    res.locals.bundle = {
      "count": count
    };
  } else {
    console.log("Return "+count+" images ")
    res.locals.bundle = {
      "count": count,
      "images": data
    };
  }

  next(); // Don't forget to call next!
});

Image.register(router, '/images');

// Return router
module.exports = router;
