from flask import Flask
from flasgger import Swagger
from app.api.whiz import api
from settings import auto_config

app = Flask(__name__)
app.config.from_object(auto_config)


Swagger(app, template=auto_config.swaggerTemplate)


app.register_blueprint(api, url_prefix='/api/v0')

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True, use_reloader=False)
