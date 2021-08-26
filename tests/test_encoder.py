import unittest

try:
    import prison
except ImportError:
    from .context import prison


class TestEncoder(unittest.TestCase):

    def test_dict(self):
        self.assertEqual('()', prison.dumps({}))
        self.assertEqual('(a:0,b:1)', prison.dumps({
            'a': 0,
            'b': 1
        }))
        self.assertEqual("(a:0,b:foo,c:'23skidoo')", prison.dumps({
            'a': 0,
            'c': '23skidoo',
            'b': 'foo'
        }))
        self.assertEqual('(id:!n,type:/common/document)', prison.dumps({
            'type': '/common/document',
            'id': None
        }))
        self.assertEqual("(a:0)", prison.dumps({
            'a': 0
        }))
        self.assertEqual("(a:%)", prison.dumps({
            'a': '%'
        }))

    def test_bool(self):
        self.assertEqual('!t', prison.dumps(True))
        self.assertEqual('!f', prison.dumps(False))

    def test_none(self):
        self.assertEqual('!n', prison.dumps(None))

    def test_list(self):
        self.assertEqual('!(1,2,3)', prison.dumps([1, 2, 3]))
        self.assertEqual('!()', prison.dumps([]))
        self.assertEqual("!(!t,!f,!n,'')", prison.dumps([True, False, None, '']))

    def test_number(self):
        self.assertEqual('0', prison.dumps(0))
        self.assertEqual('1.5', prison.dumps(1.5))
        self.assertEqual('-3', prison.dumps(-3))
        self.assertEqual('1e30', prison.dumps(1e+30))
        self.assertEqual('1e-30', prison.dumps(1.0000000000000001e-30))

    def test_string(self):
        self.assertEqual("''", prison.dumps(''))
        self.assertEqual('G.', prison.dumps('G.'))
        self.assertEqual('a', prison.dumps('a'))
        self.assertEqual("'0a'", prison.dumps('0a'))
        self.assertEqual("'abc def'", prison.dumps('abc def'))
        self.assertEqual("'-h'", prison.dumps('-h'))
        self.assertEqual('a-z', prison.dumps('a-z'))
        self.assertEqual("'wow!!'", prison.dumps('wow!'))
        self.assertEqual('domain.com', prison.dumps('domain.com'))
        self.assertEqual("'user@domain.com'", prison.dumps('user@domain.com'))
        self.assertEqual("'US $10'", prison.dumps('US $10'))
        self.assertEqual("'can!'t'", prison.dumps("can't"))
