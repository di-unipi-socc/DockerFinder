var express = require('express');
var router = express.Router();

// Models
var Software = require('../models/software')

// record all the methods
Software.methods(['get','put','post','delete']);//.updateOptions({ new: true });

Software.after('get', function(req, res, next) {
  //var tmp = res.locals.bundle.title; // Lets swap the title and year fields because we're funny!
  //res.locals.bundle.title = res.locals.bundle.year;
  //res.locals.bundle.year = tmp;
    var count = res.locals.bundle.length;
    res.json({"count": count, "software": res.locals.bundle});
        console.log("Results " + count);

  next(); // Don't forget to call next!
});

// GET /api/software
// GET /api/software/:id
// POST /api/software
// PUT /api/software/:id
// DELETE /api/software/:id

Software.register(router,'/software');

module.exports = router;
