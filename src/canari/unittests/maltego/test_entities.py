from datetime import date, datetime, timedelta
from canari.maltego.message import Entity, Field, StringEntityField, IntegerEntityField, FloatEntityField, \
    BooleanEntityField, EnumEntityField, LongEntityField, DateTimeEntityField, DateEntityField, TimeSpan, \
    TimeSpanEntityField, RegexEntityField, ColorEntityField, ValidationError
from unittest import TestCase

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'EntityTests'
]


class EntityTests(TestCase):

    def test_basic_uninitialized_entity(self):
        class TestEntity(Entity):
            pass
        self.assertEqual(TestEntity._alias_, TestEntity.__name__)
        self.assertEqual(TestEntity._namespace_, TestEntity.__module__.split('.', 1)[0])
        self.assertEqual(TestEntity._type_, '%s.%s' % (TestEntity._namespace_, TestEntity.__name__))

    def test_basic_uninitialized_entity_with_explicit_namespace(self):
        class TestEntity(Entity):
            _namespace_ = 'foo'
        self.assertEqual(TestEntity._alias_, TestEntity.__name__)
        self.assertEqual(TestEntity._namespace_, 'foo')
        self.assertEqual(TestEntity._type_, '%s.%s' % (TestEntity._namespace_, TestEntity.__name__))

    def test_basic_uninitialized_entity_with_explicit_type(self):
        class TestEntity(Entity):
            _type_ = 'foo'
        self.assertEqual(TestEntity._alias_, TestEntity.__name__)
        self.assertEqual(TestEntity._namespace_, TestEntity.__module__.split('.', 1)[0])
        self.assertEqual(TestEntity._type_, 'foo')

    def test_basic_uninitialized_entity_with_explicit_alias(self):
        class TestEntity(Entity):
            _alias_ = 'foo'
        self.assertEqual(TestEntity._alias_, 'foo')
        self.assertEqual(TestEntity._namespace_, TestEntity.__module__.split('.', 1)[0])
        self.assertEqual(TestEntity._type_, '%s.%s' % (TestEntity._namespace_, TestEntity.__name__))

    def test_basic_entity_with_explicit_string_property_and_value(self):
        class TestEntity(Entity):
            foo = StringEntityField('foo.bar')
        t = TestEntity('value', foo='random value')
        self.assertEqual(t.value, 'value')
        self.assertEqual(t.foo, 'random value')
        t.foo = 1
        self.assertEqual(t.foo, 1)

    def test_basic_entity_with_dynamic_field_and_explicity_field(self):
        class TestEntity(Entity):
            foo = StringEntityField('foo.bar')
        t = TestEntity('value', foo='random value')
        t += Field('foo.bar', 1)
        self.assertEqual(t.foo, 1)

    def test_basic_entity_with_all_static_property_types(self):
        class TestEntity(Entity):
            str = StringEntityField('type.str')
            int = IntegerEntityField('type.int')
            float = FloatEntityField('type.float')
            bool = BooleanEntityField('type.bool')
            enum = EnumEntityField('type.enum', choices=[2, 1, 0])
            date = DateEntityField('type.date')
            datetime = DateTimeEntityField('type.datetime')
            timespan = TimeSpanEntityField('type.timespan')
            color = ColorEntityField('type.color')

        t = TestEntity(
            'value',
            str='str',
            int=1,
            float=1.0,
            bool=True,
            enum=2,
            date=date(1900, 01, 01),
            datetime=datetime(1900, 01, 01),
            timespan=timedelta(days=2, minutes=1, seconds=60),
            color='#ffffff'
        )

        self.assertEqual(t.value, 'value')
        self.assertEqual(t.str, 'str')
        self.assertEqual(t.int, 1)
        self.assertEqual(t.float, 1.0)
        self.assertEqual(t.bool, True)
        self.assertEqual(t.enum, '2')
        self.assertEqual(t.date, date(1900, 01, 01))
        self.assertEqual(t.datetime, datetime(1900, 01, 01))
        self.assertEqual(t.timespan, timedelta(days=2, minutes=1, seconds=60))
        self.assertEqual(t.color, '#ffffff')

        def assign_bad_integer():
            t.int = 'str'
        self.assertRaises(ValidationError, assign_bad_integer)
        self.assertEqual(t.int, 1)

        def assign_bad_float():
            t.float = 'str'
        self.assertRaises(ValidationError, assign_bad_float)
        self.assertEqual(t.float, 1.0)

        def assign_bad_bool():
            t.bool = 'str'
        self.assertRaises(ValidationError, assign_bad_bool)
        self.assertEqual(t.bool, True)

        def assign_bad_enum():
            t.enum = 3
        self.assertRaises(ValidationError, assign_bad_enum)
        self.assertEqual(t.enum, '2')

        def assign_bad_date():
            t.date = '24-01-01'
        self.assertRaises(ValidationError, assign_bad_date)
        self.assertEqual(t.date, date(1900, 01, 01))

        def assign_bad_datetime():
            t.date = '24-01-01'
        self.assertRaises(ValidationError, assign_bad_datetime)
        self.assertEqual(t.datetime, datetime(1900, 01, 01))

        def assign_bad_timespan():
            t.date = '24-01-01'
        self.assertRaises(ValidationError, assign_bad_timespan)
        self.assertEqual(t.timespan, timedelta(days=2, minutes=1, seconds=60))

        def assign_bad_color():
            t.color = '24-01-01'
        self.assertRaises(ValidationError, assign_bad_color)
        self.assertEqual(t.color, '#ffffff')

    def test_property_type_retrieval(self):
        class TestEntity(Entity):
            str = StringEntityField('type.str')
            int = IntegerEntityField('type.int')
            float = FloatEntityField('type.float')
            bool = BooleanEntityField('type.bool')
            enum = EnumEntityField('type.enum', choices=[2, 1, 0])
            date = DateEntityField('type.date')
            datetime = DateTimeEntityField('type.datetime')
            timespan = TimeSpanEntityField('type.timespan')
            color = ColorEntityField('type.color')

        self.assertEqual(TestEntity.str.name, 'type.str')
        self.assertEqual(TestEntity.int.name, 'type.int')
        self.assertEqual(TestEntity.float.name, 'type.float')
        self.assertEqual(TestEntity.bool.name, 'type.bool')
        self.assertEqual(TestEntity.enum.name, 'type.enum')
        self.assertEqual(TestEntity.date.name, 'type.date')
        self.assertEqual(TestEntity.datetime.name, 'type.datetime')
        self.assertEqual(TestEntity.timespan.name, 'type.timespan')
        self.assertEqual(TestEntity.color.name, 'type.color')