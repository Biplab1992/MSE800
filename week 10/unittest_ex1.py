import unittest

def add(x, y):
    return x + y

class TestAddFunction(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

if __name__ == '__main__':
    unittest.main()


# The 'unittest' module is used to test a simple 'add' function by building a test case class derived from 'unittest.TestCase'.
# Inside this class, the 'test_add' method uses 'assertEqual' to evaluate several input scenarios and ensure that the 'add' function gives the proper result.
# Running 'unittest.main()' conducts the tests and reports any failures, making it easier to identify flaws early in the development process.