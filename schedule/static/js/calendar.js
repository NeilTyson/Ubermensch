$(document).ready(function(){

    var calendar = $("#calendar");

    calendar.fullCalendar({

    });

    // get the schedules
    $.ajax({
        url: "ajax/display_events",
        type: "get",
        dataType: "json",
        success: function(data) {
            var json = JSON.parse(data.schedules);

            console.log(json);

            for (var x in json) {
                var event = {
                    title: json[x].fields.name,
                    start: json[x].fields.deadline_date,
                };

                calendar.fullCalendar('renderEvent', event);
            }
        },
        error: function(data) {
            console.log(data.responseText);
        }
    });

});