function formValidation() {
        var testNameBool = false;
        var timeBool = false;


        var ifExist = true;
        var testName = $("#test-name").val();

        $.ajax({
            type: "GET",
            url: "https://futuresynth.westeurope.cloudapp.azure.com/futuresynth/check_name?name="+testName,
            async: false
        }).done(function(data){
            ifExist = data.exists;
        });

        function changeInput (id, text_err, text) {
            $('#'+id).val('');
            $('#'+id).attr('placeholder', text_err);
            $('#'+id).addClass('change-color-class-red');
            $('#'+id).bind('blur', function() {
                $('#'+id).removeClass('change-color-class-red');
                $('#'+id).addClass('change-color-class-transparent');
                $('#'+id).attr('placeholder', text);
            });
        }
        if (ifExist) {
            changeInput('test-name', 'Ta nazwa jest już zajęta.', 'Wprowadź nazwę testu');
            testNameBool = false;
        } else if (testName == "") {
            changeInput('test-name', 'Nazwa nie może być pusta.', 'Wprowadź nazwę testu');
            testNameBool = false;
        } else {
            testNameBool = true;
        }

        var inputUrl = $("#input-url").val();
        var urlVal = inputUrl.match(/(?:https|http):\/\/\S+$/);
        if (inputUrl == "") {
            changeInput('input-url', 'Adres URL nie może być pusty.', 'Wprowadź adres strony');
        }
        if (urlVal === false || urlVal === null) {
            changeInput('input-url', 'Wprowadź poprawny URL.', 'Wprowadź adres strony');
        }

        var timeNumber = $('#time_number_id').val();
//        alert(timeNumber);
        if (timeNumber == "") {
            alert("Ustal wartość interwału testu.");
            timeBool = false;
        } else {
            timeBool = true;
        }
        var passVal = testNameBool && urlVal && timeBool;
   return passVal;
}