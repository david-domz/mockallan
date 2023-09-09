from pytest import fixture
from http import HTTPStatus
from app_handler import AppHandler, StubConfig, HTTPRequest, HTTPResponse


@fixture
def app_handler(config: StubConfig):

	yield AppHandler(config)


def test_handle_request_get_config_status_200(app_handler: AppHandler):

	request = HTTPRequest('GET', '/config')
	response = app_handler.handle_request(request)

	assert response.code == 200


def test_handle_request_get_unknown_path_default_response(config: StubConfig, app_handler: AppHandler):

	# Act
	request = HTTPRequest('GET', '/unknown')
	response = app_handler.handle_request(request)

	# Assert
	assert response == config.default_response

	assert len(app_handler.request_registry.request_records) == 1

	request_record = app_handler.request_registry.request_records[0]
	assert request == request_record.request
	assert response == request_record.response


def test_handle_request_get_assert_called_status_200(config: StubConfig, app_handler: AppHandler):

	# Arrange
	unknown_path_1 = '/unknown/path/1'

	request = HTTPRequest(
		'GET',
		unknown_path_1
	)
	response = app_handler.handle_request(request)

	assert response == config.default_response

	# Act
	assert_called_request = HTTPRequest(
		'GET',
		'/assert-called',
		{
			'method': ['GET'],
			'path': [unknown_path_1]
		}
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	# Assert
	assert assert_called_response.code == 204


def test_handle_request_get_assert_called_status_409(config: StubConfig, app_handler: AppHandler):

	# Arrange
	request = HTTPRequest('GET', '/unknown/path/1')
	response = app_handler.handle_request(request)

	assert response == config.default_response

	# Act
	assert_called_request = HTTPRequest(
		'GET',
		'/assert-called',
		{
			'method': ['GET'],
			'path': ['/unknown/path/2']
		}
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	# Assert
	assert assert_called_response.code == 409


def test_handle_request_get_assert_called_status_400(config: StubConfig, app_handler: AppHandler):
	"""

	Given:
		- AppHandler handles GET /unknown/path/1
	When:
		- AppHandler handles GET /assert-called
		- Query does not include method and path
	Then:
		- AppHandler returns 400 Bad Request

	"""
	# Arrange
	request = HTTPRequest('GET', '/unknown/path/1')
	response = app_handler.handle_request(request)

	assert response == config.default_response

	# Act
	assert_called_request = HTTPRequest(
		'GET',
		'/assert-called',
		{
			'methodology': ['GET'],
			'pathetic': ['/unknown/path/2']
		}
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	# Assert
	assert assert_called_response.code == 400


def test_handle_request_get_assert_called_once_status_200(config: StubConfig, app_handler: AppHandler):

	unknown_path_1 = '/unknown/path/1'

	# Act
	request = HTTPRequest(
		'GET',
		unknown_path_1
	)
	response = app_handler.handle_request(request)

	# Assert
	assert response == config.default_response

	assert_called_request = HTTPRequest(
		'GET',
		'/assert-called-once',
		{
			'method': ['GET'],
			'path': [unknown_path_1]
		}
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	assert assert_called_response.code == 204


def test_handle_request_get_assert_called_once_status_409(config: StubConfig, app_handler: AppHandler):
	"""

	Given:
		- 2 requests GET /unknown/path/1
	When:
		- GET /assert-called-once
	Then:
		- status 409 Conflict

	"""
	path = '/unknown/path/1'

	# Arrange
	app_handler.handle_request(HTTPRequest('GET', path))
	app_handler.handle_request(HTTPRequest('GET', path))

	# Act
	response = app_handler.handle_request(
		HTTPRequest(
			'GET',
			'/assert-called-once',
			{
				'method': ['GET'],
				'path': [path]
			}
		)
	)

	# Assert
	assert response.code == HTTPStatus.CONFLICT
