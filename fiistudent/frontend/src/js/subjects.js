$.ajax(endpoint+"courses",
	{   
		type: "GET",
		dataType: 'json', // type of response data
		timeout: 500,     // timeout milliseconds
		success: function (data, status, xhr) {   // success callback function
			$('p').append(data[0].year+ ' ' + data[1].year + ' ' + data[2].year);
			alert("a mers");
		},
		error: function (jqXhr, textStatus, errorMessage) { // error callback 
			$('p').append('Error: ' + errorMessage);
			alert("eroare");
		}
	});



  