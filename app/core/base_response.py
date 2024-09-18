from flask import jsonify
from datetime import datetime


class Response:

    @staticmethod
    def success(data=None, message="Success", code=200):
        timestamp = datetime.utcnow().timestamp()
        response = {
            "code": code,
            "msg": message,
            "time": timestamp,
            "data": data or {}
        }
        return jsonify(response), code

    @staticmethod
    def error(details=None, message="Error", code=400):
        timestamp = datetime.utcnow().timestamp()
        response = {
            "code": code,
            "msg": message,
            "time": timestamp,
            "details": details or {}
        }
        return jsonify(response), code
