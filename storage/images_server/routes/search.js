/**
 * Created by dido on 7/14/16.
 */
"use strict";
var express = require('express');
var router = express.Router();
var Image = require('../models/image');

//method for looking if a string is in a list
String.prototype.inList = function (list) {
    return ( list.indexOf(this.toString()) != -1)
};

//al the parameters that are note a binary versions
var listParameters=['sort', 'limit', 'size', 'size_lt', 'size_gt', 'pulls', 'pulls_lt','pulls_gt', 'stars', 'stars_lt','stars_gt'];

// GET /search
router.get('/', function (req, res, next) {

    console.log("GET " + req.originalUrl);

    // query for retrieve the images with binary name and versions
    var findMatch = {'softwares': {$all: []}};
    var numberBins = 0;

    for (var key in req.query) {
        if(! key.inList(listParameters)) {  // get all the name and version parameters
            //elementMatch = {$elemMatch: {bin: key, ver: {$regex: '^' + req.query[key]}}};
            findMatch.softwares.$all.push({$elemMatch: {software: key, ver: {$regex: '^' + req.query[key]}}});
            numberBins +=1;
            delete req.query.key;
        }
    }
    //var query
    var queryBuild = Image.find(findMatch);
    // if(numberBins > 0)
    //     query = Image.find(findMatch);
    // else
    //     query = Image.find()

    if(req.query['size']) {
        queryBuild.where('size', req.query['size']);
        console.log("Size equal " + req.query['size_lt']);
    }
    else if(req.query['size_lt']) {
        queryBuild.where('size').lt(req.query['size_lt']);
        console.log("Size less than " + req.query['size_lt']);
    }
    else if(req.query['size_gt']) {
            // TODO grater than or equal in the API
        queryBuild.where('size').gte(req.query['size_gt']);
        //queryBuild.where('size').gt(req.query['size_gt']);
        console.log("Size greater than or equal " + req.query['size_gt']);
    }

    if(req.query['pulls']) {
        queryBuild.where('pulls', req.query['pulls']);
        console.log("Pulls equal" + req.query['pulls']);
    }
    else if(req.query['pulls_lt']) {
        queryBuild.where('pulls').lt(req.query['pulls_lt']);
        console.log("Pulls less than " + req.query['pulls_lt']);
    }
    else if(req.query['pulls_gt']) {
        // TODO grater than or equal in the API
        queryBuild.where('pulls').gt(req.query['pulls_gt']);
        //queryBuild.where('pulls').gte(req.query['pulls_gt']);
        console.log("Pulls greater than or equal" + req.query['pulls_gt']);
    }
    if(req.query['stars']) {
        queryBuild.where('stars', req.query['stars']);
        console.log("Stars equal" + req.query['stars']);
    }
    else if(req.query['stars_lt']) {
        queryBuild.where('stars').lt(req.query['stars_lt']);
        console.log("Stars less than " + req.query['stars_lt']);
    }
    else if(req.query['stars_gt']) {
        // TODO grater than or equal in the API
        queryBuild.where('stars').gte(req.query['stars_gt']);
        console.log("Stars greater than or equal" + req.query['stars_gt']);
    }
      if(req.query.limit) {
        console.log("Limit " + req.query.limit);
        queryBuild.limit(Number(req.query.limit));
    }

    switch(req.query.sort){
        case 'stars':
            console.log("Sorting  by ascending stars");
            queryBuild.sort({'stars': -1});
            break;
        case '-stars':
            console.log("Sorting  by descending stars");
            queryBuild.sort({'stars': 1});
            break;
        case 'pulls':
            console.log("Sorting  by ascending pull");
            queryBuild.sort({ 'pulls': -1});
            break;
         case '-pulls':
            console.log("Sorting  by descending pull");
            queryBuild.sort({ 'pulls': 1});
            break;
        default:
            var ordering = '-stars -pulls';  //-pull_count
            console.log("DEFAULT ordering "+ordering);
            queryBuild.sort(ordering);
            break;
}

    //execution of the query
    queryBuild.exec(function (err, results) {
        if (err) {
            console.log(err);
            return next(err);
        }

        // console.log(JSON.stringify(img, null, 4));
        res.json({"count": /*number of images that sadisfy the query*/results.length, "images": results});
        console.log("Results " + results.length)

    });

});


// Return router
module.exports = router;
