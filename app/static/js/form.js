$(function(){
    $("#submit_test").bind("click", function() {
        $('#form_div').fadeOut(300, function(){ $(this).remove();});

        $(".content_div").fadeIn(1500, function() {
            var contentDiv = document.getElementById('content_div');
            var html = '<svg id="triangle" width="175px" height="175px" viewBox="-3 -4 39 39"><polygon fill="#ffb200" fill-opacity="0" stroke="#00ffff" stroke-width="0.5" points="16,0 32,32 0,32"></polygon></svg>';
            setTimeout(function(){
                $(html).hide().appendTo(".content_div").fadeIn(1500);
            }, 300);

        });
        var jsonData = {};
        var device = "";

        var ifChecked = document.getElementById("togBtn-device").checked;
        if (ifChecked == true) {
            device = "mobile";
        } else {
            device = "desktop";
        }
        var testType = "";
        var ifChecked = document.getElementById("togBtn-testtype").checked;
        if (ifChecked == true) {
            testType = "selenium";
        } else {
            testType = "lighthouse";
        }

        var inputUrl = $("#input-url").val();
        jsonData = {
            "url": inputUrl,
            "device": device,
            "type": testType
        };

        var request = $.ajax({
            type: "POST",
            url: "/receive_test",
            data: JSON.stringify(jsonData),
            headers: {'Content-type': 'application/json'},
        });
        request.done(function(data){
            console.log(data);
            console.log(data.dom_content_loaded);

            $('#triangle').fadeOut(300, function(){ $(this).remove();});

            $(".content_div").fadeIn(1500, function() {
            var contentDiv = document.getElementById('content_div');

            var obj = "text/json;charset=utf-8," + encodeURIComponent(data['report']);
            var download_html = '<a href="data:' + obj + '" download="lighthouse_report.json">Download ' + data['description'] + ' report</a><br>';

            var html = '<div style="margin-left: 2%; margin-top: 2%; margin-bottom: 2%; display: inline-block; width: 48%; vertical-align: top;">';
            html += download_html;

            for (var key in data['metrics']) {
                if (data['metrics'].hasOwnProperty(key)) {
                    console.log(data['metrics'][key]['name'] + " -> " + data['metrics'][key]['value']);
                    html += ''+data['metrics'][key]['name']+': '+data['metrics'][key]['value']+'<br>';
                }
            }

            html += '</div>';

            setTimeout(function(){
                $(html).hide().appendTo(".content_div").fadeIn(1500);}, 300);
            });
        });
    });
});
