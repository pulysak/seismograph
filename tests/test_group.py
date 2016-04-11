import unittest

from seismograph.ext.selenium.forms.fields import FormField
from seismograph.ext.selenium.forms.group import make_field, FieldsGroup, GroupContainer, iter_fields, FieldsIterator, \
    iter_required, iter_invalid, GroupMemento
from seismograph.ext.selenium.forms.iterators import RequiredFieldsIterator, FieldsWithContainsInvalidValueIterator

import mock


class TestGroup(unittest.TestCase):
    def test_make_field(self):
        obj = mock.Mock()
        with self.assertRaises(ValueError):
            make_field(type(obj))

    def test_make_field_subclass(self):
        test_proxy = mock.MagicMock()
        obj = FieldsGroup(test_proxy)
        self.assertEqual(type(make_field(FieldsGroup)), type(GroupContainer(FieldsGroup, None, None)))

    def test_iter_fields(self):
        test_proxy = mock.MagicMock()
        obj = FieldsGroup(test_proxy)
        self.assertEqual(type(iter_fields(obj)), type(FieldsIterator(obj)))

    def test_iter_required(self):
        test_proxy = mock.MagicMock()
        obj = FieldsGroup(test_proxy)
        self.assertEqual(type(iter_required(obj)), type(RequiredFieldsIterator(obj)))

    def test_iter_invalid(self):
        test_proxy = mock.MagicMock()
        obj = FieldsGroup(test_proxy)
        self.assertEqual(type(iter_invalid(obj)), type(FieldsWithContainsInvalidValueIterator(obj)))


class TestGroupContainer(unittest.TestCase):
    def setUp(self):
        self.test_name = 'test_name'
        self.test_weight = 'test_weight'
        self.test_group = mock.MagicMock()

    def test_name(self):
        obj = GroupContainer(self.test_group, self.test_weight, self.test_name)
        self.assertEqual(obj.name, self.test_name)


class TestGroupMemento(unittest.TestCase):
    def setUp(self):
        self.test_field = mock.MagicMock(FormField)
        self.test_field.value = 'test_value'
        self.test_field.required = True
        self.test_field.error_mess = 'test_error_mess'
        self.test_field.invalid_value = True
        self.test_dict = {
            'value': self.test_field.value,
            'required': self.test_field.required,
            'error_mess': self.test_field.error_mess,
            'invalid_value': self.test_field.invalid_value,
        }
        self.obj = GroupMemento()

    def test_add_field(self):
        self.obj.add_field(self.test_field)
        self.assertEqual(self.obj[self.test_field], self.test_dict)

    def test_get_field(self):
        self.obj[self.test_field] = self.test_dict
        self.assertEqual(self.obj.get_field(self.test_field), self.test_dict)




