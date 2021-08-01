from lxml import etree
from semantic_version import Version

import io

class InvalidVersionError(Exception):
    def __init__(self, version_string, message=None):
        message = message or f"Invalid version string '{version_string}'"
        super().__init__(version_string, message)
        self.version_string = version_string
        self.message = message

    def __str__(self):
        return self.message


class MissingVersionError(Exception):
    def __init__(self):
        self.message = "Missing version"

    def __str__(self):
        return self.message


def load(file_or_filename="pom.xml"):
    doc = etree.parse(file_or_filename)
    namespace = dict(pom="http://maven.apache.org/POM/4.0.0")

    try:
        elements = doc.xpath("/pom:project/pom:version", namespaces=namespace)
        version_string = elements[0].text.strip()
    except IndexError:
        raise MissingVersionError() from None

    try:
        return Version(version_string.strip())
    except ValueError as err:
        raise InvalidVersionError(version_string, str(err)) from None


def from_xml(xml_string):
    return load(io.StringIO(xml_string))
