from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
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
	timestamp: datetime
	request: HTTPRequest
	response: HTTPResponse


class History:

	def __init__(self, requests_responses: list[tuple[HTTPRequest, HTTPResponse]] | None = None):

		self._request_records = []
		self._endpoint_record_mapping = defaultdict(list)
		if requests_responses:
			for request_response in requests_responses:
				self.append(request_response[0], request_response[1])


	def append(self, request: HTTPRequest, response: HTTPResponse):

		record = RequestRecord(datetime.utcnow(), request, response)
		endpoint = (request.method, request.path)

		self._request_records.append(record)
		self._endpoint_record_mapping[endpoint].append(record)


	def request_count(self, endpoint: tuple[str, str] | None = None) -> int:

		if endpoint is None:
			return len(self._request_records)

		return len(self._endpoint_record_mapping.get(endpoint, []))


	def request_body(self) -> tuple[str, dict | str | bytes]:
		"""
		
		Returns:
			Content-Type (str)
			body (dict | str | bytes)

		Raises:
			AssertionError	If no request was recorded yet.

		"""
		try:
			request = self._request_records[-1].request
		except IndexError as e:
			raise AssertionError('No requests') from e

		return request.headers.get('Content-Type'), request.body


	def request_body_list(self)-> list[RequestRecord]:

		return self._request_records


	def assert_called(self, endpoint: tuple[str, str]):
		"""Assert that the endpoint was called at least once. """

		if self._endpoint_record_mapping.get(endpoint) is None:
			raise AssertionError('Not called')


	def assert_called_once(self, endpoint: tuple[str, str]):
		"""Assert that the mock was called exactly once. """

		records = self._endpoint_record_mapping.get(endpoint)
		if records is None:
			raise AssertionError('Not called')

		if len(records) > 1:
			raise AssertionError('Called more than once')


	def assert_called_with(self, endpoint: tuple[str, str], request: HTTPRequest):

		records = self._endpoint_record_mapping.get(endpoint)
		if records is None:
			raise AssertionError('Not called')

		validator = self._resolve_validator(request)
		for record in records:
			if validator.validate(record.request):
				return

		raise AssertionError('Not called')


	def assert_called_once_with(self, endpoint: tuple[str, str], request: HTTPRequest):

		match_count = 0

		records = self._endpoint_record_mapping.get(endpoint)
		if records is None:
			raise AssertionError('Not called')

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
