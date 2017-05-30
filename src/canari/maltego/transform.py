import re

from canari.maltego.configuration import AuthenticationType
from canari.maltego.entities import Unknown

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'Transform'
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


class Transform(object):

    # Specifies the author of the transform. If not specified __author__ will be used for the create-profile command.
    author = ''

    # A detailed description of the transform. The description can be read from the Maltego Transforms dialog box. If
    # this is not set, the transform class' doc comments will be used.
    description = ''

    # The label found in the transform context menu when right clicking on an entity.
    display_name = ''

    # Specifies the help URL for the specified transform.
    help_url = ''

    # The unique identifier of the transform. Should be in reverse dotted format similar to Java. For example,
    # sploitego.FastNmap. If none is specified, the name will be set to the module dot class name.
    name = ''

    # The Maltego input entity type.
    input_type = Unknown

    # The Maltego transform set name.
    transform_set = ''

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

    def __init__(self):
        if not self.name:
            self.name = '.'.join([self.__module__.split('.', 1)[0], self.__class__.__name__])
        if not self.display_name:
            self.display_name = camel_to_title(self.__class__.__name__)
        if not self.description and self.__doc__:
            self.description = self.__doc__
        if not self.transform_set:
            self.transform_set = self.__module__.split('.', 1)[0].title()

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

    def on_terminate(self):
        """
        This method gets called when the transform's execution is prematurely terminated. It is only applicable for
        local transforms.
        """
        pass