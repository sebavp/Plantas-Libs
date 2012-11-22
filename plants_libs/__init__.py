# -*- coding: utf-8 -*-
import os
import re
import sys
from time import sleep

from lxml import etree

LANGUAGE_CODES = {
    'en': 'en',
    'eng': 'en',
    'english': 'en',
    'es': 'es',
    'spa': 'es',
    'spanish': 'es',
    'español': 'es',
    'ar': 'ar',
    'ara': 'ar',
    'arabic': 'ar',
    'de': 'de',
    'deu': 'de',
    'ger': 'de',
    'german': 'de',
    'deutsch': 'de',
    'fr': 'fr',
    'fre': 'fr',
    'fra': 'fr',
    'french': 'fr',
    'français': 'fr',
    'nl': 'nl',
    'nld': 'nl',
    'dut': 'nl',
    'dutch': 'nl',
    'nederlands': 'nl',
    'vlaams': 'nl',
    'it': 'it',
    'ita': 'it',
    'italian': 'it',
    'italiano': 'it',
    'pt': 'pt',
    'por': 'por',
    'portuguese': 'pt',
    'português': 'pt',
    'zh': 'zh',
    'zho': 'zh',
    'chi': 'zh',
    'chinese': 'zh'
}

MONTH_NUMBERS = {
    'jan' : '01',
    'feb' : '02',
    'mar' : '03',
    'apr' : '04',
    'may' : '05',
    'jun' : '06',
    'jul' : '07',
    'aug' : '08',
    'sep' : '09',
    'oct' : '10',
    'nov' : '11',
    'dec' : '12'
}

def format_day_text(text):
    if not text:
        return text
    if text.isdigit() and len(text) == 1:
        return '0' + text
    return text

def get_month_number_from_month_text(text):
    if not text:
        return text
    if text.isdigit():
        return text
    month_format = text.lower()[0:3]
    if month_format in MONTH_NUMBERS:
        return MONTH_NUMBERS[month_format]
    return text

def get_one_element(elements, default = None, strip = False, not_false = False):
    if strip:
        elements = map(lambda x: x.strip(), elements)
    for element in elements:
        if not_false:
            if element:
                return element
        else:
            return element

def save_debug():
    old_debug_value = 'False'
    if os.environ.get('EPISTE_DEBUG'):
        old_debug_value = os.environ['EPISTE_DEBUG']
    os.environ['EPISTE_DEBUG'] = 'False'
    os.environ['EPISTE_DEBUG_OLD'] = old_debug_value

def restore_debug():
    old_debug_value = 'False'
    if os.environ.get('EPISTE_DEBUG_OLD'):
        old_debug_value = os.environ.get('EPISTE_DEBUG_OLD')
        del os.environ['EPISTE_DEBUG_OLD']
    os.environ['EPISTE_DEBUG'] = old_debug_value

def get_tree(content):
    try:
        parser = etree.XMLParser()
        return etree.fromstring(content, parser)
    except:
        parser = etree.HTMLParser()
        return etree.fromstring(content, parser)

def to_unicode(elements):
    if type(elements) == str:
        return elements.decode('utf8')
    elif type(elements) == list:
        for i in range(0, len(elements)):
            elements[i] = to_unicode(elements[i])
    elif type(elements) == tuple:
        new_elements = []
        for i in range(0, len(elements)):
            new_elements.append(to_unicode(elements[i]))
        elements = tuple(new_elements)
    elif type(elements) == dict:
        for key, value in elements.iteritems():
            elements[key] = to_unicode(value)
    return elements

def remove_tags(text, not_in = []):
    temporal_tag_open = 'init-----episte-----'
    temporal_tag_close = '-----episte-----fin'
    
    for tag in not_in:
        text = re.sub('<(\/?)%s>' % tag, r'%s\g<1>%s%s' % (temporal_tag_open, tag, temporal_tag_close), text)
        text = re.sub('<(\/?)%s\s+[^>]*>' % tag, r'%s\g<1>%s%s' % (temporal_tag_open, tag, temporal_tag_close), text)
        
    new_text = re.sub('<\/?[a-zA-Z\/][^>]*>', ' ', text)
    new_text = re.sub(temporal_tag_open, '<', new_text)
    new_text = re.sub(temporal_tag_close, '>', new_text)
    return re.sub(' +', ' ', new_text).strip()

def convert_keys_to_str(elements, value = False):
    if isinstance(elements, dict):
        return dict((str(k), convert_keys_to_str(v, value = value)) for k, v in elements.items())
    else:
        if value and isinstance(elements, unicode):
            return elements.encode('utf-8')
        return elements

def tuple_list_to_dict(tuple_list):
    dictionary = {}
    for x,y in tuple_list:
        dictionary[x] = y
    return dictionary