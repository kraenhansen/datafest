require.config({
    urlArgs: "bust="+(new Date()).getTime(),
    paths: {
        text: 'vendor/text'
    }
});

require(
    ['router', 'views/dataset.view'],
    
    function(DatafestRouter, DataSetView) {
        console.log('app initialized');

        // Fire up the app
        // Do stuff when DOM is ready
        $(function() {
            var view = new DataSetView();
            var router = new DatafestRouter(view);
            
            $("body").append(view.$el);
            
            $("input:text").live('focus', function(el) {
                $(this).select();
                $(this).addClass('active');
            });
            
            $("input:text").live('blur', function(el) {
                $(this).removeClass('active');
            });
            
            $("input:text").live('mouseup', function(ev) {
                return false;
            });

            Backbone.history.start({});
        });
    }
);