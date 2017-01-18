var express = require('express');
var router = express.Router();

// Models
var Software = require('../models/software')

// record all the methods
Software.methods(['get','put','post','delete']);//.updateOptions({ new: true });

Software.after('get', function(req, res, next) {
    console.log(res.locals.bundle)
    var count = res.locals.bundle.length;
    var data = res.locals.bundle;
    res.locals.bundle = {"count": count, "software": data};
    console.log("Number of software returned: "+ count);
    next(); // Don't forget to call next!
});

// GET /api/software
// GET /api/software/:id
// POST /api/software
// PUT /api/software/:id
// DELETE /api/software/:id

Software.register(router,'/software');

module.exports = router;
