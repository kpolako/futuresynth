function formValidation() {
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

        var inputUrl = $("#input-url").val();
        var urlVal = inputUrl.match(/(?:https|http):\/\/\S+$/);
        if (inputUrl == "") {
            changeInput('input-url', 'Adres URL nie może być pusty.', 'Wprowadź adres strony');
        }
        if (urlVal === false || urlVal === null) {
            changeInput('input-url', 'Wprowadź poprawny URL.', 'Wprowadź adres strony');
        }

   return urlVal;
}