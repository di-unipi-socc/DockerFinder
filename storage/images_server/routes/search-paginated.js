/**
 * Created by dido on 7/14/16.
 */
"use strict";
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
    var sort = {};
    var addMatch = (key, value, op) => {
        findMatch[value] = {};
        findMatch[value][op] = req.query[key];
        console.log("Size less than equal " + req.query[key]);
    };

    for (var key in req.query) {
        switch (key) {
            case 'sort':
                switch (req.query.sort) {
                    case 'stars':
                        console.log("Sorting  by ascending stars.");
                        sort = {'stars': -1};
                        break;
                    case '-stars':
                        console.log("Sorting  by descending stars.");
                        sort = {'stars': 1};
                        break;
                    case 'pulls':
                        console.log("Sorting  by ascending pull.");
                        sort = {'pulls': -1};
                        break;
                    case '-pulls':
                        console.log("Sorting  by descending pull.");
                        sort = {'pulls': 1};
                        break;
                    default:
                        var ordering = '-stars -pulls'; //-pull_count
                        console.log("DEFAULT ordering " + ordering);
                        sort = ordering;
                        break;
                }
                break;
            case 'size':
                addMatch(key, '$eq', 'size');
                break;
            case 'size_lt':
                addMatch(key, '$lt', 'size');
                break;
            case 'size_gt':
                addMatch(key, '$gt', 'size');
                break;
            case 'size_lte':
                addMatch(key, '$lte', 'size');
                break;
            case 'size_gte':
                addMatch(key, '$gte', 'size');
                break;
            case 'pulls':
                addMatch(key, '$eq', 'pulls');
                break;
            case 'pulls_lt':
                addMatch(key, '$lt', 'pulls');
                break;
            case 'pulls_gt':
                addMatch(key, '$gt', 'pulls');
                break;
            case 'pulls_lte':
                addMatch(key, '$lte', 'pulls');
                break;
            case 'pulls_gte':
                addMatch(key, '$gte', 'pulls');
                break;
            case 'stars':
                addMatch(key, '$eq', 'stars');
                break;
            case 'stars_lt':
                addMatch(key, '$lt', 'stars');
                break;
            case 'stars_gt':
                addMatch(key, '$gt', 'stars');
                break;
            case 'stars_lte':
                addMatch(key, '$lte', 'stars');
                break;
            case 'stars_gte':
                addMatch(key, '$gte', 'stars');
                break;
            default:
                if (!findMatch.softwares) findMatch.softwares = {$all: []};
                findMatch.softwares.$all.push({
                    $elemMatch: {
                        software: key,
                        ver: {
                            $regex: '^' + req.query[key]
                        }
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
        console.log("Total Results: " + result.total)
    });
});

// Return router
module.exports = router;
