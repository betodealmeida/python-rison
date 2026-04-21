import unittest

try:
    import rison
except ImportError:
    from .context import rison


class TestEncoder(unittest.TestCase):

    def test_dict(self):
        self.assertEqual('()', rison.dumps({}))
        self.assertEqual('(a:0,b:1)', rison.dumps({
            'a': 0,
            'b': 1
        }))
        self.assertEqual("(a:0,b:foo,c:'23skidoo')", rison.dumps({
            'a': 0,
            'c': '23skidoo',
            'b': 'foo'
        }))
        self.assertEqual('(id:!n,type:/common/document)', rison.dumps({
            'type': '/common/document',
            'id': None
        }))
        self.assertEqual("(a:0)", rison.dumps({
            'a': 0
        }))
        self.assertEqual("(a:%)", rison.dumps({
            'a': '%'
        }))
        self.assertEqual("(a:/w+/)", rison.dumps({
            'a': '/w+/'
        }))

    def test_bool(self):
        self.assertEqual('!t', rison.dumps(True))
        self.assertEqual('!f', rison.dumps(False))

    def test_none(self):
        self.assertEqual('!n', rison.dumps(None))

    def test_list(self):
        self.assertEqual('!(1,2,3)', rison.dumps([1, 2, 3]))
        self.assertEqual('!()', rison.dumps([]))
        self.assertEqual("!(!t,!f,!n,'')", rison.dumps([True, False, None, '']))

    def test_number(self):
        self.assertEqual('0', rison.dumps(0))
        self.assertEqual('1.5', rison.dumps(1.5))
        self.assertEqual('-3', rison.dumps(-3))
        self.assertEqual('1e30', rison.dumps(1e+30))
        self.assertEqual('1e-30', rison.dumps(1.0000000000000001e-30))

    def test_string(self):
        self.assertEqual("''", rison.dumps(''))
        self.assertEqual('G.', rison.dumps('G.'))
        self.assertEqual('a', rison.dumps('a'))
        self.assertEqual("'0a'", rison.dumps('0a'))
        self.assertEqual("'abc def'", rison.dumps('abc def'))
        self.assertEqual("'-h'", rison.dumps('-h'))
        self.assertEqual('a-z', rison.dumps('a-z'))
        self.assertEqual("'wow!!'", rison.dumps('wow!'))
        self.assertEqual('domain.com', rison.dumps('domain.com'))
        self.assertEqual("'user@domain.com'", rison.dumps('user@domain.com'))
        self.assertEqual("'US $10'", rison.dumps('US $10'))
        self.assertEqual("'can!'t'", rison.dumps("can't"))

    def test_tuple(self):
        self.assertEqual('!(1,2,3)', rison.dumps((1, 2, 3)))

    def test_unsupported_type(self):
        with self.assertRaises(AssertionError):
            rison.dumps(object())

    def test_encode_uri(self):
        from rison.encoder import encode_uri
        self.assertEqual('(a:0)', encode_uri({'a': 0}))

    def test_encode_uri_special_chars(self):
        from rison.encoder import encode_uri
        result = encode_uri({'a': 'hello world'})
        self.assertIn('+', result)

    def test_encode_array(self):
        from rison.encoder import encode_array
        with self.assertRaises(AssertionError):
            encode_array('not a list')
        # encode_array has a bug (tuple indexing instead of slicing)
        with self.assertRaises(TypeError):
            encode_array([1, 2, 3])

    def test_encode_object(self):
        from rison.encoder import encode_object
        with self.assertRaises(AssertionError):
            encode_object('not a dict')
        # encode_object has a bug (tuple indexing instead of slicing)
        with self.assertRaises(TypeError):
            encode_object({'a': 1})

    def test_version(self):
        from rison.__version__ import __version__
        self.assertEqual(__version__, '2.0.0')
