from typing import Literal
from datetime import datetime
from datetime import timedelta as td

from pydantic import BaseModel, Field, PositiveInt, ValidationError, field_validator
from pydantic_core import PydanticCustomError

from PortOpt.weights import get_len_of_combination


TIME_FORMAT = r"%Y-%m-%d"
RUN_LIMIT = 500000
PREC_LIMIT = 3
RATIO_LIMIT = 0.5


class ParseInput(BaseModel):
    codes: str
    runs: PositiveInt = Field(le=RUN_LIMIT)
    precision: PositiveInt = Field(le=PREC_LIMIT)
    start: datetime
    end: datetime
    restricted: bool = Field(default=False, validate_default=True)
    ratio: bool = Field(default=True, validate_default=True)
    date: bool = Field(default=True, validate_default=True)

    @field_validator("ratio")
    @classmethod
    def validate_computation(cls, v, info):
        c = info.data["codes"]
        e = len([*c.split(",")])
        r = info.data["runs"]
        p = info.data["precision"]
        l = get_len_of_combination(e, p)
        ratio = r / l
        if v:
            if ratio < RATIO_LIMIT:
                raise PydanticCustomError(
                    "app_restriction",
                    f"Model coverage ('ratio:.0%') is below the 50% threshold, try increasing number of runs or reducing number of stock codes. Currently, the number of runs is '{r}', while the number of possibilities is '{l}'.",
                )
        # print(r, l)
        return v

    @field_validator("restricted")
    @classmethod
    def validate_mode(cls, v, info):
        """
        p = 1, e < 14
        p = 2, e < 5
        p = 3, e < 4
        """
        restrictions = {1: 13, 2: 4, 3: 3}
        e = len([*info.data["codes"].split(",")])
        p = info.data["precision"]
        if v:
            if e > restrictions[p]:
                raise PydanticCustomError(
                    "app_restriction",
                    f"In restricted mode, number of stock entries is restricted to '<{e}', for a given precision of '{p}'. Try reducing the precision or number of stock codes.",
                )
        return v

    @field_validator("date")
    @classmethod
    def validate_date(cls, v, info):
        s = info.data.get("start", None)
        e = info.data.get("end", None)
        diff = (e - s).days if s and e else 1
        if v:
            if diff < 1:
                raise PydanticCustomError(
                    "app_restriction",
                    f"Start date and end date cannot be on the same date.",
                )
        return v
