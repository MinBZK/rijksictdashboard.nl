from enum import IntEnum
from typing import Literal

ContentGroep = dict[str, str]
TextLoaderContent = dict[Literal["nl", "en"], ContentGroep]

SpreadsheetType = Literal["excel", "ods"]


class KwivJaar(IntEnum):
    _2022 = 2022
    _2023 = 2023
