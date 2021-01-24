from flask import Flask

from . import flask_endpoint, openapi_spec
from .misc import Methods, get_default_api_info, url_join


class FlaskRestGlue:
    def __init__(self, url="http://127.0.0.1:5000", path="/", spec_path=None, flask_app=None, api_info=None, gen_map=True):
        self._path = url_join([path])
        self._spec_path = spec_path
        self._flask_api = flask_app or Flask(__name__)
        self._pending_introspection = {}
        self._api_info = api_info
        self._gen_map = gen_map
        self._openapi_spec = None

        if self._spec_path:
            self._spec_path = url_join([spec_path])
        else:
            self._spec_path = url_join([self._path, "api.json"])

        if not self._api_info:
            self._api_info = get_default_api_info(base_url=url, path_spec=self._spec_path)

    def rest_model(self, name=None, methods=Methods.all, *args, **kwargs):
        def inner(_class):
            """
            Store items pending introspection
            """
            class_name_lower = (name or f"{_class.__name__}").lower()

            self._pending_introspection[_class] = methods, class_name_lower

            return _class

        return inner

    def build(self):
        # Generate api_doc and endpoint
        openapi_spec.mokeypatch_mongoengine()

        openapi_spec_dict = openapi_spec.__start_openapi3_dict__(**self._api_info)

        for cls in self._pending_introspection.keys():

            methods, class_name_lower = self._pending_introspection[cls]

            # Generate spec
            schema = cls._gen_schema()

            spec_path = openapi_spec.gen_openapi_path_spec(class_name_lower, methods, self._path)

            openapi_spec_dict["components"]["schemas"][class_name_lower] = schema
            openapi_spec_dict["paths"].update(spec_path)

            # Generate endpoint for each class
            flask_endpoint.build_class_endpoint(self._flask_api, cls, class_name_lower, methods, self._path)

        flask_endpoint.build_flask_openapi_spec_endpoint(self._flask_api, openapi_spec_dict, self._spec_path, self._api_info, self._path, self._gen_map)

        self._openapi_spec = openapi_spec_dict

        self._flask_api.config["JSON_SORT_KEYS"] = False

        return self._flask_api

    def run(self, *args, **kwargs):

        flask_api = self.build()

        flask_api.run(*args, **kwargs)
