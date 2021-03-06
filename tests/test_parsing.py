#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`test_parsing`
=======================

.. moduleauthor:: hbldh <henrik.blidh@swedwise.com>
Created on 2016-05-17, 14:01

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os

from xml.etree.ElementTree import ParseError
from xml.etree.cElementTree import ParseError as cParseError
from lxml.etree import XMLSyntaxError

import pytest

from xmlr import xmlparse, XMLParsingMethods
from xmlr.compat import *

from .utils import xmldata_note, xmldata_note_error, \
    xmldata_cd, xmldata_menu, xmldata_plants, walk_test


@pytest.mark.parametrize("parser", (XMLParsingMethods.ELEMENTTREE,
                                    XMLParsingMethods.C_ELEMENTTREE,
                                    XMLParsingMethods.LXML_ELEMENTTREE))
def test_parsing_note(xmldata_note, parser):
    doc = xmlparse(xmldata_note, parsing_method=parser)
    assert isinstance(doc, dict)
    walk_test(doc)


@pytest.mark.parametrize("parser", (XMLParsingMethods.ELEMENTTREE,
                                    XMLParsingMethods.C_ELEMENTTREE,
                                    XMLParsingMethods.LXML_ELEMENTTREE))
def test_parsing_note_error(xmldata_note_error, parser):
    with pytest.raises((ParseError, cParseError, XMLSyntaxError)):
        xmlparse(xmldata_note_error, parsing_method=parser)


@pytest.mark.parametrize("parser", (XMLParsingMethods.ELEMENTTREE,
                                    XMLParsingMethods.C_ELEMENTTREE,
                                    XMLParsingMethods.LXML_ELEMENTTREE))
def test_parsing_cd(xmldata_cd, parser):
    doc = xmlparse(xmldata_cd, parsing_method=parser)
    assert isinstance(doc, dict)
    walk_test(doc)


@pytest.mark.parametrize("parser", (XMLParsingMethods.ELEMENTTREE,
                                    XMLParsingMethods.C_ELEMENTTREE,
                                    XMLParsingMethods.LXML_ELEMENTTREE))
def test_parsing_plants(xmldata_plants, parser):
    doc = xmlparse(xmldata_plants, parsing_method=parser)
    assert isinstance(doc, dict)
    walk_test(doc)


@pytest.mark.parametrize("parser", (XMLParsingMethods.ELEMENTTREE,
                                    XMLParsingMethods.C_ELEMENTTREE,
                                    XMLParsingMethods.LXML_ELEMENTTREE))
def test_parsing_menu(xmldata_menu, parser):
    doc = xmlparse(xmldata_menu, parsing_method=parser)
    assert isinstance(doc, dict)
    walk_test(doc)


@pytest.mark.parametrize("parser", (XMLParsingMethods.ELEMENTTREE,
                                    XMLParsingMethods.C_ELEMENTTREE,
                                    XMLParsingMethods.LXML_ELEMENTTREE))
def test_parsing_google_renewal_data(parser):
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'google-renewals-subset-20080624.xml')
    doc = xmlparse(f, parsing_method=parser)
    assert isinstance(doc, dict)
    walk_test(doc)


@pytest.mark.parametrize("parser", (XMLParsingMethods.ELEMENTTREE,
                                    XMLParsingMethods.C_ELEMENTTREE,
                                    XMLParsingMethods.LXML_ELEMENTTREE))
def test_parsing_test_doc(parser):
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'test_doc.xml')
    doc = xmlparse(f, parsing_method=parser)
    assert isinstance(doc, dict)
    walk_test(doc)

