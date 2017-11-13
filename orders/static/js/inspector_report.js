$(document).ready(function(){

    var feedback = $(".feedback-div");

    $(".btn-add").click(function(){

        var quantity = $(this).parent().siblings().children('input').val();
        var row = $(this).parent().parent();

        if (!quantity || quantity < 0) {
            setInterval(function() {
                feedback.children().
                children().html("Invalid quantity entered");

                feedback.children().addClass('alert alert-danger');
                feedback.css('display', 'initial');

                setTimeout(function(){
                    feedback.css('display', 'none');
                });
            });
        }
    });
});