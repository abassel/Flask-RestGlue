import json

import mongoengine as mongo
from flask_rest_glue import FlaskRestGlue

mongo.connect("mongoenginetest", host="mongomock://localhost")

api = FlaskRestGlue()


@api.rest_model()
class User(mongo.Document):
    email = mongo.StringField(primary_key=True)
    password = mongo.StringField()


flask = api.build()

tclient = flask.test_client()


def test_get_empty_db_expect_pass():
    res = tclient.get("/user")
    assert res.status == "200 OK"
    assert res.headers["Content-Type"] == "application/json"
    assert json.loads(res.data) == []
