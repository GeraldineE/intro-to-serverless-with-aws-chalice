import requests
import json
import gzip

from chalice import Chalice, Response

from chalicelib.helpers import compress_response

app = Chalice(app_name="intro-to-serverless-with-aws-chalice-demo")
app.api.binary_types.append("application/json")


@app.route("/")
def index():
    return {"hello": "world"}


@app.route("/authors")
def authors():
    r = requests.get(
        "https://fakerestapi.azurewebsites.net/api/Authors",
        headers={"content-type": "application/json"},
    )
    result = r.json() * 50

    return result


@app.route("/authors/compress")
def authors_compress():
    r = requests.get(
        "https://fakerestapi.azurewebsites.net/api/Authors",
        headers={"content-type": "application/json"},
    )
    result = r.json() * 50
    blob = json.dumps(r.json()).encode("utf-8")
    payload = gzip.compress(blob)
    custom_headers = {"Content-Type": "application/json", "Content-Encoding": "gzip"}

    return Response(body=payload, status_code=200, headers=custom_headers)


@app.route("/authors/compress-with-decorator")
@compress_response
def authors_compress_with_decorator():
    r = requests.get(
        "https://fakerestapi.azurewebsites.net/api/Authors",
        headers={"content-type": "application/json"},
    )
    result = r.json() * 50

    return result


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
