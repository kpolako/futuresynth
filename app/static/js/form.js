$(function(){
    $("#submit_test").bind("click", function() {
        $('#form_div').fadeOut(300, function(){ $(this).remove();});
        $(".content_div").fadeIn(300, function() {
        var contentDiv = document.getElementById('content_div');
        var html = '<div class="loader"><span id="counter">Loading</span><div class="spinner"></div></div>';
        $(html).hide().appendTo(".content_div").fadeIn(300);

        var device = "";
        var jsonData = {};
        var ifChecked = document.getElementById("togBtn").checked;
        if (ifChecked == true) {
            device = "mobile";
        } else {
            device = "desktop";
        }
        var inputUrl = $("#input-url").val();
        jsonData = {
            "url": inputUrl,
            "device": device
        };

        var request = $.ajax({
            type: "POST",
            url: "/receive_test",
            data: JSON.stringify(jsonData),
            headers: {'Content-type': 'application/json'},
        });
        request.done(function(data){
            console.log(data);
//            var formDiv = document.getElementById('form_div');

            });

        });
    });
});
