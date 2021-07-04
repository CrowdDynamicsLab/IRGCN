import xml.etree.ElementTree as ET

def RowIter(the_file):
    for line in the_file:
        try:
            root = ET.fromstring(line)
        except:
            continue
        if root.tag == 'row':
            yield root.attrib, line.strip()

