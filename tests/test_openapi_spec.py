from json import dumps, loads
from pprint import pprint

import mongoengine as mongo
import yaml
from flask_rest_glue import FlaskRestGlue, openapi_spec
from flask_rest_glue.misc import Methods

api = FlaskRestGlue()


@api.rest_model()
class Pet(mongo.Document):
    email = mongo.StringField(primary_key=True)
    password = mongo.StringField()


flask = api.build()


def to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict))


def test_openapi_path():
    target_spec = None

    with open("tests/pet_only.yaml") as stream:
        try:
            target_spec = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    spec = dict(openapi_spec.gen_openapi_path_spec("pet", Methods.all, "/"))

    assert to_dict(spec["/pet"]["get"]) == target_spec["/pet"]["get"]
    # assert to_dict(spec["/pet/{id}"]) == target_spec["/pet/{id}"]
