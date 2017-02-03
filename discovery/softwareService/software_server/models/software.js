/**
 * Created by dido on 7/13/16.
 */
var restful = require('node-restful')
var mongoose = restful.mongoose;



var softwareSchema =  new mongoose.Schema({
    name: {
        type: String,               // python    | python2    | python3
        //required :[true, 'The name of the software cannot be empty'],
        unique: true
    },
    cmd: String,                  // --version
    regex: String                // regex: regular expression for parsing the result
});


// // schema of command
// var softwareSchema =  new mongoose.Schema({
//        cmd: String,      //python --version
//        regex: String,    //[0-9]+[0-9]
//        tag : {type: String, unique:true},      //python
//        type : String   ,   // run, inspect,....
//      }
// );

// Return a model
module.exports = restful.model("Software",softwareSchema);
//module.exports = restful.model("Run",runSchema);
// Return router
