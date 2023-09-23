import pytest
from app_handler import HTTPRequest, History


def test_call_count_empty_history(empty_history: History):

	assert empty_history.call_count('GET', '/path') == 0


def test_call_count(history: History):

	assert history.call_count('GET', '/path/1') == 1
	assert history.call_count('POST', '/path/2') == 3
	assert history.call_count('PUT', '/path/4') == 1


def test_assert_called_once_with_text_plain_success(history: History):
	"""Tests assert_called_once_with() succeeds, text body matches. """

	endpoint_called = ('POST', '/path/6')
	with_request = HTTPRequest(
		'POST',
		'/path/6',
		headers={
			'Content-Type': 'text/plain'
		},
		body='The sherried sweetness and some spice carry over from the nose.'
	)

	history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_text_plain_assertion_error_not_called(history: History):
	"""Tests assert_called_once_with() fails, path does not match. """

	endpoint_called = ('POST', '/path/unknown')
	with_request = HTTPRequest(
		'POST',
		'/path/unknown',
		headers={
			'Content-Type': 'text/plain'
		},
		body='The sherried sweetness and some spice carry over from the nose.'
	)

	with pytest.raises(AssertionError):
		history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_text_plain_assertion_error(history: History):
	"""Tests assert_called_once_with() fails, text body does not match. """

	endpoint_called = ('POST', '/path/6')
	with_request = HTTPRequest(
		'POST',
		'/path/6',
		headers={
			'Content-Type': 'text/plain'
		},
		body='Potatoe'
	)

	with pytest.raises(AssertionError):
		history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_octet_stream_success(history: History):
	"""Tests assert_called_once_with() succeeds with binary content. """

	endpoint_called = ('PUT', '/path/eicar')
	with_request = HTTPRequest(
		'PUT',
		'/path/eicar',
		headers={
			'Content-Type': 'application/octet-stream'
		},
		body=b'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
	)

	history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_octet_stream_assertion_error(history: History):
	"""Tests assert_called_once_with() fails; binary content does not match. """

	endpoint_called = ('PUT', '/path/eicar')
	with_request = HTTPRequest(
		'PUT',
		'/path/eicar',
		headers={
			'Content-Type': 'application/octet-stream'
		},
		body=b'\x00\x01\x02\x03'
	)

	with pytest.raises(AssertionError):
		history.assert_called_once_with(endpoint_called, with_request)
