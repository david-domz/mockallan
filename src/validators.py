from abc import ABC, abstractmethod
import re
from lxml import etree
import jsonschema
from request import HTTPRequest


class Validator(ABC):

	@abstractmethod
	def validate(self, request: HTTPRequest) -> bool:
		...


class IsEqualValidator(Validator):
	"""Validates that request bodies are equal. """

	def __init__(self, validation_request: HTTPRequest):
		self._validation_request = validation_request
	
	def validate(self, request: HTTPRequest) -> bool:

		return request.body == self._validation_request.body


class JSONSchemaValidator(Validator):
	"""Validates a JSON request with a JSON schema. """

	def __init__(self, validation_request: HTTPRequest):
		self._validation_request = validation_request
	
	def validate(self, request: HTTPRequest) -> bool:

		try:
			jsonschema.validate(request.body, self._validation_request.body)
		except jsonschema.ValidationError:
			return False

		return True


class XMLSchemaValidator(Validator):
	"""Validates a XML request with a XML schema. """

	def __init__(self, validation_request: HTTPRequest):
		self._schema = etree.XMLSchema(etree.fromstring(validation_request.body))
	
	def validate(self, request: HTTPRequest) -> bool:

		return self._schema.validate(etree.fromstring(request.body))


class RegexValidator(Validator):
	"""Validates that the request body matches the regex in the validation request body.

	Requires that the assert request includes the header
	'X-Mockallan-Validator: regex' to explicitly select this validator.

	"""
	def __init__(self, validation_request: HTTPRequest):

		assert isinstance(validation_request.body, str)
		self._pattern = re.compile(validation_request.body)

	def validate(self, request: HTTPRequest) -> bool:

		return bool(self._pattern.search(request.body))
