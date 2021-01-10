import json

from flask import jsonify, request

from .misc import Methods
from .openapi_spec import get_redoc_html, get_swagger_ui_html


def build_flask_openapi_spec_endpoint(flask_api, spec, path_spec, api_info):

    @flask_api.route(path_spec)
    def json_spec():
        return jsonify(spec)

    @flask_api.route(path_spec + "_doc")
    def swagger_html():
        return get_swagger_ui_html(**api_info)

    @flask_api.route(path_spec + "_rdoc")
    def redoc_html():
        return get_redoc_html(**api_info)


def build_class_endpoint(flask_api, _class, class_name, methods):

    # https://dev.to/paurakhsharma/flask-rest-api-part-1-using-mongodb-with-flask-3g7d

    if Methods.post in methods:
        @flask_api.route(f"/{class_name}", endpoint=f"{class_name}_create", methods=["POST"])
        def obj_create_post():
            body = request.get_json()
            new_item = _class(**body).save()
            return jsonify(json.loads(new_item.to_json()))

    if Methods.get in methods:
        @flask_api.route(f"/{class_name}", endpoint=f"{class_name}_read", methods=["GET"])
        def obj_read():
            items = _class.objects()
            return jsonify(json.loads(items.to_json()))

    if Methods.get in methods:
        @flask_api.route(f"/{class_name}/<pk>", endpoint=f"{class_name}_read_id", methods=["GET"])
        def obj_read(pk):
            item = _class.objects.get(pk=pk)
            return jsonify(json.loads(item.to_json()))

    if Methods.put in methods:
        @flask_api.route(f"/{class_name}/<pk>", endpoint=f"{class_name}_update", methods=["PUT"])
        def obj_update(pk):
            body = request.get_json()
            item = _class.objects.get(pk=pk)
            item.update(**body)
            item.reload()
            return jsonify(json.loads(item.to_json()))

    if Methods.delete in methods:
        @flask_api.route(f"/{class_name}/<pk>", endpoint=f"{class_name}_delete", methods=["DELETE"])
        def obj_delete(pk):
            item = _class.objects.get(pk=pk)
            item.delete()
            return jsonify(json.loads(item.to_json()))
