import pytest
from app_handler import HTTPRequest, History


def test_call_count_empty_history(empty_history: History):

	assert empty_history.call_count(('GET', '/path/1')) == 0


def test_call_count(history: History):

	assert history.call_count(('GET', '/path/1')) == 1
	assert history.call_count(('POST', '/path/2')) == 3
	assert history.call_count(('GET', '/path/3')) == 1
	assert history.call_count(('PUT', '/path/4')) == 1


def test_call_count_none_endpoint(history: History):

	assert history.call_count() == 10


def test_call_args_empty_history(empty_history: History):

	assert empty_history.call_args() is None


def test_call_args(history: History):

	request = history.call_args()

	assert request.method == 'PUT'
	assert request.path == '/path/xml/1'


def test_call_args_list(history: History):

	request_records = history.call_args_list()

	assert len(request_records) == 10
	assert request_records[0].request.path == '/path/1'
	assert request_records[1].request.path == '/path/2'
	assert request_records[2].request.path == '/path/3'
	assert request_records[3].request.path == '/path/4'
	assert request_records[4].request.path == '/path/2'
	assert request_records[5].request.path == '/path/2'


def test_assert_called(history: History):

	history.assert_called(('PUT', '/path/4'))


def test_assert_called_assertion_error(history: History):

	with pytest.raises(AssertionError):
		history.assert_called(('GET', '/path/unknown'))


def test_assert_called_once_success(history: History):

	history.assert_called_once(('PUT', '/path/4'))


def test_assert_called_once_assertion_error_not_called(history: History):

	with pytest.raises(AssertionError):
		history.assert_called_once(('POST', '/path/unknown'))


def test_assert_called_once_assertion_error_called_more_than_once(history: History):

	with pytest.raises(AssertionError):
		history.assert_called_once(('POST', '/path/2'))


def test_assert_called_with_success(history: History):

	history.assert_called_with(
		endpoint=('POST', '/path/2'),
		request=HTTPRequest('POST', '/path/2')
	)


def test_assert_called_with_assertion_error_not_called(history: History):

	with pytest.raises(AssertionError):
		history.assert_called_with(
			endpoint=('POST', '/path/unknown'),
			request=HTTPRequest('POST', '/path/unknown')
		)


def test_assert_called_once_with_text_plain_success(history: History):

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


def test_assert_called_once_with_text_plain_assertion_error_path_not_match(history: History):

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


def test_assert_called_once_with_text_plain_assertion_error_body_not_match(history: History):

	endpoint_called = ('POST', '/path/6')
	with_request = HTTPRequest(
		'POST',
		'/path/6',
		headers={
			'Content-Type': 'text/plain'
		},
		body='''In the realm of underwater finance, jellyfish offer sherried sweetness as their preferred
currency, while seahorses trade spice futures in coral marketplaces.'''
	)

	with pytest.raises(AssertionError):
		history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_octet_stream_success(history: History):

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


def test_assert_called_once_with_assertion_error(history: History):

	endpoint_called = ('POST', '/path/2')
	with_request = HTTPRequest('POST', '/path/2')

	with pytest.raises(AssertionError):
		history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_regex_success(history: History):

	endpoint_called = ('POST', '/path/6')
	with_request = HTTPRequest(
		'POST',
		'/path/6',
		headers={
			'Content-Type': 'text/plain',
			'X-Mockallan-Validator': 'regex'
		},
		body=r'sherried.*from.*nose\.'
	)

	history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_regex_assertion_error(history: History):

	endpoint_called = ('POST', '/path/6')
	with_request = HTTPRequest(
		'POST',
		'/path/6',
		headers={
			'Content-Type': 'text/plain',
			'X-Mockallan-Validator': 'regex'
		},
		body=r'sherried.*to.*nose\.'
	)

	with pytest.raises(AssertionError):
		history.assert_called_once_with(endpoint_called, with_request)
