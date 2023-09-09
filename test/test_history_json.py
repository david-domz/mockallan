import pytest
from app_handler import HTTPRequest, History


def test_assert_called_once_with_json_success(history: History):

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
