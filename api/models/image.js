//dependencies
var restful = require('node-restful')
var mongoose = restful.mongoose;


// Schema
var imageSchema =  new mongoose.Schema({
  //_id:{type: String},
  repo_name:{type: String},
  t_scan: {
      type: Date,
      Default: Date.now
  }, 
    distro:String,
  size:{
      type:Number
  },
  bins :[{
    bin : String,
    ver : String
  }]

});


// Return a model
module.exports = restful.model("Images",imageSchema)
