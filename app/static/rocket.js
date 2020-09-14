function stars(){                            i = 0;                                      count = 50;
   scena = document.querySelector('.scena');
   particule = document.createElement("i");

   while (true) {
    alert(i);
    duration = Math.random() * 1;
    h = Math.random() * 100;
    x = Math.floor(Math.random() * window.in
nerWidth);
    particule.style.left = x + "px";
    particule.style.widht = 1 + "px";
    particule.style.height = 50 + h + "px";
    particule.style.animationDuration = duration + "s";
    scena.appendChild(particule);
    i++;
};                    
};   

var interval = setInterval(toDo,100);       function toDo(){                            if (document.readyState == "complete") {   
	stars()
	clearInterval(interval);                        }                                   }

