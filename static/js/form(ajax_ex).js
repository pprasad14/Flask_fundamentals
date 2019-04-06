$(document).ready(function() {

	$('#sub_btn').click(function() {

		$.ajax({
			url : '/process',
			method : 'POST',
			data : {
				name : $('#nameInput').val(),
				email : $('#emailInput').val()
			},
			dataType: 'json',
			success: function(data) {

					if (data.error) {
						$('#errorAlert').text(data['error']).show();
						$('#successAlert').hide();
					}
					else {
						$('#successAlert').text(data['names']).show();
						$('#errorAlert').hide();
					}

				}
		})
		;

	});

});