define(
    ['collections/dataset.collection'],
    function(DataSetCollection) {
        var DatafestRouter = Backbone.Router.extend(
            {
                view: null,
                routes: {
                    "dataset/:id": "loadDataset"
                },
                initialize: function(view) {
                    this.view = view;
                },
                loadDataset: function(id) {
                    console.log('loading dataset '+id);

                    var model = null;
                    $.getJSON(
                        '/datafest/testSet.json', 
                        _.bind(function(data) { 
                            model = new Backbone.Model(data);
                            
                            var records = new DataSetCollection(data.records);
                            
                            this.view.reset(model);
                        }, this)
                    );
                }
            }
        );

        return DatafestRouter;
    }
);