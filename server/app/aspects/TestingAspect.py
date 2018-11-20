import aspectlib
import unittest

class MyTestCase(unittest.TestCase):

    def test_stuff(self):

        @aspectlib.Aspect
        def mock_stuff(self, value):
            if value == 'cnp':
                yield aspectlib.Return('mocked-hash-result')
            else:
                yield aspectlib.Proceed