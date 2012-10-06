define(
    ['vendor/text!../../templates/datasetview.template'],
    function(templateText) {
        var DataSetView = Backbone.View.extend({
            id: "dataSetView",
            template: templateText,
            recordIdx: 0,
            numRecords: 5,
            events: {
                "click #leftArrow": "clickHandler",
                "click #rightArrow": "clickHandler"
            },
            
            initialize: function() {
                var keyHandler = _.bind(this.keyHandler, this);
                $(document).bind('keyup', keyHandler);
            },
            show: function() {
                this.$el.show();
            },
            render: function() {
                var context = {
                    title: this.model.get('title'),
                    tuple: this.model.get('records')[this.recordIdx]
                };

                var content = _.template(this.template, context);
                this.$el.html(content);
            },
            
            // Sets a new dataset ID and renders
            reset: function(model) {
                this.model = model;
                this.numRecords = model.get('records').length;
                
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
                
                this.recordIdx = (this.recordIdx + direction) % this.numRecords;
                this.render();
            },
            
            hide: function() {
                // Do the hiding
                
                $(document).unbind('keyup');
            }
            
        });
        
        return DataSetView;
    }
);