"""
Celery kingdom
"""


from celery import Celery
from time import sleep
from xml_parse import parse_xml_file

from models import Url, session as s, Key

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis')


@app.task
def add_url(url: str):
    """
    Populate url info to a database
    Represent long operation that can takes significant amount of time
    What's why it's moved to a celery task
    :param url: link to a XML file
    :return: {'id': <id of created Url in DB>}
    """
    xml_dict = parse_xml_file(url)
    url_object = Url(url=xml_dict['url'],
                     processed=bool(not xml_dict['error_text']),
                     error=xml_dict['error_text'])
    url_object.keys = [Key(value=key) for key in xml_dict['keys']]
    s.add(url_object)
    s.commit()
    # sleep(20) # uncomment this, if you want to test *real* async :)
    return {'id': url_object.id}
