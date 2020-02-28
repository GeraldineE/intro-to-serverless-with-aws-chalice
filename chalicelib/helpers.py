import json
import gzip

from chalice import Response


def compress_response(view):
    def _compress_response(*args, **kwargs):
        data = view(*args, **kwargs)
        blob = json.dumps(data).encode("utf-8")
        payload = gzip.compress(blob)
        custom_headers = {
            "Content-Type": "application/json",
            "Content-Encoding": "gzip",
        }
        return Response(body=payload, status_code=200, headers=custom_headers)

    return _compress_response
