var express = require('express')
var router = express.Router();
var Image = require('../models/image')

//methodd for looking if a string is in a list
String.prototype.inList=function(list){
   return ( list.indexOf(this.toString()) != -1)
}

listParameters = {'size':null,'size_lt':null,'size_gt':null,'pulls':null,'pulls_lt':null,'pulls_gt':null}


// /search
router.get('/', function (req, res, next) {
    // {$elemMatch: {bin: 'curl', ver: {$regex: '^' + '7'}}}
    console.log("Request received: " +req.originalUrl)
    findMatch= {'bins':{$all:[]}};

    for(key in req.query) {
        if (key.localeCompare("size") == 0){
            listParameters.size = req.query.size;
            delete req.query.size;
        }
        if (key.localeCompare("size_gt") == 0){
            listParameters.size = req.query.size;
            delete req.query.size;
        }
        if (key.localeCompare("size_lt") == 0){
            listParameters.size = req.query.size;
            delete req.query.size;
        }
        if (key.localeCompare("pulls") == 0){
            listParameters.size = req.query.size;
            delete req.query.size;
        }
        if (key.localeCompare("pulls_gt") == 0){
            listParameters.size = req.query.size;
            delete req.query.size;
        }
        if (key.localeCompare("pulls_lt") == 0){
            listParameters.size = req.query.size;
            delete req.query.size;
        }
        elementMatch ={$elemMatch: {bin: key, ver: {$regex: '^'+req.query[key]}}};
        findMatch.bins.$all.push(elementMatch);
       // elementMatch.$elemMatch.bin = ;
        //elementMatch.$elemMatch.ver = ;
        // if (key.inList(listParameters)) {
        //     console.log('found' + req.query[key])
        //     delete req.query.size;
        // }
    }
    console.log(findMatch)
    var query = Image.find(findMatch);

    // var query = Image.find({
    //     'bins': {
    //         $all: [ {$elemMatch: {bin: 'curl', ver: {$regex: '^' + '7'}}},
    //             {$elemMatch: {bin: 'python', ver: {$regex: '^' + '2'}}}
    //         ]
    //     }
    // });


    query.where('size').gte(600000000);
    //query.limit
    r = query.exec(function (err, img) {
        if (err) {
            console.log(err);
            return next(err);
        }

        console.log(JSON.stringify(img, null, 4));
        res.json({"count": img.length ,"images" :img})

    });

});


// Return router
module.exports = router;
