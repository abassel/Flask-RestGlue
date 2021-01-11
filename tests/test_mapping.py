from json import dumps, loads

import mongoengine as mongo
from flask_rest_glue import openapi_spec

openapi_spec.mokeypatch_mongoengine()


def to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict))


def test_stringfiled_mapping_expect_pass():
    field = mongo.StringField()
    json = field._gen_schema()

    assert json == {"type": "string"}


def test_list_string_mapping_expect_pass():
    field = mongo.ListField(mongo.StringField())
    json = field._gen_schema()

    assert json == {"type": "array", 'items': {'type': 'string'}}


def test_list_integer_mapping_expect_pass():
    field = mongo.ListField(mongo.IntField())
    json = field._gen_schema()

    assert json == {"type": "array", 'items': {'type': 'number'}}


def test_class_with_lists_mapping_expect_pass():

    class Dummy(mongo.Document):
        comments = mongo.ListField(mongo.StringField())
        numbers = mongo.ListField(mongo.IntField())

    json = to_dict(Dummy._gen_schema())
    assert json == {
        "type": "object",
        'properties': {
            'id': {'type': 'integer', 'format': 'int64'},
            'comments': {'type': 'array', 'items': {'type': 'string'}},
            'numbers': {'type': 'array', 'items': {'type': 'number'}}
        }
    }
