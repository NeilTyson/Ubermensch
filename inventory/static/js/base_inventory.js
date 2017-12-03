$(document).ready(function() {
    $(".navbar-mine").children("li").each(function() {
        $(this).removeClass("active");
    });

    $("li.inventory").addClass("active");
    $('[data-toggle="popover"]').popover({ placement: 'left', html: true, trigger: 'hover' });
    $("[data-toggle=confirmation]").confirmation({btnOkLabel: 'Yes', btnCancelLabel: 'No', title: 'Are you sure?',container:"body",btnOkClass:"btn btn-sm btn-success btn-xs",btnCancelClass:"btn btn-sm btn-danger btn-xs",onConfirm:function(event, element) { alert('confirm clicked'); }});
});