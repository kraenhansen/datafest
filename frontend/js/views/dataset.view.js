define(
    ['vendor/text!../../templates/datasetview.template'],
    function(templateText) {
        var DataSetView = Backbone.View.extend({
            id: "dataSetView",
            template: templateText,
            events: {
                "click #leftArrow": "clickHandler",
                "click #rightArrow": "clickHandler"
            },
            
            initialize: function() {
                this.render();
                var keyHandler = _.bind(this.keyHandler, this);
                $(document).bind('keyup', keyHandler);
            },
            show: function() {
                this.$el.show();
            },
            render: function() {
                var context = {
                    title: "Woot "+this.model,
                    kvTuples: [{key: "foo", value: "bar"}]
                };

                var content = _.template(this.template, context);
                this.$el.html(content);
            },
            
            // Sets a new dataset ID and renders
            reset: function(id) {
                this.model = id;
                this.render();
                this.show();
            },
            
            clickHandler: function(event) {
                if (event.currentTarget.id === "leftArrow") {
                    this.advance(-1);
                } else if (event.currentTarget.id === "rightArrow") {
                    this.advance(1);
                }
            },
            
            keyHandler: function(event) {
                if (event.ctrlKey)
                    if (event.keyCode == 39) {
                        this.advance(1);
                    } else if (event.keyCode == 37) {
                        this.advance(-1);
                    }
            },
            
            advance: function(direction) {
                console.log('advancing '+direction);
            },
            
            hide: function() {
                // Do the hiding
                
                $(document).unbind('keyup');
            }
            
        });
        
        return DataSetView;
    }
);