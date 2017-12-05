$(document).ready(function() {
    $(".navbar-mine").children("li").each(function() {
        $(this).removeClass("active");
    });

    $("li.inventory").addClass("active");
});