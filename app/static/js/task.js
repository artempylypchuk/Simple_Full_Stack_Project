$("button[name='btn_update']").click(function() {
	var selectedSubject = $('#subject').val();
	var selectedRegion = $('#region').val();
    var selectedYear = $('#year').val();

    $.ajax({
        url: '/task',
        method: 'POST',
        data: {
            subject: selectedSubject,
			region: selectedRegion,
            year: selectedYear
        },
        success: function(response) {
            $('#results-table tbody').html(response);
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
});