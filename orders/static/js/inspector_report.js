$(document).ready(function(){

    var feedback = $(".feedback-div");
    var order = $("p#order").html();

    console.log(order);

    var cart = [];
    var listGroup = $(".cart");
    var price = 0;

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

    $(".btn-add").click(function(){

        var quantity = $(this).parent().siblings().children('input').val();
        var row = $(this).parent().parent();
        var id = $(this).parent().siblings(".product-id").html();
        var button = $(this);
        var field = $(this).parent().siblings().children('input');
        var name= button.parent().siblings(".product-name").html();
        var sellingPrice = button.parent().siblings(".price").html();

        if (!quantity || quantity <= 0) {
            feedback.children().addClass('alert alert-danger');
            feedback.children().children().html("Invalid quantity entered");
            feedback.css('display', 'initial');
        }
        else {
            cart.push({
                id: id,
                quantity: quantity
            });

            price = price + parseFloat(sellingPrice) * quantity;
            var fees = price * .2;
            price = price + fees;

            feedback.css('display', 'none');
            button.replaceWith("<p class='text-success'>Added</p>");
            field.attr("disabled", "true");

            listGroup.append(
                "<li class='list-group-item'>" +
                " <strong>"+quantity+"</strong> " + name
                + "</li>"
            );

            $("strong.cost").html(price.toFixed(2));
            $(".confirm-btn").removeAttr("disabled");
        }
    });

    $(".confirm-btn").click(function(){

        for (var x in cart) {

            $.ajax({
                url: "/orders/ajax/add_order_line",
                type: "post",
                data: {
                    order: order,
                    product: cart[x].id,
                    quantity: cart[x].quantity
                },
                success: function() {
                    console.log("added");

                    window.location = "/orders/project_requirements/" + order;
                },
                error: function(data) {
                    console.log(data.responseText);
                }
            });
        }
    });
});