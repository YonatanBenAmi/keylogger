function myFunc(){
    a = Number(document.getElementById("result").innerHTML)
    document.getElementById("result").innerHTML = a + 1
}

function changeText() {
    document.getElementById("title").textContent = document.getElementById("title").textContent === "הטקסט השתנה!" ? "שנה את הטקסט" : "הטקסט השתנה!";
}


document.getElementById("start").addEventListener('click', function() {
    let btn = document.getElementById("text-start-button");
    let circle = document.querySelector(".sircle-card");  // בחירת האלמנט של העיגול
    let animation = document.getElementById("animation")
    
    if (btn.innerHTML === "start") {
        btn.innerHTML = "stop";
        btn.style.color = "#ff3914";
        animation.style.visibility = "visible"

        circle.style.border = "1px solid #ff1414";
        circle.style.boxShadow = "0 0 10px #ff1414";
        
        document.documentElement.style.setProperty('--shine-color', 'rgba(255, 20, 20, 0.2)');
        
        circle.addEventListener('mouseenter', function() {
            this.style.boxShadow = "0 0 20px #ff1414, 0 0 40px #ff3914";
        });
        circle.addEventListener('mouseleave', function() {
            this.style.boxShadow = "0 0 10px #ff1414";
        });
    } else {
        
        btn.innerHTML = "start";
        btn.style.color = "#39ff14";
        animation.style.visibility = "hidden"
        circle.style.border = "1px solid var(--neon-blue)";
        circle.style.boxShadow = "0 0 10px var(--neon-blue)";
        
        document.documentElement.style.setProperty('--shine-color', 'rgba(0, 243, 255, 0.2)');
        
        circle.addEventListener('mouseenter', function() {
            this.style.boxShadow = "0 0 20px var(--neon-blue), 0 0 40px var(--neon-green)";
        });
        circle.addEventListener('mouseleave', function() {
            this.style.boxShadow = "0 0 10px var(--neon-blue)";
        });
    }
});