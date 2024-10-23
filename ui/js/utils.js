
function temporaryIconChange(element, newIcon, duration = 1000) {
    const original = element.textContent;
    
    element.textContent = newIcon;
    element.style.pointerEvents = 'none';
    
    setTimeout(() => {  
        element.textContent = original;
        element.style.pointerEvents = 'auto';
    }, duration);
}


function copyMessage(element) {
    // Find the closest message container (either .message-user or .message-bot)
    const messageContainer = element.closest('.message-user, .message-bot');

    // Extract only the text content without including the icons or other elements
    const messageText = Array.from(messageContainer.childNodes)
        .filter(node => node.nodeType === Node.TEXT_NODE) // Only text nodes
        .map(node => node.textContent.trim()) // Get text and trim spaces
        .join(''); // Join text together

    // Copy the message text to the clipboard
    navigator.clipboard.writeText(messageText)
        .then(() => {
            console.log('Message copied: ', messageText);
        })
        .catch(err => {
            console.error('Failed to copy: ', err);
        });

    temporaryIconChange(element, 'check', 1000);

}

function editMessage(element) {
    const messageContainer = element.closest('.message-user, .message-bot');

    // Extract only the text content without including the icons or other elements
    const messageText = Array.from(messageContainer.childNodes)
        .filter(node => node.nodeType === Node.TEXT_NODE)
        .map(node => node.textContent.trim())
        .join('');

    temporaryIconChange(element, 'check', 1000);

    const textarea = document.getElementById('messageInput');
    textarea.value = messageText;

    autoResizeTextarea(textarea);
    textarea.focus();
}


function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto'; // Reset the height so it can shrink on backspace
    const rows = textarea.scrollHeight / textarea.offsetHeight;

    if (rows < 5)
        textarea.style.height = `${textarea.scrollHeight}px`; // Adjust height
    else {
        textarea.style.height = 'calc(1.5em * 5)'; // Set to max height if exceeded
        textarea.style.overflowY = 'auto'; // Show scrollbar if limit is exceeded
    }
}

function toggleChat() {
    const chatContainer = document.getElementById('chatContainer');
    const chatToggle = document.getElementById('chatToggle');
    const overlay = document.getElementById('overlay');

    if (chatContainer.classList.contains('open')) {
        chatContainer.classList.remove('open');
        chatToggle.classList.remove('hidden');
        overlay.style.display = 'block';
    } else {
        chatContainer.classList.add('open');
        chatToggle.classList.add('hidden');
    }
}
