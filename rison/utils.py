import re
from re import Pattern
from urllib.parse import quote as urllib_quote


RE_QUOTE: Pattern[str] = re.compile(r"^[-A-Za-z0-9~!*()_.',:@$/]*$")


def quote(x: str) -> str:
    if RE_QUOTE.match(x):
        return x

    return urllib_quote(x, safe='')\
        .replace('%2C', ',')\
        .replace('%3A', ':')\
        .replace('%40', '@')\
        .replace('%24', '$')\
        .replace('%2F', '/')\
        .replace('%20', '+')
