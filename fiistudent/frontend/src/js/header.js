if (localStorage.getItem("headerColor") !== null) {
	var color = localStorage.getItem("headerColor");
	var header = document.getElementsByClassName("page-header")[0];
	header.style.backgroundColor = color;
}
if (localStorage.getItem("headerColorText") !== null) {
	var color = localStorage.getItem("headerColorText");
	var header = document.getElementsByClassName("page-header")[0];
	header.style.color = color;
	document.querySelector(".page-header .subtitle").style.color = color;
	localStorage.setItem("headerColorText", color);
}