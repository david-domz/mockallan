import pytest
from app_handler import HTTPRequest, History


def test_assert_called_once_with_xml_success(history: History):

	endpoint_called = ('PUT', '/path/xml/1')

	match_request = HTTPRequest(
		'PUT',
		'/path/xml/1',
		headers={
			'Content-Type': 'application/xml'
		},
		body='<xml></xml>'
	)
	history.assert_called_once_with(endpoint_called, match_request)


def test_assert_called_once_with_xml_assertion_error(history: History):

	endpoint_called = ('PUT', '/path/xml/1')
	with_request = HTTPRequest(
		'PUT',
		'/path/xml/1',
		headers={
			'Content-Type': 'application/xml'
		},
		body='<xml>xxxxxxx</xml>'
	)

	with pytest.raises(AssertionError):
		history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_xml_schema_success(history: History):

	endpoint_called = ('PUT', '/path/xml/1')
	with_request = HTTPRequest(
		'PUT',
		'/path/xml/1',
		headers={
			# TO DO: XML
			'Content-Type': 'application/schema+json'
		},
		body={
			# TO DO: XML schema validation body
		}
	)
	history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_xml_schema_assertion_error(history: History):

	endpoint_called = ('PUT', '/path/xml/1')
	with_request = HTTPRequest(
		'PUT',
		'/path/xml/1',
		headers={
			# TO DO: XML
			'Content-Type': 'application/schema+json'
		},
		body={
			# TO DO: XML
		}
	)
	with pytest.raises(AssertionError):
		history.assert_called_once_with(endpoint_called, with_request)
