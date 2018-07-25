import re
import sys

from canari.framework import classproperty
from canari.maltego.configuration import AuthenticationType
from canari.maltego.entities import Unknown
from canari.maltego.message import ValidationError, ElementType

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'

__all__ = [
    'Transform',
    'TransformSetting'
]


def camel_to_title(s):
    return re.sub(
        '([A-Z]+)([A-Z][a-z])',
        r'\1 \2',
        re.sub(
            '([a-z])([A-Z]+)',
            r'\1 \2',
            re.sub(
                '([0-9]+)',
                r' \1 ',
                s
            )
        )
    ).strip()


class TransformSetting(object):
    type = ElementType.string

    def __init__(self, display, default_value=None, optional=True, popup=False):
        self.optional = optional
        self.popup = popup
        self.default_value = default_value
        self.display = display

    @classmethod
    def parse(cls, value):
        return cls.type(value)


class StringSetting(TransformSetting):
    pass


class BooleanSetting(TransformSetting):
    type = ElementType.boolean


class DateSetting(TransformSetting):
    type = ElementType.date


class DoubleSetting(TransformSetting):
    type = ElementType.double


class FloatSetting(TransformSetting):
    type = ElementType.float


class IntegerSetting(TransformSetting):
    type = ElementType.int


class Transform(object):
    # Specifies the author of the transform. If not specified __author__ will be used for the create-profile command.
    @classproperty
    def author(cls):
        return getattr(sys.modules[cls.__module__], '__author__', '')

    # A detailed description of the transform. The description can be read from the Maltego Transforms dialog box. If
    # this is not set, the transform class' doc comments will be used.
    @classproperty
    def description(cls):
        return cls.__doc__ or ''

    # The label found in the transform context menu when right clicking on an entity.
    @classproperty
    def display_name(cls):
        return camel_to_title(cls.__name__)

    # Specifies the help URL for the specified transform.
    help_url = ''

    # The unique identifier of the transform. Should be in reverse dotted format similar to Java. For example,
    # sploitego.FastNmap. If none is specified, the name will be set to the module dot class name.
    @classproperty
    def name(cls):
        return '.'.join([cls.__module__.split('.', 1)[0], cls.__name__])

    # The Maltego input entity type.
    input_type = Unknown

    # The Maltego transform set name.
    @classproperty
    def transform_set(cls):
        return cls.__module__.split('.', 1)[0].title()

    # Specifies whether or not the transform is deprecated.
    deprecated = False

    # Specifies whether or not the transform can be run on an application server (remotely).
    remote = False

    # Specifies whether or not the transform should open a debugging window in Maltego when executed.
    debug = False

    # Specifies whether or not the transform requires privileged user access.
    superuser = False

    # Specifies the type of authentication used by this transform. Can be either 'none', 'mac', or 'license'.
    authentication = AuthenticationType.Anonymous

    # Specifies a disclaimer for the transform that appears prior to the first execution of a transform
    disclaimer = ''

    # Reserved for future external Maltego transforms support
    command = None

    transform_settings = {}

    def do_transform(self, request, response, config):
        """
        This is the main entry point for the transform. Parameters and transform fields are passed via the config
        variable. The input entity is passed via the request object. Once a transform has executed its data mining
        operations, values should be returned via the response object. Additional methods can be defined as long as
        they don't overwrite the built-in property names: author, description, display_name, help_url, name, deprecated,
        remote, debug, and superuser.

        :param request: a MaltegoTransformRequest object.
        :param response: a MaltegoTransformResponse object.
        :param config: a CanariConfig object.
        :return: The response object should be returned.

        :Example:

        class GoogleTransform(MaltegoTransform):
            # ...
            def do_transform(self, request, response, config):
                term = request.value
                results = google(term)
                for result in results:
                    response += WebSite(result)
                return response
        """
        raise NotImplementedError("The 'do_transform' method needs to be implemented!")

    def get_setting(self, request, setting_name, default=None):
        request_settings = request.settings

        if setting_name in self.transform_settings:
            transform_setting = self.transform_settings[setting_name]

            if setting_name not in request_settings and not transform_setting.optional:
                raise ValidationError("Required transform setting {!r} is missing. Aborting...".format(setting_name))

            return transform_setting.parse(request_settings.get(setting_name, default))

        return request_settings.get(setting_name, default)

    def on_terminate(self):
        """
        This method gets called when the transform's execution is prematurely terminated. It is only applicable for
        local transforms.
        """
        pass
