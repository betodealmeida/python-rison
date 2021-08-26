import unittest

try:
    import prison
except ImportError:
    from .context import prison


class TestDecoder(unittest.TestCase):

    def test_dict(self):
        self.assertEqual(prison.loads('()'), {})
        self.assertEqual(prison.loads('(a:0,b:1)'), {
            'a': 0,
            'b': 1
        })
        self.assertEqual(prison.loads("(a:0,b:foo,c:'23skidoo')"), {
            'a': 0,
            'c': '23skidoo',
            'b': 'foo'
        })
        self.assertEqual(prison.loads('(id:!n,type:/common/document)'), {
            'type': '/common/document',
            'id': None
        })
        self.assertEqual(prison.loads("(a:0)"), {
            'a': 0
        })
        self.assertEqual(prison.loads("(a:%)"), {
            'a': '%'
        })
        self.assertEqual(prison.loads("(a:/w+/)"), {
            'a': '/w+/'
        })

    def test_bool(self):
        self.assertEqual(prison.loads('!t'), True)
        self.assertEqual(prison.loads('!f'), False)

    def test_invalid(self):
        with self.assertRaises(prison.decoder.ParserException):
            prison.loads('(')

    def test_none(self):
        self.assertEqual(prison.loads('!n'), None)

    def test_list(self):
        self.assertEqual(prison.loads('!(1,2,3)'), [1, 2, 3])
        self.assertEqual(prison.loads('!()'), [])
        self.assertEqual(prison.loads("!(!t,!f,!n,'')"), [True, False, None, ''])

    def test_number(self):
        self.assertEqual(prison.loads('0'), 0)
        self.assertEqual(prison.loads('1.5'), 1.5)
        self.assertEqual(prison.loads('-3'), -3)
        self.assertEqual(prison.loads('1e30'), 1e+30)
        self.assertEqual(prison.loads('1e-30'), 1.0000000000000001e-30)

    def test_string(self):
        self.assertEqual(prison.loads("''"), '')
        self.assertEqual(prison.loads('G.'), 'G.')
        self.assertEqual(prison.loads('a'), 'a')
        self.assertEqual(prison.loads("'0a'"), '0a')
        self.assertEqual(prison.loads("'abc def'"), 'abc def')
        self.assertEqual(prison.loads("'-h'"), '-h')
        self.assertEqual(prison.loads('a-z'), 'a-z')
        self.assertEqual(prison.loads("'wow!!'"), 'wow!')
        self.assertEqual(prison.loads('domain.com'), 'domain.com')
        self.assertEqual(prison.loads("'user@domain.com'"), 'user@domain.com')
        self.assertEqual(prison.loads("'US $10'"), 'US $10')
        self.assertEqual(prison.loads("'can!'t'"), "can't")
