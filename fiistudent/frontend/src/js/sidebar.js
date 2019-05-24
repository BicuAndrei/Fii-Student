if (localStorage.getItem("sidebarColor") !== null) {
	var color = localStorage.getItem("sidebarColor");
	var sidebar = document.getElementsByClassName("d-flex")[0];
	sidebar.style.backgroundColor = color;
	document.getElementsByClassName("list-group-flush")[0].style.backgroundColor = color;
	var list = document.getElementsByTagName("A");
	for (var i = 0; i < list.length; i++) {
		if (list[i].className.indexOf('ch') > 0)
			list[i].style.backgroundColor = color;
	}
}
if (localStorage.getItem("sidebarColorText") !== null) {
	var color = localStorage.getItem("sidebarColorText");
	var list = document.getElementsByTagName("A");
	for (var i = 0; i < list.length; i++) {
		if (list[i].className.indexOf('ch') > 0)
			list[i].style.color = color;
	}
}
