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
                "click #rightArrow": "clickHandler",
                "click input": "inputClickHandler"
            },
            
            initialize: function() {
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
                this.$("input:first").focus();
            },
            
            // Sets a new dataset ID and renders
            reset: function(model) {
                this.model = model;
                this.numRecords = model.get('records').length;
                
                
                var keyHandler = _.bind(this.keyHandler, this);
                $(document).unbind('keyup');
                $(document).bind('keyup', keyHandler);         
                
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
            
            inputClickHandler: function(event) {

                
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
                
                this.recordIdx = (this.recordIdx + direction + this.numRecords) % this.numRecords;
                this.render();
            },
            
            hide: function() {
                // Do the hiding
                this.$el.hide();
                $(document).unbind('keyup');
            }
            
        });
        
        return DataSetView;
    }
);
