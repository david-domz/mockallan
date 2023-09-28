# `mockallan` - Lightweight HTTP Server Mock

[![](https://img.shields.io/pypi/v/mockallan.svg)](https://pypi.org/project/mockallan/)

`mockallan` is a lightweight HTTP server mock used as a replacement for a production HTTP server in testing environments.


## Features

- Command line interface for continuous integration (CI) and testing environments.

- Assertion capabilities for validating expected requests. JSON schema, XML schema, and regex validation support.

- Stub capabilities with configurable responses.

- Request history enables robust assertion capabilities and diagnostics.

- Concise codebase of under 1000 lines, focusing on simplicity and making the best use of resources.

- API naming adheres to the `Mock` class from the Python `unittest.mock` standard library.

## Requirements

- Python >= 3.10

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

2) Configure the hostname and port for Mockallan in your software under test and run it.

If you currently don't have any software whose requests you want to test, enter the following command to simulate a request performed by any software under test."

For example, if you expect the software under test to perform a `POST /orders/order_e2b9/products` run the following command.


```bash
$ curl -s -X POST http://localhost:8080/orders/order_e2b9/products --data '{'product_id': 'foo', 'description': 'bar', 'amount': 1}'
```

`mockallan` will reply with the factory default response.

```json
{
	"status": "200",
	"message": "This is mockallan factory default response.",
	"detail": "Use the Stub Configuration API to configure default and per-endpoint responses."
}
```

3) Use `mockallan` Assertion API to make assertions on the expected response.


```bash
$ curl "http://localhost:8080/assert-called-once?method=POST&path=/orders/order_e2b9/products"
```

If the assertion request returns 200 then everything went fine.

```json
{
	"status": 200,
	"type": "assertion-success",
	"title": "Assertion request GET /assert-called-once succeeded",
	"detail": "POST /orders/order_e2b9/products was called 1 times."
}
```

Otherwise, if it returns 409 then the assertion failed and the software under test did not behave as expected.

```json
{
	"status": 409,
	"type": "assertion-error",
	"title": "Assertion request GET /assert-called-once failed",
	"detail": "POST /orders/order_e2b9/products expected call count was 1 but actual call count was 2."
}
```

## Using Configurable Stub Responses

1) Configure `mockallan` responses by editing a Stub Configuration JSON file. E.g. `stub_config.json`.

```json
{
	"endpoints": [
		{
			"request": {
				"method": "POST",
				"path": "/orders/order_e2b9/products"
			},
			"response": {
				"code": 200,
				"headers": {
					"Content-type": "application/json"
				},
				"body": {
					"status": "200",
					"message": "This is the configured response for POST /orders/order_e2b9/products"
				}
			}
		}
	]
}
```

2) Run `mockallan.py` and provide the JSON file as an argument using the -c option.

```bash
$ python mockallan.py -c stub_config.json
```

3) Execute the software under test. `mockallan` will reply with the configured response to the `POST /orders/order_e2b9/products`.


4) Use the Assertion API to make assertions on expected outcomes.

```bash
$ curl -X GET http://localhost:8080/assert-called-once?method=POST&path=/orders/order_e2b9/products
```

If the assertion request returns 200 then everything went fine. Otherwise, if it returns 409 then the assertion failed and the software under test did not behave as expected.


## Using Assertions (`POST /assert-called-with` and `POST /assert-called-once-with`)

The following validation assertions can be used when performing assertion requests with `POST /assert-called-with` or `POST /assert-called-once-with`. The body corresponds to the JSON schema, XML schema, or regex to match as shown below.

### JSON Schema Validation Assertions

Add `Content-Type: application/schema+json` to the assertion request and place the JSON schema message in the body.

```bash
$ curl -X POST --header 'Content-Type: application/json+schema' http://localhost:8080/assert-called-with?method=POST&path=/orders/order_e2b9/products --data '...JSON schema here...'
```

### XML Schema Validation Assertions

Add `Content-Type: application/xml` to the assertion request and place the XML schema message in the body.

```bash
$ curl -X POST --header 'Content-Type: application/xml' http://localhost:8080/assert-called-with?method=POST&path=/orders/order_e2b9/products --data '...XML schema here...'
```

### Regex Validation Assertions

Add the custom header `X-Mockallan-Validator: regex` to the assertion request and place the regular expression in the body. 

```bash
$ curl -X POST --header 'X-Mockallan-Validator: regex' http://localhost:8080/assert-called-with?method=POST&path=/orders/order_e2b9/products --data '...regex here...'
```


## Stub Configuration JSON

The Stub Configuration JSON format configures `mockallan` responses.

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
				"path": "/orders/order_e2b9/products"
			},
			"response": {
				"code": 200
				"headers": {
					"Content-type": "application/json"
				},
				"body": {
					"status": 200,
					"message": "This is the configured response for GET /orders/order_e2b9/products"
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

The Assertion API allows for the validation of expected requests.

|Method|Path|Request Body|Status|Response Body|
|-|-|-|-|-|
|GET|/assert-called|-|200 OK; 409 Conflict|Assertion success or error message|
|GET|/assert_called_once|-|200 OK; 409 Conflict|Assertion success or error message|
|POST|/assert-called-with|JSON schema, XML schema, regex or message body|200 OK; 409 Conflict|Assertion success or error message|
|POST|/assert-called-once-with|JSON schema, XML schema, regex or message body|200 OK; 409 Conflict|Assertion success or error message|
|GET|/call-args|-|200 OK|The request body that the mock was last called with|
|GET|/call-args-list|-|200 OK|List of all the requests made to the mock in sequence.|
|GET|/call-count|-|200 OK|Request count|


## Naming

Both Stub Configuration API and Assertion API naming are inspired by class `Mock` from the standard python package `unittest.mock`.

Python developers already familiar with this package can quickly become familiar with `mockallan` API.


## Feedback

I value your feedback! If you've used `mockallan` and have suggestions, bug reports, or any other feedback, please let me know. You can reach out to me via [email](mailto:david.7b8@gmail.com).

Thank you!
