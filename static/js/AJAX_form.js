$(document).ready(function() {

	// to display database contents when page is loaded
	$.ajax({
		method : 'GET',
		url : '/get',
		success: function(data) {

			 //to clear previous contents
			$('#table_row').empty() 

			$.each(data, function(i, d) {
				$('#table_row').append('<tr><td>'+d.name+'</td><td>'+d.city+'</td>\
					<td>'+d.addr+'</td><td>'+d.pin+'</td>\
					<td><a href="#" data-value='+d.id+'> Delete </a></td><td>'+d.img_path+'</td>\
					</tr>')
			});
		}	
	}); 

	//event handlers are bound to elements when page is loaded, not during runtime
	//so, using $('a').click() will not work since they are dynamically created and do not have event handlers bound to them
	//since "table" was already present when page was loaded, we can target the 'a'
	$("table").on('click', 'tbody tr td a', function(event) {
		// console.log('h');
		event.preventDefault();
		var href = $(this).data("value");
		// var target = '/delete/'+href
		$.ajax({
			method : 'GET',
			url : '/delete/'+href,
			success : function(data){
				if (data.error){
					$('#error_msg').text(data.error).show();
					$('#data_msg').hide();
				}
				else {
					$('#data_msg').text(data.message).show();
					$('#error_msg').hide();
				}
				
			}
		})

		// to refresh contents of table:
		$.ajax({
			method : 'GET',
			url : '/get',
			success: function(data) {

				 //to clear previous contents
				$('#table_row').empty() 

				$.each(data, function(i, d) {
					$('#table_row').append('<tr><td>'+d.name+'</td><td>'+d.city+'</td>\
						<td>'+d.addr+'</td><td>'+d.pin+'</td>\
						<td><a href="#" data-value='+d.id+'> Delete </a></td><td>'+d.img_path+'</td>\
						</tr>')
				});
			}	
		});

		
		// $('#link').text(target).show();
	});

	//once submit_btn is pressed, POST new formdata, and GET updated db contents
	$('#submit_btn').click(function(event) {

		event.preventDefault();
		
		var formData = new FormData();	

		// adding form values to formData object to be sent via POST
		formData.append('id',$('#hide').val());
		formData.append('name', $('#name').val());
		formData.append('city', $('#city').val());
		formData.append('addr', $('#addr').val());
		formData.append('pin', $('#pin').val());
		// img_path: $('#img_name').val()
		
		//logging formData contents
		// for (var pair of formData.entries()) {
		// 	console.log(pair)
		// }

		// POSTing new formData obj
		$.ajax({
			method : 'POST',
			url : '/new',
			dataType : 'json',
			processData : false,
			contentType : false,
			// contentType: 'application/json',
			data : formData,
			success: function(data) {
				if (data.error) {
					$('#error_msg').text(data.error).show();
					$('#data_msg').hide();
					// $('#name').attr('value','tests');
				}
				else {
					$('#error_msg').hide();
					$('#data_msg').text(data.message).show();	
					// $('#name').attr("value").hide();
					resetValues();
				}
					
			}
		});

		
		// GETing updated db contents to display in table
		$.ajax({
			method : 'GET',
			url : '/get',
			success: function(data) {

				 //to clear previous contents
				$('#table_row').empty() 

				$.each(data, function(i, d) {
				$('#table_row').append('<tr><td>'+d.name+'</td><td>'+d.city+'</td>\
					<td>'+d.addr+'</td><td>'+d.pin+'</td>\
					<td><a href = /delete/'+d.id+'> Delete </a></td><td>'+d.img_path+'</td>\
					</tr>')
				})
			}	
		}); 
	});
});

function resetValues() {
	$('#hide').val('-1');
	$('#name').val('');
	$('#city').val('');
	$('#addr').val('');
	$('#pin').val('');
}