
define([],
       function() {
           var DataSetCollection = Backbone.Collection.extend(
               {
                   initialize: function() {
										   console.log(this);
                   }
               }
           );
           
           return DataSetCollection;
       }
      );
