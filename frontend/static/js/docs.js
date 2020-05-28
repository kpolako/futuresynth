$(function(){
    $('#results_docs').hide();
    $('#metrics_docs').hide();

    $("#menu_test_type").bind("click", function() {
        $('#results_docs').fadeOut(300, function(){ $(this).hide();});
        $('#metrics_docs').fadeOut(300, function(){ $(this).hide();});
        $(".content_div").fadeIn(300, function() {
            var html = $('#test_type_docs');
            setTimeout(function(){$(html).hide().appendTo(".content_div").fadeIn(300);}, 300);
        });
    });
    $("#menu_metrics").bind("click", function() {
        $('#results_docs').fadeOut(300, function(){ $(this).hide();});
        $('#test_type_docs').fadeOut(300, function(){ $(this).hide();});
        $(".content_div").fadeIn(300, function() {
            var html = $('#metrics_docs');
            setTimeout(function(){$(html).hide().appendTo(".content_div").fadeIn(300);}, 300);
        });
    });
    $("#menu_results").bind("click", function() {
        $('#metrics_docs').fadeOut(300, function(){ $(this).hide();});
        $('#test_type_docs').fadeOut(300, function(){ $(this).hide();});
        $(".content_div").fadeIn(300, function() {
            var html = $('#results_docs');
            setTimeout(function(){$(html).hide().appendTo(".content_div").fadeIn(300);}, 300);
        });
    });
});

$(function(){
    $(".metric_desc").hide();

    $(".metric_link").bind("click", function() {
        var classList = this.className.split(/\s+/);
        var theClass = "";
        console.log(classList);
        classList.forEach(function(aclass) {
            if (aclass != "metric_link") {
                theClass = aclass
            }
        });
        $(".metric_desc").hide();
        $("."+theClass).show();
    });
});