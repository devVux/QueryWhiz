from flask import Blueprint, request, jsonify
from flasgger import swag_from
from pydantic import ValidationError

from app.core.base_response import Response
from app.core.base_request import UserRequest
from app.core.base_model import TestModel

from app.models.huggingface_model import DefogAI

api = Blueprint('query_whiz', __name__)
model = DefogAI() 


#@swag_from('../../docs/api.yaml')
@api.route('/', methods=['GET'])
def testsa():
    return "ok", 200


@swag_from('../../docs/generate.yaml')
@api.route('/', methods=['POST'])
def generate():

    try:

        # Parse and validate the request JSON using Pydantic
        data = request.get_json()
        validated_data = UserRequest(**data)

        sql_query = model.generate(validated_data)

        return Response.success(data=sql_query)

    except ValidationError as e:
        return Response.error(e.errors(), "Invalid request")
