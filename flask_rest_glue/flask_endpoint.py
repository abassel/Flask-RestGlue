import json

from flask import jsonify, request

from .misc import Methods, url_join
from .openapi_spec import get_map_html, get_redoc_html, get_swagger_ui_html


def build_flask_openapi_spec_endpoint(flask_api, spec, path_spec, api_info, root_path, gen_map):

    @flask_api.route(path_spec)
    def json_spec():
        return jsonify(spec)

    @flask_api.route(path_spec.split(".json")[0] + "_doc")
    def swagger_html():
        return get_swagger_ui_html(**api_info)

    @flask_api.route(path_spec.split(".json")[0] + "_rdoc")
    def redoc_html():
        return get_redoc_html(**api_info)

    if gen_map:
        tmp_html = get_map_html(flask_api)

        @flask_api.route(root_path)
        def path_spec_html():
            return tmp_html


def build_class_endpoint(flask_api, _class, class_name, methods, path):

    # https://dev.to/paurakhsharma/flask-rest-api-part-1-using-mongodb-with-flask-3g7d

    root_path = url_join([path, class_name])
    root_path_pk = url_join([root_path, "<pk>"])

    if Methods.post in methods:
        @flask_api.route(root_path, endpoint=f"{class_name}_create", methods=["POST"])
        def obj_create_post():

            if hasattr(_class, "before_any"):
                _class.before_any(request)

            if hasattr(_class, "before_post"):
                _class.before_post(request)

            body = request.get_json()
            new_item = _class(**body).save()

            if hasattr(_class, 'custom_json'):
                return jsonify(new_item.custom_json())

            return jsonify(json.loads(new_item.to_json()))

    if Methods.get in methods:
        @flask_api.route(root_path, endpoint=f"{class_name}_read", methods=["GET"])
        def obj_read():

            if hasattr(_class, "before_any"):
                _class.before_any(request)

            if hasattr(_class, "before_get"):
                _class.before_get(request)

            items = _class.objects()

            if hasattr(_class, 'custom_json'):
                return jsonify([item.custom_json() for item in items])

            return jsonify(json.loads(items.to_json()))

    if Methods.get in methods:
        @flask_api.route(root_path_pk, endpoint=f"{class_name}_read_id", methods=["GET"])
        def obj_read(pk):

            if hasattr(_class, "before_any"):
                _class.before_any(request)

            if hasattr(_class, "before_get"):
                _class.before_get(request)

            item = _class.objects.get(pk=pk)

            if hasattr(_class, 'custom_json'):
                return jsonify(item.custom_json())

            return jsonify(json.loads(item.to_json()))

    if Methods.put in methods:
        @flask_api.route(root_path_pk, endpoint=f"{class_name}_update", methods=["PUT"])
        def obj_update(pk):

            if hasattr(_class, "before_any"):
                _class.before_any(request)

            if hasattr(_class, "before_put"):
                _class.before_put(request)

            body = request.get_json()
            item = _class.objects.get(pk=pk)
            item.update(**body)
            item.reload()

            if hasattr(_class, 'custom_json'):
                return jsonify(item.custom_json())

            return jsonify(json.loads(item.to_json()))

    if Methods.delete in methods:
        @flask_api.route(root_path_pk, endpoint=f"{class_name}_delete", methods=["DELETE"])
        def obj_delete(pk):

            if hasattr(_class, "before_any"):
                _class.before_any(request)

            if hasattr(_class, "before_delete"):
                _class.before_delete(request)

            item = _class.objects.get(pk=pk)
            item.delete()

            if hasattr(_class, 'custom_json'):
                return jsonify(item.custom_json())

            return jsonify(json.loads(item.to_json()))
