$(function(){
    $(".fa-trash").bind("click", function() {
        var confirmChange = confirmChange = confirm('Czy na pewno chcesz usunąć test?');

        if (confirmChange) {
            var classList = this.className.split(/\s+/);
            var testName = "";

            for (var i = 0; i < classList.length; i++) {
                if (classList[i] != "fa-trash" || classList[i] != "fa") {
                    testName = classList[i];
                }
            }

            var jsonData = {};
            jsonData = {
                "test_name": testName
            };
            console.log(jsonData);
            $.ajax({
                type: "POST",
                url: "https://futuresynth.westeurope.cloudapp.azure.com/futuresynth/delete_test",
                data: JSON.stringify(jsonData),
                headers: {'Content-type': 'application/json'}
            });
        } else {
            return;
        }
    });
});
