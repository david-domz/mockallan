from argparse import ArgumentParser
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from request import HTTPRequest, HTTPResponse
from stub_config import StubConfig
from app_handler import AppHandler


VERSION = '0.0.4'

__all__ = ['MockHTTPServer']


def http_request_handler_class_factory(app_handler: AppHandler):
	"""Returns the HTTPRequestHandler class parametrized with `app_handler`.

	"""
	class HTTPRequestHandler(BaseHTTPRequestHandler):

		def __init__(self, request, client_address, server):

			self.app_handler = app_handler
			super().__init__(request, client_address, server)

		def do_GET(self):

			parse_result = urllib.parse.urlparse(self.path)
			query = urllib.parse.parse_qs(parse_result.query)

			request = HTTPRequest('GET', parse_result.path, query, self.headers)
			response = self.app_handler.handle_request(request)
			self._write_response(response)

		def do_PUT(self):

			parse_result = urllib.parse.urlparse(self.path)
			query = urllib.parse.parse_qs(parse_result.query)

			content_length = int(self.headers['Content-Length'])
			body = self.rfile.read(content_length)
			body_str = body.decode('utf-8')
			request = HTTPRequest('PUT', parse_result.path, query, self.headers, body_str)

			response = self.app_handler.handle_request(request)

			self._write_response(response)

		def do_POST(self):

			parse_result = urllib.parse.urlparse(self.path)
			query = urllib.parse.parse_qs(parse_result.query)

			content_length = int(self.headers['Content-Length'])
			body = self.rfile.read(content_length)
			body_str = body.decode('utf-8')
			request = HTTPRequest('POST', parse_result.path, query, self.headers, body_str)

			response = self.app_handler.handle_request(request)

			self._write_response(response)

		def _write_response(self, response: HTTPResponse):

			self.send_response(response.code)
			for key, value in response.headers.items():
				self.send_header(key, value)
			self.end_headers()

			if isinstance(response.body, dict):
				response.body = json.dumps(response.body)

			self.wfile.write(response.body.encode('utf-8'))

	return HTTPRequestHandler


class MockHTTPServer():
	"""Configurable HTTP server mock.

	Configurable at initialization time from a JSON file or python dict. Configurable at run time via REST API.

	"""
	def __init__(self, server_address, stub_config_json: dict | str | None):

		self._config = StubConfig(stub_config_json)
		app_handler = AppHandler(self._config)
		http_request_handler_class = http_request_handler_class_factory(app_handler)
		self._http_server = HTTPServer(server_address, http_request_handler_class)

	def serve_forever(self, poll_interval=0.5):

		self._http_server.serve_forever(poll_interval)

	def close(self):
		self._http_server.socket.close()


def main():
	argparse = ArgumentParser(description=f'Mockallan HTTP server mock ver. {VERSION}')
	argparse.add_argument("-H", "--host", type=str, metavar="HOST", dest="host", default="0.0.0.0")
	argparse.add_argument("-p", "--port", type=int, metavar="PORT", dest="port", default=8080)
	argparse.add_argument("-c", "--stub-config", type=str, metavar="STUB_CONFIG", dest="stub_config_json")

	args = argparse.parse_args()

	server_address = (args.host, args.port)
	print(f'Listening on {server_address[0]}:{server_address[1]}')

	try:
		mock_http_server = MockHTTPServer(server_address, args.stub_config_json)
	except FileNotFoundError as e:
		print(f'Failed to instantiate MockHTTPServer: {e}')
	else:
		try:
			mock_http_server.serve_forever()
		except KeyboardInterrupt:
			print('\nShutting down')

		mock_http_server.close()


if __name__ == '__main__':
	main()
