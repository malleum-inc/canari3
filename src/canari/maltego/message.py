from datetime import datetime, date, timedelta
from numbers import Number
import re

from canari.maltego.xml import MaltegoElement, fields as fields_


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
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
    'timespan',
    'TimeSpanEntityField',
    'RegexEntityField',
    'ColorEntityField',
    'Entity'
]


class MaltegoException(MaltegoElement, Exception):
    """MaltegoException is the default container for exception messages."""
    class meta:
        tagname = 'Exception'

    def __init__(self, value):
        super(MaltegoElement, self).__init__(value=value)

    value = fields_.String(tagname='.')


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
        super(Label, self).__init__(name=name, value=value, **kwargs)

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
    displayname = fields_.String(attrname='DisplayName', required=False)
    matchingrule = fields_.String(attrname='MatchingRule', default=MatchingRule.Strict, required=False)
    value = fields_.String(tagname='.')


class _Entity(MaltegoElement):
    class meta:
        tagname = 'Entity'

    type = fields_.String(attrname='Type')
    fields = fields_.Dict(Field, key='name', tagname='AdditionalFields', required=False)
    labels = fields_.Dict(Label, key='name', tagname='DisplayInformation', required=False)
    value = fields_.String(tagname='Value')
    weight = fields_.Integer(tagname='Weight', default=1)
    iconurl = fields_.String(tagname='IconURL', required=False)

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
    def __init__(self, value=None, **kwargs):
        super(UIMessage, self).__init__(value=value, **kwargs)

    type = fields_.String(attrname='MessageType', default=UIMessageType.Inform)
    value = fields_.String(tagname='.')


class MaltegoTransformResponseMessage(MaltegoElement):
    uimessages = fields_.List(UIMessage, tagname='UIMessages')
    entities = fields_.List(_Entity, tagname='Entities')

    def __iadd__(self, other):
        if isinstance(other, Entity):
            self.entities.append(other.__entity__)
        elif isinstance(other, _Entity):
            self.entities.append(other)
        elif isinstance(other, UIMessage):
            self.uimessages.append(other)
        return self


class StringEntityField(object):
    def __init__(self, name, displayname=None, decorator=None, matchingrule=MatchingRule.Strict, is_value=False,
                 alias=None, **extras):
        self.decorator = decorator
        self.is_value = is_value
        self.name = name
        self.displayname = displayname
        self.matchingrule = matchingrule
        self.alias = alias

    def __get__(self, obj, objtype):
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
                    displayname=self.displayname,
                    matchingrule=self.matchingrule
                )
            elif self.name in obj.fields:
                obj.fields[self.name].value = val
            else:
                obj.fields[self.alias].value = val
        if callable(self.decorator):
            self.decorator(obj, val)


class EnumEntityField(StringEntityField):
    def __init__(self, name, displayname=None, choices=None, decorator=None, matchingrule=MatchingRule.Strict,
                 is_value=False, **extras):
        self.choices = [str(c) if not isinstance(c, basestring) else c for c in choices or []]
        super(EnumEntityField, self).__init__(name, displayname, decorator, matchingrule, is_value)

    def __set__(self, obj, val):
        val = str(val) if not isinstance(val, basestring) else val
        if val not in self.choices:
            raise ValueError('Expected one of %s (got %s instead)' % (self.choices, val))
        super(EnumEntityField, self).__set__(obj, val)


class IntegerEntityField(StringEntityField):
    def __get__(self, obj, objtype):
        i = super(IntegerEntityField, self).__get__(obj, objtype)
        return int(i) if i is not None else None

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise TypeError('Expected an instance of int (got %s instance instead)' % type(val).__name__)
        super(IntegerEntityField, self).__set__(obj, val)


class BooleanEntityField(StringEntityField):
    def __get__(self, obj, objtype):
        b = super(BooleanEntityField, self).__get__(obj, objtype)
        return b.startswith('t') or b == '1' if b is not None else None

    def __set__(self, obj, val):
        if not isinstance(val, bool):
            raise TypeError('Expected an instance of bool (got %s instance instead)' % type(val).__name__)
        super(BooleanEntityField, self).__set__(obj, str(val).lower())


class FloatEntityField(StringEntityField):
    def __get__(self, obj, objtype):
        f = super(FloatEntityField, self).__get__(obj, objtype)
        return float(f) if f is not None else None

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise TypeError('Expected an instance of float (got %s instance instead)' % type(val).__name__)
        super(FloatEntityField, self).__set__(obj, val)


class LongEntityField(StringEntityField):
    def __get__(self, obj, objtype):
        l = super(LongEntityField, self).__get__(obj, objtype)
        return long(l) if l is not None else None

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise TypeError('Expected an instance of float (got %s instance instead)' % type(val).__name__)
        super(LongEntityField, self).__set__(obj, val)


class DateTimeEntityField(StringEntityField):
    def __get__(self, obj, objtype):
        d = super(DateTimeEntityField, self).__get__(obj, objtype)
        return datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f') if d is not None else None

    def __set__(self, obj, val):
        if not isinstance(val, datetime):
            raise TypeError('Expected an instance of datetime (got %s instance instead)' % type(val).__name__)
        super(DateTimeEntityField, self).__set__(obj, val.strftime('%Y-%m-%d %H:%M:%S.%f'))


class DateEntityField(StringEntityField):
    def __get__(self, obj, objtype):
        d = super(DateEntityField, self).__get__(obj, objtype)
        return datetime.strptime(d, '%Y-%m-%d').date() if d is not None else None

    def __set__(self, obj, val):
        if not isinstance(val, date):
            raise TypeError('Expected an instance of date (got %s instance instead)' % type(val).__name__)
        super(DateEntityField, self).__set__(obj, val.strftime('%Y-%m-%d'))


class timespan(timedelta):
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
        return timespan(days, (hours * 3600) + (minutes * 60) + seconds, useconds)


class TimeSpanEntityField(StringEntityField):
    def __get__(self, obj, objtype):
        d = super(TimeSpanEntityField, self).__get__(obj, objtype)
        return timespan.fromstring(d) if d is not None else None

    def __set__(self, obj, val):
        if not isinstance(val, timedelta):
            raise TypeError('Expected an instance of timedelta or timespan (got %s instance instead)' %
                            type(val).__name__)
        if val.__class__ is timedelta:
            val = timespan(val.days, val.seconds, val.microseconds)
        super(TimeSpanEntityField, self).__set__(obj, str(val))


class RegexEntityField(StringEntityField):
    def __init__(self, name, displayname=None, pattern='.*', decorator=None, matchingrule=MatchingRule.Strict,
                 is_value=False, **extras):
        super(RegexEntityField, self).__init__(name, displayname, decorator, matchingrule, is_value, **extras)
        self.pattern = re.compile(pattern)

    def __set__(self, obj, val):
        if not isinstance(val, basestring):
            val = str(val)
        if not self.pattern.match(val):
            raise ValueError('Failed match for %r, expected pattern %r instead.' % (val, self.pattern.pattern))
        super(RegexEntityField, self).__set__(obj, val)


class ColorEntityField(RegexEntityField):
    def __init__(self, name, displayname=None, decorator=None, matchingrule=MatchingRule.Strict, is_value=False,
                 **extras):
        super(ColorEntityField, self).__init__(name, displayname, '^#[0-9a-fA-F]{6}$', decorator, matchingrule,
                                               is_value, **extras)


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
        if not cls._alias_:
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

        if not cls._type_:
            cls._type_ = '%s.%s' % (cls._namespace_, name)

        mcs.registry[cls._type_] = cls
        mcs.registry[cls._alias_] = cls

        return cls

    @classmethod
    def create(mcs, entity_type):
        return mcs.registry[entity_type]


class Entity(object):
    __metaclass__ = EntityTypeFactory
    _namespace_ = None
    _alias_ = None
    _type_ = None

    notes = StringEntityField('notes#', matchingrule=MatchingRule.Loose)
    bookmark = IntegerEntityField('bookmark#', matchingrule=MatchingRule.Loose)
    link_label = StringEntityField('link#maltego.link.label', matchingrule=MatchingRule.Loose)
    link_style = IntegerEntityField('link#maltego.link.style', matchingrule=MatchingRule.Loose)
    link_color = StringEntityField('link#maltego.link.color', matchingrule=MatchingRule.Loose)
    link_thickness = IntegerEntityField('link#maltego.link.thickness', matchingrule=MatchingRule.Loose)
    link_show_label = EnumEntityField('link#maltego.link.show-label', choices=[0, 1], matchingrule=MatchingRule.Loose)

    def __init__(self, value='', **kwargs):
        if isinstance(value, _Entity):
            self._entity = value
        else:
            self._entity = _Entity(
                type=kwargs.pop('type', self._type_),
                value=value,
                weight=kwargs.pop('weight', None),
                iconurl=kwargs.pop('iconurl', None),
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
    def iconurl(self):
        return self._entity.iconurl

    @iconurl.setter
    def iconurl(self, url):
        self._entity.iconurl = url

    def __iadd__(self, other):
        self._entity += other
        return self

    def __getitem__(self, item):
        return self._entity.fields[item].value

    def __setitem__(self, key, value):
        if key not in self._entity.fields:
            self._entity.fields[key] = Field(key, value)
        else:
            self._entity.fields[key].value = value


class MaltegoTransformRequestMessage(MaltegoElement):

    __entities = fields_.List(_Entity, tagname='Entities', required=False)
    _entities = None  # This is so we can cache the transform entity object list.
    _parameters = fields_.Dict(Field, tagname='TransformFields', key='name', required=False)
    limits = fields_.Model(Limits, required=False)

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
            self._entities = [EntityTypeFactory.create(e.type)(e) for e in self.__entities]
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


class MaltegoMessage(MaltegoElement):
    """This is the root element for all Maltego request, response, and exception messages that are exchanged between the
    client and the transform server. In the case of local transforms, only response and exception messages are exchanged
    from transform to client."""
    message = fields_.Choice(
        fields_.Model(MaltegoTransformExceptionMessage),
        fields_.Model(MaltegoTransformResponseMessage),
        fields_.Model(MaltegoTransformRequestMessage)
    )