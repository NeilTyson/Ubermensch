$(document).ready(function() {



    $.ajax({
        url: '/schedule/ajax/display_user_type',
        dataType: "json",
        type: "get",
        success: function(data) {
            $(".user-type").html(data.user_type);
        },
        error: function(data) {
            console.log(data.responseText);
        }
    });


});