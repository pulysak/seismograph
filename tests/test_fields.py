import unittest
from seismograph.ext.selenium.forms.fields import SimpleFieldInterface, selector, FormField, RadioButton, \
    fill_field_handler, clear_field_handler
import mock


class TestFields(unittest.TestCase):
    def test_selector(self):
        self.assertEqual(selector(k=2), {'k': 2})
        self.assertEqual(selector(k=2, b=3), {'k': 2, 'b': 3})


class TestSimpleFieldInterface(unittest.TestCase):
    def test_weight(self):
        obj = SimpleFieldInterface()
        with self.assertRaises(NotImplementedError):
            obj.weight

    def test_fill(self):
        obj = SimpleFieldInterface()
        with self.assertRaises(NotImplementedError):
            obj.fill()

    def test_clear(self):
        obj = SimpleFieldInterface()
        with self.assertRaises(NotImplementedError):
            obj.clear()


class TestFormField(unittest.TestCase):
    def setUp(self):
        self.test_name = 'test_name'
        self.selector = {'k': 'some_value'}
        self.test_group = mock.MagicMock()
        self.test_weight = 'test_weight'

    def test_constructor(self):
        with self.assertRaises(ValueError):
            obj = FormField(self.test_name)

    def test_constructor_with_dict_selector(self):
        obj = FormField(self.test_name, selector=self.selector)
        self.assertEqual(obj.name, self.test_name)
        self.assertEqual(obj.selector, self.selector)

    def test_group(self):
        obj = FormField(self.test_name, selector=self.selector, group=self.test_group)
        self.assertEqual(obj.group, self.test_group)

    def test_group_without_group(self):
        obj = FormField(self.test_name, selector=self.selector)
        with self.assertRaises(RuntimeError):
            obj.group

    def test_weight(self):
        obj = FormField(self.test_name, selector=self.selector, weight=self.test_weight)
        self.assertEqual(obj.weight, self.test_weight)

    def test_weight_without_value(self):
        obj = FormField(self.test_name, selector=self.selector)
        self.assertEqual(obj.weight, None)

    def test_selector(self):
        obj = FormField(self.test_name, selector=self.selector)
        self.assertEqual(obj.selector, self.selector)

    def test_call(self):
        obj = FormField(self.test_name, selector=self.selector)
        obj(self.test_group)
        self.assertEqual(obj.value, None)
        self.assertEqual(obj.invalid_value, None)

    def test_call_with_value_and_invalid_value(self):
        callable_test_function = mock.Mock(return_value='return_value')
        obj = FormField(self.test_name, selector=self.selector, value=callable_test_function,
                        invalid_value=callable_test_function)
        obj.value()
        self.assertEqual(True, obj.value.called)


if __name__ == '__main__':
    unittest.main()
