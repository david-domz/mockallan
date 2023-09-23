# `mockallan`- HTTP Server Mock

`mockallan` is a HTTP server mock designed for use as a substitute for a production HTTP server within a testing environment.

## Features

- Command line interface for CI environments, making it ideal for automated testing workflows.

- Assertion capabilities for validating expected responses during testing.

- Stub capabilities with configurable responses.

- JSON-based initialization time and runtime configuration.
   
- Request history empowering robust assertion capabilities and diagnostics.

- API adheres to naming conventions in line with the `Mock` class from the Python `unittest.mock` standard library.

- Concise codebase of under 1000 lines, emphasizing minimalism and efficient resource utilization.


## Requirements

- Python >= 3.10

<!-- TO DO: Move to implementation section: It uses the standard python module `http.server`.
TO DO: requirement or dependency?
TO DO: jsonschema: requirement or dependency? -->

## Installation

`mockallan` is available on PyPI. You can install using pip:

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

Alternatively, enter the following command to simulate a request to the software under test. For example, if you expect the software under test to perform a `POST /mockallan-reserve`.


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
				"path": "/configured-path/mockallan-reserve"
			},
			"response": {
				"code": 200,
				"headers": {
					"Content-type": "application/json"
				},
				"body": "{\"message\": \"This is the configured response for POST /configured-path/mockallan-reserve\"}"
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
curl -X GET http://localhost:8080/assert-called-once?method=POST&path=/configured-path/mockallan-reserve
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
	"defaults": {
		"response": {
			"code": 200,
			"headers": {
				"Content-Type": "application/json"
			},
			"body": {
				"status": 200,
				"message": "This is the default response configured in stub_config.json"
			}
		}
	},
	"endpoints": [
		{
			"request": {
				"method": "GET"
				"path": "/configured-path/mockallan-reserve"
			},
			"response": {
				"code": 200
				"headers": {
					"Content-type": "application/json"
				},
				"body": {
					"status": 200,
					"message: "This is the configured response for GET /configured-path/mockallan-reserve"
				}
			}
		}
	]
}
```

## Stub Configuration API

|Method|Path|Request Body|Status|Response Body|
|-|-|-|-|-|
|PUT|/configure|JSON stub configuration|204|-|
|GET|/configure|-|200|JSON stub configuration|


## Assertion API

|Method|Path|Request Body|Status|Response Body|
|-|-|-|-|-|
|GET|/assert-called|-|200 OK; 409 Conflict|Assertion success or error message|
|GET|/assert_called_once|-|200 OK; 409 Conflict|Assertion success or error message|
|POST|/assert-called-with|Matching JSON schema or message body|200 OK; 409 Conflict|Assertion success or error message|
|POST|/assert-called-once-with|Matching JSON schema or message body|200 OK; 409 Conflict|Assertion success or error message|
|GET|/call-args|-|200 OK|The request body that the mock was last called with|
|GET|/call-args-list|-|200 OK|List of all the requests made to the mock in sequence.|
|GET|/call-count|-|200 OK|Request count|


## Naming

Both Stub Configuration API and Assertion API naming are inspired by class `Mock` from the standard python package `unittest.mock`.

Python developers already familiar with this package can quickly become familiar with `mockallan` API.

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
git clone https://github.com/david-domz/mockallan.git
```
