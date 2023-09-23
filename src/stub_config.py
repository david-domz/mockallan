import json
from request import HTTPRequest, HTTPResponse


class StubConfig():
	"""Stub Configuration. Holds default and per-endpoint responses.

	Attributes:
		_default_response (HTTPResponse)
		_endpoints

	"""
	_FACTORY_DEFAULT_RESPONSE = HTTPResponse(
		code=200,
		headers={
			"Content-Type": "application/json"
		},
		body={
			"status": "200",
			"message": "This is mockallan factory default response.",
			"detail": "Use the Stub Configuration API to configure default and per-endpoint responses."
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

		defaults_json = config_json['defaults']
		default_response_json = defaults_json['response']
		self._default_response = HTTPResponse(**default_response_json)

		self._endpoints = {}

		endpoints_json = config_json['endpoints']
		for endpoint_json in endpoints_json:
			request_json = endpoint_json['request']
			request = HTTPRequest(**request_json)
			endpoint = (request.method.upper(), request.path)

			self._endpoints[endpoint] = StubConfig._load_response_json(endpoint_json)


	@staticmethod
	def _load_response_json(endpoint_json: dict) -> HTTPResponse | list[HTTPResponse]:

		response_json = endpoint_json['response']
		if isinstance(response_json, dict):
			response = HTTPResponse(**response_json)
		elif isinstance(response_json, list):
			response = [HTTPResponse(**response_json_item) for response_json_item in response_json]
		else:
			raise ValueError(f'Error loading response JSON element. Invalid type {type(response_json)}')

		return response


	def dump_json(self) -> dict:

		default_response_json = {
			"code": self._default_response.code,
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
							"code": response_item.code,
							"headers": response_item.headers,
							"body": response_item.body
						}
					)
			elif isinstance(response, HTTPResponse):
				output_response = {
					"code": response.code,
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
