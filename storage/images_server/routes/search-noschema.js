/**
 * Created by dido on 7/14/16.
 */
"use strict";
var express = require('express');
var router = express.Router();
var Image = require('../models/image-noschema');


//method for looking if a string is in a list
String.prototype.inList = function (list) {
    return ( list.indexOf(this.toString()) != -1)
};

// all the parameters that are note a binary versions
// var listParameters=['sort','select', 'limit', 'size', 'size_lt', 'size_gt', 'pulls', 'pulls_lt','pulls_gt', 'stars', 'stars_lt','stars_gt', 'page'];

// GET /search
router.get('/', function (req, res, next) {

    console.log("GET " + req.originalUrl);

    // query for retrieve the images with binary name and versions
    //var findMatch = {'description': { }};
      var findMatch = {'description': { }};
  //  var numberBins = 0;

    for (var key in req.query) {
        //if(!key.inList(listParameters)) {  // get all the name and version parameters
            //elementMatch = {$elemMatch: {bin: key, ver: {$regex: '^' + req.query[key]}}};
        console.log(key+"  " +req.query[key])
   //findMatch.description.$all.push({$elemMatch: {mio: req.query[key]}});
      findMatch.description[key] = req.query[key] // .$all.push({$elemMatch: { k : req.query[key]}});
        console.log(findMatch.description )
        //findMatch.description[key] 
        //  delete req.query.key;
    }
    //##########################################################################

    if(req.query['size']) {
        findMatch.size = {$eq : req.query['size']}
        //queryBuild.where('size', req.query['size']);
        console.log("Size equal " + req.query['size']);
    }
    else if(req.query['size_lt']) {
        findMatch.size = {$lt : req.query['size_lt']}
        //queryBuild.where('size').lt(req.query['size_lt']);
        console.log("Size less than " + req.query['size_lt']);
    }
    else if(req.query['size_gt']) {
        findMatch.size = {$gt : req.query['size_gt']}
        //queryBuild.where('size').gte(req.query['size_gt']);
        //queryBuild.where('size').gt(req.query['size_gt']);
        console.log("Size greater than or equal " + req.query['size_gt']);
    }

    if(req.query['pulls']) {
        //queryBuild.where('pulls', req.query['pulls']);
        findMatch.pulls = {$eq : req.query['pulls']}
        console.log("Pulls equal" + req.query['pulls']);
    }
    else if(req.query['pulls_lt']) {
        findMatch.pulls = {$lt: req.query['pulls_lt']}
        //queryBuild.where('pulls').lt(req.query['pulls_lt']);
        console.log("Pulls less than " + req.query['pulls_lt']);
    }
    else if(req.query['pulls_gt']) {
        findMatch.pulls = {$gt: req.query['pulls_gt']}
        // TODO grater than or equal in the API
        //queryBuild.where('pulls').gt(req.query['pulls_gt']);
        //queryBuild.where('pulls').gte(req.query['pulls_gt']);
        console.log("Pulls greater than or equal" + req.query['pulls_gt']);
    }
    if(req.query['stars']) {
        findMatch.stars = {$eq: req.query['stars']}
        //queryBuild.where('stars', req.query['stars']);
        console.log("Stars equal" + req.query['stars']);
    }
    else if(req.query['stars_lt']) {
        findMatch.stars = {$lt: req.query['stars_lt']}
      //  queryBuild.where('stars').lt(req.query['stars_lt']);
        console.log("Stars less than " + req.query['stars_lt']);
    }
    else if(req.query['stars_gt']) {
      findMatch.stars = {$gt: req.query['stars_gt']}
        // TODO grater than or equal in the API
      //  queryBuild.where('stars').gte(req.query['stars_gt']);
        console.log("Stars greater than or equal" + req.query['stars_gt']);
    }

    var sort = {};
    switch(req.query.sort){
        case 'stars':
            console.log("Sorting  by ascending stars.");
            //queryBuild.sort({'stars': -1});
            sort =  {'stars': -1};
            break;
        case '-stars':
            console.log("Sorting  by descending stars.");
            //queryBuild.sort({'stars': 1});
            sort =  {'stars': 1};
            break;
        case 'pulls':
            console.log("Sorting  by ascending pull.");
            //queryBuild.sort({ 'pulls': -1});
            sort = { 'pulls': -1};
            break;
         case '-pulls':
            console.log("Sorting  by descending pull.");
            //queryBuild.sort({'pulls': 1});
            sort = { 'pulls': 1};
            break;
        default:
            var ordering = '-stars -pulls';  //-pull_count
            console.log("DEFAULT ordering "+ordering);
          //  queryBuild.sort(ordering);
            sort =  ordering
            break;
      }

      // if(req.query['select']) {
      //     //queryBuild.where('pulls', req.query['pulls']);
      //     findMatch.pulls = {$eq : req.query['pulls']}
      //     console.log("Pulls equal" + req.query['pulls']);
      // }

    var options = {
        select: (req.query.select)?req.query.select: '',
        sort: sort,
        //populate: 'author',
        //lean: true,
        page: (req.query.page)?Number(req.query.page): 1,
        limit: (req.query.limit)?Number(req.query.limit): 20
      };

    Image.paginate(findMatch, options, function(err, result) {
      if (err) {
              console.log(err);
              return next(err);
          }
      // result.docs
      // result.total
      // result.limit
      // result.page
      // result.pages
      //  "limit":result.limit,

      res.json({"count": result.total,
                "page":result.page,
                "limit":result.limit,
                "pages":result.pages,
                "images": result.docs
              });
      console.log("Total Results: " + result.total)
});
    //#########################################################################
    /*
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

    if(req.query['page']) {
          console.log("Page " + req.query.page);
    }

    //before the sort
    queryBuild.limit(2);

    switch(req.query.sort){
        case 'stars':
            console.log("Sorting  by ascending stars.");
            queryBuild.sort({'stars': -1});
            break;
        case '-stars':
            console.log("Sorting  by descending stars.");
            queryBuild.sort({'stars': 1});
            break;
        case 'pulls':
            console.log("Sorting  by ascending pull.");
            queryBuild.sort({ 'pulls': -1});
            break;
         case '-pulls':
            console.log("Sorting  by descending pull.");
            queryBuild.sort({ 'pulls': 1});
            break;
        default:
            var ordering = '-stars -pulls';  //-pull_count
            console.log("DEFAULT ordering "+ordering);
            queryBuild.sort(ordering);
            break;
      }

     // total number of results of the query
     var count = queryBuild.count()

     console.log("With limit query:" + count);

    // execute the query (before the limit execution) for the total number of images tht satisfy the query
    queryBuild.exec(function(err,results){
      if (err) {
          console.log(err);
          return next(err);
      }
      console.log(results)
     count = results.length
      console.log("executed fist query:" + count);
    }); //executed

    console.log("executing the second query")
    // //limit: return only from the limit to the end
    if(req.query.page) {
          console.log("Limit page " + req.query.page);
          perPage = 2
         //       .limit(perPage)
        //  queryBuild.skip(perPage * page);
          queryBuild.limit(perPage);
              console.log("Settedn limit parameter")
          //limit(perPage)
          // .skip(perPage * page)
    }

    queryBuild.exec(function(err, results){
      if (err) {
          console.log(err);
          return next(err);
      }

     var count2 = results.length
     console.log("Second query with limit pr page :" + count2);
    });
*/
    ///users/?limit=5 will give you the first 5 items
    // var perPage = 10, page = Math.max(0, Number(req.query.page))
    // if(req.query['page']) {
    //       console.log("Page " + req.query.page);
    //       queryBuild
    //       .skip(page)
    //       .limit(perPage);
    // }
    //
    // .select('name')
    // .limit(perPage)
    // .skip(perPage * page)
    // .sort({
    //     name: 'asc'
    // })
    // .exec(function(err, events)

    //execution of the query
    // queryBuild.exec(function (err, results) {
    //     if (err) {
    //         console.log(err);
    //         return next(err);
    //     }
    //
    //     //console.log(JSON.stringify(img, null, 4));
    //     console.log("After limit:" + count);
    //     //res.json({"count": /*number of images that sadisfy the query*/results.length, "images": results});
    //     res.json({"count": count, "images": results});
    //     console.log("Results " + results.length)
    //
    // });

});


// Return router
module.exports = router;
