from lxml import etree, objectify


def normalise_xml(xmlstring):
    as_object = etree.fromstring(xmlstring)
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

        self.assertEqual(expected_lines, actual_lines)
