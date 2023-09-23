import pytest
from app_handler import HTTPRequest, History


def test_assert_called_once_with_json_success(history: History):
	"""Tests assert_called_once_with() succeeds; JSON body matches. """

	endpoint_called = ('PUT', '/path/4')
	with_request = HTTPRequest(
		'PUT',
		'/path/4',
		headers={
			'Content-Type': 'application/json'
		},
		body={
			'foo': 'bar'
		}
	)
	history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_json_assertion_error(history: History):
	"""Tests assert_called_once_with() fails; JSON body does not match. """

	endpoint_called = ('PUT', '/path/4')
	with_request = HTTPRequest(
		'PUT',
		'/path/4',
		headers={
			'Content-Type': 'application/json'
		},
		body={
			'foo': 'beer'
		}
	)

	with pytest.raises(AssertionError):
		history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_json_schema_success(history: History):
	"""Tests assert_called_once_with() succeeds; JSON schema matches. """

	endpoint_called = ('PUT', '/path/4')
	with_request = HTTPRequest(
		'PUT',
		'/path/4',
		headers={
			'Content-Type': 'application/schema+json'
		},
		body={
			"$schema": "http://json-schema.org/draft-07/schema#",
			'type': 'object',
			'properties': {
				'foo': {
					'type': 'string'
				}
			}
		}
	)
	history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_json_schema_assertion_error(history: History):
	"""Tests assert_called_once_with() fails; JSON schema does not match. """

	endpoint_called = ('PUT', '/path/4')
	with_request = HTTPRequest(
		'PUT',
		'/path/4',
		headers={
			'Content-Type': 'application/schema+json'
		},
		body={
			"$schema": "http://json-schema.org/draft-07/schema#",
			'type': 'object',
			'properties': {
				'foo': {
					'type': 'boolean'
				}
			}
		}
	)
	with pytest.raises(AssertionError):
		history.assert_called_once_with(endpoint_called, with_request)
