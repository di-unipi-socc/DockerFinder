//dependencies
var restful = require('node-restful')
var mongoose = restful.mongoose;


// Schema
var imageSchema =  new mongoose.Schema({
  repo_name:{type: String,  unique : true},
  last_scan:Date,
  last_updated: Date,  // time of the last updated of the repo  in the docker hub
  full_size: Number,
  star_count:{type: Number, min:0 },
  pull_count:Number,
  description:String,
  distro:String,
  bins :[{
      _id:false,
       bin : String,
       ver : String
  }]

});


// Return a model
module.exports = restful.model("Images",imageSchema)
