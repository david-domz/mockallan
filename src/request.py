from dataclasses import dataclass, field
from typing import Union


Body = Union[str, bytes, dict]
"""

	Class type	Content-Type
	---		---
	str		text/plain
	bytes		application/octet-stream
	dict		application/json

"""


@dataclass
class HTTPRequest:
	method: str
	path: str
	query: dict = field(default_factory=dict)
	headers: dict = field(default_factory=dict)

	body: Body = ''

	@staticmethod
	def endpoint(request: 'HTTPRequest') -> tuple[str, str]:
		return (request.method.upper(), request.path)


@dataclass
class HTTPResponse:
	code: int
	headers: dict = field(default_factory=dict)
	body: Body = ''
