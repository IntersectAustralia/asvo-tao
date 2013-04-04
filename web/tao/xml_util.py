"""
===========================
tao.xml_util
===========================

Helper methods for XML
"""
from lxml import etree
import re

def create_root(tag, **attrs):
    return etree.Element(tag, **attrs)

def find_or_create(root, tag, **attrs):
    elem = root.find(tag)
    if elem is None:
        elem = etree.SubElement(root, tag, **attrs)
    return elem


def child_element(parent, tag, text=None, **attrs):
    elem = etree.SubElement(parent, tag, **attrs)
    if text is not None:
        elem.text = str(text)
    return elem

def xml_print(root):
    return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)

def xml_parse(xml_str):
    return etree.fromstring(xml_str)

def remove_comments(root):
    comments = root.xpath('//comment()')
    for c in comments:
        p = c.getparent()
        if p is not None:
            p.remove(c)
    return root

_XPATH_SLASH_BEFORE_TOKEN = rx = re.compile('/(?=[^/])')

def module_xpath(xml_root, path, text=True, attribute=None):
    """
    utility to simplify our xpaths so we use a known namespace
    :param xml_root: the root xml we are searching from
    :param path: a quasi-xpath to which name space is attached
    :return: the text (if true), or an attribute (if provided) or the element
    """
    path = _XPATH_SLASH_BEFORE_TOKEN.sub('/m:', path)
    elems = xml_root.xpath(path, namespaces={'m':'http://tao.asvo.org.au/schema/module-parameters-v1'})
    resp = None
    if elems is not None and len(elems) == 1:
        if attribute is not None:
            resp = elems[0].get(attribute)
        elif text:
            resp = elems[0].text
        else:
            resp = elems[0]
    return resp

