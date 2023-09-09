import json
from stub_config import StubConfig, HTTPRequest, HTTPResponse



def test_load_json(stub_config: StubConfig):

	assert stub_config.default_response, HTTPResponse(
		200,
		{
			'Content-type': 'application/json'
		},
		'{\"message\": \"This is the mock-http-server default response. Please use the Configuration API to configure the response status code, headers and body.\"}'
	)




def test_dump_json(stub_config: StubConfig):

	# Act
	config_json = stub_config.dump_json()

	# Assert
	with open('stub_config.json', "r", encoding='utf-8') as f:
		config_read_str = f.read()

	config_read_json = json.loads(config_read_str)

	assert config_json == config_read_json


def test_dump_json_factory(factory_stub_config: StubConfig):

	config_json = factory_stub_config.dump_json()

	assert len(config_json['defaults']) == 1
	assert not config_json['endpoints']


def test_lookup_default_response(stub_config: StubConfig):

	response = stub_config.lookup(HTTPRequest('POST', '/path/unknown/1'))

	assert response.code == 200
	assert response.headers['Content-Type'] == 'application/json'
	assert response.body == "{\"message\": \"This is the mock-http-server default response. Please use the Configuration API to configure the response status code, headers and body.\"}"


def test_lookup_custom_response(stub_config: StubConfig):

	response = stub_config.lookup(HTTPRequest('POST', '/path/soap/1'))

	assert response.code == 200
	assert response.headers['Content-Type'] == 'application/xml'
	assert response.body == "<SOAP:Envelope xmlns:SOAP=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"><SOAP:Body><m:CreateUser><Integer xsi:type=\"xsd:integer\">0</Integer></m:CreateUser></SOAP:Body></SOAP:Envelope>"
