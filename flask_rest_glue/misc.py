class Methods:

    get = "GET"
    put = "PUT"
    post = "POST"
    delete = "DELETE"
    update = "UPDATE"

    all = [get, put, post, delete, update]


def get_default_api_info(base_url, path_spec):
    default_api_info = {
        "title": "Flask_Rest_Glue",
        "version": "0.0.1",
        "description": "N/A",
        "url": f"{base_url}",
        "openapi_url": f"{base_url}{path_spec}"
    }
    return default_api_info
