"use strict"
var restful = require('node-restful')
var mongoose = restful.mongoose;


// Schema
// var imageSchema =  new mongoose.Schema({
//     repo_name:      {
//         type:       String,
//         unique:     true,
//         required    :[true, 'The name of the image cannot be empty']
//     },
//     tag : String,
//     last_scan:      Date,
//     last_updated:   Date,  // time of the last updated of the repo in the docker hub
//     size:      Number,
//     stars:     {
//         type:       Number,
//         min:        [0, 'stars must be positive number']
//     },
//     pulls:     Number,
//     description:    String,
//     distro:     String,
//     softwares:       [{
//         _id: false,
//         software: String,
//         ver: String
//     }]
//
// });

var imageSchema =  new mongoose.Schema({

    // Docker tag information
    name:      { // <repo:tag>
        type:       String,
        unique:     true,
        required    :[true, 'The name of the image cannot be empty']
    },
    id_tag: Number,
    last_scan:      Date,
    last_updated:   Date,  // time of the last updated of the repo in the docker hub
    size:      Number,
    repository: Number,
    creator: Number,

    //Docker repository informations
    user:String,
    stars:     {
        type:       Number,
        min:        [0, 'stars must be positive number']
    },
    pulls:     Number,
    description:    String,
    is_automated: Boolean,
    is_private: Boolean,

    //Docker Finedr added info
    distro:     String,
    softwares:       [{
        _id: false,
        software: String,
        ver: String
    }],

    inspect_info:  mongoose.Schema.Types.Mixed

});


// Return a model
module.exports = restful.model("Images",imageSchema);
