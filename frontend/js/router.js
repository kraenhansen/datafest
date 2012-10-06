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

									  var tastypieModel = new Backbone.Collection();
   									tastypieModel.url = '/api/dataset/1/record/?format=json';
									  tastypieModel.fetch({
											success: _.bind(function (data) {
												this.view.reset(data.at(0).attributes.objects);
											}, this)});
									  
                    var model = null;
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
