from flask import Blueprint, request, jsonify, current_app
from flasgger import swag_from
from pydantic import ValidationError
from flask_cors import CORS
from werkzeug.local import LocalProxy

from app.core.base_response import Response
from app.core.base_request import UserRequest
from app.core.base_model import TestModel

from app.models.huggingface_model import *

api = Blueprint('query_whiz', __name__)
model = TestModel() 

logger = LocalProxy(lambda: current_app.logger)
CORS(api)

@api.route('/status', methods=['GET'])
def status():
    return 'ok'

@swag_from('../../docs/generate.yaml')
@api.route('/generate', methods=['POST'])
def generate():

    try:

        data = request.get_json()
        validated_data = UserRequest(**data)

        sql_query = model.generate(validated_data)
        logger.debug(validated_data)
        logger.debug(sql_query)

        return Response.success(data=sql_query)

    except ValidationError as e:
        return Response.error(e.errors(), "Invalid request")
