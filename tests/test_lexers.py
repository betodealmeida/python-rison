import unittest

from pygments.token import Keyword, Name, Number, Operator, Punctuation, String, Text

from rison.lexers import ARisonLexer, ORisonLexer, RisonLexer


class TestLexers(unittest.TestCase):
    def test_rison_lexer_tokens(self) -> None:
        lexer = RisonLexer()
        tokens = list(lexer.get_tokens("(a:1,b:!t,c:'wow!!')"))

        self.assertIn((Punctuation, '('), tokens)
        self.assertIn((Name.Tag, 'a'), tokens)
        self.assertIn((Number, '1'), tokens)
        self.assertIn((Keyword.Constant, '!t'), tokens)
        self.assertIn((String.Single, "'wow!!'"), tokens)
        self.assertIn((Punctuation, ')'), tokens)

    def test_orison_and_arison_aliases(self) -> None:
        self.assertIn('orison', ORisonLexer.aliases)
        self.assertIn('o-rison', ORisonLexer.aliases)
        self.assertIn('arison', ARisonLexer.aliases)
        self.assertIn('a-rison', ARisonLexer.aliases)
        self.assertEqual(ORisonLexer.name, 'O-Rison')
        self.assertEqual(ARisonLexer.name, 'A-Rison')

    def test_rison_lexer_covers_remaining_rules(self) -> None:
        lexer = RisonLexer()
        tokens = list(lexer.get_tokens("! foo,bar:'x',n:!n"))

        self.assertIn((Operator, '!'), tokens)
        self.assertIn((Text, ' '), tokens)
        self.assertIn((String.Double, 'foo'), tokens)
        self.assertIn((Punctuation, ','), tokens)
