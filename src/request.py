from dataclasses import dataclass, field



class ContentType:
	TEXT_PLAIN = {'Content-Type': 'text/plain'}
	APPLICATION_JSON = {'Content-Type': 'application/json'}
	APPLICATION_JSON_ERROR = {'Content-Type': 'application/json+error'}
	APPLICATION_XML = {'Content-Type': 'application/xml'}
	APPLICATION_OCTET_STREAM = {'Content-Type': 'application/octet-stream'}


@dataclass
class HTTPRequest:
	method: str
	path: str
	query: dict = field(default_factory=dict)
	headers: dict = field(default_factory=dict)
	body: dict | str | bytes = ''

	@staticmethod
	def endpoint(request: 'HTTPRequest') -> tuple[str, str]:
		return (request.method.upper(), request.path)


@dataclass
class HTTPResponse:
	code: int
	headers: dict = field(default_factory=dict)
	body: dict | str | bytes = ''

	def __post_init__(self):
		if not isinstance(self.code, int):
			raise TypeError(f"'code' must be {int} but it is actually {type(self.code)}")
