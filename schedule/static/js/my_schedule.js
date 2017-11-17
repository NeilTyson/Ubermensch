$(document).ready(function(){

    var calendar = $("#calendar");

    calendar.fullCalendar({

    });

    // display own events
    $.ajax({
        url: "ajax/display_own_events",
        type: "post",
        dataType: "json",
        data: {username: $("#username").html() },
        success: function(data) {

            var json = JSON.parse(data.my_schedules);

            for (var x in json) {
                var event;

                event = {
                    title: json[x].fields.name,
                    start: json[x].fields.start_date,
                    url: "details/" + json[x].pk,
                    end: json[x].fields.end_date,
                };

                calendar.fullCalendar('renderEvent', event);
            }
        },
        error: function(data) {
            console.log(data.responseText);
        }
    });
});