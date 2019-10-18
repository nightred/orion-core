
from .context import orion_core
import unittest


class BasicTestSuite(unittest.TestCase):
    """ Basic unit tests cases """

    def test_absolute_truth(self):
        return True


if __name__ == '__main__':
    unittest.main()
