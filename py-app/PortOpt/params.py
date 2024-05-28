class PlotlyParams:

    def __init__(self) -> None:
        pass

    @property
    def margin_layout(self):
        margin_layout = {
            "autoexpand": True,
            "t": 0,
            "b": 0,
            "r": 0,
            "l": 0,
        }
        return margin_layout

    @property
    def legend_layout(self):
        legend_layout = {
            "xref": "paper",
            "x": 0,
            "yref": "paper",
            "y": 1,
            "orientation": "h",
            "bgcolor": "rgba(0,0,0,0)",
        }
        return legend_layout

    @property
    def layout(self):
        layout = {
            # "title": "Efficient Frontier by Simulation",
            # "autosize": True,
            "xaxis_title": "Annualized Risk",
            "yaxis_title": "Annualized Return",
            "dragmode": "pan",
        }
        return layout

    @property
    def modebar(self):
        modebar = {
            "bgcolor": "rgba(0,0,0,0)",
            "color": "rgba(0,0,0,1)",
            "activecolor": "rgba(0,0,0,0.5)",
        }
        return modebar

    @property
    def config(self):
        config = {
            "displaylogo": False,
            "scrollZoom": True,
            "modeBarButtonsToRemove": [
                "zoom",
                "pan",
                "toImage",
                "lasso",
                "select",
                "zoomin",
                "zoomout",
                "resetScale2d",
            ],
            "modeBarButtonsToAdd": [
                # "drawline",
                # "hoverClosestCartesian",
                # "hoverclosest",
            ],
        }
        return config

    def get_layout(self, margin=True, legend=True, modebar=True):
        l = self.layout
        l = {**l, "margin": self.margin_layout} if margin else l
        l = {**l, "legend": self.legend_layout} if legend else l
        l = {**l, "modebar": self.modebar} if modebar else l
        return l

    def get_config(self):
        c = self.config
        return c

    def get_textpos(self):
        return [
            ("top center", -45, 45),
            ("middle left", -135, -45),
            ("middle right", 45, 135),
            ("bottom center", 999, -999),
        ]
