# encoding: utf-8

import re
from typing import Any, Literal

from .constants import NEXT_ID_RE, WHITESPACE


Format = type[str] | type[list[Any]] | type[dict[str, Any]] | Literal['A', 'O']


class ParserException(Exception):
    pass


class Parser:

    def __init__(self) -> None:
        self.string: str = ''
        self.index: int = 0

    """
    This parser supports RISON, RISON-A and RISON-O.
    """
    def parse(self, string: str, format: Format = str) -> Any:
        if format in (list, 'A'):
            self.string = f'!({string})'
        elif format in (dict, 'O'):
            self.string = f'({string})'
        elif format is str:
            self.string = string
        else:
            raise ValueError("""Parse format should be one of str, list, dict,
                'A' (alias for list), 'O' (alias for dict).""")

        self.index = 0

        value = self.read_value()
        if self.next():
            raise ParserException(f'unable to parse rison string {string!r}')
        return value

    def read_value(self) -> Any:
        c = self.next()

        if c == '!':
            return self.parse_bang()
        if c == '(':
            return self.parse_open_paren()
        if c == "'":
            return self.parse_single_quote()
        if c is not None and c in '-0123456789':
            return self.parse_number()

        # fell through table, parse as an id
        s = self.string
        i = self.index - 1

        m = NEXT_ID_RE.match(s, i)
        if m:
            _id = m.group(0)
            self.index = i + len(_id)
            return _id

        if c:
            raise ParserException("invalid character: '" + c + "'")
        raise ParserException("empty expression")

    def parse_array(self) -> list[Any]:
        ar: list[Any] = []
        while True:
            c = self.next()
            if c == ')':
                return ar

            if c is None:
                raise ParserException("unmatched '!('")

            if len(ar):
                if c != ',':
                    raise ParserException("missing ','")
            elif c == ',':
                raise ParserException("extra ','")
            else:
                self.index -= 1
            n = self.read_value()
            ar.append(n)

    def parse_bang(self) -> Any:
        s = self.string
        if self.index >= len(s):
            raise ParserException('"!" at end of input')
        c = s[self.index]
        self.index += 1
        if c not in self.bangs:
            raise ParserException('unknown literal: "!' + c + '"')
        x = self.bangs[c]
        if callable(x):
            return x(self)

        return x

    def parse_open_paren(self) -> dict[str, Any]:
        count = 0
        o: dict[str, Any] = {}

        while True:
            c = self.next()
            if c == ')':
                return o
            if count:
                if c != ',':
                    raise ParserException("missing ','")
            elif c == ',':
                raise ParserException("extra ','")
            elif c is None:
                raise ParserException("unmatched '('")
            else:
                self.index -= 1
            k = self.read_value()

            if self.next() != ':':
                raise ParserException("missing ':'")
            v = self.read_value()

            o[k] = v
            count += 1

    def parse_single_quote(self) -> str:
        s = self.string
        i = self.index
        start = i
        segments: list[str] = []

        while True:
            if i >= len(s):
                raise ParserException('unmatched "\'"')

            c = s[i]
            i += 1
            if c == "'":
                break

            if c == '!':
                if start < i - 1:
                    segments.append(s[start : i - 1])
                c = s[i]
                i += 1
                if c in "!'":
                    segments.append(c)
                else:
                    raise ParserException(f'invalid string escape: "!{c}"')

                start = i

        if start < i - 1:
            segments.append(s[start : i - 1])
        self.index = i
        return ''.join(segments)

    # Also any number start (digit or '-')
    def parse_number(self) -> int | float:
        s = self.string
        i = self.index
        start = i - 1
        state = 'int'
        permitted_signs = '-'
        transitions = {
            'int+.': 'frac',
            'int+e': 'exp',
            'frac+e': 'exp'
        }

        while True:
            if i >= len(s):
                i += 1
                break

            c = s[i]
            i += 1

            if '0' <= c <= '9':
                continue

            if permitted_signs.find(c) >= 0:
                permitted_signs = ''
                continue

            state = transitions.get(state + '+' + c.lower(), None)
            if state is None:
                break
            if state == 'exp':
                permitted_signs = '-'

        self.index = i - 1
        s = s[start:self.index]
        if s == '-':
            raise ParserException("invalid number")
        if re.search('[.e]', s):
            return float(s)
        return int(s)

    # return the next non-whitespace character, or undefined
    def next(self) -> str | None:
        s = self.string
        i = self.index

        while True:
            if i == len(s):
                return None
            c = s[i]
            i += 1
            if c not in WHITESPACE:
                break

        self.index = i
        return c

    bangs: dict[str, Any] = {
        't': True,
        'f': False,
        'n': None,
        '(': parse_array
    }


def loads(s: str, format: Format = str) -> Any:
    return Parser().parse(s, format=format)
