//dependencies
var restful = require('node-restful')
var mongoose = restful.mongoose;


// Schema
var imageSchema =  new mongoose.Schema({
  repo_name:{type: String,  unique : true},
  t_scan: {
      type: Date,
      Default: Date.now
  }, 
    distro:String,
  size:{
      type:Number
  },
  bins :[{
      _id:false,
       bin : String,
       ver : String
  }]

});


// Return a model
module.exports = restful.model("Images",imageSchema)
