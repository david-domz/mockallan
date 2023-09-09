# `mockallan`- Universal HTTP Server Mock

`mockallan` is a universal HTTP server mock that can be used as a replacement of a production HTTP server in a test environment.

## Features

- Command line Interface for CI Integration: Enables seamless integration into continuous integration environments, making it ideal for automated testing workflows.
- Mock and Stub Capabilities: Provides both mock and stub functionalities, allowing you to simulate different behaviors of HTTP endpoints.
- Configurable Stub Responses: Offers the flexibility to configure stub responses for specific endpoints and provides a default response for all other endpoints.
- Initialization Time Configuration: Allows you to set up stub responses using a JSON file at the time of initialization.
- Runtime Configuration: Permits the dynamic configuration of stub responses during runtime by posting a JSON file. Refer to the Stub Configuration API section below for details.
- Assertions can be done after running the software under test.
- Assertions: Supports assertions after running the software under test, helping you validate expected responses.
- Request History: Maintains a request history, allowing powerful assertion capabilities and diagnostics.
- Stub Configuration - API and Mock Assertion API naming based on the class `Mock` from the standard python package `unittest.mock`.
- API Naming Consistency: Adheres to a naming convention for the Stub Configuration API and Mock Assertion API, based on the Mock class from the standard Python package unittest.mock. This ensures a familiar and consistent experience for Python developers.


## Requirements

- Python >= 3.10

TO DO: Move to implementation section: It uses the standard python module `http.server`.
TO DO: requirement or dependency?
TO DO: jsonschema: requirement or dependency?

## Installation

```python
pip install mockallan
```

## Getting Started


1) Configure `mockallan` responses by using the Stub Configuration JSON Format.

E.g. `stub_config.json`

```json
{
	"endpoints": [
		{
			"request": {
				"method": "POST",
				"path": "/path-1"
			},
			"response": {
				"code": 200,
				"headers": {
					"Content-type": "application/json"
				},
				"body": "{\"message\": \"Hello there! This is the response for POST /path-1\"}"
			}
		}
	]
}


```

2) Run `mockallan.py`
	- `python mockallan.py -p 8080`

3) Use the Stub Configuration API to POST the configuration to the running `mockallan` instance.

   - `curl -X POST /config --data @config.json`

4) Execute the software under test.

5) Use Mock Assertion API to make assertions on expected outcomes.

   - `curl -X GET /assert-called-once?method=POST&path=/path`

6) If the Mock Assertion response returned 204 then everything went fine. If it returned 409 then the assertion failed and the software under test did not behave as expected.

## Running `mockallan`


```bash
usage: mockallan.py [-h] [-H HOST] [-p PORT] [-c CONFIG]

Mock HTTP server

options:
  -h, --help            show this help message and exit
  -H HOST, --host HOST
  -p PORT, --port PORT
  -c CONFIG, --config CONFIG
```

E.g.

```bash
$ mockallan.py -p 8080

```

## Stub Configuration JSON

Stub Configuration JSON format is used to configure `mockallan` responses.

### Example #1 - Permanent Response

`response` value is a JSON object.

```json
{
	"endpoints": [
		{
			"request": {
				"method": "GET"
				"path": "/path-1"
			},
			"response": {
				"code": 200
				"headers": {
					"Content-type": "application/json"
				},
				"body": "{\"message\": \"Permanent response to GET /path-1\"}"
			}
		}
	]
}
```

### Configuration JSON Example #2 - Sequential Response

`response` value is a JSON array containing the sequence of responses to return.

```json
{
	"endpoints": [
		{
			"request": {
				"method": "POST" | "GET"
				"path": "/path-2"
			},
			"response": [
				{
					"code": 200,
					"headers": {
						"Content-type": "application/json"
					},
					"body": "{\"message\": \"Sequential response #1 to GET /path-2\"}"
				},
				{
					"code": 200,
					"headers": {
						"Content-type": "application/json"
					},
					"body": "{\"message\": \"Sequential response #2 to GET /path-2\"}"
				}
			]
		}
	]
}
```

## Stub Configuration API


|Method|Path|Body||
|-|-|-|-|
|PUT|/configure|JSON config|Update config|
|GET|/configure|-|Get config|


## Mock Assertion API


Assertions

|`http-mock-server` endpoint||Status codes|
|-|-|-|
|GET /assert-called||204 OK; 409|
|GET /assert_called_once||204 OK; 409|
|POST /assert_called_with||204 OK; 409|
|POST /assert_called_once_with||204 OK; 409|
|GET /call-args||This is either None (if the mock hasn’t been called), or the arguments that the mock was last called with.|
|GET /call-args-list||This is a list of all the calls made to the mock object in sequence (so the length of the list is the number of times it has been called).|
|GET /call-count|||

## Naming

Both Stub Configuration API and Mock Assertion API naming are inspired by class `Mock` from the standard python package `unittest.mock`.

Python developers already familiar with this package will quickly become familiar with `mockallan` API.

|`mockallan` Assertion API endpoint|Python class `Mock` method|
|-|-|
|GET /assert-called|assert_called()|
|GET /assert-called-once|assert_called_once()|
|POST /assert-called-with|assert_called_with()|
|POST /assert-called-once-with|assert_called_once_with()|
|GET /call-args|call_args()|
|GET /called|called|
|GET /call-count|call_count|
|GET /method-calls|method_calls()|


### `mockallan` Python Package Usage

`mockallan` can be integrated also as a package into your python project or test environment.

Similar to the standard python class `http_server.HTTPServer`.

E.g.

```python
from mockallan import MockHTTPServer

# Stub configuration python dict
# Equivalent to configuration JSON file
stub_config_json = {
	"endpoints": [
		{
			"request": {
				"method": "GET"
				"path": "/path-1"
			},
			"response": {
				"code": 200,
				"content-type": "application/json"
				"response": '{"message": "Hello, you"}'
			}
		}
	]
}

mock_http_server = MockHTTPServer(server_address, config_json)
mock_http_server.serve_forever()
```

## Source code

Clone the Github repository with the command:

```bash
git clone https://github.com/vurutal/mock-http-server.git

```
