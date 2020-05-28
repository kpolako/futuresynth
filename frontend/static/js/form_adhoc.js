$(function(){
    $("#submit_test").bind("click", function() {

        var formVal = formValidation();

        if (formVal === null || formVal === false) {
            return;
        }

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

        var testType = $('input[name=testtype]:checked').val();

        var inputUrl = $("#input-url").val();
        jsonData = {
            "url": inputUrl,
            "device": device,
            "type": testType
        };

        var request = $.ajax({
            type: "POST",
            url: "http://127.0.0.1:4999/execute_test_run",
            data: JSON.stringify(jsonData),
            headers: {'Content-type': 'application/json'},
        });
        request.done(function(data){
            $('#triangle').fadeOut(300, function(){ $(this).remove();});

            $(".content_div").fadeIn(1500, function() {
            var contentDiv = document.getElementById('content_div');
            var html = '<div style="margin-left: 2%; margin-top: 2%; margin-bottom: 2%; display: inline-block; width: 48%; vertical-align: top;">';

            if (data['test_conf']['type'] == 'lighthouse') {
                var obj = "text/json;charset=utf-8," + encodeURIComponent(data['report']);
                var download_html = '<a href="data:' + obj + '" download="lighthouse_report.json">Download ' + data['description'] + ' report</a><br>';

                html += download_html;
                var metrics = '<h4>Result:</h4><span>'

                for (var key in data['metrics']) {
                    metrics += ''+data['metrics'][key]['name']+': '+data['metrics'][key]['value']+'<br>';
                }
                metrics += '</span>';

                html += metrics+'</div>';

            } else if (data['test_conf']['type'] == 'selenium') {
                var obj = "text/json;charset=utf-8," + encodeURIComponent(data['report']);
                var download_html = '<a href="data:' + obj + '" download="har_report.har">Download ' + data['description'] + ' report</a><br>';

                var html = '<div style="margin-left: 2%; margin-top: 2%; margin-bottom: 2%; display: inline-block; width: 48%; vertical-align: top;">';
                html += download_html;

                var timingMarks = '<h4>Timing marks:</h4><span>'
                var paintMetrics = '<h4>Paint metrics:</h4><span>'
                var calculatedMetrics = '<h4>Calculated metrics:</h4><span>'

                for (var key in data['metrics']) {
                    console.log(data['metrics'][key]);
                    if (data['metrics'].hasOwnProperty(key)) {
                        if (data['metrics'][key]['type'] == 'timing_marks') {
                            timingMarks += ''+data['metrics'][key]['name']+': '+data['metrics'][key]['value']+'<br>';
                        } else if (data['metrics'][key]['type'] == 'paint_metrics') {
                            paintMetrics += ''+data['metrics'][key]['name']+': '+data['metrics'][key]['value']+'<br>';
                        } else if (data['metrics'][key]['type'] == 'calculated') {
                            calculatedMetrics += ''+data['metrics'][key]['name']+': '+data['metrics'][key]['value']+'<br>';
                        }
    //                    console.log(data['metrics'][key]['name'] + " -> " + data['metrics'][key]['value']);
                    }
                }
                timingMarks += '</span>';
                paintMetrics += '</span>';
                calculatedMetrics += '</span>';

                html += timingMarks+paintMetrics+calculatedMetrics+'</div>';
            }



            setTimeout(function(){
                $(html).hide().appendTo(".content_div").fadeIn(1500);}, 300);
            });
        });
    });
});
