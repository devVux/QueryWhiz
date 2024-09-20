from flask import Flask
from flasgger import Swagger
from app.api.whiz import api

app = Flask(__name__)


template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask QueryWhiz API",
        "description": "This API was developed using Python Flask, which provides an interface for producing and consuming messages via HTTP endpoints.",
        "version": "1.0"
    }
}
app.config['SWAGGER'] = {
    'title': 'Flask QueryWhiz API',
    'uiversion': 2,
    'template': './resources/flasgger/swagger_ui.html'
}
Swagger(app, template=template)


app.register_blueprint(api, url_prefix='/api/v0')

if __name__ == '__main__':

    app.run(debug=True, use_reloader=False)
