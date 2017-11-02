$(document).ready(function() {

    $(function() {
        var date = $(".datepicker").datepicker({
            minDate: new Date()
        });


    });

    $('.timepicker').timepicker({
        timeFormat: "H:mm"
    });
});