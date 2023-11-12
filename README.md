<!-- # Mockallan - Lightweight HTTP Server Mock -->

![image](mockallan.png)

[![PyPI package version](https://badge.fury.io/py/mockallan.svg)](https://pypi.org/project/mockallan/) [![Supported Python versions](https://img.shields.io/pypi/pyversions/mockallan.svg)](https://pypi.org/project/mockallan/) [![Python package](https://github.com/david-domz/mockallan/actions/workflows/python-package.yml/badge.svg)](https://github.com/david-domz/mockallan/actions/workflows/python-package.yml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=david-domz_mockallan&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=david-domz_mockallan)

Mockallan is a lightweight HTTP server mock for CI and testing environments.


## Highlights

- Command-line interface for CI and testing environments.

- Configurable default and per-endpoint responses.

- Assert expected requests performed by the system under test based on the endpoint and the request body.

- Match the request body in assertions based on
  - text/plain message matching
  - JSON message matching
  - JSON schema validation
  - XML schema validation
  - Regular expression matching

- Request history enables robust assertion capabilities.

- Concise codebase focusing on simplicity.

- API naming inspired by the `Mock` class from the Python `unittest.mock` standard library.

## Requirements

- Python >= 3.10

## Installation

Mockallan is available on [PyPI](https://pypi.org/project/mockallan/). Install it using pip.

```bash
pip install mockallan
```

## Getting Started


1) Run `mockallan.py`

```bash
python mockallan.py
Listening on 0.0.0.0:8080
```

2) Run the system under test.

You can use `curl` to simulate a request performed by the system under test. For example, if we expect our system under test to perform a `POST /orders/order_e2b9/products`, run the following `curl` command.

```bash
curl -s -X POST http://localhost:8080/orders/order_e2b9/products --data '{
	"product_id": "foo",
	"description": "bar",
	"amount": 1
}'
```

Mockallan will reply with the factory default response.

```json
{
	"status": "200",
	"message": "This is mockallan factory default response."
}
```

3) Make assertions on the expected request.

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

If it returns 409 then the assertion failed and the system under test did not behave as expected.

```json
{
	"status": 409,
	"type": "assertion-error",
	"title": "Assertion request GET /assert-called failed",
	"detail": "Expected POST /orders/order_e2b9/products to be called 1 times. Called 0 times."
}
```

## Using Configurable Stub Responses

1) Create a stub configuration JSON file or use the `stub_config.json` provided in this repository.

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
				"status_code": 200,
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

3) Run the system under test or simulate the request performed by it. The mock will reply with the configured response for `POST /orders/order_e2b9/products`.

4) Make assertions on the expected request.

```bash
curl -X GET 'http://localhost:8080/assert-called?method=POST&path=/orders/order_e2b9/products'
```

If the assertion request returns 200 then everything went fine. If it returns 409 then the assertion failed and the system under test did not behave as expected.


## Using `/assert-called-with` And `/assert-called-once-with`

The following validations can be used when performing assertion requests with `POST /assert-called-with` or `POST /assert-called-once-with`. The body message provided in these requests corresponds to a `text/plain` body, JSON message, JSON schema, XML schema, or regular expression to match as shown below.


### JSON Schema Validation Assertions

Add `Content-Type: application/schema+json` to the `POST /assert-called-with` or `POST /assert-called-once-with` request and place the JSON schema message in the body.

E.g. 

```bash
curl -X POST --header 'Content-Type: application/json+schema'	\
	http://localhost:8080/assert-called-with?method=POST&path=/orders/order_e2b9/products	\
	--data '{
		"$schema": "http://json-schema.org/draft-07/schema#",
		"type": "object",
		"properties": {
			"orderNumber": {
				"type": "string"
			},
			"products": {
				"type": "array",
				"items": {
					"type": "object",
					"properties": {
						"productId": {
							"type": "string"
						},
						"quantity": {
							"type": "integer",
							"minimum": 1
						}
					},
					"required": ["productId", "quantity"]
				}
			}
		},
		"required": ["orderNumber", "products"]
	}'
```

### XML Schema Validation Assertions

Add `Content-Type: application/xml` to the `POST /assert-called-with` or `POST /assert-called-once-with` request and place the XML schema message in the body.

E.g.

```bash
curl -X POST --header 'Content-Type: application/xml'	\
	http://localhost:8080/assert-called-with?method=POST&path=/orders/order_e2b9/products	\
	--data '<?xml version="1.0" encoding="UTF-8"?>
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
        <xs:element name="order">
            <xs:complexType>
                <xs:sequence>
                    <xs:element name="orderNumber" type="xs:string"/>
                    <xs:element name="products" type="productListType"/>
                </xs:sequence>
            </xs:complexType>
        </xs:element>
        <xs:complexType name="productListType">
            <xs:sequence>
                <xs:element name="product" type="productType" minOccurs="0" maxOccurs="unbounded"/>
            </xs:sequence>
        </xs:complexType>
        <xs:complexType name="productType">
            <xs:sequence>
                <xs:element name="productId" type="xs:string"/>
                <xs:element name="quantity" type="xs:integer"/>
            </xs:sequence>
        </xs:complexType>
    </xs:schema>'
```

### Regex Validation Assertions

Add the custom header `X-Mockallan-Validator: regex` to the `POST /assert-called-with` or `POST /assert-called-once-with` request and place the regular expression in the body. 

E.g.

```bash
curl -X POST --header 'X-Mockallan-Validator: regex'	\
	http://localhost:8080/assert-called-with?method=POST&path=/orders/order_e2b9/products	\
	--data '{"orderNumber":"\w+","products":\[\{"productId":"\w+","quantity":\d+}(,\{"productId":"\w+","quantity":\d+\})*\]}'
```

<!-- ## Stub Configuration JSON

The Stub Configuration JSON format configures mockallan responses.

### Stub Configuration Example


```json
{
	"defaults": {
		"response": {
			"status_code": 200,
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
				"status_code": 200
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
|PUT|/configure|-|JSON stub configuration|204; 400|-|
|GET|/configure|-|-|200|JSON stub configuration|


## Assertion API

The Assertion API allows for the validation of expected requests.

|Method|Path|Query Params|Request Body|Status|Response Body|
|-|-|-|-|-|-|
|GET|/assert-called|method, path|-|200 OK; 400; 409|Assertion success or error message|
|GET|/assert-called-once|method, path|-|200 OK; 400; 409|Assertion success or error message|
|POST|/assert-called-with|method, path|JSON object, JSON schema, XML schema or regex|200 OK; 400; 409|Assertion success or error message|
|POST|/assert-called-once-with|method, path|JSON object, JSON schema, XML schema, regex or message body|200 OK; 400; 409|Assertion success or error message|
|GET|/request-body|-|-|200 OK; 409|The request body that the mock was last called with|
|GET|/request-body-list|-|-|200 OK|List of all the requests made to the mock in sequence|
|GET|/request-count|-|-|200 OK|Request count|


## Naming

Stub Configuration API and Assertion API naming are inspired by class `Mock` from the standard python package `unittest.mock`.


## Contributing

Found a bug, facing some unexpected quirks, or got ideas for making this project better? Don't hesitate to [raise an issue](https://github.com/david-domz/mockallan/issues). Your help is appreciated.


## License

This project is licensed under the terms of the MIT license.


## Related Projects

- [mockallan-docker](https://github.com/david-domz/mockallan-docker) - Containerized lightweight HTTP server mock.
- [mockallan-python-client](https://github.com/david-domz/mockallan-python-client) - Mockallan python client class.
