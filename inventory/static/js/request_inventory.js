$(document).ready(function() {
            $(".navbar-mine").children("li").each(function() {
                $(this).removeClass("active");
            });

            $("li.inventory").addClass("active");


        });
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
function changeFunc() {
                var selectBox = document.getElementById("selectBox");
                var selectedValue = selectBox.options[selectBox.selectedIndex].value;
                alert(selectedValue);
                $.ajax({
                    url: "ajax/get_products_using_supplier",
                    type: "post",
                    dataType: "json",
                    data: {supplier_name: selectedValue},
                    success: function (data) {
                        var json = JSON.parse(data.products);
                        for (var x in json){
                            $("#context").append('<tr>');
                            $("#context").append('<th><div class="checkbox"><input type="checkbox" value="" name=""></div></th>')
                            $("#context").append('<td class="text-center">'+json[x].fields.name+'</td>');
                            $("#context").append('<td class="text-center">'+json[x].fields.description+'</td>');
                            $("#context").append('<td class="text-center">'+json[x].fields.category.name+'</td>');
                            $("#context").append('<td class="text-center" id="qty_in_stock">'+json[x].fields.quantity_in_stock+'</td>');
                            $("#context").append('<td class="text-right">'+json[x].fields.unit_cost+'</td>');
                            $("#context").append('<td class="text-center"><input type="number" min="0"></td>');
                            $("#context").append('</tr>')

                        }
                    },
                    error: function (data) {
                        console.log(data.responseText);
                    }
                });
            }