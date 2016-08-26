var express = require('express');
var router = express.Router();

// Models
var System = require('../models/system')

// record all the methods
System.methods(['get','put','post','delete']);//.updateOptions({ new: true });

System.after('get', function(req, res, next) {

    var count = res.locals.bundle.length;
    res.json({"count": count, "system": res.locals.bundle});
    console.log("Results " + count);
    next(); // Don't forget to call next!
});

// GET /api/system
// GET /api/system/:id
// POST /api/system
// PUT /api/system/:id
// DELETE /api/system/:id

System.register(router,'/system');

module.exports = router;
