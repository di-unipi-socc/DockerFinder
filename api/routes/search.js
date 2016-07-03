var express = require('express');
var router = express.Router();
var Image = require('../models/image');

//methodd for looking if a string is in a list
String.prototype.inList = function (list) {
    return ( list.indexOf(this.toString()) != -1)
};

//al the parameters that are note a binary
listParameters=[,'limit', 'size', 'size_lt', 'size_gt', 'pulls', 'pulls_lt','pulls_gt'];

// /search
router.get('/', function (req, res, next) {

    console.log("GET " + req.originalUrl);

    // query for retriving the images starting from the  binary and the versions
    findMatch = {'bins': {$all: []}};

    for (key in req.query) {

        // if (key.localeCompare("size") == 0) {
        //     listParameters.size = req.query.size;
        //     delete req.query.size;
        // }
        // if (key.localeCompare("size_gt") == 0) {
        //     listParameters.size = req.query.size;
        //     delete req.query.size;
        // }
        // if (key.localeCompare("size_lt") == 0) {
        //     listParameters.size = req.query.size;
        //     delete req.query.size;
        // }
        // if (key.localeCompare("pulls") == 0) {
        //     listParameters.size = req.query.size;
        //     delete req.query.size;
        // }
        // if (key.localeCompare("pulls_gt") == 0) {
        //     listParameters.size = req.query.size;
        //     delete req.query.size;
        // }
        // if (key.localeCompare("pulls_lt") == 0) {
        //     listParameters.size = req.query.size;
        //     delete req.query.size;
        // }
        if(! key.inList(listParameters)) {
            elementMatch = {$elemMatch: {bin: key, ver: {$regex: '^' + req.query[key]}}};
            findMatch.bins.$all.push(elementMatch);
            delete req.query.key;
        }
    }

    var query = Image.find(findMatch);


    if(req.query['size']) {
        query.where('size', req.query['size']);
        console.log("Less than size " + req.query['size_lt']);
    }
    if(req.query['size_lt']) {
        query.where('size').lt(req.query['size_lt']);
        console.log("Equal ize " + req.query['size']);
    }
     if(req.query['size_gt']) {
        query.where('size').gt(req.query['size_gt']);
        console.log("Greater than size " + req.query['size_gt']);
    }

    if(req.query.limit) {
        console.log("Limit " + req.query.limit);
        query.limit(Number(req.query.limit));
    }
    //query.limit
    query.exec(function (err, img) {
        if (err) {
            console.log(err);
            return next(err);
        }

        // console.log(JSON.stringify(img, null, 4));
        res.json({"count": img.length, "images": img});
        console.log("Results " + img.length)

    });

});


// Return router
module.exports = router;
