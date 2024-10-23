
document.addEventListener('user.message', (event) => {
    appendUserMessage(event.detail.content);
});

document.addEventListener('response.generation.start', (event) => {
    sendButton.disabled = true;
    sendButton.style.opacity = '0.3';
    appendBotMessage("thinking");
});

document.addEventListener('response.generation.end', (event) => {
    sendButton.disabled = false;
    sendButton.style.opacity = '1';

    // Get the chat history and the last bot message (assuming it's the last child)
    const chatHistory = document.getElementById('chatHistory');
    const messageBotDiv = chatHistory.lastElementChild;


    // Clear the loading dots
    while (messageBotDiv.firstChild)
        messageBotDiv.removeChild(messageBotDiv.firstChild);
    

    // Remove the 'loading' class
    messageBotDiv.classList.remove('loading');


    data = event.detail.content;

    // Add the bot response text
    const messageText = document.createTextNode(data);
    messageBotDiv.appendChild(messageText);

    // Create the options div
    const optionsDiv = document.createElement('div');
    optionsDiv.className = 'options';

    // Create the copy span
    const copySpan = document.createElement('span');
    copySpan.className = 'material-symbols-outlined';
    copySpan.onclick = function() { copyMessage(copySpan); };
    copySpan.textContent = 'content_copy';

    // Append the copy icon to options
    optionsDiv.appendChild(copySpan);
    messageBotDiv.appendChild(optionsDiv);



});

