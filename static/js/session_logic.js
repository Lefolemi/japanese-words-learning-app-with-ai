let currentIndex = 0;
let flags = new Array(totalQuestions).fill(false);
let timeRemaining = timerLimit * 60; // Convert minutes to seconds

// --- NAVIGATION ---
function showCard(index) {
    // Hide all
    document.querySelectorAll('.question-card').forEach(c => c.style.display = 'none');
    // Show current
    document.getElementById(`card-${index}`).style.display = 'block';
    
    currentIndex = index;
    document.getElementById('current-index-display').innerText = index + 1;
    
    // Update Jump Grid Visuals
    updateGridUI();
}

function changeQuestion(step) {
    let newIndex = currentIndex + step;
    if (newIndex >= 0 && newIndex < totalQuestions) {
        showCard(newIndex);
    }
}

function jumpToQuestion(index) {
    showCard(index);
    toggleJumpGrid(); // Close grid
}

// --- FLAGGING ---
function toggleFlag() {
    flags[currentIndex] = !flags[currentIndex];
    const btn = document.getElementById('flag-btn');
    btn.classList.toggle('flagged', flags[currentIndex]);
    updateGridUI();
}

function updateGridUI() {
    for (let i = 0; i < totalQuestions; i++) {
        const item = document.getElementById(`grid-item-${i}`);
        if (flags[i]) item.classList.add('flagged-item');
        else item.classList.remove('flagged-item');
        
        // Highlight current
        if (i === currentIndex) item.classList.add('current-item');
        else item.classList.remove('current-item');
    }
}

// --- TIMER ---
if (timerLimit > 0) {
    const timerInterval = setInterval(() => {
        timeRemaining--;
        let mins = Math.floor(timeRemaining / 60);
        let secs = timeRemaining % 60;
        document.getElementById('timer-display').innerText = 
            `Time: ${mins}:${secs < 10 ? '0' : ''}${secs}`;

        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            alert("Time is up! Submitting session.");
            window.location.href = "/"; // Auto-exit
        }
    }, 1000);
} else {
    document.getElementById('timer-display').style.display = 'none';
}

function toggleJumpGrid() {
    document.getElementById('jump-grid').classList.toggle('hidden');
}