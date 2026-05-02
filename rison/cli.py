from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .decoder import Format, ParserException, loads
from .encoder import dumps


def parse_document(document: str, format: str) -> Any:
    cleaned = document.strip()

    if format == "rison":
        return loads(cleaned, format=str)
    if format == "o-rison":
        return loads(cleaned, format="O")
    if format == "a-rison":
        return loads(cleaned, format="A")

    attempts: list[Format] = [str, "O", "A"]
    errors: list[str] = []
    for candidate in attempts:
        try:
            return loads(cleaned, format=candidate)
        except (ParserException, ValueError) as exc:
            errors.append(str(exc))

    raise ParserException("; ".join(errors))


def encode_document(document: str, format: str) -> str:
    value = json.loads(document)

    if format in ("auto", "rison"):
        return dumps(value, format=str)
    if format == "o-rison":
        return dumps(value, format="O")
    return dumps(value, format="A")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rison",
        description="Convert between RISON and JSON.",
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="-",
        help="Input file path (default: stdin).",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["auto", "rison", "o-rison", "a-rison"],
        default="auto",
        help="RISON format (auto, rison, o-rison, a-rison).",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        help="Convert JSON input to RISON output.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.file == "-":
            document = sys.stdin.read()
        else:
            with open(args.file, encoding="utf-8") as handle:
                document = handle.read()

        if args.reverse:
            output = encode_document(document, format=args.format)
        else:
            value = parse_document(document, format=args.format)
            output = json.dumps(value, ensure_ascii=False)
    except (OSError, ParserException, ValueError, json.JSONDecodeError) as exc:
        print(f"rison: error: {exc}", file=sys.stderr)
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
