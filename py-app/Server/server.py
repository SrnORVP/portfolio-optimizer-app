from datetime import datetime as dt, timedelta as td
from time import sleep
from pathlib import Path

from pydantic import ValidationError
from flask import Flask, request, send_from_directory, Response, Request, jsonify

from Server.parse import ParseInput
from PortOpt import EfficientFrontier


global EF_ENGINE
global cache

APP = Flask(__name__)
APP.static_folder = (Path(APP.root_path) / "../../build").resolve(strict=True)
# DATAPATH = (Path(APP.root_path) / "../../.data").resolve(strict=True)
# print(APP.static_folder)


class MockCache:
    RESTRICTED_MODE = True
    TIME_FORMAT = r"%Y-%m-%d"
    ERROR_STATE = "ERROR"
    STATES = {
        "w": "wait",
        "c": "check",
        "r": "run",
        "p": "plot",
        "o": "opti",
        "e": ERROR_STATE,
    }

    base = {
        "state": "w",
        "codes": "GOOG, AAPL, MSFT",
        "start": (dt.now() - td(days=100)).strftime(TIME_FORMAT),
        "end": dt.now().strftime(TIME_FORMAT),
        "runs": 1000,
        "precision": 1,
        "chart": "",
        "charts": "",
        "html": "",
        "fwidth": "",
        "fheight": "",
        "target": "",
        "messages": "",
    }

    readable = {
        "codes": "stock codes",
        "start": "start date",
        "end": "end date",
        "runs": "number of monte carlo runs",
        "precision": "model precisions",
        "ratio": "Model representativeness",
        "restricted": "server restriction",
        "date": "same dates",
    }

    def __init__(self) -> None:
        self._cache = MockCache.base

    def update(self, key, value):
        self._cache[key] = value

    def dict_update(self, d):
        for k, v in d.items():
            self.update(k, v)

    def read(self, key):
        return self._cache[key]

    def reset(self, key):
        self._cache[key] = MockCache.base[key]

    @property
    def content(self):
        return self._cache

    def get_state(self):
        return self.STATES[self._cache["state"]]

    def reset_state(self):
        self._cache["state"] = "w"

    def __repr__(self) -> str:
        def render_each(element):
            try:
                return f"longer than {len(element)}" if len(element) > 50 else element
            except TypeError:
                return element

        return ", ".join([f"({k}: {render_each(v)})" for k, v in self._cache.items()])

    def feedback_on_input(self):
        msg = {
            k: (self.readable[k], f"Value of '{v}' is accepted.", False)
            for k, v in self.content.items()
            if k in self.readable
        }

        try:
            ParseInput(**self.content, restricted=self.RESTRICTED_MODE)
        except ValidationError as error:
            err = {
                e["loc"][0]: (self.readable[e["loc"][0]], e["msg"], True)
                for e in error.errors()
            }
            msg.update(**err)
            self._cache["state"] = "e"

        return [
            {"display": display, "explain": explain, "err": err}
            for display, explain, err in msg.values()
        ]


cache = MockCache()


#############################################################################
# Serve static html as build with sevltekit/vite


@APP.route("/")
def index():
    return send_from_directory(APP.static_folder, "index.html")


@APP.route("/favicon.png")
def favicon():
    return send_from_directory(APP.static_folder, "favicon.png")


@APP.route("/README.md")
def readme():
    return send_from_directory(APP.static_folder, "README.md")


@APP.route("/_app/<path:path>")
def resp(path):
    # abspath = APP.static_folder + "/_app/" + path
    # abspath = Path(abspath).resolve(strict=True)
    # a = send_file(abspath)
    # print(abspath)

    b = "_app/" + path
    b = send_from_directory(APP.static_folder, b)
    return b


#############################################################################
# hydrate content as needed by state
# ensure compability with Tauri need to change request.get_json()
# so the code receive json string directly


@APP.route("/post/state", methods=["POST"])
def handle_post():
    global cache

    j = request.get_json()
    cache.dict_update(j)
    # content = cache.content
    print("rece resq", cache)
    match cache.get_state():
        case "check":
            cache = check(cache)
        case "run":
            cache = check(cache)
            if cache.get_state() != MockCache.ERROR_STATE:
                cache = run(cache)
        case "plot":
            cache = serve_chart(cache)
        case "opti":
            print("opti")
    cache.reset_state()
    print("send resp", cache)
    return jsonify(cache.content)


@APP.route("/get/state", methods=["GET"])
def handle_get():
    return jsonify(cache.content)


#############################################################################


def check(cache):
    msg = cache.feedback_on_input()
    cache.update("messages", msg)
    return cache


def run(cache):
    content = cache.content

    global EF_ENGINE
    EF_ENGINE = EfficientFrontier(
        content["codes"], int(content["runs"]), int(content["precision"])
    )
    EF_ENGINE.raw_df = EF_ENGINE.download_stock_data(
        content["codes"], content["start"], content["end"]
    )
    EF_ENGINE.get_numpy_repr()
    EF_ENGINE.get_risk_return()
    EF_ENGINE.generate_portfolio_weights()
    EF_ENGINE.run_simulation()
    EF_ENGINE.get_efficient_frontier(from_max_risk=False, from_min_ret=True)
    plot_list = EF_ENGINE.plot_engine_plots_list()

    cache.update("charts", plot_list)
    return cache


def serve_chart(cache):
    SCALE = 0.95

    content = cache.content

    global EF_ENGINE
    plot_only = content["chart"]
    EF_ENGINE.gen_plot_collection(
        # write_disk=DATAPATH,
        with_labels=True,
        cases=[plot_only],
        default_width=content["fwidth"] * SCALE,
        default_height=content["fheight"] * SCALE,
    )
    cache.update("html", EF_ENGINE.plot_collection[plot_only])
    sleep(1)
    return cache
