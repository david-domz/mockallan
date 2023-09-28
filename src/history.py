from dataclasses import dataclass, field
from request import HTTPRequest, HTTPResponse
from validators import (
	Validator,
	IsEqualValidator,
	JSONSchemaValidator,
	XMLSchemaValidator,
	RegexValidator
)


@dataclass
class RequestRecord:
	timestamp: float
	request: HTTPRequest
	response: HTTPResponse


@dataclass
class History:

	# TO DO: Make attrs private to enforce consistency
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


	def call_count(self, endpoint: tuple[str, str] | None = None) -> int:

		if endpoint is None:
			return len(self.request_records)

		return len(self.endpoint_record_mapping.get(endpoint, []))


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
			validator = self._resolve_validator(request)
			for record in records:
				if validator.validate(record.request):
					return

		raise AssertionError('Not called')


	def assert_called_once_with(self, endpoint: tuple[str, str], request: HTTPRequest):

		match_count = 0

		try:
			records = self.endpoint_record_mapping[endpoint]
		except KeyError:
			...
		else:
			validator = self._resolve_validator(request)
			for record in records:
				if validator.validate(record.request):
					match_count += 1
					if match_count > 1:
						raise AssertionError('Called more than once')
		if match_count == 0:
			raise AssertionError('Not called')


	@staticmethod
	def _resolve_validator(validation_request: HTTPRequest) -> Validator:

		validation_content_type = validation_request.headers.get('Content-Type')

		if validation_content_type == 'application/schema+json':
			return JSONSchemaValidator(validation_request)

		if validation_content_type == 'application/xml':
			return XMLSchemaValidator(validation_request)

		validator_header = validation_request.headers.get('X-Mockallan-Validator')
		if validator_header == 'regex':
			return RegexValidator(validation_request)

		return IsEqualValidator(validation_request)
