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
  t_crawl: {
      type: Date,
      Default: Date.now
  },
  size:{
      type:Number
  },
  hub :{
    type: String,
    get: function(data) {
      try {
        return JSON.parse(data);
      } catch(exception) {
        return data;
      }
    },
    set: function(data) {
      return JSON.stringify(data);
    }
  },
  bins : {
      type: [String]
  },
  distro:String
  /*
   repo_name_tag = StringField(required=True, primary_key=True) #name:tag
    t_scan = DateTimeField(default=datetime.datetime.utcnow)
    t_crawl = DateTimeField(default=None )
    #layers = ListField(StringField(max_length=50))  #sha256 layers IDs
    size = StringField()
    hub = EmbeddedDocumentField(Hub)        # docker hub info
    bins = ListField(EmbeddedDocumentField(Bin))  # pyfinder results
    distro = StringField()
   */
});


// Return a model
module.exports = restful.model("Images",imageSchema)
