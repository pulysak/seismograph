import unittest
from seismograph.ext.selenium.forms.iterators import FieldsIterator, FieldsWithContainsInvalidValueIterator,\
    RequiredFieldsIterator
import mock


class TestFieldsIterator(unittest.TestCase):
    def test_constructor(self):
        test_group = mock.Mock()
        test_group.fields = [1, 2, 3]
        obj = FieldsIterator(test_group)
        self.assertEqual(obj.next(), test_group.fields[0])
        self.assertEqual(obj.next(), test_group.fields[1])
        self.assertEqual(obj.next(), test_group.fields[2])
        with self.assertRaises(StopIteration):
            obj.next()

    def test_constructor_with_exclude(self):
        test_group = mock.Mock()
        test_group.fields = [1, 2, 3]
        obj = FieldsIterator(test_group, (test_group.fields[1],))
        self.assertEqual(obj.next(), test_group.fields[0])
        self.assertEqual(obj.next(), test_group.fields[2])
        with self.assertRaises(StopIteration):
            obj.next()


class TestFieldsWithContainsInvalidValueIterator(unittest.TestCase):
    def setUp(self):
        self.test_group = mock.Mock()
        self.test_obj1 = mock.Mock()
        self.test_obj2 = mock.Mock()
        self.test_obj3 = mock.Mock()
        self.test_group.fields = [self.test_obj1, self.test_obj2, self.test_obj3]
        self.test_obj1.invalid_value = None
        self.test_obj2.invalid_value = True
        self.test_obj3.invalid_value = True

    def test_constructor(self):
        obj = FieldsWithContainsInvalidValueIterator(self.test_group)
        self.assertEqual(obj.next(), self.test_group.fields[1])
        self.assertEqual(obj.next(), self.test_group.fields[2])
        with self.assertRaises(StopIteration):
            obj.next()

    def test_constructor_with_exclude(self):
        obj = FieldsWithContainsInvalidValueIterator(self.test_group, (self.test_group.fields[1],))
        self.assertEqual(obj.next(), self.test_group.fields[2])
        with self.assertRaises(StopIteration):
            obj.next()
            obj.next()


class TestRequiredFieldsIterator(unittest.TestCase):
    def setUp(self):
        self.test_group = mock.Mock()
        self.test_obj1 = mock.Mock()
        self.test_obj2 = mock.Mock()
        self.test_obj3 = mock.Mock()
        self.test_group.fields = [self.test_obj1, self.test_obj2, self.test_obj3]
        self.test_obj1.required = False
        self.test_obj2.required = True
        self.test_obj3.required = True

    def test_constructor(self):
        obj = RequiredFieldsIterator(self.test_group)
        self.assertEqual(obj.next(), self.test_group.fields[1])
        self.assertEqual(obj.next(), self.test_group.fields[2])
        with self.assertRaises(StopIteration):
            obj.next()

    def test_constructor_with_exclude(self):
        obj = RequiredFieldsIterator(self.test_group, (self.test_group.fields[1],))
        self.assertEqual(obj.next(), self.test_group.fields[2])
        with self.assertRaises(StopIteration):
            obj.next()
            obj.next()

if __name__ == '__main__':
    unittest.main()