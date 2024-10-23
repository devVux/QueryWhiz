
class QueryApplier {
    
    apply(query) {
        throw new Error("Cannot call `apply` on abstract class");
    }

}

class TestQueryApplier {

	apply(query) {
		return `[backend response]: ${query}`;
	}
	
}

class AlaSQLQueryApplier extends QueryApplier {
	constructor(name, data) {
        super();
        this.name = name;
		this.data = data;
	}
	
	apply(query) {
		const count = (query.match(this.name) || []).length;
		query = query.replaceAll(this.name, '?');

		let results = [];
		for (let i = 0; i < count; i++)
			results.push(this.data);

	        const res = alasql(query, results);
		return res;
	}

}

export { TestQueryApplier, AlaSQLQueryApplier };