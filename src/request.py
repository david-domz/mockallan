from dataclasses import dataclass, field


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
