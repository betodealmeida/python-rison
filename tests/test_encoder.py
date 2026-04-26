import unittest

try:
    import rison
except ImportError:
    from .context import rison


class TestEncoder(unittest.TestCase):

    def test_dict(self) -> None:
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

    def test_bool(self) -> None:
        self.assertEqual('!t', rison.dumps(True))
        self.assertEqual('!f', rison.dumps(False))

    def test_none(self) -> None:
        self.assertEqual('!n', rison.dumps(None))

    def test_list(self) -> None:
        self.assertEqual('!(1,2,3)', rison.dumps([1, 2, 3]))
        self.assertEqual('!()', rison.dumps([]))
        self.assertEqual("!(!t,!f,!n,'')", rison.dumps([True, False, None, '']))

    def test_number(self) -> None:
        self.assertEqual('0', rison.dumps(0))
        self.assertEqual('1.5', rison.dumps(1.5))
        self.assertEqual('-3', rison.dumps(-3))
        self.assertEqual('1e30', rison.dumps(1e+30))
        self.assertEqual('1e-30', rison.dumps(1.0000000000000001e-30))

    def test_string(self) -> None:
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

    def test_tuple(self) -> None:
        self.assertEqual('!(1,2,3)', rison.dumps((1, 2, 3)))

    def test_unsupported_type(self) -> None:
        with self.assertRaises(AssertionError):
            rison.dumps(object())

    def test_encode_uri(self) -> None:
        from rison.encoder import encode_uri
        self.assertEqual('(a:0)', encode_uri({'a': 0}))

    def test_encode_uri_special_chars(self) -> None:
        from rison.encoder import encode_uri
        result = encode_uri({'a': 'hello world'})
        self.assertIn('+', result)

    def test_encode_array(self) -> None:
        from rison.encoder import encode_array
        with self.assertRaises(AssertionError):
            encode_array('not a list')
        self.assertEqual('1,2,3', encode_array([1, 2, 3]))

    def test_encode_object(self) -> None:
        from rison.encoder import encode_object
        with self.assertRaises(AssertionError):
            encode_object('not a dict')
        self.assertEqual('a:1', encode_object({'a': 1}))

    def test_dumps_a_rison(self) -> None:
        self.assertEqual('1,2,3', rison.dumps([1, 2, 3], format=list))
        self.assertEqual('1,2,3', rison.dumps([1, 2, 3], format='A'))
        self.assertEqual('1,2,3', rison.dumps((1, 2, 3), format='A'))
        with self.assertRaises(ValueError):
            rison.dumps({'a': 1}, format='A')

    def test_dumps_o_rison(self) -> None:
        self.assertEqual('a:1,b:2', rison.dumps({'a': 1, 'b': 2}, format=dict))
        self.assertEqual('a:1,b:2', rison.dumps({'a': 1, 'b': 2}, format='O'))
        with self.assertRaises(ValueError):
            rison.dumps([1, 2], format='O')

    def test_dumps_invalid_format(self) -> None:
        with self.assertRaises(ValueError):
            rison.dumps('x', format='invalid')

    def test_version(self) -> None:
        from rison.__version__ import __version__
        self.assertEqual(__version__, '2.0.0')
