$("button[name='btn_delete_eduplace']").click(function() {
	$.ajax({
		type: 'POST',
		url: "/delEduPlace",
		data: {eduplaceid : $(this).data('eduplaceid')},
		dataType: "text",
		success: function(resultData) {
			location.reload();
		}
	});
});

$("button[name='btn_edit_eduplace']").click(function() {
    window.location = "editEduPlace?eduplaceid="+$(this).data('eduplaceid');
});

$("button[name='btn_new_eduplace']").click(function() {
    window.location = "addEduPlace";
});