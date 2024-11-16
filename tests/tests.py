import pytest
from unittest.mock import patch
from flask import json

from app.core.base_request import UserRequest
from app.core.base_model import Model
from app.core.base_response import Response
from app.api.whiz import api


# Mock Classes
class MockLogger:
	def __init__(self):
		self.debug_messages = []
		self.error_messages = []

	def debug(self, message):
		self.debug_messages.append(message)

	def error(self, message, exc_info=None):  # Added exc_info parameter
		self.error_messages.append({
			'message': message,
			'exc_info': exc_info
		})


class MockModel(Model):
	def generate(self, data: UserRequest) -> str:
		return "mocked_sql_query"


# Fixtures
@pytest.fixture
def app():
	from flask import Flask
	app = Flask(__name__)
	app.register_blueprint(api, url_prefix='/api/v1')

	# Setup mock logger
	app.logger = MockLogger()
	return app


@pytest.fixture
def client(app):
	return app.test_client()


@pytest.fixture
def app_context(app):
	with app.app_context():
		yield


@pytest.fixture
def valid_request_data():
	return {
		"question": "Show all users",
		"context": "CREATE TABLE users..."
	}


@pytest.fixture
def mock_model():
	return MockModel()


# Test Groups
class TestStatusEndpoint:
	def test_status_returns_ok(self, client):
		"""Test the status endpoint returns 'ok'"""
		response = client.get('/api/v1/status')
		assert response.status_code == 200
		assert response.data.decode('utf-8') == 'ok'


class TestGenerateEndpoint:
	@patch('app.api.whiz.model')
	def test_successful_generation(self, mock_model, client, valid_request_data):
		"""Test successful query generation with mocked model"""
		expected_sql = "SELECT * FROM users"
		mock_model.generate.return_value = expected_sql

		response = client.post(
			'/api/v1/generate',
			data=json.dumps(valid_request_data),
			content_type='application/json'
		)

		assert response.status_code == 200
		data = json.loads(response.data)
		assert data['code'] == 200
		assert data['data'] == expected_sql
		mock_model.generate.assert_called_once()

	@patch('app.api.whiz.model')
	def test_model_exception_handling(self, mock_model, client, valid_request_data):
		"""Test handling of model generation exceptions"""
		mock_model.generate.side_effect = Exception("Model error")

		with patch('app.api.whiz.logger') as mock_logger:
			response = client.post(
				'/api/v1/generate',
				data=json.dumps(valid_request_data),
				content_type='application/json'
			)

			assert response.status_code == 500  # Changed to 500 for server errors
			data = json.loads(response.data)
			assert data['msg'] == 'Internal server error'
			assert 'Model error' in str(data['details'])

	def test_validation_error_handling(self, client):
		"""Test handling of validation errors with invalid input"""
		invalid_data = {"question": 123}

		response = client.post(
			'/api/v1/generate',
			data=json.dumps(invalid_data),
			content_type='application/json'
		)

		assert response.status_code == 400
		data = json.loads(response.data)
		assert 'details' in data

	@patch('app.api.whiz.logger')
	def test_logger_called(self, mock_logger, client, valid_request_data):
		"""Test that logger is called with appropriate messages"""
		response = client.post(
			'/api/v1/generate',
			data=json.dumps(valid_request_data),
			content_type='application/json'
		)

		assert response.status_code == 200
		assert mock_logger.debug.called


class TestResponse:
	def test_success_response(self, app_context):
		"""Test success response creation"""
		test_data = {"key": "value"}
		response, code = Response.success(data=test_data)

		assert code == 200
		response_data = json.loads(response.data)
		assert response_data['code'] == 200
		assert response_data['data'] == test_data
		assert isinstance(response_data['time'], float)

	def test_error_response(self, app_context):
		"""Test error response creation"""
		test_details = ["error1", "error2"]
		response, code = Response.error(details=test_details)

		assert code == 400
		response_data = json.loads(response.data)
		assert response_data['code'] == 400
		assert response_data['details'] == test_details
		assert isinstance(response_data['time'], float)


@pytest.mark.integration
class TestIntegration:
	def test_end_to_end_flow(self, client, valid_request_data):
		"""Test the complete flow from request to response"""
		with patch('app.api.whiz.model') as mock_model:
			expected_sql = "SELECT * FROM users"
			mock_model.generate.return_value = expected_sql

			response = client.post(
				'/api/v1/generate',
				data=json.dumps(valid_request_data),
				content_type='application/json'
			)

			assert response.status_code == 200
			data = json.loads(response.data)
			assert data['data'] == expected_sql


# Parametrized tests for different scenarios
@pytest.mark.parametrize("invalid_data,expected_error", [
	({"question": ""}, "missing context"),
	({"context": ""}, "missing question"),
	({"question": 123, "context": "test"}, "invalid type"),
	({}, "empty request"),
])
def test_various_invalid_requests(client, invalid_data, expected_error):
	"""Test various invalid request scenarios"""
	response = client.post(
		'/api/v1/generate',
		data=json.dumps(invalid_data),
		content_type='application/json'
	)

	assert response.status_code == 400
	data = json.loads(response.data)
	assert data['code'] == 400