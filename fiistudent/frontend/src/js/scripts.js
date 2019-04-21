const endpoint = "https://develop-dot-fii-student.appspot.com/";

$('#loginForm').submit(function(event) {
	event.preventDefault();

	$.ajax({
		url: endpoint + "login",
		data: {
			email: $(this).find('#email').val(),
			password: $(this).find('#password').val()
		}
	}).then(function (data) {
		if(data.status === "error") {
			alert(data.errors[0].message);
		}
		if(data.status === "ok") {
			alert('Success!');
		}
	});
});
