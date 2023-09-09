from dataclasses import dataclass, field
import jsonschema
from request import HTTPRequest, HTTPResponse


@dataclass
class RequestRecord:
	timestamp: float
	request: HTTPRequest
	response: HTTPResponse


@dataclass
class History:
	request_records: list[RequestRecord] = field(default_factory=list)
	endpoint_record_mapping: dict = field(default_factory=dict)

	def append(self, request: HTTPRequest, response: HTTPResponse):

		record = RequestRecord(0.0, request, response)
		endpoint = (request.method, request.path)

		self.request_records.append(record)

		endpoint_records = self.endpoint_record_mapping.get(endpoint)
		if endpoint_records is None:
			self.endpoint_record_mapping[endpoint] = [record]
		else:
			endpoint_records.append(record)


	def append_many(self, requests_responses: list[tuple[HTTPRequest, HTTPResponse]]):

		for request_response in requests_responses:
			self.append(request_response[0], request_response[1])


	def call_count(self, method: str, path: str) -> int:
		# TO DO: tuple[str, str]

		call_count = 0
		for request_record in self.request_records:
			if request_record.request.method == method and request_record.request.path == path:
				call_count += 1
		return call_count


	def call_args(self) -> HTTPRequest | None:
		"""

		This is either None (if the mock hasn't been called), or the arguments that the mock was last called with.

		"""
		try:
			return self.request_records[-1].request
		except IndexError:
			return None


	def call_args_list(self)-> list[RequestRecord]:
		"""

		This is a list of all the calls made to the mock object in sequence (so the length of the list is the number of times it has been called).

		"""
		return self.request_records


	def assert_called(self, endpoint: tuple[str, str]):
		"""Assert that the mock was called at least once. """

		if self.endpoint_record_mapping.get(endpoint) is None:
			raise AssertionError('Not called')


	def assert_called_once(self, endpoint: tuple[str, str]):
		"""Assert that the mock was called exactly once. """

		records = self.endpoint_record_mapping.get(endpoint)
		if records is None:
			raise AssertionError('Not called')

		if len(records) > 1:
			raise AssertionError('Called more than once')


	def assert_called_with(self, endpoint: tuple[str, str], request: HTTPRequest):

		try:
			records = self.endpoint_record_mapping[endpoint]
		except KeyError:
			...
		else:
			for record in records:
				if History._request_matches(record.request, request):
					return

		raise AssertionError('Not called')


	def assert_called_once_with(self, endpoint: tuple[str, str], request: HTTPRequest):

		match_count = 0

		try:
			records = self.endpoint_record_mapping[endpoint]
		except KeyError:
			...
		else:
			for record in records:
				if History._request_matches(record.request, request):
					match_count += 1
					if match_count > 1:
						raise AssertionError('Called more than once')
		if match_count == 0:
			raise AssertionError('Not called')


	@staticmethod
	def _request_matches(record_request: HTTPRequest, validation_request: HTTPRequest) -> bool:
		"""

		Returns:
			True if record_request matches validation_request, False otherwise.

		Raises:
			jsonschema.SchemaError	Invalid JSON-schema supplied in `validation_request`.

		"""
		matches = False
		content_type = record_request.headers.get('Content-Type')
		with_content_type = validation_request.headers.get('Content-Type')

		if with_content_type == 'application/schema+json' and content_type == 'application/json':
			try:
				jsonschema.validate(record_request.body, validation_request.body)
				matches = True
			except jsonschema.ValidationError:
				...
		else:
			# text/plain
			# application/octet-stream
			# application/json
			matches = record_request == validation_request

		return matches
