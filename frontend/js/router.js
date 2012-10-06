define(
    function() {
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
                    this.view.reset(id);
                }
            }
        );
        
        return DatafestRouter;
    }
);