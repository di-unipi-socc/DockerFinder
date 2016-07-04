//dependencies
var restful = require('node-restful')
var mongoose = restful.mongoose;


// Schema
var imageSchema =  new mongoose.Schema({
  repo_name:{type: String,  unique : true},
  last_scan:Date,
  last_updated: Date,  //last updated time in the docker hub
  start_count:Number,
  pull_count:Number,
  description:String,
  distro:String,
  size:Number,
  bins :[{
      _id:false,
       bin : String,
       ver : String
  }]

});


// Return a model
module.exports = restful.model("Images",imageSchema)
