# `mockallan`- HTTP Server Mock

`mockallan` is a versatile HTTP server mock designed for use as a substitute for a production HTTP server within a testing environment.

## Features

- Command line Interface for CI Integration: Enables seamless integration into continuous integration environments, making it ideal for automated testing workflows.

- Assertion Capabilities: Provides assertion support for validating expected responses during testing.

- Stub Capabilities with Configurable Responses: Offers endpoint-specific response configuration and a default response for unmatched endpoints.

- Configuration Flexibility: Supports JSON-based stub response setup during initialization and dynamic runtime configuration. See the Stub Configuration API section below for details.

- History: Maintains a comprehensive request history, empowering robust assertion capabilities and diagnostics.

- API Naming Consistency: Adheres to naming conventions in line with the Mock class from the Python unittest.mock standard library, ensuring a consistent experience for Python developers.

- Lean and Compact: Features a concise codebase of under 1000 lines, emphasizing minimalism and efficient resource utilization.


## Requirements

- Python >= 3.10

<!-- TO DO: Move to implementation section: It uses the standard python module `http.server`.
TO DO: requirement or dependency?
TO DO: jsonschema: requirement or dependency? -->

## Installation

```bash
$ pip install mockallan
```

## Getting Started


1) Run `mockallan.py`

```bash
$ python mockallan.py
Listening on 0.0.0.0:8080
```

2) Run the software under test.

Alternatively, you can enter the following command to simulate a request to the software under test. For example, if you expect the software under test to perform a `POST /mockallan-reserve`.


```bash
$ curl -X POST http://localhost:8080/mockallan-reserve --data '{'foo': 'bar'}'
```

`mockallan` will reply with the default response.

```json
{
	"status": "200",
	"message": "This is mockallan default response. Use the Stub Configuration API to configure responses per endpoint."
}
```

1) Use `mockallan` Assertion API to make assertions on the expected response.

If the assertion request returns 200 then everything went fine.


```bash
$ curl "http://localhost:8080/assert-called-once?method=POST&path=/mockallan-reserve" ; echo

```

Otherwise, if it returns 409 then the assertion failed and the software under test did not behave as expected.

```json
{
	"status": 409,
	"type": "assertion-error",
	"title": "Assertion request GET /assert-called-once failed",
	"detail": "POST /mockallan-reserve expected call count was 1 but actual call count was 2."
}
```

## Using Configurable Stub Responses

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

1) Run `mockallan.py` and pass the JSON file using the -c option argument.

```bash
python mockallan.py -p 8080 -c stub_config.json
```

2) Execute the software under test.

3) Use the Assertion API to make assertions on expected outcomes.

```bash
curl -X GET http://localhost:8080/assert-called-once?method=POST&path=/path
```


4) Alternativelly, use the Stub Configuration API to POST a new stub configuration to the running `mockallan` instance.

```bash
curl -X POST http://localhost:8080/config --data @stub_config.json
```


## Running `mockallan`


```bash
usage: mockallan.py [-h] [-H HOST] [-p PORT] [-c STUB_CONFIG]

Mock HTTP server

options:
  -h, --help            show this help message and exit
  -H HOST, --host HOST
  -p PORT, --port PORT
  -c STUB_CONFIG, --stub-config STUB_CONFIG

```

## Stub Configuration JSON

The Stub Configuration JSON format configures mockallan responses.

### Stub Configuration Example


```json
{
	"endpoints": [
		{
			"request": {
				"method": "GET"
				"path": "/mockallan-reserve"
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


## Stub Configuration API


|Method|Path|Body||
|-|-|-|-|
|PUT|/configure|JSON config|Update config|
|GET|/configure|-|Get config|


## Assertion API


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

## Source code

Clone the Github repository with the command:

```bash
git clone https://github.com/vurutal/mock-http-server.git
```
