from flask import Flask

from . import openapi_spec
from .flask_endpoint import _PF_Build_Flask_endpoint, _PF_build_flask_endpoint


class FlaskRestGlue:
    def __init__(self):
        self.__pending_introspection = []
        pass

    def rest_model(self, *args, **kwargs):
        def inner(func):
            """
            do operations with func
            """
            self.__pending_introspection.append(func)
            return func

        return inner  # this is the fun_obj mentioned in the above content

    def build(self):
        # Generate api_doc endpoint
        flask_api = Flask(__name__)

        openapi_spec_ordDict = openapi_spec.__start_openapi3_dict__()

        for cls in self.__pending_introspection:
            print(f"doing introspection {cls}")

            # Generate spec
            class_name, schema = cls._PF_gen_schema()

            openapi_spec_ordDict["components"]["schemas"][class_name] = schema
            openapi_spec_ordDict["paths"]["/" + class_name] = schema

            # Generate endpoint for each class
            _PF_build_flask_endpoint(flask_api, cls)

        # finalSpec_str = json.dumps(openapi_spec_data)
        # print(type(finalSpec_str))
        # print(finalSpec_str)

        _PF_Build_Flask_endpoint(flask_api, openapi_spec_ordDict)

        flask_api.config["JSON_SORT_KEYS"] = False

        # def has_no_empty_params(rule):
        #     defaults = rule.defaults if rule.defaults is not None else ()
        #     arguments = rule.arguments if rule.arguments is not None else ()
        #     return len(defaults) >= len(arguments)
        #
        #
        # @flask_api.route("/site-map")
        # def site_map():
        #     links = []
        #     for rule in flask_api.url_map.iter_rules():
        #         # Filter out rules we can't navigate to in a browser
        #         # and rules that require parameters
        #         if "GET" in rule.methods and has_no_empty_params(rule):
        #             url = flask_api(rule.endpoint, **(rule.defaults or {}))
        #             print(url)
        #             print(rule.endpoint)
        #             links.append((url, rule.endpoint))
        #     return str(links)

        return flask_api

    def run(self):

        flask_api = self.build()

        flask_api.run()
