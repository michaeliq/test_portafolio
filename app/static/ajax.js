//archivo de peticiones ajax para conectar
//con postgres y mostrar información en la
//pantalla.
/*
function main(){
alert();
var formData = new FormData();
var target_req = document.getElementsByTagName('input').value();

var h1_ = document.getElementsByTagName('h1').innerHTML = 'hola a mas personas';

formData.append("target", target_req);

document.getElementsByClassName('form_ajax')[0].addEventListener('submit',(e)=>{
	e.preventDefault();
}

document.getElementById('enviar').addEventListener('click', () =>{
	var xhr = new XMLHttpRequest();
	xhr.open("POST", " {{url_for('db_req'}} ", true);
xhr.send(formData);
	}
}*/


var interval = setInterval(toDo,100);
function toDo(){
if (document.readyState == "complete") {
    main();
    clearInterval(interval);
	}
}

function main(){
	var target = document.getElementsByTagName('input')[0];
	var h1 = document.getElementsByClassName('h1');
	var buttom = document.getElementById('enviar');	

	document.getElementsByClassName('form_ajax')[0].addEventListener('submit',(e)=>{
		e.preventDefault();
	}
	document.getElementsByClassName('h1')[0].addEventListener('click', function (e){
		this.setAttribute("style","color:red");
		alert(e);
	}
	
}
