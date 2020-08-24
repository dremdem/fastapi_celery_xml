"""
Small module that serve XML-parsing
"""

import requests
import xml.etree.cElementTree as ET


def parse_xml_file(url: str) -> dict:
    """
    Fetch XML-file by url, parse it and return dict
    :param url:
    :return: dict with the following structure:
    {
        'url': <url>,
        'keys': [list of keys from XML-file],
        'error_text': <Error text if any>
    }
    """

    keys = []

    try:
        r = requests.get(url)
        root = ET.fromstring(r.content)
        keys = [element.text for element in root if element.tag == 'key']
        error_text = ''
    except Exception as e:
        error_text = str(e)

    url_dict = {
        'url': url,
        'keys': keys,
        'error_text': error_text
    }

    return url_dict


