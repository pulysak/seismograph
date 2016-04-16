import unittest

from seismograph.ext.selenium import pageobject

from seismograph.ext.selenium.forms.fields import FormField
from seismograph.ext.selenium.forms.group import make_field, FieldsGroup, GroupContainer, iter_fields, FieldsIterator, \
    iter_required, iter_invalid, GroupMemento
from seismograph.ext.selenium.forms.iterators import RequiredFieldsIterator, FieldsWithContainsInvalidValueIterator

import mock

from seismograph.ext.selenium.query import QueryObject


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
        self.obj[self.test_field] = self.test_dict

    def test_add_field(self):
        self.obj.add_field(self.test_field)
        self.assertEqual(self.obj[self.test_field], self.test_dict)

    def test_get_field(self):

        self.assertEqual(self.obj.get_field(self.test_field), self.test_dict)

    def test_restore(self):
        self.test_field.value = 'test_changed_value'
        self.test_field.required = True
        self.test_field.error_mess = 'test_changed_error_mess'
        self.test_field.invalid_value = True

        self.test_list = [self.test_field, 2]
        self.obj.restore(self.test_list)
        self.restored_test_dict = {
            'value': self.test_field.value,
            'required': self.test_field.required,
            'error_mess': self.test_field.error_mess,
            'invalid_value': self.test_field.invalid_value,
        }

        self.assertEqual(self.restored_test_dict, self.test_dict)


class TestFieldsGroup(unittest.TestCase):
    def setUp(self):
        self.test_proxy = mock.MagicMock()
        self.test_proxy.is_web_element = True
        self.test_proxy.browser = 'some_browser'
        self.test_weight = 'test_weight'
        self.obj = FieldsGroup(self.test_proxy, weight=self.test_weight)

    def test_cache(self):
        self.assertEqual(self.obj.cache, pageobject.PageCache())

    def test_we(self):
        self.assertEqual(self.obj.we, self.test_proxy)
        self.test_proxy.is_web_element = False
        self.assertEqual(self.obj.we, None)

    def test_browser(self):
        self.assertEqual(self.obj.browser, self.test_proxy.browser)

    def test_area_none(self):
        self.assertEqual(self.obj.area, self.test_proxy)

    def test_area_not_query_object(self):
        test_area = mock.Mock()
        self.obj.__area__ = test_area
        with self.assertRaises(TypeError):
            self.obj.area

    def test_area_query_object(self):
        test_area = mock.MagicMock(QueryObject)
        self.obj.__area__ = test_area
        self.obj.area
        self.assertEqual(True, test_area.called)

    def test_weight(self):
        self.assertEqual(self.obj.weight, self.test_weight)

    def test_fill_memo(self):
        self.assertEqual(type(self.obj.fill_memo), set)

    def test_bind_to(self):
        test_proxy = mock.Mock()
        self.obj.bind_to(test_proxy)
        self.assertEqual(self.obj._FieldsGroup__proxy, test_proxy)

    def test_add_field(self):
        test_field = mock.Mock()
        test_field2 = mock.Mock()
        test_field.weight = 1
        test_field2.weight = 2
        self.obj._FieldsGroup__fields.append(test_field)
        self.obj.add_field('test_name', test_field)
        self.assertEqual(self.obj._FieldsGroup__fields[0], test_field)


