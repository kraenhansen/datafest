define(
    ['collections/dataset.collection'],
    function(DataSetCollection) {
        var DatafestRouter = Backbone.Router.extend(
            {
                view: null,
                routes: {
                    "dataset/:id": "loadDataset",
                    "": "hideDataset"
                },
                initialize: function(view) {
                    this.view = view;
                },
                loadDataset: function(id) {
                    console.log('loading dataset '+id);

                    var model = null;
                    $.getJSON(
                        'testSet.json', 
                        _.bind(function(data) { 
                            model = new Backbone.Model(data);
                            
                            var records = new DataSetCollection(data.records);
                            $("#datasets_table").hide();
                            this.view.reset(model);
                        }, this)
                    );
                },
                hideDataset: function() {
                    console.log('hide');
                    $("#datasets_table").show();
                    this.view.hide();
                }
            }
        );

        return DatafestRouter;
    }
);
