$(document).ready(function() {
    console.log("hello");

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

    var button = $("button#view-engineers");
    var orderID = $("#order-id").html();

    button.click(function() {
        $.ajax({
            url: "ajax/view_engineers",
            type: "post",
            data: {
                order: orderID
            },
            dataType: "json",
            success: function(data) {
                var json = JSON.parse(data);
                console.log(json);

                var body = $("#modal-body");
                body.empty();

                body.append("<ul class='list-group eng-list'>" +
                            "</ul>");

                for (var x in json) {
                    $(".eng-list").append(
                        "<li class='list-group-item'>"+json[x].fields.first_name+" "+json[x].fields.last_name+"</li>"
                    );
                }
            },
            error: function(data) {
                console.log(data.responseText);
            }
        });
    });
});