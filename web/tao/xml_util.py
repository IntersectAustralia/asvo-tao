from lxml import etree

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
    return etree.tostring(root, pretty_print=True)

def remove_comments(root):
    comments = root.xpath('//comment()')
    for c in comments:
        p = c.getparent()
        if p is not None:
            p.remove(c)
    return root
