$(document).ready(function() {
    $(".navbar-mine").children("li").each(function() {
        $(this).removeClass("active");
    });

    $("li.schedules").addClass("active");


    // csrf
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

    //view involved people ajax
    $(".view-btn").click(function() {

        var body = $(".body-involved");

        body.empty();

        var id = $(this).parent().siblings(".sched-id").html();

        $.ajax({
            url: "/schedule/ajax/view_people",
            data: {
                'schedule': id
            },
            dataType: "json",
            success: function(data) {

                var obj = JSON.parse(data.data);

                var html = "<table class='table table-striped table-people'>" +
                    "<thead class='thead-dark'>" +
                    "<tr>" +
                    "<th>Last Name</th>" +
                    "<th>First Name</th>" +
                    "<th>Deparment</th>" +
                    "</tr>" +
                    "</thead>" +
                    "</table>";

                body.append(html);
                var table = $(".table-people");

                for (var x in obj) {
                    var content = "<tr>" +
                        "<td>"+ obj[x].fields.last_name +"</td>" +
                        "<td>"+ obj[x].fields.first_name +"</td>" +
                        "<td>"+ obj[x].fields.user_type +"</td>" +
                        "</tr>";

                    table.append(content);
                }


            },
            error: function(data) {
                console.log(data.responseText);
            },
            type: "post"
        });
    });



});