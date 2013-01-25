from lxml import etree, objectify
from tao.xml_util import remove_comments


def normalise_xml(xmlstring):
    as_object = etree.fromstring(xmlstring)
    as_object = remove_comments(as_object)
    normalised_string = etree.tostring(as_object, pretty_print=True)
    return normalised_string


class XmlDiffMixin(object):
    """
        This class provides xml diff capabilities
    """
    def assertXmlEqual(self, expected, actual):
        normalised_expected = normalise_xml(expected)
        normalised_actual = normalise_xml(actual)

        expected_lines = normalised_expected.split('\n')
        actual_lines = normalised_actual.split('\n')
        maxDiff = self.maxDiff
        self.maxDiff = None
        self.assertEqual(expected_lines, actual_lines)
        self.maxDiff = maxDiff

