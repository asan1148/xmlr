#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
xmller.parse
~~~~~~~~~~~~~

:copyright: 2016 by Henrik Blidh <henrik.blidh@nedomkull.com>

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from operator import setitem

import xml.etree.ElementTree as etree

from xmller.compat import *


def xmlparse(source):
    """Parses a XML document into a dictionary.

    Details about how the XML is converted into this dictionary (json)
    representation is described in reference [3] in the README.

    :param str,file-like source: Either the path to a XML document to parse
        or a file-like object (with `read` attribute) containing an XML.
    :return: The parsed XML in dictionary representation.
    :rtype: dict

    """

    # This is the output dict.
    output = {}

    # Keeping track of the depth and position to store data in.
    current_position = []
    current_index = []

    # Start iterating over the Element Tree.
    for event, elem in etree.iterparse(source, events=('start', 'end')):

        if event == 'start':
            # Start of new tag.

            # Extract the current endpoint so add the new element to it.
            tmp = output
            for cp, ci in zip(current_position, current_index):
                tmp = tmp[cp]
                if ci:
                    tmp = tmp[ci]

            # If it is a previously unseen tag, create a new key and
            # stick an empty dict there. Set index of this level to None.
            if elem.tag not in tmp:
                tmp[elem.tag] = {}
                current_index.append(None)
            else:
                # The tag name already exists. This means that we have to change
                # the value of this element's key to a list if this hasn't
                # been done already and add an empty dict to the end of that
                # list. If it already is a list, just add an new dict and update
                # the current index.
                if isinstance(tmp[elem.tag], list):
                    current_index.append(len(tmp[elem.tag]))
                    tmp[elem.tag].append({})
                else:
                    tmp[elem.tag] = [tmp[elem.tag], {}]
                    current_index.append(1)

            # Set the position of the iteration to this element's tag name.
            current_position.append(elem.tag)
        elif event == 'end':
            # End of a tag.

            # Extract the current endpoint's parent so we can handle
            # the endpoint's data by reference.
            tmp = output
            for cp, ci in zip(current_position[:-1], current_index[:-1]):
                tmp = tmp[cp]
                if ci:
                    tmp = tmp[ci]
            cp = current_position[-1]
            ci = current_index[-1]

            # If this current endpoint is a dict in a list or not has
            # implications on how to set data.
            if ci:
                setfcn = lambda x: setitem(tmp[cp], ci, x)
                for attr_name, attr_value in elem.attrib.items():
                    tmp[cp][ci]["@{0}".format(attr_name)] = attr_value
            else:
                setfcn = lambda x: setitem(tmp, cp, x)
                for attr_name, attr_value in elem.attrib.items():
                    tmp[cp]["@{0}".format(attr_name)] = attr_value

            # If there is any text in the tag, add it here.
            if elem.text and elem.text.strip():
                setfcn({'#text': elem.text.strip()})

            # Handle special cases:
            # 1) when the tag only harbours text, replace the dict content with
            #    that very text string.
            # 2) when no text, attributes or children are present, content
            #    is set to None
            # These are detailed in reference [3] in README.
            if ci:
                if tmp[cp][ci]:
                    nk = len(tmp[cp][ci].keys())
                    if nk == 1 and "#text" in tmp[cp][ci]:
                        tmp[cp][ci] = tmp[cp][ci]["#text"]
                    elif nk == 0:
                        tmp[cp][ci] = None
                else:
                    tmp[cp][ci] = None
            else:
                nk = len(tmp[cp].keys())
                if nk == 1 and "#text" in tmp[cp]:
                    tmp[cp] = tmp[cp]["#text"]
                elif nk == 0:
                    tmp[cp] = None

            # Remove the outermost position and index, since we just finished
            # handling that element.
            current_position.pop()
            current_index.pop()

            # Most important of all, release the element's memory allocations
            # so we actually benefit from the iterative processing!
            elem.clear()

    return output


def main():
    import os

    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'data', 'google-renewals-all-20080624.xml')

    doc = xmlparse(filepath)


if __name__ == "__main__":
    main()