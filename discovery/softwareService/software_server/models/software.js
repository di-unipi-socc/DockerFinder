/**
 * Created by dido on 7/13/16.
 */
var restful = require('node-restful')
var mongoose = restful.mongoose;

// // Schema
// var softwareSchema =  new mongoose.Schema({
//     name: {
//         type: String,
//         unique: true,
//         required :[true, 'The name of the software cannot be empty']
//     },
//     alias: [{
//         _id: false,
//         software: String,             // python    | python2    | python3
//         cmd: String,                  // --version | --version  | --version
//         regex: String,                // regex     | regex      | regex
//     }]
// });

// Schema
var softwareSchema =  new mongoose.Schema({
    name: {
        type: String,               // python    | python2    | python3
        //required :[true, 'The name of the software cannot be empty'],
        unique: true
    },
    cmd: String,                  // --version
    regex: String                // regex: regular expression for parsing the result
});

// Return a model
module.exports = restful.model("Software",softwareSchema);
// Return router
