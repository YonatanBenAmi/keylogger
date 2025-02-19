async function myFunc() {
    // בניית ה-URL
    const url = `/${document.getElementById("computer").value}/${document.getElementById("date").value}`;
    const str = document.getElementById("inp").value;
    
    try {
        // קריאה לשרת וקבלת ה-JSON
        const response = await fetch(url);
        const jsonData = await response.json();
        
        // ספירת המחרוזת ב-JSON
        const count = countStringInJSON(jsonData, str);
        
        // עדכון התוצאה
        document.getElementById("result").innerHTML = count;
    } catch (error) {
        console.error('שגיאה בקריאת הנתונים:', error);
        document.getElementById("result").innerHTML = "שגיאה בטעינת הנתונים";
    }
}

function countStringInJSON(jsonData, searchStr) {
    // בדיקה שהערכים תקינים
    if (!jsonData || !searchStr) return 0;
    
    // ממיר את ה-JSON למחרוזת
    const jsonString = JSON.stringify(jsonData).toLowerCase();
    // ממיר את מחרוזת החיפוש לאותיות קטנות
    searchStr = searchStr.toLowerCase();
    
    // סופר את ההופעות
    return jsonString.split(searchStr).length - 1;
}
function changeText() {
    document.getElementById("title").textContent = document.getElementById("title").textContent === "הטקסט השתנה!" ? "שנה את הטקסט" : "הטקסט השתנה!";
}

function getName(){
    document.getElementById("Follo").textContent = document.getElementById("computer").value;
} 
getName();

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

function fetchDataFromForm(event) {
    event.preventDefault(); // מונע רענון של הדף
    const computer = document.getElementById("computer").value;
    const day = document.getElementById("date").value;
    getName();
    fetch(`/${computer}/${day}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        document.getElementById("result-data").innerHTML =
          "<pre>" + JSON.stringify(data, null, 4) + "</pre>";
      })
      .catch(error => console.error('Error:', error));
  }

  const button = document.querySelector('.show-button');
  const block = document.querySelector('.block');
  const overlay = document.querySelector('.overlay');
  const closeButton = document.querySelector('.close-button');
  
  button.addEventListener('click', () => {
      document.body.classList.add('modal-open'); // מוסיף class לחסימת אינטראקציה
      block.classList.add('show');
      overlay.classList.add('show');
      button.style.display = 'none';
  });

  closeButton.addEventListener('click', () => {
      document.body.classList.remove('modal-open'); // מסיר את החסימה
      block.classList.remove('show');
      overlay.classList.remove('show');
      button.style.display = 'block';
  });

  // סגירת הבלוק בלחיצה על ה-overlay
  overlay.addEventListener('click', () => {
      closeButton.click();
  });