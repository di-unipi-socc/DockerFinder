var mongoose = require('mongoose');


//create a schema (every time is Schema: properties of object)
var MovieSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  url: {
    type: String,
    required: true
  }
});

// Export the model.
module.exports = mongoose.model('movie', MovieSchema);
