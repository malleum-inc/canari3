from past.builtins import long
from future.utils import with_metaclass

from collections import Iterable
from datetime import datetime, date, timedelta
from numbers import Number
import re

from six import string_types

from canari.maltego.oxml import MaltegoElement, fields as fields_


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'

__all__ = [
    'MaltegoException',
    'MaltegoTransformExceptionMessage',
    'MaltegoTransformRequestMessage',
    'Label',
    'MatchingRule',
    'Field',
    'UIMessageType',
    'UIMessage',
    'Unknown',
    'MaltegoTransformResponseMessage',
    'MaltegoMessage',
    'StringEntityField',
    'EnumEntityField',
    'IntegerEntityField',
    'BooleanEntityField',
    'FloatEntityField',
    'LongEntityField',
    'DateTimeEntityField',
    'DateEntityField',
    'TimeSpan',
    'TimeSpanEntityField',
    'RegexEntityField',
    'ColorEntityField',
    'ArrayEntityField',
    'Entity',
    'Limits'
]


class MaltegoException(MaltegoElement, Exception):
    """MaltegoException is the default container for exception messages."""
    class meta:
        tagname = 'Exception'

    value = fields_.String(tagname='.')
    code = fields_.Integer(attrname='code', required=False)

    def __init__(self, value=None):
        super(MaltegoElement, self).__init__(value=value)

    def __str__(self):
        return self.value


class MaltegoTransformExceptionMessage(MaltegoElement):
    """
    MaltegoTransformExceptionMessage is the root container for the MaltegoException element.
    """
    exceptions = fields_.List(MaltegoException, tagname='Exceptions')

    def __iadd__(self, exception):
        if isinstance(exception, MaltegoException):
            self.exceptions.append(exception)
        else:
            self.exceptions.append(MaltegoException(str(exception)))
        return self


class Limits(MaltegoElement):
    """
    Limits specifies the soft and hard limits of the MaltegoTransformResponseMessage. The soft and hard limits specify
    the maximum number of entities for response messages.
    """
    soft = fields_.Integer(attrname='SoftLimit', default=500)
    hard = fields_.Integer(attrname='HardLimit', default=10000)


class Label(MaltegoElement):
    """
    Labels are used to convey extra information associated with an Entity in the Maltego user interface. Unlike entity
    fields, labels are only transmitted in response messages and cannot be passed from transform to transform as a
    source of input.
    """
    def __init__(self, name=None, value=None, **kwargs):
        super(Label, self).__init__(name=name, value=value or '', **kwargs)

    value = fields_.CDATA(tagname='.')
    type = fields_.String(attrname='Type', default='text/text')
    name = fields_.String(attrname='Name')


class MatchingRule(object):
    """Matching rules are used to specify how an entity will be merged in the Maltego user interface. Strict matching
    specifies that an entity will only be merged with another if all it's fields (including the value) are equal.
    Loose matching specifies that two entities will be merged if only the entity values are equal."""
    Strict = "strict"
    Loose = "loose"


class Field(MaltegoElement):
    """Fields are additional sources of input that are attached to an entity."""
    def __init__(self, name=None, value=None, **kwargs):
        super(Field, self).__init__(name=name, value=value, **kwargs)

    name = fields_.String(attrname='Name')
    display_name = fields_.String(attrname='DisplayName', required=False)
    matching_rule = fields_.String(attrname='MatchingRule', default=MatchingRule.Strict, required=False)
    value = fields_.String(tagname='.')


class _Entity(MaltegoElement):
    class meta:
        tagname = 'Entity'

    type = fields_.String(attrname='Type')
    fields = fields_.Dict(Field, key='name', tagname='AdditionalFields', required=False)
    labels = fields_.Dict(Label, key='name', tagname='DisplayInformation', required=False)
    value = fields_.String(tagname='Value')
    weight = fields_.Integer(tagname='Weight', default=1)
    icon_url = fields_.String(tagname='IconURL', required=False)

    def __iadd__(self, other):
        if isinstance(other, Field):
            self.fields[other.name] = other
        elif isinstance(other, Label):
            self.labels[other.name] = other
        return self


class UIMessageType:
    Fatal = "FatalError"
    Partial = "PartialError"
    Inform = "Inform"
    Debug = "Debug"


class UIMessage(MaltegoElement):
    def __init__(self, message=None, **kwargs):
        super(UIMessage, self).__init__(message=message, **kwargs)

    type = fields_.String(attrname='MessageType', default=UIMessageType.Inform)
    message = fields_.String(tagname='.')


class MaltegoTransformResponseMessage(MaltegoElement):
    messages = fields_.List(UIMessage, tagname='UIMessages')
    entities = fields_.List(_Entity, tagname='Entities')

    def __iadd__(self, other):
        if isinstance(other, Entity):
            self.entities.append(other.__entity__)
        elif isinstance(other, _Entity):
            self.entities.append(other)
        elif isinstance(other, UIMessage):
            self.messages.append(other)
        return self


class ValidationError(MaltegoException):
    pass


class StringEntityField(object):

    error_msg = ''

    def __init__(self, name, **extras):
        self.name = name
        self.decorator = extras.pop('decorator', None)
        self.is_value = extras.pop('is_value', False)
        self.display_name = extras.pop('display_name', '')
        self.matching_rule = extras.pop('matching_rule', MatchingRule.Strict)
        self.alias = extras.pop('alias', None)
        self.error_msg = extras.pop('error_msg', self.error_msg)

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        if self.is_value:
            return obj.value
        elif self.name in obj.fields:
            return obj.fields[self.name].value
        elif self.alias in obj.fields:
            return obj.fields[self.alias].value
        return None

    def __set__(self, obj, val):
        if self.is_value:
            obj.value = val
        elif not val:
            if self.name in obj.fields:
                del obj.fields[self.name]
            elif self.alias in obj.fields:
                del obj.fields[self.alias]
        else:
            if self.name not in obj.fields and self.alias not in obj.fields:
                obj.fields[self.name] = Field(
                    name=self.name,
                    value=val,
                    display_name=self.display_name,
                    matching_rule=self.matching_rule
                )
            elif self.name in obj.fields:
                obj.fields[self.name].value = val
            else:
                obj.fields[self.alias].value = val
        if callable(self.decorator):
            self.decorator(obj, val)

    def get_error_msg(self, field, value, **extras):
        return self.error_msg.format(field=field, value=value, **extras)


class EnumEntityField(StringEntityField):

    error_msg = 'Invalid value ({value!r}) set for field {field!r}. Expected one of these values: {expected!r}.'

    def __init__(self, name, choices=None, **extras):
        if not choices:
            raise ValueError('You must specify a non-empty set of choices.')
        self.choices = [str(c) if not isinstance(c, string_types) else c for c in choices]
        super(EnumEntityField, self).__init__(name, **extras)

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        c = super(EnumEntityField, self).__get__(obj, objtype)
        if c is not None and not isinstance(c, string_types):
            c = str(c)
        if c and c not in self.choices:
            raise ValidationError(self.get_error_msg(self.display_name or self.name, c, expected=self.choices))
        return c

    def __set__(self, obj, val):
        val = str(val) if not isinstance(val, string_types) else val
        if val not in self.choices:
            raise ValidationError(self.get_error_msg(self.display_name or self.name, val, expected=self.choices))
        super(EnumEntityField, self).__set__(obj, val)


class IntegerEntityField(StringEntityField):

    error_msg = 'The field value ({value!r}) set for field {field!r} is not an integer.'

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        i = super(IntegerEntityField, self).__get__(obj, objtype)
        try:
            return int(i) if i is not None else None
        except ValueError:
            raise ValidationError(self.get_error_msg(self.display_name or self.name, i))

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise ValidationError(self.get_error_msg(self.display_name or self.name, val))
        super(IntegerEntityField, self).__set__(obj, val)


class BooleanEntityField(StringEntityField):

    error_msg = 'The field value ({value!r}) set for field {field!r} is not a boolean.'

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        b = super(BooleanEntityField, self).__get__(obj, objtype)
        return b.startswith('t') or b == '1' if b is not None else None

    def __set__(self, obj, val):
        if not isinstance(val, bool):
            raise ValidationError(self.get_error_msg(self.display_name or self.name, val))
        super(BooleanEntityField, self).__set__(obj, str(val).lower())


class FloatEntityField(StringEntityField):

    error_msg = 'The field value ({value!r}) set for field {field!r} is not a float.'

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        f = super(FloatEntityField, self).__get__(obj, objtype)
        try:
            return float(f) if f is not None else None
        except ValueError:
            raise ValidationError(self.get_error_msg(self.display_name or self.name, f))

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise ValidationError(self.get_error_msg(self.display_name or self.name, val))
        super(FloatEntityField, self).__set__(obj, val)


class LongEntityField(StringEntityField):

    error_msg = 'The field value ({value!r}) set for field {field!r} is not a long integer.'

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        l = super(LongEntityField, self).__get__(obj, objtype)
        try:
            return long(l) if l is not None else None
        except ValueError:
            raise ValidationError(self.get_error_msg(self.display_name or self.name, l))

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise ValidationError(self.get_error_msg(self.display_name or self.name, val))
        super(LongEntityField, self).__set__(obj, val)


class DateTimeEntityField(StringEntityField):

    error_msg = 'The field value ({value!r}) set for field {field!r} is not a valid date time. Date time fields must ' \
                'have the following format: YYYY-MM-DD HH:MM:SS.MS.'

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        d = super(DateTimeEntityField, self).__get__(obj, objtype)
        try:
            return datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f') if d is not None else None
        except ValueError:
            raise ValidationError(self.get_error_msg(self.display_name or self.name, d))

    def __set__(self, obj, val):
        if not isinstance(val, datetime):
            raise ValidationError(self.get_error_msg(self.display_name or self.name, val))
        super(DateTimeEntityField, self).__set__(obj, val.strftime('%Y-%m-%d %H:%M:%S.%f'))


class DateEntityField(StringEntityField):

    error_msg = 'The field value ({value!r}) set for field {field!r} is not a valid date. Date fields must have the ' \
                'following format: YYYY-MM-DD.'

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        d = super(DateEntityField, self).__get__(obj, objtype)
        try:
            return datetime.strptime(d, '%Y-%m-%d').date() if d is not None else None
        except ValueError:
            raise ValidationError(self.get_error_msg(self.display_name or self.name, d))

    def __set__(self, obj, val):
        if not isinstance(val, date):
            raise ValidationError(self.get_error_msg(self.display_name or self.name, val))
        super(DateEntityField, self).__set__(obj, val.strftime('%Y-%m-%d'))


class TimeSpan(timedelta):
    matcher = re.compile('(\d+)d (\d+)h(\d+)m(\d+)\.(\d+)s')

    def __str__(self):
        return '%dd %dh%dm%d.%03ds' % (
            abs(self.days),
            int(self.seconds) // 3600,
            int(self.seconds) % 3600 // 60,
            int(self.seconds) % 60,
            int(self.microseconds)
        )

    @classmethod
    def fromstring(cls, ts):
        m = cls.matcher.match(ts)
        if m is None:
            raise ValueError('Time span must be in "%%dd %%Hh%%Mm%%S.%%fs" format')
        days, hours, minutes, seconds, useconds = [int(i) for i in m.groups()]
        return TimeSpan(days, (hours * 3600) + (minutes * 60) + seconds, useconds)


class TimeSpanEntityField(StringEntityField):

    error_msg = 'The field value ({value!r}) set for field {field!r} is not a valid time span. Time spans must have ' \
                'the following format: DDd HHhMMmSS.MSs.'

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        d = super(TimeSpanEntityField, self).__get__(obj, objtype)
        try:
            return TimeSpan.fromstring(d) if d is not None else None
        except ValueError:
            raise ValidationError(self.get_error_msg(self.display_name or self.name, d))

    def __set__(self, obj, val):
        if not isinstance(val, timedelta):
            raise ValidationError(self.get_error_msg(self.display_name or self.name, val))
        if val.__class__ is timedelta:
            val = TimeSpan(val.days, val.seconds, val.microseconds)
        super(TimeSpanEntityField, self).__set__(obj, str(val))


class RegexEntityField(StringEntityField):

    error_msg = 'The field value ({value!r}) set for field {field!r} does not match the regular expression /{pattern}/.'

    def __init__(self, name, pattern='.*', **extras):
        super(RegexEntityField, self).__init__(name, **extras)
        self.matcher = re.compile(pattern)

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        v = super(RegexEntityField, self).__get__(obj, objtype)
        if v and not self.matcher.match(v):
            raise ValidationError(self.get_error_msg(self.display_name or self.name, v, pattern=self.matcher.pattern))
        return v

    def __set__(self, obj, val):
        if not isinstance(val, string_types):
            val = str(val)
        if not self.matcher.match(val):
            raise ValidationError(self.get_error_msg(self.display_name or self.name, val, pattern=self.matcher.pattern))
        super(RegexEntityField, self).__set__(obj, val)


class ColorEntityField(RegexEntityField):

    error_msg = 'The field value ({value!r}) set for {field!r} is not a valid color (i.e. #000000-#ffffff)'

    def __init__(self, name, **extras):
        super(ColorEntityField, self).__init__(name, pattern='^#[0-9a-fA-F]{6}$', **extras)


class ElementType(object):

    @staticmethod
    def int(value):
        return None if value is None else int(value)

    @staticmethod
    def string(value):
        return None if value is None else str(value).replace('\\,', ',')

    @staticmethod
    def boolean(value):
        return None if value is None else value.startswith('t') or value == '1'

    @staticmethod
    def double(value):
        return None if value is None else float(value)

    @staticmethod
    def float(value):
        return None if value is None else float(value)

    @staticmethod
    def date(value):
        return None if value is None else datetime.strptime(value, '%Y-%m-%d').date()

    @staticmethod
    def matches_type(type_, value):
        return (type_ is ElementType.int and isinstance(value, int)) or \
               (type_ is ElementType.string and isinstance(value, string_types)) or \
               (type_ is ElementType.boolean and isinstance(value, bool)) or \
               ((type_ is ElementType.float or type_ is ElementType.double) and isinstance(value, float)) or \
               (type_ is ElementType.date and isinstance(value, date))


class ArrayEntityField(StringEntityField):

    splitter = re.compile(r'(?<!\\),')

    error_msg = 'The field value ({value!r}) set for {field!r} is not an enumerable type.'
    error_msg_element = 'Could not parse element value ({value!r}) at index {element_pos!r} ' \
                        'as a type of {element_type!r} in field {field!r}.'
    error_msg_array = 'Could not parse input array {value!r} as array of {element_type!r} for field {field!r}.'

    def __init__(self, name, element_type=ElementType.string, **extras):
        super(ArrayEntityField, self).__init__(name, **extras)
        self.element_type = element_type

    def _iter_and_validate(self, val):
        for i, e in enumerate(val):
            if not ElementType.matches_type(self.element_type, e):
                raise ValidationError(self.error_msg_element.format(
                    field=self.display_name or self.name, value=e,
                    element_type=self.element_type.__name__, element_pos=i))
            yield e.replace(',', '\\,') if self.element_type is ElementType.string else str(e)

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        a = super(ArrayEntityField, self).__get__(obj, objtype)
        try:
            return [self.element_type(e) for e in self.splitter.split(a)] if a is not None else None
        except ValueError:
            raise ValidationError(self.error_msg_array.format(
                field=self.display_name or self.name, value=a, element_type=self.element_type.__name__))

    def __set__(self, obj, val):
        if not isinstance(val, Iterable):
            raise ValidationError(self.get_error_msg(self.display_name or self.name, val))
        super(ArrayEntityField, self).__set__(obj, ','.join(self._iter_and_validate(val)))


class EntityTypeFactory(type):
    """The EntityFactory metaclass is responsible for keeping track of and initializing custom entity classes. This is
    required to create entity instances based on the type specifier from the entity XML document."""

    registry = {}

    def __new__(mcs, name, bases, dict_):
        # Just create the class without mangling anything first.
        cls = type.__new__(mcs, name, bases, dict_)

        # We don't need to initialize and register the base Entity class.
        if name == 'Entity':
            return cls

        # This is where we register our custom Entity subclasses.
        # We can register an alias for the entity. This was done to accommodate the difference between V2 and V3
        # entities. This is to support backwards compatibility with older versions of Maltego.
        if '_alias_' not in dict_:
            cls._alias_ = name

        # Create a namespace if it is not explicitly defined. Dynamically created namespaces are based on which module
        # the entity class is defined in.
        if not cls._namespace_:
            # If the entities are coming from the Canari framework then we are going to automatically assign these
            # entities the 'maltego' namespace since they are the Canari definitions of the built-in Maltego entities.
            if cls.__module__ == 'canari.maltego.entities':
                cls._namespace_ = 'maltego'
            # Otherwise, we create the namespace based on the package name
            else:
                cls._namespace_ = cls.__module__.split('.', 1)[0]

        if '_type_' not in dict_:
            cls._type_ = '%s.%s' % (cls._namespace_, name)

        mcs.registry[cls._type_] = cls
        mcs.registry[cls._alias_] = cls

        return cls

    @classmethod
    def create(mcs, entity_type):
        return mcs.registry.get(entity_type)


class Bookmark:
    NoColor = -1
    Cyan = 0
    Green = 1
    Yellow = 2
    Orange = 3
    Red = 4


class LinkStyle:
    Normal = 0
    Dashed = 1
    Dotted = 2
    DashDot = 3


class LinkLabel:
    UseGlobalSetting = 0
    Show = 1
    Hide = 2


class LinkColor:
    Black = '#000000'
    DarkGray = '#7F7F7F'
    LightGray = '#C3C3C3'
    Red = '#F4291A'
    Orange = '#FF810F'
    DarkGreen = '#30AF44'
    NavyBlue = '#00A2EB'
    Magenta = '##A14DA7'
    Cyan = '#99D9EB'
    Lime = '#B9E500'
    Yellow = '#FFE100'
    Pink = '#FEAFCA'


class Entity(with_metaclass(EntityTypeFactory, object)):

    _namespace_ = None
    _alias_ = None
    _type_ = None
    _category_ = None

    notes = StringEntityField('notes#', display_name='Notes', matching_rule=MatchingRule.Loose)
    bookmark = IntegerEntityField('bookmark#', display_name='Bookmark', choices=range(-1, 5),
                                  matchingrule=MatchingRule.Loose)
    link_label = StringEntityField('link#maltego.link.label', display_name='Link Label',
                                   matching_rule=MatchingRule.Loose)
    link_style = EnumEntityField('link#maltego.link.style', display_name='Link Style',
                                 choices=range(4), matching_rule=MatchingRule.Loose)
    link_thickness = EnumEntityField('link#maltego.link.thickness', display_name='Link Thickness',
                                     choices=range(6), matching_rule=MatchingRule.Loose)
    link_show_label = EnumEntityField('link#maltego.link.show-label', display_name='Link Show Label', choices=range(3),
                                      matching_rule=MatchingRule.Loose)
    link_color = EnumEntityField('link#maltego.link.color', display_name= 'Link Color',
                                 choices=[LinkColor.Black, LinkColor.DarkGray, LinkColor.LightGray, LinkColor.Red,
                                          LinkColor.Orange, LinkColor.DarkGreen, LinkColor.NavyBlue, LinkColor.Magenta,
                                          LinkColor.Cyan, LinkColor.Lime, LinkColor.Yellow, LinkColor.Pink],
                                 matching_rule=MatchingRule.Loose)

    def __init__(self, value='', **kwargs):
        if isinstance(value, _Entity):
            self._entity = value
        else:
            self._entity = _Entity(
                type=kwargs.pop('type', self._type_),
                value=value,
                weight=kwargs.pop('weight', None),
                icon_url=kwargs.pop('icon_url', None),
                fields=self._list_to_dict(kwargs.pop('fields', None)),
                labels=self._list_to_dict(kwargs.pop('labels', None))
            )
        for p in kwargs:
            if hasattr(self, p):
                setattr(self, p, kwargs[p])

    def _list_to_dict(self, obj):
        if not obj:
            return
        if isinstance(obj, dict):
            return obj
        return dict([(i.name, i) for i in obj])

    @property
    def __entity__(self):
        return self._entity

    @property
    def __type__(self):
        return self._type_

    @property
    def fields(self):
        return self._entity.fields

    @property
    def labels(self):
        return self._entity.labels

    @property
    def type(self):
        return self._entity.type

    @type.setter
    def type(self, t):
        self._entity.type = t

    @property
    def value(self):
        return self._entity.value

    @value.setter
    def value(self, v):
        self._entity.value = v

    @property
    def weight(self):
        return self._entity.weight

    @weight.setter
    def weight(self, w):
        self._entity.weight = w

    @property
    def icon_url(self):
        return self._entity.icon_url

    @icon_url.setter
    def icon_url(self, url):
        self._entity.icon_url = url

    def __iadd__(self, other):
        self._entity += other
        return self

    __add__ = __iadd__

    def __getitem__(self, item):
        return self._entity.fields[item].value

    def __setitem__(self, key, value):
        if key not in self._entity.fields:
            self._entity.fields[key] = Field(key, value)
        else:
            self._entity.fields[key].value = value


class Unknown(Entity):
    _category_ = 'Unknown'


class MaltegoTransformRequestMessage(MaltegoElement):

    __entities = fields_.List(_Entity, tagname='Entities', required=False)
    _entities = None  # This is so we can cache the transform entity object list.
    _parameters = fields_.Dict(Field, tagname='TransformFields', key='name', required=False)
    limits = fields_.Model(Limits, required=False)

    def __iadd__(self, other):
        if isinstance(other, Entity):
            self.__entities.append(other.__entity__)
        elif isinstance(other, _Entity):
            self.__entities.append(other)
        elif isinstance(other, Field):
            self._parameters[other.name] = other
        elif isinstance(other, Limits):
            self.limits = other
        return self

    @property
    def entity(self):
        """Returns the first Entity object in the transform request.

        :return: first Entity object."""
        if self.entities:
            return self.entities[0]
        return Entity('')

    @property
    def entities(self):
        if not self._entities:
            self._entities = [(EntityTypeFactory.create(e.type) or Unknown)(e) for e in self.__entities]
        return self._entities

    @property
    def parameters(self):
        """Returns a list of passed transform parameters in the event that a transform has additional parameters that
        are required in order to operate (i.e. API key). For local transforms, the program arguments are returned
        instead.

        :return: list of parameters."""
        if 'canari.local.arguments' in self._parameters:
            return self._parameters['canari.local.arguments'].value
        return self._parameters

    @property
    def settings(self):
        return {k: v.value for k, v in self._parameters.items()}


class MaltegoMessage(MaltegoElement):
    """This is the root element for all Maltego request, response, and exception messages that are exchanged between the
    client and the transform server. In the case of local transforms, only response and exception messages are exchanged
    from transform to client."""
    message = fields_.Choice(
        fields_.Model(MaltegoTransformExceptionMessage),
        fields_.Model(MaltegoTransformResponseMessage),
        fields_.Model(MaltegoTransformRequestMessage)
    )
