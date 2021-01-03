from collections import OrderedDict

import mongoengine as mongo


def __field_mapping__(self):
    # Define mappings between Mongoengine fields and OpenAPI 3

    types_mapping = {
        "ObjectIdField": {"type": "integer", "format": "int64"},
        "BooleanField": {"type": "boolean"},
        "StringField": {"type": "string"},
    }

    # print(self.__class__.__name__)
    try:
        return types_mapping[self.__class__.__name__]
    except:
        # Return StringField if you don't find the exact mapping
        return types_mapping["StringField"]


def generic_endpoint_spec(class_name, operation):

    operation2verb = {
        "create": "created",
        "read": "read",
        "update": "updated",
        "delete": "deleted",
    }

    toRet = OrderedDict()
    toRet["tags"] = [class_name]
    toRet["summary"] = f"{operation} a {class_name}"
    toRet["operationId"] = f"{class_name}_{operation}"
    if operation not in ["read", "delete"]:
        toRet["requestBody"] = OrderedDict()
        toRet["requestBody"][
            "description"
        ] = "{} object that needs to be {}".format(
            class_name, operation2verb[operation]
        )
        toRet["requestBody"]["content"] = OrderedDict()
        toRet["requestBody"]["content"]["application/json"] = {
            "schema": {"$ref": f"#/components/schemas/{class_name}"}
        }
        #  toRet["requestBody"]["content"]["application/xml"] = {"schema": {"$ref": "#/components/schemas/{}".format(class_name) }}
        toRet["requestBody"]["required"] = True
    toRet["responses"] = OrderedDict()
    toRet["responses"]["200"] = {"description": "Success"}
    toRet["responses"]["500"] = {"description": "Internal error"}

    return toRet


def _PF_gen_endpoint_spec(self):

    operation2httpverb = {
        "create": "post",
        "read": "get",
        "update": "put",
        "delete": "delete",
    }

    toRet = OrderedDict()
    class_name = self._class_name.lower()

    toRet[operation2httpverb["create"]] = generic_endpoint_spec(
        class_name, "create"
    )
    toRet[operation2httpverb["read"]] = generic_endpoint_spec(
        class_name, "read"
    )
    toRet[operation2httpverb["update"]] = generic_endpoint_spec(
        class_name, "update"
    )
    toRet[operation2httpverb["delete"]] = generic_endpoint_spec(
        class_name, "delete"
    )

    return (class_name, toRet)


@classmethod
def _PF_gen_root_document_OpenAPI_spec(self):
    properties = OrderedDict()
    for (
        key
    ) in (
        self._fields_ordered
    ):  # <mongoengine.base.fields.ObjectIdField object at 0x10a2e8208>
        # print("---------------------------------")
        # print(key) #name
        # print(self._fields[key])
        # print(type(self._fields[key]).__name__) # StringFiled
        # print(self._fields[key].__class__.__name__) # StringFiled
        # print(vars(type(self._fields[key])) ) # StringFiled
        # if key=="id": continue
        # try:
        properties[self._fields[key].name] = self._fields[key]._PF_gen_schema()
        # except: pass

    ToRet = (
        self._class_name.lower(),
        OrderedDict({"type": "object", "properties": properties}),
    )
    return ToRet


def __start_openapi3_dict__(
    version="1.0.0",
    title="No Title",
    description="N/A",
    url="http://localhost/api",
):

    json_result = OrderedDict()
    json_result["openapi"] = "3.0.1"
    json_result["info"] = {
        "title": title,
        "version": version,
        "description": description,
    }
    json_result["servers"] = [{"url": url}]
    json_result["paths"] = OrderedDict()
    json_result["components"] = {"schemas": OrderedDict()}

    return json_result


# All Monkey Patch schema to generate class definition


mongo.Document._PF_gen_schema = _PF_gen_root_document_OpenAPI_spec
mongo.ObjectIdField._PF_gen_schema = __field_mapping__
mongo.StringField._PF_gen_schema = __field_mapping__
# mongo.URLField
# mongo.EmailField
# mongo.IntField._PF_gen_schema = _PF_gen_schema_int
# mongo.LongField
# mongo.FloatField
# mongo.DecimalField._PF_gen_schema = _PF_gen_schema_dict
mongo.BooleanField._PF_gen_schema = __field_mapping__
# mongo.DateTimeField._PF_gen_schema = _PF_gen_schema_date_time
# mongo.ComplexDateTimeField._PF_gen_schema = _PF_gen_schema_cdate
# mongo.EmbeddedDocumentField
# mongo.GenericEmbeddedDocumentField
# mongo.DynamicField
# mongo.ListField
# mongo.SortedListField
# mongo.DictField._PF_gen_schema = _PF_gen_schema_dict
# mongo.MapField
# mongo.ReferenceField
# mongo.GenericReferenceField
# mongo.BinaryField
# mongo.FileField
# mongo.ImageField
# mongo.SequenceField
# mongo.GeoPointField
# mongo.PointField
# mongo.LineStringField
# mongo.PolygonField
# mongo.GridFSError
# mongo.GridFSProxy
# mongo.ImageGridFsProxy
# mongo.ImproperlyConfigured ?????


# Monkey Patch schema to generate endpoint spec
# mongo.Document._PF_gen_endpoint = _PF_gen_endpoint_spec
