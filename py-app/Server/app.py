import os
from datetime import datetime as dt
from pathlib import Path

from flask import Flask, send_from_directory, Response, jsonify
from PortOpt import EfficientFrontier


APP = Flask(__name__)
APP.static_folder = (Path(APP.root_path) / "../../build").resolve(strict=True)
# print(APP.static_folder)

LOGIC = EfficientFrontier(["", "aa"])


class MockCache:
    TIME_FORMAT = r"%Y-%m-%d"
    STATES = [
        "wait",
        "run",
        "plot",
        "opti",
        "",
    ]

    base = {
        "codes": ["GOOG", "AAPL", "MSFT"],
        "start": "",
        "end": dt.now().strftime(TIME_FORMAT),
        "runs": 50000,
        "precision": 1,
        "display_chart": "",
        "target_risk": "",
        "state_code": 0
    }

    def __init__(self) -> None:
        self._cache = MockCache.base

    def update(self, key, value):
        self._cache[key] = value

    def read(self, key):
        return self._cache[key]

    def reset(self, key):
        self._cache[key] = MockCache.base[key]


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


@APP.route("/run")
def run_simulation():
    # TODO get form data
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
