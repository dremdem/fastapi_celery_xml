from fastapi_app.app.xml_parse import parse_xml_file

url1 = "https://hub.b2basket.ru/media/test_problem/file_1.xml"
url2 = "https://hub.b2basket.ru/media/test_problem/file_2.xml"
url3 = "https://hub.b2basket.ru/media/test_problem/file_3.xml"


def test_parse_xml_file():
    assert type(parse_xml_file(url1)) == dict
    assert type(parse_xml_file(url2)) == dict
    assert type(parse_xml_file(url3)) == dict
