import json
from request import HTTPRequest, HTTPResponse


class MissingProperty(Exception):
	def __init__(self, property: str):
		super().__init__(f'{property}: missing required property')


class UnexpectedProperty(Exception):
	def __init__(self, property: str):
		super().__init__(f'{property}: unexpected property')


class StubConfig():
	"""Stub Configuration. Holds default and per-endpoint responses.

	Attributes:
		_default_response (HTTPResponse):			Default response.
		_endpoints (dict[tuple[str, str], HTTPResponse]):	Per-endpoint response mapping.

	"""
	_FACTORY_DEFAULT_RESPONSE = HTTPResponse(
		status_code=200,
		headers={
			"Content-Type": "application/json"
		},
		body={
			"status": "200",
			"message": "This is mockallan factory default response."
		}
	)

	def __init__(self, config_json=None):
		"""

		Args:
			config_json (dict | str):	If type is a `str` then it is the path to a stub config JSON file.

		"""
		self._default_response = StubConfig._FACTORY_DEFAULT_RESPONSE
		self._endpoints = {}

		if config_json is not None:
			if isinstance(config_json, dict):
				self.load_json(config_json)
			elif isinstance(config_json, str):
				with open(config_json, encoding='utf-8') as fp:
					self.load_json(json.load(fp))


	@property
	def default_response(self) -> HTTPResponse:
		return self._default_response


	def load_json(self, config_json: dict):
		"""

		Raises:
			MissingProperty
			TypeError

		"""
		try:
			defaults_json = config_json['defaults']
			default_response_json = defaults_json['response']
		except KeyError as e:
			raise MissingProperty(e) from e

		self._default_response = HTTPResponse(**default_response_json)

		self._endpoints = {}

		endpoints_json = config_json.get('endpoints', [])
		for endpoint_json in endpoints_json:
			try:
				request_json = endpoint_json['request']
			except KeyError as e:
				raise MissingProperty(e) from e

			request = HTTPRequest(**request_json)
			endpoint = (request.method.upper(), request.path)

			self._endpoints[endpoint] = StubConfig._load_response_json(endpoint_json)


	@staticmethod
	def _load_response_json(endpoint_json: dict) -> HTTPResponse | list[HTTPResponse]:

		try:
			response_json = endpoint_json['response']
		except KeyError as e:
			raise MissingProperty(e) from e

		if isinstance(response_json, dict):
			response = HTTPResponse(**response_json)
		elif isinstance(response_json, list):
			response = [HTTPResponse(**response_json_item) for response_json_item in response_json]
		else:
			raise ValueError(f'Error loading response JSON element. Invalid type {type(response_json)}')

		return response


	def dump_json(self) -> dict:

		default_response_json = {
			"status_code": self._default_response.status_code,
			"headers": self._default_response.headers,
			"body": self._default_response.body
		}

		endpoints_json = []
		for endpoint, response in self._endpoints.items():
			method = endpoint[0]
			path = endpoint[1]

			if isinstance(response, list):
				output_response = []
				for response_item in response:
					output_response.append(
						{
							"status_code": response_item.status_code,
							"headers": response_item.headers,
							"body": response_item.body
						}
					)
			elif isinstance(response, HTTPResponse):
				output_response = {
					"status_code": response.status_code,
					"headers": response.headers,
					"body": response.body
				}

			endpoint_json = {
				"request": {
					"method": method,
					"path": path
				},
				"response": output_response
			}
			endpoints_json.append(endpoint_json)

		return {
			"defaults": {
				"response": default_response_json
			},
			"endpoints": endpoints_json
		}


	def lookup(self, request: HTTPRequest) -> HTTPResponse | None:

		endpoint = HTTPRequest.endpoint(request)
		response =  self._endpoints.get(endpoint)
		if response is None:
			response = self._default_response

		return response
