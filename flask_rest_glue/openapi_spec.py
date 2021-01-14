from collections import OrderedDict

import mongoengine as mongo
from mongoengine.base import BaseField, ComplexBaseField

from .misc import Methods, url_join

base_types_mapping = {
    "ObjectIdField": {"type": "integer", "format": "int64"},
    "BooleanField": {"type": "boolean"},
    "StringField": {"type": "string"},
    "IntField": {"type": "number"},
    "ListField": {"type": "array", "items": {}}
}


def __field_mapping__(self):
    # Define mappings between Mongoengine fields and OpenAPI 3

    try:
        # base_types_mapping is static and without the dict the references will
        # confuse the generator thus dict is required to create a new item
        toRet = dict(base_types_mapping[self.__class__.__name__])

        if self.__class__.__name__ in ["ListField"]:  # Complex field? Generate mapping recursively
            toRet["items"] = self.field._gen_schema()

        return toRet
    except:
        # Return StringField if you don't find the exact mapping
        return base_types_mapping["StringField"]


def generic_endpoint_spec(class_name, operation, require_id):
    operation2verb = {
        "create": "created",
        "read": "read",
        "update": "updated",
        "delete": "deleted",
    }

    toRet = OrderedDict()

    toRet["tags"] = [class_name]
    toRet["summary"] = f"{operation} a {class_name}"

    if require_id:
        toRet["operationId"] = f"{class_name}_{operation}_id"

        toRet["parameters"] = [{}]
        toRet["parameters"][0]["name"] = "id"
        toRet["parameters"][0]["in"] = "path"
        toRet["parameters"][0]["description"] = f"ID/pk of {class_name} to return"
        toRet["parameters"][0]["required"] = "true"
        toRet["parameters"][0]["schema"] = {}
        toRet["parameters"][0]["schema"]["type"] = "string"
        # toRet["parameters"][0]["schema"]["format"] = "int64"

    else:
        toRet["operationId"] = f"{class_name}_{operation}"

    if operation not in ["read", "delete"]:
        toRet["requestBody"] = {}
        toRet["requestBody"]["description"] = f"{class_name} object that needs to be {operation2verb[operation]}"
        toRet["requestBody"]["required"] = True
        toRet["requestBody"]["content"] = {}
        toRet["requestBody"]["content"]["application/json"] = {"schema": {"$ref": f"#/components/schemas/{class_name}"}}
        # toRet["requestBody"]["content"]["application/xml"] = {"schema": {"$ref": "#/components/schemas/{}".format(class_name) }}

    toRet["responses"] = {}
    toRet["responses"]["200"] = {
        "description": "Successful operation",
        "content": {
            "application/json": {
                "schema": {"$ref": f"#/components/schemas/{class_name}"}
            }
        },
    }
    toRet["responses"]["405"] = {"description": "Invalid input"}

    return toRet


def gen_openapi_path_spec(class_name, methods, path):
    toRet = OrderedDict()

    path_no_id = url_join([path, class_name])
    path_with_id = url_join([path, class_name, "{id}"])

    toRet[path_with_id] = OrderedDict()
    toRet[path_no_id] = OrderedDict()

    if Methods.post in methods:
        toRet[path_no_id]["post"] = generic_endpoint_spec(class_name, "create", require_id=False)

    if Methods.get in methods:
        toRet[path_no_id]["get"] = generic_endpoint_spec(class_name, "read", require_id=False)
        toRet[path_with_id]["get"] = generic_endpoint_spec(class_name, "read", require_id=True)

    if Methods.update in methods:
        toRet[path_with_id]["put"] = generic_endpoint_spec(class_name, "update", require_id=True)

    if Methods.delete in methods:
        toRet[path_with_id]["delete"] = generic_endpoint_spec(class_name, "delete", require_id=True)

    if len(toRet[path_with_id]) == 0:
        del toRet[path_with_id]

    if len(toRet[path_no_id]) == 0:
        del toRet[path_no_id]

    return toRet


@classmethod
def __gen_root_document_OpenAPI_spec(_class):
    properties = OrderedDict()

    for key in _class._fields_ordered:  # <mongoengine.base.fields.ObjectIdField object at 0x10a2e8208>
        # print("---------------------------------")
        # print(key) #name
        # print(self._fields[key])
        # print(type(self._fields[key]).__name__) # StringFiled
        # print(self._fields[key].__class__.__name__) # StringFiled
        # print(vars(type(self._fields[key])) ) # StringFiled
        # if key=="id": continue
        # try:
        field_name = _class._fields[key].name
        properties[field_name] = _class._fields[key]._gen_schema()

    return OrderedDict({"type": "object", "properties": properties})


def __start_openapi3_dict__(url, title, version, description, **kwargs):

    json_result = OrderedDict()
    json_result["openapi"] = "3.0.3"
    json_result["info"] = {
        "title": title,
        "version": version,
        "description": description,
    }
    json_result["servers"] = [{"url": url}]
    json_result["paths"] = OrderedDict()
    json_result["components"] = {"schemas": OrderedDict()}

    return json_result


def mokeypatch_mongoengine():
    # Monkey Patch schema to generate class definition

    BaseField._gen_schema = __field_mapping__

    mongo.Document._gen_schema = __gen_root_document_OpenAPI_spec

    # mongo.ObjectIdField._gen_schema = __field_mapping__
    # mongo.StringField._gen_schema = __field_mapping__
    # # mongo.URLField
    # # mongo.EmailField
    # # mongo.IntField._gen_schema = _gen_schema_int
    # # mongo.LongField
    # # mongo.FloatField
    # # mongo.DecimalField._gen_schema = _gen_schema_dict
    # mongo.BooleanField._gen_schema = __field_mapping__
    # # mongo.DateTimeField._gen_schema = _gen_schema_date_time
    # # mongo.ComplexDateTimeField._gen_schema = _gen_schema_cdate
    # # mongo.EmbeddedDocumentField
    # # mongo.GenericEmbeddedDocumentField
    # # mongo.DynamicField
    # mongo.ListField._gen_schema = __field_mapping__
    # # mongo.SortedListField
    # # mongo.DictField._gen_schema = _gen_schema_dict
    # # mongo.MapField
    # # mongo.ReferenceField
    # # mongo.GenericReferenceField
    # # mongo.BinaryField
    # # mongo.FileField
    # # mongo.ImageField
    # # mongo.SequenceField
    # # mongo.GeoPointField
    # # mongo.PointField
    # # mongo.LineStringField
    # # mongo.PolygonField
    # # mongo.GridFSError
    # # mongo.GridFSProxy
    # # mongo.ImageGridFsProxy
    # # mongo.ImproperlyConfigured ?????


# Stolen from https://github.com/tiangolo/fastapi/blob/5614b94ccc9f72f1de2f63aae63f5fe90b86c8b5/fastapi/openapi/docs.py


from typing import Any, Dict, Optional, OrderedDict


# Generate basic html map with all possible routes inside flask
def get_map_html(flask_api) -> str:

    endpoint_routes = {}
    for rule in flask_api.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        endpoint_routes[f"{rule.rule}{methods}"] = rule.rule, methods

    html = """
    <!DOCTYPE html>
    <html>
    <head>

    </head>
    <body>
    <div>
    <ul>
    """

    for t in sorted(endpoint_routes.keys()):
        route = endpoint_routes[t]
        print(route)
        tmp = route[0].replace("<", "&lt;").replace(">", "&gt;")
        html += f"<li><a href='{tmp}'>{tmp} {route[1]}</a></li>"

    html += """
    </ul>
    </div>
    </body>
    </html>
    """

    return html


def get_swagger_ui_html(
    *,
    openapi_url: str,
    title: str,
    swagger_js_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
    swagger_css_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css",
    swagger_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    oauth2_redirect_url: Optional[str] = None,
    init_oauth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> str:  # HTMLResponse:

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="{swagger_js_url}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
    """

    if oauth2_redirect_url:
        html += f"oauth2RedirectUrl: window.location.origin + '{oauth2_redirect_url}',"

    html += """
        dom_id: '#swagger-ui',
        presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout",
        deepLinking: true,
        showExtensions: true,
        showCommonExtensions: true
    })"""

    # if init_oauth:
    #     html += f"""
    #     ui.initOAuth({json.dumps(jsonable_encoder(init_oauth))})
    #     """

    html += """
    </script>
    </body>
    </html>
    """
    # return HTMLResponse(html)
    return html


def get_redoc_html(
    *,
    openapi_url: str,
    title: str,
    redoc_js_url: str = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    redoc_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    **kwargs
    # with_google_fonts: bool = True,
) -> str:  # HTMLResponse:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{title}</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """
    # if with_google_fonts:
    #     html += """
    # <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    # """
    html += f"""
    <link rel="shortcut icon" href="{redoc_favicon_url}">
    <!--
    ReDoc doesn't change outer page styles
    -->
    <style>
      body {{
        margin: 0;
        padding: 0;
      }}
    </style>
    </head>
    <body>
    <redoc spec-url="{openapi_url}"></redoc>
    <script src="{redoc_js_url}"> </script>
    </body>
    </html>
    """
    # return HTMLResponse(html)
    return html

#
# def get_swagger_ui_oauth2_redirect_html() -> HTMLResponse:
#     html = """
#     <!DOCTYPE html>
#     <html lang="en-US">
#     <body onload="run()">
#     </body>
#     </html>
#     <script>
#         'use strict';
#         function run () {
#             var oauth2 = window.opener.swaggerUIRedirectOauth2;
#             var sentState = oauth2.state;
#             var redirectUrl = oauth2.redirectUrl;
#             var isValid, qp, arr;
#             if (/code|token|error/.test(window.location.hash)) {
#                 qp = window.location.hash.substring(1);
#             } else {
#                 qp = location.search.substring(1);
#             }
#             arr = qp.split("&")
#             arr.forEach(function (v,i,_arr) { _arr[i] = '"' + v.replace('=', '":"') + '"';})
#             qp = qp ? JSON.parse('{' + arr.join() + '}',
#                     function (key, value) {
#                         return key === "" ? value : decodeURIComponent(value)
#                     }
#             ) : {}
#             isValid = qp.state === sentState
#             if ((
#             oauth2.auth.schema.get("flow") === "accessCode"||
#             oauth2.auth.schema.get("flow") === "authorizationCode"
#             ) && !oauth2.auth.code) {
#                 if (!isValid) {
#                     oauth2.errCb({
#                         authId: oauth2.auth.name,
#                         source: "auth",
#                         level: "warning",
#                         message: "Authorization may be unsafe, passed state was changed in server Passed state wasn't returned from auth server"
#                     });
#                 }
#                 if (qp.code) {
#                     delete oauth2.state;
#                     oauth2.auth.code = qp.code;
#                     oauth2.callback({auth: oauth2.auth, redirectUrl: redirectUrl});
#                 } else {
#                     let oauthErrorMsg
#                     if (qp.error) {
#                         oauthErrorMsg = "["+qp.error+"]: " +
#                             (qp.error_description ? qp.error_description+ ". " : "no accessCode received from the server. ") +
#                             (qp.error_uri ? "More info: "+qp.error_uri : "");
#                     }
#                     oauth2.errCb({
#                         authId: oauth2.auth.name,
#                         source: "auth",
#                         level: "error",
#                         message: oauthErrorMsg || "[Authorization failed]: no accessCode received from the server"
#                     });
#                 }
#             } else {
#                 oauth2.callback({auth: oauth2.auth, token: qp, isValid: isValid, redirectUrl: redirectUrl});
#             }
#             window.close();
#         }
#     </script>
#         """
#     return HTMLResponse(content=html)
