/**
 * ⚡ J.A.R.V.I.S - Web Client
 * WebSocket orqali server bilan aloqa
 */

// ==================== SOCKET CONNECTION ====================
const socket = io();
const chatArea = document.getElementById('chatArea');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const micBtn = document.getElementById('micBtn');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const clock = document.getElementById('clock');

let isListening = false;
let recognition = null;

// ==================== SOCKET EVENTS ====================

socket.on('connect', () => {
    statusDot.textContent = '●';
    statusDot.classList.remove('offline');
    statusText.textContent = 'Ulangan';
});

socket.on('disconnect', () => {
    statusDot.classList.add('offline');
    statusText.textContent = 'Uzilgan';
});

socket.on('message', (data) => {
    hideTyping();
    
    if (data.text === '__CLEAR__') {
        chatArea.innerHTML = '';
        addMessage('jarvis', '🧹 Chat tozalandi. Yangi suhbat boshlang!', data.time);
        return;
    }
    
    addMessage(data.role, data.text, data.time);
});

// ==================== MESSAGE HANDLING ====================

function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;
    
    // Show user message
    addMessage('user', text, getCurrentTime());
    messageInput.value = '';
    
    // Show typing indicator
    showTyping();
    
    // Send to server
    socket.emit('user_message', { text: text });
}

function addMessage(role, text, time) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = role === 'jarvis' ? '⚡' : '👤';
    
    // Parse markdown
    let htmlContent = '';
    try {
        htmlContent = marked.parse(text);
    } catch (e) {
        htmlContent = text.replace(/\n/g, '<br>');
    }
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div>
            <div class="message-content">${htmlContent}</div>
            <div class="message-time">${time || getCurrentTime()}</div>
        </div>
    `;
    
    chatArea.appendChild(messageDiv);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function showTyping() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message jarvis';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">⚡</div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    chatArea.appendChild(typingDiv);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function hideTyping() {
    const typing = document.getElementById('typing-indicator');
    if (typing) typing.remove();
}

// ==================== SPEECH RECOGNITION ====================

function initSpeechRecognition() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        console.log('Speech Recognition not supported');
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'uz-UZ'; // O'zbek tili
    
    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        messageInput.value = text;
        sendMessage();
        stopListening();
    };
    
    recognition.onerror = (event) => {
        console.log('Speech error:', event.error);
        stopListening();
        if (event.error === 'not-allowed') {
            addMessage('jarvis', '⚠️ Mikrofondan foydalanishga ruxsat bering!', getCurrentTime());
        }
    };
    
    recognition.onend = () => {
        stopListening();
    };
}

function toggleMic() {
    if (isListening) {
        stopListening();
    } else {
        startListening();
    }
}

function startListening() {
    if (!recognition) {
        initSpeechRecognition();
    }
    if (!recognition) {
        addMessage('jarvis', '❌ Brauzeringiz ovozni taniy olmaydi. Chrome yoki Edge ishlating.', getCurrentTime());
        return;
    }
    
    try {
        recognition.start();
        isListening = true;
        micBtn.classList.add('active');
        statusText.textContent = '🎤 Tinglayapman...';
    } catch (e) {
        console.log('Mic error:', e);
    }
}

function stopListening() {
    if (recognition) {
        try { recognition.stop(); } catch(e) {}
    }
    isListening = false;
    micBtn.classList.remove('active');
    statusText.textContent = 'Ulangan';
}

// ==================== CLOCK ====================

function updateClock() {
    const now = new Date();
    const time = now.toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const date = now.toLocaleDateString('uz-UZ');
    clock.textContent = `${time} | ${date}`;
}

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' });
}

// ==================== PARTICLES ====================

function initParticles() {
    const canvas = document.getElementById('particles');
    const ctx = canvas.getContext('2d');
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const particles = [];
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2 + 0.5,
            speedX: (Math.random() - 0.5) * 0.5,
            speedY: (Math.random() - 0.5) * 0.5,
            opacity: Math.random() * 0.5 + 0.1
        });
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(p => {
            p.x += p.speedX;
            p.y += p.speedY;
            
            if (p.x < 0) p.x = canvas.width;
            if (p.x > canvas.width) p.x = 0;
            if (p.y < 0) p.y = canvas.height;
            if (p.y > canvas.height) p.y = 0;
            
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(0, 212, 255, ${p.opacity})`;
            ctx.fill();
        });
        
        // Draw connections
        particles.forEach((p1, i) => {
            particles.slice(i + 1).forEach(p2 => {
                const dist = Math.hypot(p1.x - p2.x, p1.y - p2.y);
                if (dist < 150) {
                    ctx.beginPath();
                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = `rgba(0, 212, 255, ${0.05 * (1 - dist / 150)})`;
                    ctx.stroke();
                }
            });
        });
        
        requestAnimationFrame(animate);
    }
    
    animate();
    
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}

// ==================== EVENT LISTENERS ====================

sendBtn.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

micBtn.addEventListener('click', toggleMic);

// Keyboard shortcut
document.addEventListener('keydown', (e) => {
    // Ctrl+M = toggle mic
    if (e.ctrlKey && e.key === 'm') {
        e.preventDefault();
        toggleMic();
    }
    // Escape = focus input
    if (e.key === 'Escape') {
        messageInput.focus();
    }
});

// ==================== INIT ====================

document.addEventListener('DOMContentLoaded', () => {
    updateClock();
    setInterval(updateClock, 1000);
    initParticles();
    initSpeechRecognition();
    messageInput.focus();
});
