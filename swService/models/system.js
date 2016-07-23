/**
 * Created by dido on 7/13/16.
 */
var restful = require('node-restful')
var mongoose = restful.mongoose;

// Schema
var systemSchema =  new mongoose.Schema({
    cmd: String,        // command to search OS or other system configuration
    regex: String       // regex: regular expression for parsing the result
});

// Return a model
module.exports = restful.model("System",systemSchema);
// Return router
