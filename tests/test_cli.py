import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from rison.cli import encode_document, main, parse_document


class TestCLI(unittest.TestCase):
    def test_parse_document_auto_rison(self) -> None:
        value = parse_document("(a:1,b:!(2,3))", format="auto")
        self.assertEqual(value, {"a": 1, "b": [2, 3]})

    def test_parse_document_orison(self) -> None:
        value = parse_document("a:1,b:2", format="o-rison")
        self.assertEqual(value, {"a": 1, "b": 2})

    def test_encode_document_default(self) -> None:
        value = encode_document('{"a":1,"b":[2,3]}', format="auto")
        self.assertEqual(value, "(a:1,b:!(2,3))")

    def test_encode_document_orison(self) -> None:
        value = encode_document('{"a":1,"b":2}', format="o-rison")
        self.assertEqual(value, "a:1,b:2")

    def test_main_from_stdin(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch("sys.stdin", io.StringIO("(b:2,a:1)")),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            code = main([])

        self.assertEqual(code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(
            stdout.getvalue(),
            json.dumps({"b": 2, "a": 1}, ensure_ascii=False) + "\n",
        )

    def test_main_from_file(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=True) as handle:
            handle.write("a:1,b:2")
            handle.flush()

            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(["--format", "o-rison", handle.name])

        self.assertEqual(code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(
            stdout.getvalue(),
            json.dumps({"a": 1, "b": 2}, ensure_ascii=False) + "\n",
        )

    def test_main_invalid_document(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch("sys.stdin", io.StringIO("(")),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            code = main([])

        self.assertEqual(code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("rison: error:", stderr.getvalue())

    def test_main_reverse_from_stdin(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch("sys.stdin", io.StringIO('{"b":2,"a":1}')),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            code = main(["--reverse"])

        self.assertEqual(code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(stdout.getvalue(), "(a:1,b:2)\n")

    def test_main_reverse_invalid_json(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch("sys.stdin", io.StringIO("{")),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            code = main(["--reverse"])

        self.assertEqual(code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("rison: error:", stderr.getvalue())
