from pytest import fixture
from request import HTTPRequest, HTTPResponse
from stub_config import StubConfig
from app_handler import History


@fixture
def factory_stub_config():

	yield StubConfig()


@fixture
def stub_config():

	yield StubConfig(config_json='stub_config.json')


@fixture
def empty_history():

	yield History()


@fixture
def history():

	history_instance = History()
	history_instance.append_many(
		[
			(
				HTTPRequest('GET', '/path/1'),
				HTTPResponse(200)
			),
			(
				HTTPRequest(
					'POST',
					'/path/2',
					body=b''
				),
				HTTPResponse(200)
			),
			(
				HTTPRequest('GET', '/path/3'),
				HTTPResponse(200)
			),
			(
				HTTPRequest(
					'PUT',
					'/path/4',
					headers={
						'Content-Type': 'application/json'
					},
					body={
						"foo": "bar"
					}
				),
				HTTPResponse(204)
			),
			(
				HTTPRequest('POST', '/path/2'),
				HTTPResponse(200)
			),
			(
				HTTPRequest('POST', '/path/2'),
				HTTPResponse(200)
			),
			(
				HTTPRequest(
					'POST',
					'/path/5',
					headers={
						'Content-Type': 'application/octet-stream'
					},
					body=b'ffeeffeeff'
				),
				HTTPResponse(200)
			),
			(
				HTTPRequest(
					'POST',
					'/path/6',
					headers={
						'Content-Type': 'text/plain'
					},
					body='aaaabb'
				),
				HTTPResponse(200)
			),
			(
				HTTPRequest(
					'PUT',
					'/path/eicar',
					headers={
						'Content-Type': 'application/octet-stream'
					},
					body=b'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
				),
				HTTPResponse(200)
			),
			# See https://lxml.de/validation.html
			(
				HTTPRequest(
					'PUT',
					'/path/xml/1',
					headers={
						'Content-Type': 'application/xml'
					},
					body='<xml></xml>'
				),
				HTTPResponse(200)
			)
		]
	)

	yield history_instance
