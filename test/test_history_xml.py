import pytest
from mockallan.request import ContentType, HTTPRequest
from mockallan.app_handler import History


def test_assert_called_once_with_xml_schema_success(history: History):
	"""Tests assert_called_once_with() fails; XML schema matches. """

	endpoint_called = ('PUT', '/path/xml/1')
	with_request = HTTPRequest(
		'PUT',
		'/path/xml/1',
		headers=ContentType.APPLICATION_XML,
		body='''
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
	<xs:element name="individual">
		<xs:complexType>
			<xs:sequence>
				<xs:element name="name" type="xs:string" />
				<xs:element name="address">
				<xs:complexType>
					<xs:sequence>
						<xs:element name="zip" type="xs:string" />
						<xs:element name="city" type="xs:string" />
					</xs:sequence>
				</xs:complexType>
				</xs:element>
			</xs:sequence>
		</xs:complexType>
	</xs:element>
</xs:schema>''')

	history.assert_called_once_with(endpoint_called, with_request)


def test_assert_called_once_with_xml_schema_assertion_error(history: History):
	"""Tests assert_called_once_with() fails; XML schema does not match. """

	endpoint_called = ('PUT', '/path/xml/1')
	with_request = HTTPRequest(
		'PUT',
		'/path/xml/1',
		headers=ContentType.APPLICATION_XML,
		body='''
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
	<xs:element name="individual">
		<xs:complexType>
			<xs:sequence>
				<xs:element name="name" type="xs:string" />
				<xs:element name="address">
					<xs:complexType>
						<xs:sequence>
							<xs:element name="zip" type="xs:string" />
							<xs:element name="city" type="xs:string" />
							<xs:element name="street" type="xs:string" />
						</xs:sequence>
					</xs:complexType>
				</xs:element>
			</xs:sequence>
		</xs:complexType>
	</xs:element>
</xs:schema>
''')

	with pytest.raises(AssertionError):
		history.assert_called_once_with(endpoint_called, with_request)
