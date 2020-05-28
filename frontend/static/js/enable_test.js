$(function(){
    $(".enable-test").bind("change", function() {
        var ifChecked = this.checked;
        var confirmChange;
        if (ifChecked) {
            confirmChange = confirm('Czy na pewno chcesz włączyć test?');
        } else {
            confirmChange = confirm('Czy na pewno chcesz wyłączyć test?');
        }

        if (confirmChange) {
            var classList = this.className.split(/\s+/);
            var testName = "";

            for (var i = 0; i < classList.length; i++) {
                if (classList[i] != "enable-test") {
                    testName = classList[i];
                }
            }

            var jsonData = {};
            jsonData = {
                "enabled": ifChecked,
                "test_name": testName
            };
            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:4999/enable_test",
                data: JSON.stringify(jsonData),
                headers: {'Content-type': 'application/json'}
            });


        } else {
            console.log('elo');
            if (ifChecked) {
                $(this).prop('checked', false);
            } else {
                $(this).prop('checked', true);
            }
        }
    });
});
