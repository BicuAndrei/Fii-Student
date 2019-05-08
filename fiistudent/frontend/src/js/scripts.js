$(document).ready(function() {
	if (shouldBeLoggedIn === true) {
		if (sessionStorage.getItem("accessToken") == null) {
			window.location.href = "/";
		}
	}
});

