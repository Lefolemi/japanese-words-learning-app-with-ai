// Connect to the SocketIO server
const socket = io();

socket.on('connect', () => {
    console.log("Connected to Sensei Server!");
});

// Function to simulate sending voice (we'll add real mic logic later)
function sendVoiceSample(wordId) {
    console.log("Sending voice data for word ID:", wordId);
    socket.emit('voice_input', {
        word_id: wordId,
        audio: "base64_audio_blob_here" 
    });
}

// Receive feedback from AI
socket.on('feedback', (data) => {
    console.log("Sensei says:", data.message);
    document.getElementById('feedback-box').innerText = data.message;
});

// Marking System Logic
async function toggleMark(wordId, btnElement) {
    const isCurrentlyMarked = btnElement.innerText.includes('⭐');
    const newStatus = !isCurrentlyMarked;

    // 1. Immediate UI update (Optimistic UI)
    btnElement.innerText = newStatus ? '⭐ Marked' : '☆ Mark';
    btnElement.style.backgroundColor = newStatus ? 'gold' : 'white';

    // 2. Save to Database
    try {
        await fetch('/api/mark', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ word_id: wordId, marked: newStatus })
        });
    } catch (e) {
        console.error("Failed to save mark status");
    }
}