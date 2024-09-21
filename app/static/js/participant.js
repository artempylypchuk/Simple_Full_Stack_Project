$("button[name='btn_delete_participant']").click(function() {
    var data = $(this).data('del').split('|');

    $.ajax({
        type: 'POST',
        url: "/delParticipant",
        data: {
			outid: data[0],
			placeid: data[1]
		},
        dataType: "text",
        success: function(resultData) {
            location.reload();
        }
    });
});

$("button[name='btn_edit_participant']").click(function() {
	window.location = "editParticipant?outid="+$(this).data('outid');
});

$("button[name='btn_new_participant']").click(function() {
    window.location = "addParticipant";
});