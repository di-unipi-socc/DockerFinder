/* jshint node: true, esversion: 6 */
"use strict";

/**
 * Created by dido on 7/14/16.
 */

var express = require('express');
var router = express.Router();
var Image = require('../models/image');


//method for looking if a string is in a list
String.prototype.inList = function(list) {
    return (list.indexOf(this.toString()) != -1);
};

// GET /search
router.get('/', function(req, res, next) {

    console.log("GET " + req.originalUrl);

    // query for retrieve the images with binary name and versions
    var findMatch = {};
    var sort = {'stars': -1, 'pulls': -1};

    function addMatch(key, value, op) {
        if (!findMatch[value]) findMatch[value] = {};
        findMatch[value][op] = req.query[key];
        console.log(value + " " + op + " " + req.query[key]);
    }
    function parseSort(value) {
        if (value[0] == '-')
            return [value.substring(1), 1];
        else
            return [value, -1];
    }

    for (var key in req.query) {
        switch (key) {
            case 'sort':
                sort = {};
                console.log('Sorting by', req.query.sort);
                switch (req.query.sort) {
                    case 'stars':
                    case '-stars':
                    case 'pulls':
                    case '-pulls':
                    case 'size':
                    case '-size':
                        var [value, order] = parseSort(req.query.sort);
                        sort[value] = order;
                        break;
                    default:
                        req.query.sort.forEach((k) => {
                            var [value, order] = parseSort(k);
                            sort[value] = order;
                        });
                }
                break;
            case 'size':
                addMatch(key, 'size', '$eq');
                break;
            case 'size_lt':
                addMatch(key, 'size', '$lt');
                break;
            case 'size_gt':
                addMatch(key, 'size', '$gt');
                break;
            case 'size_lte':
                addMatch(key, 'size', '$lte');
                break;
            case 'size_gte':
                addMatch(key, 'size', '$gte');
                break;
            case 'pulls':
                addMatch(key, 'pulls', '$eq');
                break;
            case 'pulls_lt':
                addMatch(key, 'pulls', '$lt');
                break;
            case 'pulls_gt':
                addMatch(key, 'pulls', '$gt');
                break;
            case 'pulls_lte':
                addMatch(key, 'pulls', '$lte');
                break;
            case 'pulls_gte':
                addMatch(key, 'pulls', '$gte');
                break;
            case 'stars':
                addMatch(key, 'stars', '$eq');
                break;
            case 'stars_lt':
                addMatch(key, 'stars', '$lt');
                break;
            case 'stars_gt':
                addMatch(key, 'stars', '$gt');
                break;
            case 'stars_lte':
                addMatch(key, 'stars', '$lte');
                break;
            case 'stars_gte':
                addMatch(key, 'stars', '$gte');
                break;
            case 'distro':
                findMatch.distro = {
                    $regex: `.*${req.query[key].split(' ').join('.*')}.*`,
                    $options: 'i'
                };
                break;
            default:
                if (!findMatch.softwares) findMatch.softwares = {$all: []};
                findMatch.softwares.$all.push({
                    $elemMatch: {
                        software: key,
                        ver: {$regex: '^' + req.query[key]}
                    }
                });
                break;
            case 'select':
            case 'limit':
            case 'page':
                break;
        }
    }

    var options = {
        select: (req.query.select) ? req.query.select : '',
        sort: sort,
        page: (req.query.page) ? Number(req.query.page) : 1,
        limit: (req.query.limit) ? Number(req.query.limit) : 20
    };
    // console.log('DEBUG', JSON.stringify(findMatch), JSON.stringify(options));
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

        res.json({
            "count": result.total,
            "page": result.page,
            "limit": result.limit,
            "pages": result.pages,
            "images": result.docs
        });
        console.log("Total Results: " + result.total);
    });
});

// Return router
module.exports = router;
