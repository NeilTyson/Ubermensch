 $(document).ready(function() {
            $(".navbar-mine").children("li").each(function() {
                $(this).removeClass("active");
            });

            $("li.inventory").addClass("active");
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
                        {% for var x in products %}
                            $("#context").append('<tr>');
                            $("#context").append('<th><div class="checkbox"><input type="checkbox" value="" name=""></div></th>')
                            $("#context").append('<td class="text-center">'+json[x].fields.name+'</td>');
                            $("#context").append('<td class="text-center">'+json[x].fields.description+'</td>');
                            $("#context").append('<td class="text-center">'+json[x].fields.category+'</td>');
                            $("#context").append('<td class="text-center" id="qty_in_stock">'+json[x].fields.quantity_in_stock+'</td>');
                            $("#context").append('<td class="text-right">'+json[x].fields.unit_cost+'</td>');
                            $("#context").append('<td class="text-center"><input type="number" min="0"></td>');
                            $("#context").append('</tr>')

                        {% endfor %}
                    },
                    error: function (data) {
                        console.log(data.responseText);
                    }
                });
            }
        });