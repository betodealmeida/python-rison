from pygments.lexer import RegexLexer
from pygments.token import Keyword, Name, Number, Operator, Punctuation, String, Text


class RisonLexer(RegexLexer):
    name = "Rison"
    aliases = ["rison"]
    filenames = ["*.rison"]
    tokens = {
        "root": [
            (r"\s+", Text),
            (r"!(?:t|f|n)\b", Keyword.Constant),
            (r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", Number),
            (r"'(?:[^'!]|!!|!')*'", String.Single),
            (r"[A-Za-z_][\w.-]*(?=\s*:)", Name.Tag),
            (r"!", Operator),
            (r"[:(),]", Punctuation),
            (r"[A-Za-z_][\w.-]*", String.Double),
        ]
    }


class ORisonLexer(RisonLexer):
    name = "O-Rison"
    aliases = ["orison", "o-rison"]
    filenames = ["*.orison"]


class ARisonLexer(RisonLexer):
    name = "A-Rison"
    aliases = ["arison", "a-rison"]
    filenames = ["*.arison"]
