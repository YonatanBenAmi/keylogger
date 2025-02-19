// async function myFunc() {
//     // בניית ה-URL
//     const url = `/${document.getElementById("computer").value}/${document.getElementById("date").value}`;
//     const str = document.getElementById("inp").value;
    
//     try {
//         // קריאה לשרת וקבלת ה-JSON
//         const response = await fetch(url);
//         const jsonData = await response.json();
        
//         // ספירת המחרוזת ב-JSON
//         const count = countStringInJSON(jsonData, str);
        
//         // עדכון התוצאה
//         document.getElementById("result").innerHTML = count;
//     } catch (error) {
//         console.error('שגיאה בקריאת הנתונים:', error);
//         document.getElementById("result").innerHTML = "שגיאה בטעינת הנתונים";
//     }
// }

// function countStringInJSON(jsonData, searchStr) {
//     // בדיקה אם יש נתונים, מערך keypresses ומחרוזת חיפוש
//     if (!jsonData || !jsonData.keypresses || !Array.isArray(jsonData.keypresses) || !searchStr) return 0;
    
//     let count = 0;
//     const lowerSearch = searchStr.toLowerCase();
    
//     // מעבר על כל האיברים במערך keypresses
//     jsonData.keypresses.forEach(item => {
//         if (item.key) {
//             // המרה לאותיות קטנות
//             const keyValue = item.key.toString().toLowerCase();
//             // ספירת ההופעות במחרוזת זו
//             count += keyValue.split(lowerSearch).length - 1;
//         }
//     });
    
//     return count;
// }

// פונקציה לספירת מחרוזת בתוך ערכי "key" בכל הקשות ב-JSON
function countStringInJSON(jsonData, searchStr) {
    if (!jsonData || !jsonData.keypresses || !Array.isArray(jsonData.keypresses) || !searchStr) return 0;
    
    let count = 0;
    const lowerSearch = searchStr.toLowerCase();

    jsonData.keypresses.forEach(item => {
        if (item.key) {
            const keyValue = item.key.toString().toLowerCase();
            count += keyValue.split(lowerSearch).length - 1;
        }
    });

    return count;
}

// פונקציה שמבצעת את הספירה עבור כל הימים עבור מחשב נתון
async function fetchAndCountForComputer(computer, searchStr) {
    let totalCount = 0;
    try {
        // קריאה לשרת לקבלת רשימת התיקיות/ימים עבור המחשב
        const listUrl = `/${computer}`;
        const listResponse = await fetch(listUrl);
        if (!listResponse.ok) {
            throw new Error(`שגיאה בטעינת רשימת התאריכים עבור ${computer}`);
        }
        const listData = await listResponse.json();
        
        // נניח שה-JSON מחזיר מערך תחת המפתח "days"
        const days = listData.days;
        if (!Array.isArray(days)) {
            throw new Error("המבנה של רשימת התאריכים לא תואם את הציפיות");
        }
        
        // מעבר על כל יום וביצוע קריאה לנתונים של אותו יום
        for (const day of days) {
            const dayUrl = `/${computer}/${day}`;
            try {
                const dayResponse = await fetch(dayUrl);
                if (!dayResponse.ok) {
                    console.error(`שגיאה בטעינת הנתונים עבור היום ${day}: ${dayResponse.status}`);
                    continue; // ממשיכים ליום הבא
                }
                const dayData = await dayResponse.json();
                const count = countStringInJSON(dayData, searchStr);
                totalCount += count;
            } catch (dayError) {
                console.error(`שגיאה בעיבוד הנתונים עבור היום ${day}:`, dayError);
            }
        }
    } catch (error) {
        console.error("שגיאה בטעינת רשימת התאריכים:", error);
        throw error;
    }
    
    return totalCount;
}

// דוגמה לשימוש
async function myFunc() {
    // קבלת הערכים מהאלמנטים (ודאו שה-IDs נכונים בהנב HTML)
    const computerElem = document.getElementById("computer");
    const searchElem = document.getElementById("inp");
    const resultElem = document.getElementById("result");

    if (!computerElem || !searchElem || !resultElem) {
        console.error("אחד מהאלמנטים לא נמצא");
        return;
    }

    const computer = computerElem.value;
    const searchStr = searchElem.value;

    try {
        const totalCount = await fetchAndCountForComputer(computer, searchStr);
        resultElem.innerHTML = totalCount;
    } catch (error) {
        resultElem.innerHTML = "שגיאה בטעינת הנתונים";
    }
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