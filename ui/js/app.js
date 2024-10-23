import { TestQueryApplier } from "./core/queryApplier.js";
import { TestGenerator, QueryWhizAPIGenerator } from "./core/responseGenerator.js";
import { MessageController } from "./core/messageController.js";


const sendButton = document.getElementById('sendButton');
const textarea = document.getElementById('messageInput');
const schemaInput = document.getElementById('schemaInput');


var apiService = new QueryWhizAPIGenerator(schemaInput.value.replace(/\s+/g, ' '));
const queryApplier = new TestQueryApplier('articoli', []);
const messageHandler = new MessageController(apiService, queryApplier);


textarea.addEventListener('input', function() {
	autoResizeTextarea(textarea);
});

textarea.addEventListener('keypress', function(event) {
	if (event.key === 'Enter' && !event.shiftKey) {
		event.preventDefault();
		sendButton.click();	
	}
});

sendButton.addEventListener('click', function(event) {
	const message = textarea.value.trim();
	if (message === '')
		return;

	textarea.value = '';
	autoResizeTextarea(textarea);

	messageHandler.handleMessage(message);
});

schemaInput.addEventListener('keypress', function(event) {
	if (event.key === 'Enter' && !event.shiftKey) {
		event.preventDefault();
		apiService.setContext(schemaInput.value.replace(/\s+/g, ' '));
	}
});
