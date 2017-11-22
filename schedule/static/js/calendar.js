$(document).ready(function(){

    var calendar = $("#calendar");

    calendar.fullCalendar({

    });

    // display events on document load
    display_events();

    $(".fc-right").click(function() {
        display_events();
    });

    // get the schedules
    function display_events() {
        $.ajax({
        url: "ajax/display_events",
        type: "get",
        dataType: "json",
        success: function(data) {
            var json = JSON.parse(data.schedules);

            // console.log(json);

            for (var x in json) {
                var event;

                event = {
                    title: json[x].fields.name,
                    start: json[x].fields.start_date,
                    url: "details/" + json[x].pk,
                    end: json[x].fields.end_date
                };

                calendar.fullCalendar('renderEvent', event);
            }
        },
        error: function(data) {
            console.log(data.responseText);
        }
    });
    }

});