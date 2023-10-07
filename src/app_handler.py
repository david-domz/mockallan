import json
import jsonschema
from request import ContentType, HTTPRequest, HTTPResponse
from stub_config import StubConfig
from history import History, RequestRecord


class AppHandler():

	def __init__(self, config: StubConfig, history: History | None = None):

		if history is None:
			history = History()

		self._config = config
		self._api_endpoints = {
			# Stub Configuration API
			('GET', '/config'): self._get_config,
			('PUT', '/config'): self._put_config,
			# Assertion API
			('GET', '/assert-called'): self._assert_called,
			('GET', '/assert-called-once'): self._assert_called_once,
			('POST', '/assert-called-with'): self._assert_called_with,
			('POST', '/assert-called-once-with'): self._assert_called_once_with,
			('GET', '/call-args'): self._call_args,
			('GET', '/call-args-list'): self._call_args_list,
			('GET', '/call-count'): self._call_count
		}

		self._history = history


	@property
	def history(self) -> History:

		return self._history


	def handle_request(self, request: HTTPRequest) -> HTTPResponse:

		response = self._handle_api_request(request)
		if response is None:
			response = self._handle_test_request(request)

		return response


	def _handle_api_request(self, request: HTTPRequest) -> HTTPResponse | None:
		"""Handles Stub Configuration/Assertion API request by the test client. """

		endpoint = (request.method.upper(), request.path)
		method = self._api_endpoints.get(endpoint)
		if method:
			try:
				return method(request)
			except jsonschema.SchemaError as e:
				# Raised by
				# History.assert_called_with() or
				# History.assert_called_once_with()
				return self._create_json_schema_error_response(request, e)

		return None


	def _handle_test_request(self, request: HTTPRequest) -> HTTPResponse:

		response = self._config.lookup(request)

		self._history.append(request, response)

		return response


	def _get_config(self, request: HTTPRequest) -> HTTPResponse:	# pylint: disable=unused-argument

		return HTTPResponse(
			200,
			ContentType.APPLICATION_JSON,
			self._config.dump_json()
		)


	def _put_config(self, request: HTTPRequest) -> HTTPResponse:

		if isinstance(request.body, str):
			request.body = json.loads(request.body)
		self._config.load_json(request.body)

		return HTTPResponse(204)


	def _assert_called(self, request: HTTPRequest) -> HTTPResponse:	# pylint: disable=unused-argument

		try:
			method_called = request.query['method'][0]
			path_called = request.query['path'][0]
			endpoint_called = (method_called, path_called)
		except KeyError:
			response = HTTPResponse(
				400,
				headers=ContentType.APPLICATION_JSON_ERROR,
				body={
					"status": 400,
					"type": "missing-query-param",
					"message": "Bad request. Query parameter {e} not found."
				}
			)
		else:
			call_count = self._history.call_count(endpoint_called)

			if call_count > 0:
				response = self._create_assertion_success_response(request, endpoint_called, call_count)
			else:
				response = self._create_assertion_error_response(request, endpoint_called, 1, call_count)

		return response


	def _assert_called_once(self, request: HTTPRequest) -> HTTPResponse:	# pylint: disable=unused-argument

		method_called = request.query['method'][0]
		path_called = request.query['path'][0]
		endpoint_called = (method_called, path_called)

		call_count = self._history.call_count(endpoint_called)

		if call_count == 1:
			response = self._create_assertion_success_response(request, endpoint_called, call_count)
		else:
			response = self._create_assertion_error_response(request, endpoint_called, 1, call_count)

		return response


	def _assert_called_with(self, request: HTTPRequest) -> HTTPResponse:	# pylint: disable=unused-argument

		try:
			method_called = request.query['method'][0]
			path_called = request.query['path'][0]
			endpoint_called = (method_called, path_called)
		except KeyError as e:
			response = self._create_query_param_not_found_error_response(e)
		else:
			try:
				self._history.assert_called_with(endpoint_called, request)
			except AssertionError as e:
				response = self._create_assertion_error_response(request, endpoint_called, 1, 0)
			else:
				response = self._create_assertion_success_response(request, endpoint_called, 1)

		return response


	def _assert_called_once_with(self, request: HTTPRequest) -> HTTPResponse:	# pylint: disable=unused-argument

		try:
			method_called = request.query['method'][0]
			path_called = request.query['path'][0]
			endpoint_called = (method_called, path_called)
		except KeyError as e:
			response = self._create_query_param_not_found_error_response(e)
		else:
			try:
				self._history.assert_called_once_with(endpoint_called, request)
			except AssertionError as e:
				response = self._create_assertion_error_response(request, endpoint_called, 1, 0)
			else:
				response = self._create_assertion_success_response(request, endpoint_called, 1)

		return response


	def _call_args(self, request: HTTPRequest) -> HTTPResponse:
		"""

		Returns:
			HTTPResponse	A 200 response with the Content-Type and body that the mock was
				last called with.
					A 409 response if the mock wasn't called yet.

		"""
		try:
			content_type, body = self._history.call_args()
		except AssertionError:
			status = 409
			headers = ContentType.APPLICATION_JSON_ERROR
			body = {
				"status": status,
				"type": "assertion-error",
				"title": "No request was performed by the software under test (SUT)",
			}
		else:
			status = 200
			headers = {'Content-Type': content_type}

		return HTTPResponse(status, headers, body)


	def _call_args_list(self, request: HTTPRequest) -> HTTPResponse:
		"""

		Returns:
			HTTPResponse	A 200 response with the Content-Type application/json and
				a list of request records in the body.

		"""
		def create_request_record(request_record: RequestRecord) -> dict:

			# E.g. 2023-10-02T21:48:16Z
			timestamp_str = request_record.timestamp.isoformat(sep='T', timespec='seconds') + 'Z'

			return {
				"date-time": timestamp_str,
				"request": (
					f'{request_record.request.method} {request_record.request.path} '
					f'{request_record.request.body}'
				),
				"response": (
					f'{request_record.response.code} {request_record.response.body}'
				)
			}

		request_records = self._history.call_args_list()

		status = 200
		headers = ContentType.APPLICATION_JSON
		records_json = {
			"items": [create_request_record(request_record) for request_record in request_records]
		}

		return HTTPResponse(status, headers, records_json)


	def _call_count(self, request: HTTPRequest) -> HTTPResponse:	# pylint: disable=unused-argument

		method = request.query.get('method')
		path = request.query.get('path')
		if method:
			if path:
				# Endpoint's call count
				method_called = method[0]
				path_called = path[0]
				endpoint_called = (method_called, path_called)
				count = self._history.call_count(endpoint_called)
				response = self._create_call_count_response(count, endpoint_called)
			else:
				response = self._create_query_param_not_found_error_response(KeyError('path'))
		else:
			if path:
				response = self._create_query_param_not_found_error_response(KeyError('method'))
			else:
				# Total call count
				count = self._history.call_count()
				response = self._create_call_count_response(count)

		return response


	@staticmethod
	def _create_call_count_response(count: int, endpoint: tuple[str, str] | None = None) -> HTTPResponse:

		body = {
			"status": 200,
			"call_count": count
		}
		if endpoint:
			body['method'] = endpoint[0]
			body['path'] = endpoint[1]

		return HTTPResponse(
			200,
			headers={'Content-Type': 'application/json'},
			body=body
		)


	@staticmethod
	def _create_json_schema_error_response(
			assert_request: HTTPRequest,
			e: jsonschema.SchemaError) -> HTTPResponse:

		status = 400
		headers = ContentType.APPLICATION_JSON_ERROR
		body = {
			"status": status,
			"type": "json-schema-error",
			"title": f"JSON-schema assertion request {assert_request.method} {assert_request.path} failed",
			"detail": f"{e.__class__.__name__}: {e}"
		}

		return HTTPResponse(status, headers, body)


	@staticmethod
	def _create_assertion_success_response(
			assert_request: HTTPRequest,
			endpoint_called: tuple[str, str],
			call_count: int) -> HTTPResponse:

		status = 200
		headers = {'Content-Type': 'application/json'}
		body = {
			"status": status,
			"type": "assertion-success",
			"title": f"Assertion request {assert_request.method} {assert_request.path} succeeded",
			"detail": f"{endpoint_called[0]} {endpoint_called[1]} called {call_count} times."
		}

		return HTTPResponse(status, headers, body)

	@staticmethod
	def _create_assertion_error_response(
			assert_request: HTTPRequest,
			endpoint_called: tuple[str, str],
			expected_call_count: int,
			call_count: int) -> HTTPResponse:

		status = 409
		headers = {'Content-Type': 'application/json+error'}
		body = {
			"status": status,
			"type": "assertion-error",
			"title": f"Assertion request {assert_request.method} {assert_request.path} failed",
			"detail": f"Expected {endpoint_called[0]} {endpoint_called[1]} to be called {expected_call_count} times. Called {call_count} times."
		}

		return HTTPResponse(status, headers, body)


	@staticmethod
	def _create_query_param_not_found_error_response(key_error: KeyError) -> HTTPResponse:

		return HTTPResponse(
			400,
			headers={'Content-Type': 'application/json+error'},
			body={
				"status": 400,
				"type": "missing-query-param",
				"message": f"Bad request. Query parameter {key_error} not found."
			}
		)
