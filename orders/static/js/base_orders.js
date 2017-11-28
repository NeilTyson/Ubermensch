$(document).ready(function() {

    $(document).ready(function() {
        $(".navbar-mine").children("li").each(function() {
            $(this).removeClass("active");
        });

        $("li.orders").addClass("active");
    });

    $(function() {
        $("[data-toggle='tooltip']").tooltip();
    })
});

function goBack() {
    window.history.back();
}