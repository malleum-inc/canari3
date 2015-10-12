:mod:`canari.maltego.message` - Maltego Messaging Objects
=========================================================

.. module:: canari.maltego.message
    :synopsis: Maltego transform messaging objects.
.. moduleauthor:: Nadeem Douba <ndouba@redcanari.com>
.. sectionauthor:: Nadeem Douba <ndouba@redcanari.com>


.. versionadded:: 3.0

----

The :mod:`canari.maltego.message` module provides the complete implementation of all the Maltego transform messaging
objects. These objects are used to deserialize Maltego transform requests and serialize Canari transform responses for
both local and remote transforms. For example, the ``request`` and ``response`` objects that gets passed into the
:meth:`Transform.do_transform` method are instances of
:class:`~canari.maltego.message.MaltegoTransformRequest` and :class:`~canari.maltego.message.MaltegoTransformResponse`,
respectively.

All Maltego messaging objects are subclasses of the :class:`~canari.maltego.xml.MaltegoElement` super class, which adds
support for two arithmetic operations:

+------------+------------------------------------------------------------------------------+
| Operations | Meaning                                                                      |
+============+==============================================================================+
| ``p += c`` | Add a child object (``c``) to the parent object (``p``)                      |
+------------+------------------------------------------------------------------------------+
| ``p + c``  | Same as ``+=`` but it can be chained with multiple child objects.            |
+------------+------------------------------------------------------------------------------+

Here's an example demonstrating the use of these two arithmetic operations on the ``response`` object::


    from canari.maltego.transform import Transform
    from canari.maltego.entities import Phrase, Person

    class HelloWorld(Transform):

        input_type = Person

        def do_transform(self, request, response, config):
            person = request.entity
            response += Phrase('Hello %s!' % person.value)
            response = response + Phrase('Hello Mr(s) %s!' % person.lastname) \
                                + Phrase('Hello %s!' + person.firstname)
            return response

Finally, each messaging object can be separately serialized and deserialized to and from XML using the :meth:`render` and
:meth:`parse` methods::

    >>> from canari.maltego.entities import Phrase
    >>> print (MaltegoTransformResponseMessage() + Phrase('test')).render(pretty=True)
    <?xml version="1.0" ?>
    <MaltegoTransformResponseMessage>
        <UIMessages/>
        <Entities>
            <Entity Type="maltego.Phrase">
                <Value>test</Value>
                <Weight>1</Weight>
            </Entity>
        </Entities>
    </MaltegoTransformResponseMessage>
    >>> MaltegoTransformResponseMessage.parse('<MaltegoTransformResponseMessage/>')
    <canari.maltego.message.MaltegoTransformResponseMessage object at 0x10e99e150>

However, if you're a transform developer you will never really need to use the :meth:`render` or :meth:`parse` methods
as they are primarily used by the ``dispatcher``, ``canari debug-transform``, and ``plume`` transform runners.

Maltego Request and Response Objects
------------------------------------
The :class:`MaltegoTransformRequestMessage` and :class:`MaltegoTransformResponseMessage` represent the parent container
for Maltego request and response messages, respectively. When a transform is executed, Canari automatically deserializes
a request into a :class:`MaltegoTransformRequestMessage` object and creates an empty
:class:`MaltegoTransformResponseMessage`, which it then passes to :meth:`Transform.do_transform`.

Maltego transform request messages can be created using either the factory method :meth:`parse`, which accepts an XML
string whose root element is the ``<MaltegoTransformRequestMessage>`` tag, or by calling the empty constructor.

.. class:: MaltegoTransformRequestMessage(**kwarg)

    Return a new Maltego transform request message with no child elements. Each Maltego transform request message comes
    with the following read-only attributes:

    .. attribute:: limits

        A :class:`Limits` object which contains the soft and hard limits for the number of entities Maltego
        would like returned.

        One can access the soft and hard limits of a ``request`` object by doing the following::

            >>> print 'Transform hard limit=%s, soft limit=%s' % (request.limits.soft, request.limits.hard)
            Transform hard limit=500, soft limit=5000

        .. note:: :attr:`limits` do not apply to local transforms since the local transform adapter in Maltego does not
                  transmit this information.

    .. attribute:: parameters

        In **local transform execution mode**, :attr:`parameters` is a list of extraneous command line arguments
        not handled by the Canari ``dispatcher``. This is useful in scenarios where you want to use command line
        arguments to manage the behavior of a transform, for example::

                # transform executed using 'dispatcher foo.transforms.HelloWorld -u Bob'
                def do_transform(self, request, response, config):
                    """If '-u' detected in command line arguments make entity value all upper case."""
                    if '-u' in request.parameters:
                        response += Phrase('Hello %s!' + request.entity.value.upper())
                    else:
                        response += Phrase('Hello %s!' + request.entity.value)
                    return response

        In **remote transform execution mode**, :attr:`parameters` is a dictionary of additional transform fields,
        keyed by their names. Transform fields are typically used to communicate additional transform parameters. For
        example, many commercial transforms use the transform field to transmit API keys. Alternatively, one can use
        transform fields to alter transform behaviour - just like in our local mode example. The following is an example
        of a custom transform that expects an API key::

                # ...
                def do_transform(self, request, response, config):
                    fields = request.parameters
                    if 'my.license' not in fields or not valid_api_key(fields['my.license'].value):
                        raise MaltegoException('Invalid API key! Send cheque!')
                    response += Phrase('Hello %s!' + request.entity.value)
                    return response

        .. note:: If you intend to use a transform package in both local and remote mode, make sure to check Canari's
                  operating mode prior to accessing :attr:`parameters`. See :mod:`canari.mode` for more information.

    .. attribute:: entity

        The :class:`Entity` object to be processed by the Canari transform. The entity object's type is
        determined by the value of the :attr:`Transform.input_type` attribute. If `Transform.input_type` is not set
        explicitly, then :attr:`entity` will return an entity of type :class:`~canari.maltego.entities.Unknown`. For
        example, a :class:`~canari.maltego.entities.Person` entity will always be returned in the following transform::

            class HelloWorld(Transform):
                # Ensure request.entity returns a Person object
                input_set = Person

                def do_transform(self, request, response, config):
                    person = request.entity
                    response += Phrase('Hello %s!' + person.fullname)
                    return response

:class:`MaltegoTransformResponseMessage` can be created in the same way as our request objects; either by using
:meth:`parse` or by using the constructor explicitly.

.. class:: MaltegoTransformResponseMessage(**kwarg)

    Return a new Maltego transform response message object with no child elements. The various attributes of the
    response can also be manipulated using regular list operations via these attributes:

    .. attribute:: messages

        A list of :class:`UIMessage` objects that contain user interface messages to be displayed in Maltego's
        "Transform Output" pane or in a dialog window. For example, let's say we wanted to display a fatal message::

            # ...
            def do_transform(self, request, response, config):
                response += UIMessage("This transform is not implemented yet!", type=UIMessageType.Fatal)
                return response


        This would result in the following message box appearing in Maltego:

        .. figure:: images/uimessage_fatal.png
            :align: center
            :alt: Fatal UI message appearance

            Fatal UI message appearance

        .. seealso::

            :class:`UIMessage` for an overview of the different message types and how they are rendered in Maltego's UI.

    .. attribute:: entities

        The list of :class:`Entity` objects to be returned as transform results to the Maltego UI. Entities can be added
        to a response message by using the ``+=`` operator, like so::

            # ...
            def do_transform(self, request, response, config):
                response += Location('Brooklyn')
                return response

        Or by using the ``+`` operator to chain multiple entity results in one line, like so::

            # ...
            def do_transform(self, request, response, config):
                return (response + Location('Brooklyn') + Location('Broadway'))


Communicating Exceptions
------------------------
Using :class:`MaltegoExceptionResponseMessage` objects, a transform can communicate an error state back to the Maltego
user. Canari generates a Maltego exception object if an exception is raised during transform execution. There are two
different behaviours when it comes to reporting exceptions. If a transform raises a :exc:`MaltegoException` then the
exception message is what's communicated to the user. However, other exception types will render a message box with
full stack trace details. Here's a visual example::

    # ...
    def do_transform(self, request, response, config):
        raise MaltegoException('Just pooped!')

Results in the following dialog box:

.. figure:: images/maltego_exception.png
    :align: center
    :alt: MaltegoException exception appearance

    :exc:`MaltegoException` exception appearance

Whereas::

    # ...
    def do_transform(self, request, response, config):
        import foobar # non-existent module

Results in the following dialog box:

.. figure:: images/maltego_raw_exception.png
    :align: center
    :alt: Non-MaltegoException exception appearance

    Non-:exc:`MaltegoException` exception appearance

.. warning::

    Users who are security conscious may find this behaviour undesirable since full stack traces often disclose
    internal information such as file system paths, and module names. Support for cross-referencable logs and
    generic error messaging will appear in Canari v3.1.

Communicating Diagnostic Information
------------------------------------
A second form of communicating status or diagnostic information is via the use of :class:`UIMessage` objects. UI
messages either appear in the "Transform Output" pane (usually at the bottom) or as dialog message boxes depending on
the message type assigned to them. For your convenience, Canari has defined all the different UI message types as class
attributes in :class:`UIMessageType`:

.. class:: UIMessageType

    .. attribute:: Fatal

        Fatal errors are communicated to Maltego users using a dialog message box.

    .. attribute:: Partial

        Partial errors are communicated to Maltego users in the "Transform Output" pane and are orange in color.

    .. attribute:: Inform

        Informational errors are communicated to Maltego users in the "Transform Output" pane but are not colored.

    .. attribute:: Debug

        These errors do not appear to be displayed anywhere in the Maltego user interface. Instead they may appear in
        debug logs.


Communicating diagnostic information to a Maltego user is simple. Simply, use the ``+=`` or ``+`` operators to add
a :class:`UIMessage` object to a response object, like so::

    # ...
    def do_transform(self, request, response, config):
        import time
        response += Phrase('Hello sleepy head!')
        time.sleep(3)
        response += UIMessage("This transform took 3 seconds to complete.", type=UIMessageType.Inform)
        return response


The :class:`UIMessage` accepts two arguments, ``msg`` and ``type``.

.. class:: UIMessage(message, [type=UIMessageType.Inform])

    :arg str message:               The message to communicate to the Maltego user.
    :keyword UIMessageType type:    The type of message to communicate to the user (default:
                                    :attr:`UIMessageType.Inform`).

    Values for ``message`` and ``type`` can also be set via these attributes:

    .. attribute:: type

        The type of message that will be communicated. Valid values for this attribute are defined in
        :class:`UIMessageType`.

    .. attribute:: message

        The message to communicate to the user.

Local transforms also support real-time diagnostic messaging. See :func:`~canari.maltego.utils.debug` and
:func:`~canari.maltego.utils.progress` for more information.


Using and Defining Maltego Entities
-----------------------------------
All Maltego entities are subclasses of the :class:`Entity` type. :class:`Entity` objects are used in both request and
response messages. Canari comes with a list of pre-defined entity types that correspond to the built-in types in
Maltego. These types can be found in :mod:`canari.maltego.entities`. Defining a custom entity in Canari is as simple as
this::

    >>> from canari.maltego.message import Entity, StringEntityField
    >>> class Threat(Entity):
    ...    name = StringEntityField('threat.name', is_value=True)
    ...    country = StringEntityField('threat.country')
    >>> t = Threat('Cheese', country='Switzerland')
    >>> print 'Detected threat %r from %s' % (t.name, t.country)
    Detected threat 'Cheese' from Switzerland.

In the example above we are defining a custom entity of type :class:`Threat` with two string entity fields, :attr:`name`
and :attr:`country`. The ``is_value`` keyword argument in our ``name`` entity field definition instructs Canari that
``name`` is the entity's default value. As a result, we can set the value of ``name`` via the entity's first argument in
the constructor. Alternatively, we could have completely omitted the definition of ``name`` since all entity objects
have an entity :attr:`value` attribute. All other entity fields can be set using a keyword argument that matches the
attribute's name.

:class:`Entity` objects can be instantiated in the following manner:

.. class:: Entity(value='', **kwarg)

    Where ``value`` is the default entity value and ``**kwarg`` is a dictionary containing the optional entity field
    names and values. You can also set pass the following additional keyword arguments:

    :keyword str type:      The entity's type name (default: ``<package name>.<class name>``).
    :keyword str value:     The entity's default entity field value.
    :keyword float weight:  The entity's weight value from 0.0 to 1.0. Useful for transforms that return ranked
                            search result entities from search engines.
    :keyword str iconurl:   The entity's icon URL. Maltego supports the built-in Java URL protocol schemes
                            (``file://``, ``http://``, ``https://``, etc.).
    :keyword list fields:   A list of entity fields, of type :class:`Field`, to be added to the entity.
    :keyword list labels:   A list of entity labels, of type :class:`Label`, to be added to the entity.

    The following attributes are also inherited by all the subclasses of the :class:`Entity` type:

    .. attribute:: notes

        A string containing additional notes that can be attached to a Maltego entity. You can set a note in the
        following manner::

            >>> Threat('Cheese', country='Switzerland', note='This is a note') # or
            >>> t = Threat('Wine', country='Italy')
            >>> t.note = 'This is another note'

        The following figure demonstrates the appearance of an entity note in Maltego:

        .. figure:: images/maltego_note.png
            :align: center
            :alt: Maltego Entity Note

            Maltego Entity Note

        .. note::

            Entity notes are not transmitted as transform input. Consider adding an additional entity field that
            encapsulates the information in your notes if you wish to pass it to your transforms as input.

    .. attribute:: bookmark

        Determines whether an entity should be marked with a colored star. Can be one of the following values:


        .. csv-table::
            :header: Value,Appearance

            :attr:`Bookmark.NoColor`,|bookmark_nocolor| **(default)**
            :attr:`Bookmark.Cyan`,|bookmark_cyan|
            :attr:`Bookmark.Green`,|bookmark_green|
            :attr:`Bookmark.Yellow`,|bookmark_yellow|
            :attr:`Bookmark.Orange`,|bookmark_orange|
            :attr:`Bookmark.Red`,|bookmark_red|

        .. |bookmark_nocolor| image:: images/bookmark_nocolor.png
        .. |bookmark_cyan| image:: images/bookmark_cyan.png
        .. |bookmark_green| image:: images/bookmark_green.png
        .. |bookmark_yellow| image:: images/bookmark_yellow.png
        .. |bookmark_orange| image:: images/bookmark_orange.png
        .. |bookmark_red| image:: images/bookmark_red.png

        Here's an example of how to set a bookmark::

            >>> from canari.maltego.message import Bookmark
            >>> Threat('Cheese', country='Switzerland', bookmark=Bookmark.Red) # or
            >>> t = Threat('Wine', country='Italy')
            >>> t.bookmark = Bookmark.Cyan

        The following figure demonstrates the appearance of an entity bookmark in Maltego:

        .. figure:: images/maltego_bookmark.png
            :align: center
            :alt: Maltego entity bookmark

            Maltego entity bookmark


    .. attribute:: link_label

        A string attribute that adds a label to the link that connects the parent and child entity. Like notes, link
        labels can be set via the ``link_label`` keyword argument in the constructor or by accessing the ``link_label``
        attribute. Here's an example of the link label in action::

            # ...
            def do_transform(self, request, response, config):
                return (response + IPv4Address('74.207.243.85', link_label='This is a link label'))

        This is what it would look like in Maltego:

        .. figure:: images/maltego_link_label.png
            :align: center
            :alt: Link label appearance

            Link label appearance

        Link labels can be shown or hidden by setting the :attr:`link_show_label`.

    .. attribute:: link_show_label

        Determines whether or not the link label will be shown based on the following values:

        .. csv-table::
            :header: Value,Meaning

            :attr:`LinkLabel.UseGlobalSetting`,The visibility of the link label will depend on the global setting.
            :attr:`LinkLabel.Show`,The link label will be visible on the graph.
            :attr:`LinkLabel.Hide`,The link label value will be set but will not be visible on the graph.

        The global setting can be found under the "View" ribbon within the "Links" settings group.

        .. figure:: images/maltego_global_label_visibility_settings.png
            :align: center
            :alt: Maltego global link label visibility setting

            Maltego global link label visibility setting

        Here's an example of the link visibility setting in action::

            from canari.maltego.message import LinkLabel
            # ...
            def do_transform(self, request, response, config):
                return (response + IPv4Address('74.207.243.85', link_show_label=LinkLabel.Hide))

    .. attribute:: link_style

        Dictates the appearance of the link's line, which can be one of the following choices:

        .. csv-table::
            :header: Value,Appearance

            :attr:`LinkStyle.Normal`,|link_style_normal| **(default)**
            :attr:`LinkStyle.Dashed`,|link_style_dashed|
            :attr:`LinkStyle.Dotted`,|link_style_dotted|
            :attr:`LinkStyle.DashDot`,|link_style_dashdot|

        .. |link_style_normal| image:: images/link_style_normal.png
        .. |link_style_dashed| image:: images/link_style_dashed.png
        .. |link_style_dotted| image:: images/link_style_dotted.png
        .. |link_style_dashdot| image:: images/link_style_dashdot.png

        Here's an example of the link style in action::

            from canari.maltego.message import LinkStyle
            # ...
            def do_transform(self, request, response, config):
                return (response + IPv4Address('74.207.243.85', link_style=LinkStyle.DashDot))

        This is what it would look like in Maltego:

        .. figure:: images/maltego_link_style.png
            :align: center
            :alt: Link style appearance

            Link style appearance

    .. attribute:: link_color

        Dictates the color of the link connecting the parent and child entities. The link color is limited to the
        following values:

        .. csv-table::
            :header: Value,Appearance

            :attr:`LinkColor.Black`,|link_color_black|
            :attr:`LinkColor.DarkGray`,|link_color_darkgray| **(default)**
            :attr:`LinkColor.LightGray`,|link_color_lightgray|
            :attr:`LinkColor.Red`,|link_color_red|
            :attr:`LinkColor.Orange`,|link_color_orange|
            :attr:`LinkColor.DarkGreen`,|link_color_darkgreen|
            :attr:`LinkColor.NavyBlue`,|link_color_navyblue|
            :attr:`LinkColor.Magenta`,|link_color_magenta|
            :attr:`LinkColor.Cyan`,|link_color_cyan|
            :attr:`LinkColor.Lime`,|link_color_lime|
            :attr:`LinkColor.Yellow`,|link_color_yellow|
            :attr:`LinkColor.Pink`,|link_color_pink|

        .. |link_color_black| image:: images/link_color_black.png
        .. |link_color_darkgray| image:: images/link_color_darkgray.png
        .. |link_color_lightgray| image:: images/link_color_lightgray.png
        .. |link_color_red| image:: images/link_color_red.png
        .. |link_color_orange| image:: images/link_color_orange.png
        .. |link_color_darkgreen| image:: images/link_color_darkgreen.png
        .. |link_color_navyblue| image:: images/link_color_navyblue.png
        .. |link_color_magenta| image:: images/link_color_magenta.png
        .. |link_color_cyan| image:: images/link_color_cyan.png
        .. |link_color_lime| image:: images/link_color_lime.png
        .. |link_color_yellow| image:: images/link_color_yellow.png
        .. |link_color_pink| image:: images/link_color_pink.png

        Here's an example of the link color in action::

            from canari.maltego.message import LinkColor
            # ...
            def do_transform(self, request, response, config):
                return (response + IPv4Address('74.207.243.85', link_color=LinkColor.Red))

        This is what it would look like in Maltego:

        .. figure:: images/maltego_link_color.png
            :align: center
            :alt: Maltego link color

            Maltego link color

    .. attribute:: link_thickness

        Dictates the thickness of the link connecting the parent and child entities. Valid values range from ``0`` to
        ``5``. The greater the number, the thicker the link and vice versa. Here's an example of the link thickness in
        action::

            # ...
            def do_transform(self, request, response, config):
                return (response + IPv4Address('74.207.243.85', link_thickness=5))

        This is what it would look like in Maltego:

        .. figure:: images/maltego_link_thickness.png
            :align: center
            :alt: Maltego link thickness

            Maltego link thickness
