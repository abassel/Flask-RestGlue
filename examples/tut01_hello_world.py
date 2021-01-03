import mongoengine as mongo
from flask_rest_glue import FlaskRestGlue

mongo.connect("pyglue", host="localhost:27017")

api = FlaskRestGlue()


@api.rest_model()
class User(mongo.Document):
    # id = mongo.StringField(primary_key=True)
    email = mongo.StringField(primary_key=True)
    password = mongo.StringField()


api.run()
