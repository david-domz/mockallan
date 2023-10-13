<!-- # `mockallan` - Lightweight HTTP Server Mock -->

![image](mockallan.png)

[![PyPI package version](https://badge.fury.io/py/mockallan.svg)](https://pypi.org/project/mockallan/) [![Supported Python versions](https://img.shields.io/pypi/pyversions/mockallan.svg)](https://pypi.org/project/mockallan/) [![Python package](https://github.com/david-domz/mockallan/actions/workflows/python-package.yml/badge.svg)](https://github.com/david-domz/mockallan/actions/workflows/python-package.yml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=david-domz_mockallan&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=david-domz_mockallan)

`mockallan` is a lightweight HTTP server mock used as a replacement for a production HTTP server in testing environments.


## Highlights

- Command-line interface for CI and testing environments.

- The Stub Configuration API allows to configure default and per-endpoint responses.

- The Assertion API enables the assertion of expected requests performed by the software under test based on the endpoint and the request body.

- Match the request body in assertions based on
  - text/plain message matching
  - JSON message matching
  - JSON schema validation
  - XML schema validation
  - Regular expression matching

- Request history enables robust assertion capabilities and diagnostics.

- Concise codebase of under 1000 lines, focusing on simplicity and making the best use of resources.

- API naming adheres to the `Mock` class from the Python `unittest.mock` standard library.

## Requirements

- Python >= 3.10

## Installation

`mockallan` is available on [PyPI](https://pypi.org/project/mockallan/). Install it using pip.

```bash
pip install mockallan
```

## Getting Started


1) Run `mockallan.py`

```bash
python mockallan.py
Listening on 0.0.0.0:8080
```

2) Run your software under test.

If you currently don't have any software whose requests you want to test, you can simulate a request performed by software under test.

For example, if we expect our software under test to perform a `POST /orders/order_e2b9/products` we can run the following `curl` command.

```bash
cat > product.json << EOF
{
	"product_id": "foo",
	"description": "bar",
	"amount": 1
}
EOF
```

```bash
curl -s -X POST http://localhost:8080/orders/order_e2b9/products --data @product.json
```

`mockallan` will reply with the factory default response.

```json
{
	"status": "200",
	"message": "This is mockallan factory default response."
}
```

3) Use the Assertion API to make assertions on the expected request.

```bash
curl "http://localhost:8080/assert-called?method=POST&path=/orders/order_e2b9/products"
```

If the assertion request returns 200 then everything went fine.

```json
{
	"status": 200,
	"type": "assertion-success",
	"title": "Assertion request GET /assert-called succeeded",
	"detail": "POST /orders/order_e2b9/products called 1 times."
}
```

If it returns 409 then the assertion failed and the software under test did not behave as expected.

```json
{
	"status": 409,
	"type": "assertion-error",
	"title": "Assertion request GET /assert-called failed",
	"detail": "Expected POST /orders/order_e2b9/products to be called 1 times. Called 0 times."
}
```

## Using Configurable Stub Responses

1) Create a Stub Configuration JSON file or use `stub_config.json` in this repository.

E.g.
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

2) Run `mockallan.py` and provide the JSON file.

```bash
python mockallan.py -c stub_config.json
```

3) Run the software under test. The mock will reply with the configured response for `POST /orders/order_e2b9/products`.

4) Use the Assertion API to make assertions on expected requests.

```bash
curl -X GET 'http://localhost:8080/assert-called?method=POST&path=/orders/order_e2b9/products'
```

If the assertion request returns 200 then everything went fine. If it returns 409 then the assertion failed and the software under test did not behave as expected.


## Using Assertions `with`

The following validations can be used when performing assertion requests with `POST /assert-called-with` or `POST /assert-called-once-with`. The request body corresponds to the `text/plain` body, JSON message, JSON schema, XML schema, or regular expression to match as shown below.

### JSON Schema Validation Assertions

Add `Content-Type: application/schema+json` to the assertion request and place the JSON schema message in the body.

E.g.
```bash
curl -X POST --header 'Content-Type: application/json+schema'	\
	http://localhost:8080/assert-called-with?method=POST&path=/orders/order_e2b9/products	\
	--data '...JSON schema here...'
```

### XML Schema Validation Assertions

Add `Content-Type: application/xml` to the assertion request and place the XML schema message in the body.

E.g.
```bash
curl -X POST --header 'Content-Type: application/xml'	\
	http://localhost:8080/assert-called-with?method=POST&path=/orders/order_e2b9/products	\
	--data '...XML schema here...'
```

### Regex Validation Assertions

Add the custom header `X-Mockallan-Validator: regex` to the assertion request and place the regular expression in the body. 

E.g.
```bash
curl -X POST --header 'X-Mockallan-Validator: regex'	\
	http://localhost:8080/assert-called-with?method=POST&path=/orders/order_e2b9/products	\
	--data '...regex here...'
```

<!-- ## Stub Configuration JSON

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
``` -->

## Stub Configuration API

The Stub Configuration API allows the test client to configure the mock at runtime.

|Method|Path|Query Params|Request Body|Status|Response Body|
|-|-|-|-|-|-|
|PUT|/configure|-|JSON stub configuration|204|-|
|GET|/configure|-|-|200|JSON stub configuration|


## Assertion API

The Assertion API allows for the validation of expected requests.

|Method|Path|Query Params|Request Body|Status|Response Body|
|-|-|-|-|-|-|
|GET|/assert-called|method, path|-|200 OK; 409 Conflict|Assertion success or error message|
|GET|/assert-called-once|method, path|-|200 OK; 409 Conflict|Assertion success or error message|
|POST|/assert-called-with|method, path|JSON object, JSON schema, XML schema or regex|200 OK; 409 Conflict|Assertion success or error message|
|POST|/assert-called-once-with|method, path|JSON object, JSON schema, XML schema, regex or message body|200 OK; 409 Conflict|Assertion success or error message|
|GET|/call-args|-|-|200 OK|The request body that the mock was last called with|
|GET|/call-args-list|-|-|200 OK|List of all the requests made to the mock in sequence|
|GET|/call-count|-|-|200 OK|Request count|


## Naming

Stub Configuration API and Assertion API naming are inspired by class `Mock` from the standard python package `unittest.mock`.


## Contributing

We welcome contributions to improve this project. Whether you want to report a bug, suggest an enhancement, or submit a pull request, your help is highly valuable.

If you encounter a bug, experience unexpected behavior, or have ideas for improving this project, please [open an issue](https://github.com/david-domz/mockallan/issues).

If you're interested in contributing to the codebase, follow these steps:

- Fork the repository and create your branch from the main branch.
- Make your changes and ensure they adhere to our coding standards.
- Thoroughly test your changes.
- Create a pull request, describing the changes you've made and their purpose.

Thank you!

## License

This project is licensed under the terms of the MIT license.

## Related Projects

- [mockallan-docker](https://github.com/david-domz/mockallan-docker) - Containerized lightweight HTTP server mock.
- [mockallan-python-client](https://github.com/david-domz/mockallan-python-client) - Mockallan python client class.
