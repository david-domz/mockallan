from pytest import fixture
from app_handler import AppHandler, StubConfig, HTTPRequest


@fixture
def app_handler(stub_config: StubConfig):

	yield AppHandler(stub_config)


def test_handle_request_get_config_status_200(app_handler: AppHandler):
	"""Tests GET /config """

	request = HTTPRequest('GET', '/config')
	response = app_handler.handle_request(request)

	assert response.code == 200


def test_handle_request_put_config_status_204(app_handler: AppHandler):
	"""Tests PUT /config """

	request = HTTPRequest(
		'PUT',
		'/config',
		headers='application/json',
		body={
			"defaults": {
				"response": {
					"code": 204,
					"headers": {
						"Content-Type": "application/json"
					},
					"body": ""
				}
			},
			"endpoints": []
		}
	)
	response = app_handler.handle_request(request)

	assert response.code == 204


def test_handle_request_get_unknown_status_200(stub_config: StubConfig, app_handler: AppHandler):
	"""

	When:
		- GET /unknown
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
		- GET /path/1824 has been called
	When:
		- GET /assert-called?method=GET&path=/path/1824
	Then:
		- handle_request() returns status 200, type assertion-success

	"""
	# Arrange
	path = '/path/1824'
	request = HTTPRequest('GET', path)
	app_handler.handle_request(request)

	# Act
	assert_called_request = HTTPRequest(
		'GET',
		'/assert-called',
		{
			'method': ['GET'],
			'path': [path]
		}
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	# Assert
	assert assert_called_response.code == 200
	assert assert_called_response.body['type'] == 'assertion-success'


def test_handle_request_get_assert_called_status_409(stub_config: StubConfig, app_handler: AppHandler):
	"""

	Given:
		- /path/1824 has not been called
	When:
		- GET /assert-called?method=GET&path=/path/1824
	Then:
		- handle_request() returns status 409, type assertion-error

	"""
	assert_called_request = HTTPRequest(
		'GET',
		'/assert-called',
		{
			'method': ['GET'],
			'path': ['/path/1824']
		}
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	assert assert_called_response.code == 409
	assert assert_called_response.body['type'] == 'assertion-error'


def test_handle_request_get_assert_called_status_400(stub_config: StubConfig, app_handler: AppHandler):
	"""

	When:
		- GET /assert-called
		- URL query does not include method and path
	Then:
		- handle_request() returns 400 Bad Request

	"""
	assert_called_request = HTTPRequest(
		'GET',
		'/assert-called',
		{
			'foo': 'bar'
		}
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	assert assert_called_response.code == 400


def test_handle_request_get_assert_called_once_status_200(stub_config: StubConfig, app_handler: AppHandler):
	"""

	Given:
		- GET /path/1823 has been called once
	When:
		- GET /assert-called-once?method=GET&path=/path/1823
	Then:
		- handle_request() returns 200

	"""
	path = '/path/1823'

	# Act
	request = HTTPRequest(
		'GET',
		path
	)
	response = app_handler.handle_request(request)

	# Assert
	assert response == stub_config.default_response

	assert_called_request = HTTPRequest(
		'GET',
		'/assert-called-once',
		{
			'method': ['GET'],
			'path': [path]
		}
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	assert assert_called_response.code == 200


def test_handle_request_get_assert_called_once_status_409(app_handler: AppHandler):
	"""

	Given:
		- 2 requests GET /path/1823
	When:
		- GET /assert-called-once?method=GET&path=/path/1823
	Then:
		- status 409 Conflict

	"""
	path = '/path/1823'

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
	assert response.code == 409


def test_handle_request_get_assert_called_with_status_200(stub_config: StubConfig, app_handler: AppHandler):
	"""

	Given:
		- POST /path/1823 with body 1823 has been called
	When:
		- GET /assert-called-with?method=POST&path=/path/1823 and body 1823
	Then:
		- handle_request() returns 200

	"""
	# Arrange
	path = '/path/1823'

	request = HTTPRequest(
		'POST',
		path,
		headers={
			'Content-Type': 'text/plain'
		},
		body='1823'
	)
	app_handler.handle_request(request)

	# Act
	assert_called_request = HTTPRequest(
		'POST',
		'/assert-called-with',
		{
			'method': ['POST'],
			'path': [path]
		},
		headers={
			'Content-Type': 'text/plain'
		},
		body='1823'
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	assert assert_called_response.code == 200


def test_handle_request_get_assert_called_with_status_409(stub_config: StubConfig, app_handler: AppHandler):
	"""

	Given:
		- POST /path/1823 with body 1823 has been called
	When:
		- GET /assert-called-with?method=POST&path=/path/1823 and body 2023
	Then:
		- handle_request() returns 409

	"""
	# Arrange
	path = '/path/1823'

	request = HTTPRequest(
		'POST',
		path,
		headers={
			'Content-Type': 'text/plain'
		},
		body='1823'
	)
	app_handler.handle_request(request)

	# Act
	assert_called_request = HTTPRequest(
		'POST',
		'/assert-called-with',
		{
			'method': ['POST'],
			'path': [path]
		},
		headers={
			'Content-Type': 'text/plain'
		},
		body='2023'
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	assert assert_called_response.code == 409
	assert assert_called_response.body['type'] == 'assertion-error'


def test_handle_request_get_assert_called_with_status_400_missing_query_param(
		stub_config: StubConfig,
		app_handler: AppHandler):
	"""

	Given:
		- POST /path/1823 with body 1823 has been called
	When:
		- GET /assert-called-with?method=POST without path query parameter
	Then:
		- handle_request() returns 400

	"""
	# Arrange
	path = '/path/1823'

	request = HTTPRequest(
		'POST',
		path,
		headers={
			'Content-Type': 'text/plain'
		},
		body='1823'
	)
	app_handler.handle_request(request)

	# Act
	assert_called_request = HTTPRequest(
		'POST',
		'/assert-called-with',
		{
			'method': ['POST']
			# path query parameter missing
		},
		headers={
			'Content-Type': 'text/plain'
		},
		body='2023'
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	assert assert_called_response.code == 400
	assert assert_called_response.body['type'] == 'missing-query-param'


def test_handle_request_get_assert_called_with_status_400_json_schema_error(
		stub_config: StubConfig,
		app_handler: AppHandler):
	"""

	Given:
		- POST /path/1823 with body 1823 has been called
	When:
		- GET /assert-called-with?method=POST without path query parameter
	Then:
		- handle_request() returns 400

	"""
	# Arrange
	path = '/path/1823'

	request = HTTPRequest(
		'POST',
		path,
		headers={
			'Content-Type': 'application/json'
		},
		body={
			"foo": "bar"
		}
	)
	app_handler.handle_request(request)

	# Act
	assert_called_request = HTTPRequest(
		'POST',
		'/assert-called-with',
		{
			'method': ['POST'],
			'path': [path]
		},
		headers={
			'Content-Type': 'application/schema+json'
		},
		body='Bad JSON schema'
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	assert assert_called_response.code == 400
	assert assert_called_response.headers['Content-Type'] == 'application/json+error'
	assert assert_called_response.body['type'] == 'json-schema-error'


def test_handle_request_get_assert_called_once_with_status_200(stub_config: StubConfig, app_handler: AppHandler):
	"""

	Given:
		- POST /path/1823 with body 1823 has been called once
	When:
		- GET /assert-called-once-with?method=POST&path=/path/1823 and body 1823
	Then:
		- handle_request() returns 200

	"""
	# Arrange
	path = '/path/1823'

	request = HTTPRequest(
		'POST',
		path,
		headers={
			'Content-Type': 'text/plain'
		},
		body='1823'
	)
	app_handler.handle_request(request)

	# Act
	assert_called_request = HTTPRequest(
		'POST',
		'/assert-called-once-with',
		{
			'method': ['POST'],
			'path': [path]
		},
		headers={
			'Content-Type': 'text/plain'
		},
		body='1823'
	)
	assert_called_response = app_handler.handle_request(assert_called_request)

	assert assert_called_response.code == 200


def test_handle_request_get_call_count_status_200(app_handler: AppHandler):
	"""
	
	Given:
		- 2 GET /path/1823 has been called
		- 1 GET / has been called
	When:
		- GET /call-count
	Then:
		- Response has call_count == 3

	"""
	# Arrange
	path = '/path/1823'
	app_handler.handle_request(HTTPRequest('GET', path))
	app_handler.handle_request(HTTPRequest('GET', path))
	app_handler.handle_request(HTTPRequest('GET', '/'))

	# Act
	response = app_handler.handle_request(
		HTTPRequest(
			'GET',
			'/call-count'
		)
	)

	# Assert
	assert response.body['call_count'] == 3


def test_handle_request_get_call_count_per_endpoint_status_200(app_handler: AppHandler):
	"""
	
	Given:
		- 2 GET /path/1823 has been called
		- 1 GET / has been called
	When:
		- GET /call-count?method=GET&path=/path/1823
	Then:
		- Response has call_count == 2

	"""
	# Arrange
	path = '/path/1823'
	app_handler.handle_request(HTTPRequest('GET', path))
	app_handler.handle_request(HTTPRequest('GET', path))
	app_handler.handle_request(HTTPRequest('GET', '/'))

	# Act
	response = app_handler.handle_request(
		HTTPRequest(
			'GET',
			'/call-count',
			query={
				'method': ['GET'],
				'path': ['/path/1823']
			}
		)
	)

	# Assert
	assert response.body['call_count'] == 2


def test_handle_request_get_call_args_status_200(app_handler: AppHandler):
	"""
	
	Given:
		- 1 request was made
	When:
		- GET /call-args
	Then:
		- Response has status 200

	"""
	request_content_type = 'application/octet-stream'
	request_body = b'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

	app_handler.handle_request(
		HTTPRequest(
			'POST',
			'/path/1823',
			headers={'Content-Type': request_content_type},
			body=request_body
		)
	)

	response = app_handler.handle_request(
		HTTPRequest(
			'GET',
			'/call-args'
		)
	)
	assert response.code == 200
	assert response.headers['Content-Type'] == request_content_type
	assert response.body == request_body


def test_handle_request_get_call_args_status_409(app_handler: AppHandler):
	"""
	
	Given:
		- No requests
	When:
		- GET /call-args
	Then:
		- Response has status 409

	"""
	response = app_handler.handle_request(
		HTTPRequest(
			'GET',
			'/call-args'
		)
	)
	assert response.code == 409
	assert response.headers['Content-Type'] == 'application/json+error'
