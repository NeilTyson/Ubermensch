$(document).ready(function() {

    function getCookie(name) {

        var cookieValue = null;

        if (document.cookie && document.cookie != '') {

            var cookies = document.cookie.split(';');

            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function setClass(newClass, element) {
        element.removeClass();
        element.addClass(newClass);
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var calendar = $("#calendar");

    calendar.fullCalendar({

    });

    displayProjectEvent();

    $(".fc-right").click(function() {
        displayProjectEvent();
    });

    function displayProjectEvent() {
        $.ajax({
            url: "ajax/view_project_event",
            data: {
                order: $("#order-no").html()
            },
            type: "post",
            dataType: "json",
            success: function(data) {
                var json = JSON.parse(data);
                console.log(json);

                for (var x in json) {
                    var event;

                    event = {
                        title: json[x].fields.name,
                        start: json[x].fields.start_date,
                        url: "/schedule/details/" + json[x].pk,
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

