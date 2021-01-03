import json

from flask import jsonify, request


def _PF_Build_Flask_endpoint(flask_api, spec, path="/api/spec"):
    @flask_api.route(path)
    def json_spec():
        return jsonify(spec)

    # @flask_api.route('/<path:subpath>')
    # def show_subpath(subpath):
    #     # show the subpath after /path/
    #     return 'Subpath %s' % subpath

    # TODO: Add Swagger UI
    # https://github.com/tiangolo/fastapi/blob/5614b94ccc9f72f1de2f63aae63f5fe90b86c8b5/fastapi/openapi/docs.py
    #

    # def has_no_empty_params(rule):
    #     defaults = rule.defaults if rule.defaults is not None else ()
    #     arguments = rule.arguments if rule.arguments is not None else ()
    #     return len(defaults) >= len(arguments)
    #
    #
    # from flask import Flask, url_for
    # @app.route("/site-map")
    # def site_map():
    #     links = []
    #     for rule in app.url_map.iter_rules():
    #         # Filter out rules we can't navigate to in a browser
    #         # and rules that require parameters
    #         if "GET" in rule.methods and has_no_empty_params(rule):
    #             url = url_for(rule.endpoint, **(rule.defaults or {}))
    #             links.append((url, rule.endpoint))
    #     return str(links)


def _PF_build_flask_endpoint(flask_api, _class, name=None, plural=None):

    class_name = (name or _class.__name__).lower()
    class_plural = (plural or class_name + "s").lower()

    # https://dev.to/paurakhsharma/flask-rest-api-part-1-using-mongodb-with-flask-3g7d
    @flask_api.route(
        f"/{class_name}", endpoint=class_name + "_create", methods=["POST"]
    )
    def obj_create_post():
        body = request.get_json()
        new_item = _class(**body).save()
        return jsonify(json.loads(new_item.to_json()))

    @flask_api.route(
        f"/{class_plural}", endpoint=class_name + "_read", methods=["GET"]
    )
    def obj_read():
        items = _class.objects()
        return jsonify(json.loads(items.to_json()))

    @flask_api.route(
        f"/{class_name}/<pk>", endpoint=class_name + "_read_id", methods=["GET"]
    )
    def obj_read(pk):
        item = _class.objects.get(pk=pk)
        return jsonify(json.loads(item.to_json()))

    @flask_api.route(
        f"/{class_name}/<pk>", endpoint=class_name + "_update", methods=["PUT"]
    )
    def obj_update(pk):
        body = request.get_json()
        item = _class.objects.get(pk=pk)
        item.update(**body)
        item.reload()
        return jsonify(json.loads(item.to_json()))

    @flask_api.route(
        f"/{class_name}/<pk>",
        endpoint=class_name + "_delete",
        methods=["DELETE"],
    )
    def obj_delete(pk):
        item = _class.objects.get(pk=pk)
        item.delete()
        return jsonify(json.loads(item.to_json()))
