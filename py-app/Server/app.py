import os
import time
from pathlib import Path

from flask import Flask, send_from_directory, Response, jsonify


APP = Flask(__name__)
APP.static_folder = (Path(APP.root_path) / "../../build").resolve(strict=True)
# print(APP.static_folder)


class MockCache:
    def __init__(self) -> None:
        self._cache = [0]

    def incr(self, input_string):
        print(input_string, self._cache[0])
        self._cache[0] += 1
        print(input_string, self._cache[0])
        return self._cache[0]


cache = MockCache()



@APP.route("/")
def hello():
    return send_from_directory(APP.static_folder, "index.html")


@APP.route("/favicon.png")
def icon():
    return send_from_directory(APP.static_folder, "favicon.png")


@APP.route("/_app/<path:path>")
def resp(path):
    abspath = APP.static_folder + "/_app/" + path
    abspath = Path(abspath).resolve(strict=True)
    # a = send_file(abspath)
    # print(abspath)

    b = "_app/" + path
    b = send_from_directory(APP.static_folder, b)
    return b


@APP.route("/abc")
def abc():
    print("asdfsdafasdfsdfds")
    return jsonify("123")


@APP.route("/chartList")
def chart_list():
    dp = (Path(APP.root_path) / "../../data").resolve(strict=True)
    lst = [str(e.stem) for e in dp.iterdir()]
    # lst = [e for e in range(10)]
    return jsonify(lst)


@APP.route("/charts/<path:path>")
def get_chart(path):
    # print("getting charts")
    dp = (Path(APP.root_path) / "../../data").resolve(strict=True)
    pattern = path + ".*"

    if path == "plotly.min.js":
        # print(path)
        # print(dp)
        return send_from_directory(dp, path)

    elif files := [e for e in dp.glob(pattern)]:
        dp = (Path(APP.root_path) / "../../data").resolve(strict=True)
        return send_from_directory(dp, files[0].name)

    else:
        return Response(status=400)

