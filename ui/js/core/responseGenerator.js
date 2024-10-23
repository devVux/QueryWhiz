
class ResponseGenerator {
	constructor(context) {
		this.context = context;
	}

	setContext(context) {
		this.context = context;
	}

	async generate(question) {
		throw new Error("Cannot call `generate` on abstract class");
	}
}

class TestGenerator extends ResponseGenerator {
	async generate(question) {
		return new Promise((resolve) => {
			setTimeout(() => {
				resolve("select 'This is a test response' as answer");
			}, 1000);
		});
	}
}

class QueryWhizAPIGenerator extends ResponseGenerator {
    async generate(question) {
        const response = await fetch('http://localhost/api/v1/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
				'context': this.context,
				'question': question
			}),
			signal: AbortSignal.timeout(10000)
        });

        if (!response.ok) 
			return 'Unable to process that request';

        const data = await response.json();
        return data['data'];
    }
}

export { ResponseGenerator, TestGenerator, QueryWhizAPIGenerator };
