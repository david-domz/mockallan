import json
import jsonschema
from stub_config import StubConfig, HTTPRequest, HTTPResponse
from history import History, RequestRecord


class AppHandler():

	def __init__(self, config: StubConfig):

		self._config = config
		self._api_endpoints = {
			# Stub Configuration API
			('GET', '/config'): self._get_config,
			('PUT', '/config'): self._put_config,
			# Mock Assertion API
			('GET', '/assert-called'): self._assert_called,
			('GET', '/assert-called-once'): self._assert_called_once,
			('GET', '/assert-called-with'): self._assert_called_with,
			('GET', '/assert-called-once-with'): self._assert_called_once_with,
			('GET', '/call-args'): ...,
			('GET', '/call-count'): ...,
			('GET', '/method-calls'): ...
		}

		self._history = History()


	@property
	def request_registry(self) -> History:

		return self._history


	def handle_request(self, request: HTTPRequest) -> HTTPResponse:
		"""

		TO DO: Better naming
			E.g. _handle_config_request()
				_handle_assert_request()
				_handle_test_request()

		"""
		response = self._handle_config_request(request)
		if response is None:
			response = self._handle_test_request(request)

		return response


	def _handle_config_request(self, request: HTTPRequest) -> HTTPResponse | None:
		"""Handles request by system under test. """

		endpoint = (request.method.upper(), request.path)
		method = self._api_endpoints.get(endpoint)
		if method:
			try:
				return method(request)
			except jsonschema.SchemaError as e:
				return self._create_json_schema_error_response(request, e)

		return None


	def _handle_test_request(self, request: HTTPRequest) -> HTTPResponse:
		"""Handles request by system under test. """

		response = self._config.lookup(request)
		if response is None:
			response = self._config.default_response

		self._history.request_records.append(RequestRecord(0.0, request, response))

		return response


	def _get_config(self, request: HTTPRequest) -> HTTPResponse:	# pylint: disable=unused-argument

		response_json = self._config.dump_json()
		response_str = json.dumps(response_json)
		return HTTPResponse(
			200,
			{'Content-type': 'application/json'},
			response_str
		)


	def _put_config(self, request: HTTPRequest) -> HTTPResponse:

		request_body_json = json.loads(request.body)
		self._config.load_json(request_body_json)

		return HTTPResponse(204)


	def _assert_called(self, request: HTTPRequest) -> HTTPResponse:	# pylint: disable=unused-argument

		try:
			method_called = request.query['method'][0]
			path_called = request.query['path'][0]
			endpoint_called = (method_called, path_called)
		except KeyError as e:
			# TODO
			# JSON response body with status, type, title, detail
			# dumps()
			response = HTTPResponse(
				400,
				headers={'Content-Type': 'application/json+error'},
				body=f'{{"message": "Bad request. Query parameter {e} not found."}}'
			)
		else:
			call_count = self._history.call_count(method_called, path_called)

			if call_count > 0:
				response = HTTPResponse(204)
			else:
				response = self._create_assertion_error_response(request, endpoint_called, 1, call_count)

		return response


	def _assert_called_once(self, request: HTTPRequest) -> HTTPResponse:	# pylint: disable=unused-argument

		method_called = request.query['method'][0]
		path_called = request.query['path'][0]
		endpoint_called = (method_called, path_called)

		call_count = self._history.call_count(method_called, path_called)

		if call_count == 1:
			response = HTTPResponse(204)
		else:
			# response = HTTPResponse(
			# 	409,
			# 	headers={'Content-Type': 'application/json+error'},
			# 	body='{\"message\": \"/assert-called-once assertion failed.\"}'
			# 	# TO DO: endpoint method, path was called (x) times
			# )
			response = self._create_assertion_error_response(request, endpoint_called, 1, call_count)

		return response


	def _assert_called_with(self, request: HTTPRequest) -> HTTPResponse:	# pylint: disable=unused-argument

		# TO DO: 400 Bad request if KeyError
		try:
			method_called = request.query['method'][0]
			path_called = request.query['path'][0]
			endpoint_called = (method_called, path_called)
		except KeyError as e:
			# TODO
			# JSON response body with status, type, title, detail
			# dumps()
			response = HTTPResponse(
				400,
				headers={'Content-Type': 'application/json+error'},
				body=f'{{"message": "Bad request. Query parameter {e} not found."}}'
			)
		else:
			call_count = self._history.call_count(method_called, path_called)



			if call_count > 0:
				response = HTTPResponse(204)
			else:
				response = self._create_assertion_error_response(request, endpoint_called, 1, call_count)

		return response


	def _assert_called_once_with(self, request: HTTPRequest) -> HTTPResponse:	# pylint: disable=unused-argument

		try:
			method_called = request.query['method'][0]
			path_called = request.query['path'][0]
			endpoint_called = (method_called, path_called)
		except KeyError as e:
			# TODO
			# JSON response body with status, type, title, detail
			# dumps()
			response = HTTPResponse(
				400,
				headers={'Content-Type': 'application/json+error'},
				body=f'{{"message": "Bad request. Query parameter {e} not found."}}'
			)
		else:
			try:
				self._history.assert_called_once_with(endpoint_called, request)
			except AssertionError as e:
				response = self._create_assertion_error_response(request, endpoint_called, 1, 0)
			else:
				response = HTTPResponse(204)

		return response

	@staticmethod
	def _create_json_schema_error_response(
			assert_request: HTTPRequest,
			e: jsonschema.SchemaError) -> HTTPResponse:

		status = 400
		headers = {'Content-Type': 'application/json+error'}
		body = {
			"status": status,
			"type": "json-schema-error",
			"title": f"JSON-schema assertion request {assert_request.method} {assert_request.path} failed",
			"detail": f"{e.__class__.__name__}: {e}"
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
			"detail": f"{endpoint_called[0]} {endpoint_called[1]} expected call count was {expected_call_count} but actual call count was {call_count}.",
			"detail_": "Query parameter {e} not found."
		}

		return HTTPResponse(status, headers, body)
