from pytest import fixture
from request import HTTPRequest, HTTPResponse, ContentType
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
	"""History instance with many requests. """

	history_instance = History()
	history_instance.append_many(
		[
			(
				HTTPRequest('GET', '/path/1'),
				HTTPResponse(200)
			),
			(
				HTTPRequest('POST', '/path/2'),
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
					headers=ContentType.APPLICATION_JSON,
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
					headers=ContentType.APPLICATION_OCTET_STREAM,
					body=b'ffeeffeeffee'
				),
				HTTPResponse(200)
			),
			(
				HTTPRequest(
					'POST',
					'/path/6',
					headers=ContentType.TEXT_PLAIN,
					body='The sherried sweetness and some spice carry over from the nose.'
				),
				HTTPResponse(200)
			),
			(
				HTTPRequest(
					'PUT',
					'/path/eicar',
					headers=ContentType.APPLICATION_OCTET_STREAM,
					body=b'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
				),
				HTTPResponse(200)
			),
			(
				HTTPRequest(
					'PUT',
					'/path/xml/1',
					headers=ContentType.APPLICATION_XML,
					body='''
<individual>
	<name>Liam Campbell</name>
	<address>
		<zip>AB38 9RX</zip>
		<city>Craigellachie</city>
	</address>
</individual>'''
				),
				HTTPResponse(200)
			)
		]
	)

	yield history_instance
