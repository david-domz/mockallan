from pytest import fixture
from http import HTTPStatus
from app_handler import AppHandler, StubConfig, HTTPRequest


@fixture
def app_handler(stub_config: StubConfig):

	yield AppHandler(stub_config)


def test_handle_request_get_config_status_200(app_handler: AppHandler):

	request = HTTPRequest('GET', '/config')
	response = app_handler.handle_request(request)

	assert response.code == 200


def test_handle_request_get_unknown_path_default_response(stub_config: StubConfig, app_handler: AppHandler):
	"""

	When:
		- handle_request() is called with GET /unknown
	Then:
		- handle_request() returns default response
		- The request is added to the history

	"""
	request = HTTPRequest('GET', '/unknown')
	response = app_handler.handle_request(request)

	assert response == stub_config.default_response

	assert len(app_handler.request_registry.request_records) == 1

	request_record = app_handler.request_registry.request_records[0]
	assert request == request_record.request
	assert response == request_record.response


def test_handle_request_get_assert_called_status_200(stub_config: StubConfig, app_handler: AppHandler):
	"""

	Given:
		- GET /mockallan-reserve has been called
	When:
		- handle_request() is called with GET /assert-called?method=GET&path=/mockallan-reserve
	Then:
		- handle_request() returns status 200, type assertion-success

	"""
	# Arrange
	path_1 = '/path-1824'

	request = HTTPRequest('GET', path_1)
	response = app_handler.handle_request(request)

	assert response == stub_config.default_response

	# Act
	assert_called_request = HTTPRequest(
		'GET',
		'/assert-called',
		{
			'method': ['GET'],
			'path': [path_1]
		}
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	# Assert
	assert assert_called_response.code == 200
	assert assert_called_response.body['type'] == 'assertion-success'


def test_handle_request_get_assert_called_status_409(stub_config: StubConfig, app_handler: AppHandler):
	"""

	Given:
		- /mockallan-reserve has not been called
	When:
		- handle_request() is called with GET /assert-called?method=GET&path=/mockallan-reserve
	Then:
		- handle_request() returns status 409, type assertion-error

	"""
	# Arrange
	request = HTTPRequest('GET', '/reserve-')
	response = app_handler.handle_request(request)

	assert response == stub_config.default_response

	# Act
	assert_called_request = HTTPRequest(
		'GET',
		'/assert-called',
		{
			'method': ['GET'],
			'path': ['/mockallan-reserve']
		}
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	# Assert
	assert assert_called_response.code == 409
	assert assert_called_response.body['type'] == 'assertion-error'


def test_handle_request_get_assert_called_status_400(stub_config: StubConfig, app_handler: AppHandler):
	"""

	Given:
	When:
		- handle_request() called with GET /assert-called
		- URL query does not include method and path
	Then:
		- handle_request() returns 400 Bad Request

	"""
	# Arrange
	path_1 = '/unknown'
	request = HTTPRequest('GET', path_1)
	response = app_handler.handle_request(request)

	assert response == stub_config.default_response

	# Act
	assert_called_request = HTTPRequest(
		'GET',
		'/assert-called',
		{
			'methodology': ['GET'],	# Invalid query parameter
			'pathetic': [path_1]	# Invalid query parameter
		}
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	# Assert
	assert assert_called_response.code == 400


def test_handle_request_get_assert_called_once_status_200(stub_config: StubConfig, app_handler: AppHandler):

	unknown_path_1 = '/unknown/path/1'

	# Act
	request = HTTPRequest(
		'GET',
		unknown_path_1
	)
	response = app_handler.handle_request(request)

	# Assert
	assert response == stub_config.default_response

	assert_called_request = HTTPRequest(
		'GET',
		'/assert-called-once',
		{
			'method': ['GET'],
			'path': [unknown_path_1]
		}
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	assert assert_called_response.code == 200


def test_handle_request_get_assert_called_once_status_409(stub_config: StubConfig, app_handler: AppHandler):
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
