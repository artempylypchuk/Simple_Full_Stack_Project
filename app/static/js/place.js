$("button[name='btn_delete_place']").click(function() {
	$.ajax({
		type: 'POST',
		url: "/delPlace",
		data: {placeid : $(this).data('placeid')},
		dataType: "text",
		success: function(resultData) {
			location.reload();
		}
	});
});

$("button[name='btn_edit_place']").click(function() {
	window.location = "editPlace?placeid="+$(this).data('placeid');
});

$("button[name='btn_new_place']").click(function() {
    window.location = "addPlace";
});