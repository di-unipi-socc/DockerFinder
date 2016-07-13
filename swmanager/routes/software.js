var express = require('express');
var router = express.Router();

// Models
var Software = require('../models/software')

// record all the methods
Software.methods(['get','put','post','delete']).updateOptions({ new: true });

Software.register(router,'/software');

module.exports = router;
