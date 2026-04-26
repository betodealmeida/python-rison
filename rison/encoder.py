import re
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Literal

from .constants import ID_OK_RE
from .utils import quote

Format = type[str] | type[list[Any]] | type[dict[Any, Any]] | Literal["A", "O"]
EncodeFn = Callable[[Any], str]


class Encoder:

    @staticmethod
    def encoder(v: Any) -> EncodeFn:
        if isinstance(v, (list, tuple)):
            return Encoder.list
        if isinstance(v, str):
            return Encoder.string
        if isinstance(v, bool):
            return Encoder.bool
        if isinstance(v, (float, int)):
            return Encoder.number
        if isinstance(v, type(None)):
            return Encoder.none
        if isinstance(v, dict):
            return Encoder.dict
        raise AssertionError(f"Unable to encode type: {type(v)}")

    @staticmethod
    def encode(v: Any) -> str:
        encoder = Encoder.encoder(v)
        return encoder(v)

    @staticmethod
    def list(x: Sequence[Any]) -> str:
        a: list[str] = ["!("]
        has_values = False
        for value in x:
            encoded = Encoder.encoder(value)(value)
            if has_values:
                a.append(",")
            a.append(encoded)
            has_values = True
        a.append(")")
        return "".join(a)

    @staticmethod
    def number(v: float | int) -> str:
        return str(v).replace("+", "")

    @staticmethod
    def none(_: None) -> str:
        return "!n"

    @staticmethod
    def bool(v: bool) -> str:
        return "!t" if v else "!f"

    @staticmethod
    def string(v: str) -> str:
        if v == "":
            return "''"

        if ID_OK_RE.match(v):
            return v

        def replace(match: re.Match[str]) -> str:
            return "!" + match.group(0)

        v = re.sub(r"([\'!])", replace, v)

        return "'" + v + "'"

    @staticmethod
    def dict(x: Mapping[str, Any]) -> str:
        a: list[str] = ["("]
        has_values = False
        for key in sorted(x.keys()):
            encoded = Encoder.encoder(x[key])(x[key])
            if has_values:
                a.append(",")
            a.append(Encoder.string(key))
            a.append(":")
            a.append(encoded)
            has_values = True

        a.append(")")
        return "".join(a)


def encode_array(v: list[Any]) -> str:
    if not isinstance(v, list):
        raise AssertionError("encode_array expects a list argument")
    return dumps(v, format="A")


def encode_object(v: dict[str, Any]) -> str:
    if not isinstance(v, dict):
        raise AssertionError("encode_object expects an dict argument")
    return dumps(v, format="O")


def encode_uri(v: Any) -> str:
    return quote(dumps(v))


def dumps(value: Any, format: Format = str) -> str:
    encoded = Encoder.encode(value)

    if format in (str,):
        return encoded
    if format in (list, "A"):
        if not isinstance(value, (list, tuple)):
            raise ValueError("A-RISON output format requires a list or tuple input.")
        return encoded[2:-1]
    if format in (dict, "O"):
        if not isinstance(value, dict):
            raise ValueError("O-RISON output format requires a dict input.")
        return encoded[1:-1]

    raise ValueError(
        "Dump format should be one of str, list, dict, 'A' (alias for list), "
        "'O' (alias for dict)."
    )
