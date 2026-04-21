import unittest

try:
    import rison
except ImportError:
    from .context import rison


class TestDecoder(unittest.TestCase):

    def test_dict(self):
        self.assertEqual(rison.loads('()'), {})
        self.assertEqual(rison.loads('(a:0,b:1)'), {
            'a': 0,
            'b': 1
        })
        self.assertEqual(rison.loads("(a:0,b:foo,c:'23skidoo')"), {
            'a': 0,
            'c': '23skidoo',
            'b': 'foo'
        })
        self.assertEqual(rison.loads('(id:!n,type:/common/document)'), {
            'type': '/common/document',
            'id': None
        })
        self.assertEqual(rison.loads("(a:0)"), {
            'a': 0
        })
        self.assertEqual(rison.loads("(a:%)"), {
            'a': '%'
        })
        self.assertEqual(rison.loads("(a:/w+/)"), {
            'a': '/w+/'
        })

    def test_bool(self):
        self.assertEqual(rison.loads('!t'), True)
        self.assertEqual(rison.loads('!f'), False)

    def test_invalid(self):
        self.assertRaisesRegex(rison.decoder.ParserException, r"unmatched '\('", rison.loads, '(')
        self.assertRaisesRegex(rison.decoder.ParserException, r"unmatched '\('", rison.loads, '(a:(')

    def test_none(self):
        self.assertEqual(rison.loads('!n'), None)

    def test_list(self):
        self.assertEqual(rison.loads('!(1,2,3)'), [1, 2, 3])
        self.assertEqual(rison.loads('!()'), [])
        self.assertEqual(rison.loads("!(!t,!f,!n,'')"), [True, False, None, ''])

    def test_number(self):
        self.assertEqual(rison.loads('0'), 0)
        self.assertEqual(rison.loads('1.5'), 1.5)
        self.assertEqual(rison.loads('-3'), -3)
        self.assertEqual(rison.loads('1e30'), 1e+30)
        self.assertEqual(rison.loads('1e-30'), 1.0000000000000001e-30)

    def test_string(self):
        self.assertEqual(rison.loads("''"), '')
        self.assertEqual(rison.loads('G.'), 'G.')
        self.assertEqual(rison.loads('a'), 'a')
        self.assertEqual(rison.loads("'0a'"), '0a')
        self.assertEqual(rison.loads("'abc def'"), 'abc def')
        self.assertEqual(rison.loads("'-h'"), '-h')
        self.assertEqual(rison.loads('a-z'), 'a-z')
        self.assertEqual(rison.loads("'wow!!'"), 'wow!')
        self.assertEqual(rison.loads('domain.com'), 'domain.com')
        self.assertEqual(rison.loads("'user@domain.com'"), 'user@domain.com')
        self.assertEqual(rison.loads("'US $10'"), 'US $10')
        self.assertEqual(rison.loads("'can!'t'"), "can't")

    def test_a_rison_format(self):
        self.assertEqual(rison.loads('1,2,3', format=list), [1, 2, 3])
        self.assertEqual(rison.loads('1,2,3', format='A'), [1, 2, 3])

    def test_o_rison_format(self):
        self.assertEqual(rison.loads('a:1,b:2', format=dict), {'a': 1, 'b': 2})
        self.assertEqual(rison.loads('a:1,b:2', format='O'), {'a': 1, 'b': 2})

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            rison.loads('a', format=int)

    def test_trailing_content(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads('(a:0)b')

    def test_invalid_character(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads(')')

    def test_empty_expression(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads('')

    def test_unmatched_array(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads('!(1,2')

    def test_array_missing_comma(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads('!(1 2)')

    def test_array_extra_comma(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads('!(,1)')

    def test_unknown_bang_literal(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads('!x')

    def test_bang_at_end_of_input(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads('!')

    def test_dict_missing_comma(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads('(a:0 b:1)')

    def test_dict_extra_comma(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads('(,a:0)')

    def test_dict_missing_colon(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads('(a 0)')

    def test_unmatched_single_quote(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads("'abc")

    def test_invalid_string_escape(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads("'a!b'")

    def test_invalid_number(self):
        with self.assertRaises(rison.decoder.ParserException):
            rison.loads('(-)')

    def test_number_with_frac_and_exp(self):
        self.assertEqual(rison.loads('1.5e2'), 150.0)
