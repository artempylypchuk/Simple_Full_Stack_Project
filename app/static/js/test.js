$("button[name='btn_delete_test']").click(function() {
    var data = $(this).data('del').split('|');

    $.ajax({
        type: 'POST',
        url: "/delTest",
        data: {
			outid: data[1],
			testid: data[0]
		},
        dataType: "text",
        success: function(resultData) {
            location.reload();
        }
    });
});


$("button[name='btn_edit_test']").click(function() {
    window.location = "editTest?testid=" + $(this).data('testid') + "&outid=" + $(this).data('outid');
});


$("button[name='btn_new_test']").click(function() {

    window.location = "addTest";

});