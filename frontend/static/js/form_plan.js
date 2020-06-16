$(function(){

    $("#submit_test").bind("click", function() {

        var formVal = formValidation();

        if (formVal === null || formVal === false) {
            return;
        }

        $('#form_div').fadeOut(300, function(){ $(this).remove();});

        var jsonData = {};
        var device = "";

        var ifChecked = document.getElementById("togBtn-device").checked;
        if (ifChecked == true) {
            device = "mobile";
        } else {
            device = "desktop";
        }
        var testName = $("#test-name").val();
        var testType = $('input[name=testtype]:checked').val();

        var timeNumber = $('.time_number').val();
        var timeType = $('.time_type').val();

        var inputUrl = $("#input-url").val();


        jsonData = {
            "name": testName,
            "url": inputUrl,
            "device": device,
            "type": testType,
            "time_number": parseInt(timeNumber),
            "time_type": timeType
        };

        var request = $.ajax({
            type: "POST",
            url: "https://futuresynth.westeurope.cloudapp.azure.com/futuresynth/plan_test_run",
            data: JSON.stringify(jsonData),
            headers: {'Content-type': 'application/json'},
        });
        request.done(function(data){

            $(".content_div").fadeIn(300, function() {
            var contentDiv = document.getElementById('content_div');
            if (data['error']) {
                var html = '<h4>'+data['error']+'</h4>';
            } else {
                var html = '<h4>'+data+'</h4>';
            }

            setTimeout(function(){
                $(html).hide().appendTo(".content_div").fadeIn(300);}, 300);
            });
        });
    });
});

$(function(){
    $(".testtypechoice_input").bind("click", function () {
        var ifChecked = document.getElementById("http").checked;
        if (ifChecked == true) {
            document.getElementsByClassName("switch-box")[0].style.display = "none";
        } else {
            document.getElementsByClassName("switch-box")[0].style.display = "block";
        }
    });
});