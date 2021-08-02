import pytest
import pomversion
import semantic_version
import lxml

# Helpers

def load_pom_xml(filename):
    with open(filename, "r") as file:
        return file.read()


def load_artifact_version(filename):
    doc = lxml.etree.parse(filename)
    version_elements = doc.xpath("/pom:project/pom:version", namespaces=pomversion.POM_NAMESPACE)
    if len(version_elements) == 0:
        return None
    return version_elements[0].text.strip()

# pomversion.load tests

def test_load_without_parameters():
    expected_artifact_version = semantic_version.Version(load_artifact_version("pom.xml"))
    assert pomversion.load() == expected_artifact_version


def test_load_with_filename():
    expected_artifact_version = semantic_version.Version(load_artifact_version("pom.xml"))
    assert pomversion.load("pom.xml") == expected_artifact_version


def test_load_with_file():
    expected_artifact_version = semantic_version.Version(load_artifact_version("pom.xml"))
    with open("pom.xml", "r") as file:
        assert pomversion.load(file) == expected_artifact_version


def test_load_with_invalid_artifact_version():
    with pytest.raises(pomversion.InvalidVersionError):
        pomversion.load("invalid-version-pom.xml")


def test_load_with_missing_artifact_version():
    with pytest.raises(pomversion.MissingVersionError):
        pomversion.load("missing-version-pom.xml")


def test_load_with_missing_file():
    with pytest.raises(OSError):
        pomversion.load("no-such-pom.xml")

# pomversion.from_xml tests

def test_from_xml():
    expected_artifact_version = semantic_version.Version(load_artifact_version("pom.xml"))
    pom_xml = load_pom_xml("pom.xml")
    assert pomversion.from_xml(pom_xml) == expected_artifact_version


def test_from_xml_with_invalid_artifact_version():
    pom_xml = load_pom_xml("invalid-version-pom.xml")
    with pytest.raises(pomversion.InvalidVersionError):
        pomversion.from_xml(pom_xml)


def test_from_xml_with_missing_artifact_version():
    pom_xml = load_pom_xml("missing-version-pom.xml")
    with pytest.raises(pomversion.MissingVersionError):
        pomversion.from_xml(pom_xml)
