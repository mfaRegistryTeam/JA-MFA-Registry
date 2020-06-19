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
  
function openCity(evt, cityName) {
	var i, tabcontent, tablinks;
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}
	tablinks = document.getElementsByClassName("tablinks");
	for (i = 0; i < tablinks.length; i++) {
		tablinks[i].className = tablinks[i].className.replace(" active", "");
	}
	document.getElementById(cityName).style.display = "block";
	evt.currentTarget.className += " active";
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();