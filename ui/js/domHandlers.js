function appendUserMessage(content) {
    const chatHistory = document.getElementById('chatHistory');

    const element = createUserMessage(content);

    chatHistory.appendChild(element);
    chatHistory.scrollTop = chatHistory.scrollHeight;

}

function appendBotMessage(content) {
    const chatHistory = document.getElementById('chatHistory');

    const element = createBotMessage(content);

    chatHistory.appendChild(element);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function createUserMessage(content) {
    // Create the outer message-user div
    const messageUserDiv = document.createElement('div');
    messageUserDiv.className = 'message-user';

    // Create the text node for the message content
    const messageText = document.createTextNode(content);
    messageUserDiv.appendChild(messageText);



    // Create the options div
    const optionsDiv = document.createElement('div');
    optionsDiv.className = 'options';

    // Create the edit span
    const editSpan = document.createElement('span');
    editSpan.className = 'material-symbols-outlined';
    editSpan.onclick = function() { editMessage(editSpan); }; // Attach the edit function
    editSpan.textContent = 'edit'; // Set the text content for the edit icon

    // Create the copy span
    const copySpan = document.createElement('span');
    copySpan.className = 'material-symbols-outlined';
    copySpan.onclick = function() { copyMessage(copySpan); }; // Attach the copy function
    copySpan.textContent = 'content_copy'; // Set the text content for the copy icon

    optionsDiv.appendChild(editSpan);
    optionsDiv.appendChild(copySpan);



    messageUserDiv.appendChild(optionsDiv);

    

    // Return the constructed message user div
    return messageUserDiv;
}

function createBotMessage(content) {
    // Create the outer message-user div
    const messageBotDiv = document.createElement('div');
    messageBotDiv.classList.add('message-bot', 'loading');

    // Create the dots for the loading animation
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('span');
        dot.classList.add('dot');
        messageBotDiv.appendChild(dot);
    }

    return messageBotDiv;
}
