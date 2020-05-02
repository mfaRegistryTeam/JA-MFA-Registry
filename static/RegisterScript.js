function myFunction() {
	var checkBox = document.getElementById("myCheck");
	var text = document.getElementById("textme");
	if (checkBox.checked == true){
	  text.style.display = "block";
	} else {
	   text.style.display = "none";
	}
	
  }
  
  function myFunctionw() {
	var checkBox = document.getElementById("myCheckn");
	var text = document.getElementById("text");
	if (checkBox.checked == true){
	  text.style.display = "block";
	} else {
	   text.style.display = "none";
	}
	
  }

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();

document.body.onload = function () {
	openCity(event, 'London');
	document.getElementById("first").className += " active";
};

function openCity(evt, cityName) {
var i, npage, pagelinks;
npage = document.getElementsByClassName("npage");
for (i = 0; i < npage.length; i++) {
npage[i].style.display = "none";
}
pagelinks = document.getElementsByClassName("pagelinks");
for (i = 0; i < pagelinks.length; i++) {
pagelinks[i].className = pagelinks[i].className.replace(" active", "");
}
document.getElementById(cityName).style.display = "block";
evt.currentTarget.className += " active";
}

