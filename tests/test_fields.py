import unittest

from selenium.common.exceptions import NoSuchElementException

from seismograph.ext.selenium.exceptions import FieldError
from seismograph.ext.selenium.forms.fields import SimpleFieldInterface, selector, FormField, RadioButton, \
    fill_field_handler, clear_field_handler, Checkbox, Select
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

    def test_get_attr(self):
        with mock.patch.object(FormField, 'we') as mock_we:
            test_obj = mock.Mock()
            test_obj.test_attr = 'test_value'
            mock_we.__get__ = mock.Mock(return_value=test_obj)
            obj = FormField(self.test_name, selector=self.selector)
            self.assertEqual(obj.__getattr__('test_attr'), 'test_value')

    def test_css(self):
        with mock.patch.object(FormField, 'we') as mock_we:
            test_obj = mock.Mock()
            test_obj.css = 'test_value'
            mock_we.__get__ = mock.Mock(return_value=test_obj)
            obj = FormField(self.test_name, selector=self.selector)
            self.assertEqual(obj.css, 'test_value')

    def test_attr(self):
        with mock.patch.object(FormField, 'we') as mock_we:
            test_obj = mock.Mock()
            test_obj.attr = 'test_value'
            mock_we.__get__ = mock.Mock(return_value=test_obj)
            obj = FormField(self.test_name, selector=self.selector)
            self.assertEqual(obj.attr, 'test_value')

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
        self.assertIsNone(obj.weight)

    def test_selector(self):
        obj = FormField(self.test_name, selector=self.selector)
        self.assertEqual(obj.selector, self.selector)

    def test_call(self):
        obj = FormField(self.test_name, selector=self.selector)
        obj(self.test_group)
        self.assertIsNone(obj.value)
        self.assertIsNone(obj.invalid_value)

    def test_call_with_value_and_invalid_value(self):
        callable_test_function = mock.Mock(return_value='return_value')
        obj = FormField(self.test_name, selector=self.selector, value=callable_test_function,
                        invalid_value=callable_test_function)
        obj.value()
        self.assertTrue(obj.value.called)

    def test_fill_field_handler_value_none(self):
        f = mock.MagicMock()
        fake_arg = mock.MagicMock()
        fake_arg.value = None
        f.__name__ = 'test_function'
        f = fill_field_handler(f)
        self.assertIsNone(f(fake_arg))

    def test_fill_field_handler_with_value(self):
        f = mock.MagicMock()
        fake_arg = mock.MagicMock()
        fake_arg.value = 'some_value'
        f.__name__ = 'test_function'
        f = fill_field_handler(f)
        f(fake_arg)
        self.assertTrue(fake_arg.before_fill_trigger.called)
        self.assertTrue(fake_arg.after_fill_trigger.called)

    def test_clear_field_handler(self):
        f = mock.MagicMock()
        f.__name__ = 'test_function'
        fake_arg = mock.MagicMock()
        f = clear_field_handler(f)
        f(fake_arg)
        self.assertTrue(fake_arg.group.fill_memo.remove.called)


class TestCheckbox(unittest.TestCase):
    def setUp(self):
        self.test_name = 'test_name'
        self.test_selector = dict()
        self.test_group = mock.MagicMock()
        self.test_group.__allow_raises__ = True

    def test_fill_value(self):
        with mock.patch.object(Checkbox, 'we') as mock_we:
            mock_we.__get__ = mock.Mock(return_value=mock.MagicMock())
            obj = Checkbox(self.test_name, selector=self.test_selector, group=self.test_group)
            obj.value = 'test_value'
            with self.assertRaises(FieldError):
                obj.fill()

    def test_fill_value_none(self):
        with mock.patch.object(Checkbox, 'we') as mock_we:
            mock_obj = mock.MagicMock()
            mock_obj.is_selected = mock.MagicMock(return_value=False)
            mock_we.__get__ = mock.Mock(return_value=mock_obj)
            obj = Checkbox(self.test_name, selector=self.test_selector, group=self.test_group)
            obj.value = ''
            with self.assertRaises(FieldError):
                obj.fill(value=None)

    def test_fill_value_click(self):
        with mock.patch.object(Checkbox, 'we') as mock_we:
            mock_obj = mock.MagicMock()
            mock_obj.is_selected = mock.MagicMock(return_value=False)
            mock_obj.click = mock.Mock()
            mock_we.__get__ = mock.Mock(return_value=mock_obj)
            obj = Checkbox(self.test_name, selector=self.test_selector, group=self.test_group)
            obj.value = 'test_value'
            obj.fill()
            self.assertTrue(mock_obj.click.called)

    def test_clear(self):
        with mock.patch.object(Checkbox, 'we') as mock_we:
            mock_obj = mock.MagicMock()
            mock_obj.is_selected = mock.MagicMock(return_value=True)
            mock_obj.click = mock.Mock()
            mock_we.__get__ = mock.Mock(return_value=mock_obj)
            obj = Checkbox(self.test_name, selector=self.test_selector, group=self.test_group)
            obj.clear()
            self.assertTrue(mock_obj.click.called)

    def test_not_clear(self):
        with mock.patch.object(Checkbox, 'we') as mock_we:
            mock_obj = mock.MagicMock()
            mock_obj.is_selected = mock.MagicMock(return_value=False)
            mock_obj.click = mock.Mock()
            mock_we.__get__ = mock.Mock(return_value=mock_obj)
            obj = Checkbox(self.test_name, selector=self.test_selector, group=self.test_group)
            obj.clear()
            self.assertFalse(mock_obj.click.called)


class TestRadioButton(unittest.TestCase):
    def setUp(self):
        self.test_name = 'test_name'
        self.test_selector = dict()
        self.test_group = mock.MagicMock()

    def test_not_fill(self):
        obj = RadioButton(self.test_name, selector=self.test_selector, group=self.test_group)
        obj.value = None
        self.assertFalse(obj.fill(value=''))

    def test_fill_not_changed(self):
        with mock.patch.object(Checkbox, 'we') as mock_we:
            mock_obj = mock.MagicMock()
            mock_obj.is_selected = mock.MagicMock(return_value=True)
            mock_we.__get__ = mock.Mock(return_value=mock_obj)
            obj = RadioButton(self.test_name, selector=self.test_selector, group=self.test_group)
            obj.fill(value='test_value')
            self.assertFalse(obj.fill(value=''))

    def test_fill_changed(self):
        with mock.patch.object(Checkbox, 'we') as mock_we:
            mock_obj = mock.MagicMock()
            mock_obj.is_selected = mock.MagicMock(return_value=False)
            mock_we.__get__ = mock.Mock(return_value=mock_obj)
            obj = RadioButton(self.test_name, selector=self.test_selector, group=self.test_group)
            obj.fill(value='test_value')
            self.assertFalse(obj.fill(value=''))


class TestSelect(unittest.TestCase):
    def setUp(self):
        self.test_name = 'test_name'
        self.selector = dict()
        self.test_group = mock.MagicMock()
        self.test_group = mock.MagicMock()

    def test_fill_false(self):
        with mock.patch.object(Select, 'we', autospec=True) as mock_we:
            mock_obj_get_by = mock.Mock()
            mock_obj_get_by.get_by = mock.Mock(return_value=False)
            mock_obj_all = mock.Mock()
            mock_obj_all.all = mock.Mock(return_value=mock_obj_get_by)
            mock_obj = mock.Mock()
            mock_obj.option = mock.Mock(return_value=mock_obj_all)
            mock_we.__get__ = mock.Mock(return_value=mock_obj)
            obj = Select(self.test_name, selector=self.selector, group=self.test_group)
            with self.assertRaises(NoSuchElementException):
                obj.fill(value='test_value')

    def test_fill(self):
        with mock.patch.object(Select, 'we', autospec=True) as mock_we:
            final_mock = mock.Mock()
            mock_obj_get_by = mock.Mock()
            mock_obj_get_by.get_by = mock.Mock(return_value=final_mock)
            mock_obj_all = mock.Mock()
            mock_obj_all.all = mock.Mock(return_value=mock_obj_get_by)
            mock_obj = mock.Mock()
            mock_obj.option = mock.Mock(return_value=mock_obj_all)
            mock_we.__get__ = mock.Mock(return_value=mock_obj)
            obj = Select(self.test_name, selector=self.selector, group=self.test_group)
            obj.fill(value='test_value')
            self.assertTrue(final_mock.click.called)

if __name__ == '__main__':
    unittest.main()
