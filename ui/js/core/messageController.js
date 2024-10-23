
class MessageController {
    constructor(apiService, queryApplier) {
        this.apiService = apiService;
		this.queryApplier = queryApplier;
    }

	handleMessage(message) {
		if (message) {
			document.dispatchEvent(new CustomEvent('user.message', { detail: {
				'content': message
			}}));
			document.dispatchEvent(new Event('response.generation.start'));
			

			var formattedResponse;
			this.apiService.generate(message)
			.then(response => {
				formattedResponse = this.queryApplier.apply(response)
			})
			.catch(error => {
				formattedResponse = "Unable to get response";
				console.error(error);
			})
			.finally(() => {
 				document.dispatchEvent(new CustomEvent('response.generation.end', { detail: {
					'content': formattedResponse 
				}}));
			});

		}
	}

}

export { MessageController };   
