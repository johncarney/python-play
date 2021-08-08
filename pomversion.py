"""Load an artifact version from a POM file or XML."""

from semantic_version import Version

import xml.etree.ElementTree as ElementTree
import io

POM_NAMESPACE = {"pom": "http://maven.apache.org/POM/4.0.0"}


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
    """Loads the version from a POM file

    Parameters
    ----------
    file_or_filename : str
        A file object or a file name to load the POM from.

    Returns
    -------
    semantic_version.Version
        The version from the POM file as a semantic version.
    """

    root = ElementTree.parse(file_or_filename)
    elements = root.findall("./pom:version", POM_NAMESPACE)
    # doc = etree.parse(file_or_filename)
    # elements = doc.xpath("/pom:project/pom:version", namespaces=POM_NAMESPACE)
    if len(elements) < 1:
        raise MissingVersionError()
    version_string = elements[0].text.strip()

    try:
        return Version(version_string.strip())
    except ValueError as err:
        raise InvalidVersionError(version_string, str(err)) from None


def from_xml(xml_string):
    """Loads the version from POM XML

    Parameters
    ----------
    file_or_xml_string : str
        An XML string

    Returns
    -------
    semantic_version.Version
        The version from the XML as a semantic version.
    """

    return load(io.StringIO(xml_string))
