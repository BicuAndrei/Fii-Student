if (localStorage.getItem("backgroundColor") !== null) {
	var color = localStorage.getItem("backgroundColor");
	var background = document.getElementById("page-content-wrapper");
	background.style.backgroundColor = color;
	background.classList.remove("bg-light");
}
if (localStorage.getItem("fontSize") !== null) {
	var size = localStorage.getItem("fontSize");
	var body = document.getElementsByTagName("body")[0];
	body.style.fontSize = size + "px";
}