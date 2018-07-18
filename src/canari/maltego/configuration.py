"""
This module defines the various configuration elements that appear in the Maltego profile files (*.mtz). These
configuration elements specify the configuration options for Maltego transforms, servers, entities, machines, and
viewlets. Canari uses these elements to generate Maltego profiles that can be imported into Maltego.
"""

import time
from canari.maltego.oxml import MaltegoElement, fields as fields_


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.3'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
__status__ = 'Development'

__all__ = [
    'TransformAdapter',
    'VisibilityType',
    'BuiltInTransformSets',
    'Set',
    'Transform',
    'TransformSet',
    'InputConstraint',
    'OutputEntity',
    'InputEntity',
    'PropertyType',
    'TransformProperty',
    'TransformPropertySetting',
    'CmdLineTransformProperty',
    'CmdLineTransformPropertySetting',
    'CmdParmTransformProperty',
    'CmdParmTransformPropertySetting',
    'CmdCwdTransformProperty',
    'CmdCwdTransformPropertySetting',
    'CmdDbgTransformProperty',
    'CmdDbgTransformPropertySetting',
    'TransformSettings',
    'Protocol',
    'AuthenticationType',
    'Authentication',
    'MaltegoServer',
    'EntityCategory',
    'attr',
    'fileobject',
    'attributes',
    'Properties',
    'MaltegoTransform'
]


class TransformAdapter:
    """Defines the transform adapter for the running transform. Currently, there are only two transform adapters
    available in Maltego. They are listed below. This is just an enumeration class.
    """
    Local = 'com.paterva.maltego.transform.protocol.v2.LocalTransformAdapterV2'
    Localv2 = 'com.paterva.maltego.transform.protocol.v2api.LocalTransformAdapterV2'
    Remote = 'com.paterva.maltego.transform.protocol.v2.RemoteTransformAdapterV2'


class VisibilityType:
    """An enumeration class that defines the visibility of a transform."""
    Public = 'public'
    Private = 'private'


class BuiltInTransformSets:
    """An enumeration class that specifies the names of built-in transform sets in Maltego"""
    ConvertToDomain = "Convert to Domain"
    DomainsUsingMXNS = "Domains using MX NS"
    FindOnWebpage = "Find on webpage"
    RelatedEmailAddresses = "Related Email addresses"
    DNSFromDomain = "DNS from Domain"
    EmailAddressesFromDomain = "Email addresses from Domain"
    IPOwnerDetail = "IP owner detail"
    ResolveToIP = "Resolve to IP"
    DNSFromIP = "DNS from IP"
    EmailAddressesFromPerson = "Email addresses from Person"
    InfoFromNS = "Info from NS"
    DomainFromDNS = "Domain From DNS"
    FilesAndDocumentsFromDomain = "Files and Documents from Domain"
    LinksInAndOutOfSite = "Links in and out of site"
    DomainOwnerDetail = "Domain owner detail"
    FilesAndDocumentsFromPhrase = "Files and Documents from Phrase"


class Set(MaltegoElement):
    name = fields_.String()


class Transform(MaltegoElement):
    name = fields_.String()


class TransformSet(MaltegoElement):

    name = fields_.String()
    description = fields_.String(default='')
    transforms = fields_.List(Transform, tagname='Transforms')

    def __iadd__(self, other):
        if isinstance(other, Transform):
            self.transforms.append(other)
        return self


class InputConstraint(MaltegoElement):

    class meta:
        tagname = 'Entity'

    type = fields_.String()
    min = fields_.Integer(default=1)
    max = fields_.Integer(default=1)


class OutputEntity(InputConstraint):

    class meta:
        tagname = 'Entity'


class InputEntity(InputConstraint):

    class meta:
        tagname = 'Entity'


class PropertyType(object):
    String = 'string'
    Boolean = 'boolean'
    Integer = 'int'


class TransformProperty(MaltegoElement):

    class meta:
        tagname = 'Property'

    defaultvalue = fields_.String(tagname='DefaultValue', required=False)
    samplevalue = fields_.String(tagname='SampleValue', default='')
    abstract = fields_.Boolean(default=False)
    description = fields_.String(default='')
    displayname = fields_.String(attrname='displayName', required=False)
    hidden = fields_.Boolean(default=False)
    name = fields_.String()
    nullable = fields_.Boolean(default=False)
    readonly = fields_.Boolean(default=False)
    popup = fields_.Boolean(default=False)
    type = fields_.String(default=PropertyType.String)
    visibility = fields_.String(default=VisibilityType.Public)


class TransformPropertySetting(MaltegoElement):

    class meta:
        tagname='Property'

    name = fields_.String()
    popup = fields_.Boolean(default=False)
    type = fields_.String(default=PropertyType.String)
    value = fields_.String(tagname=".")


def CmdLineTransformProperty(cmd=''):
    return TransformProperty(
        name='transform.local.command',
        defaultvalue=cmd,
        displayname='Command line',
        description='The command to execute for this transform'
    )


def CmdLineTransformPropertySetting(cmd=''):
    return TransformPropertySetting(
        name='transform.local.command',
        value=cmd
    )


def CmdParmTransformProperty(params=''):
    return TransformProperty(
        name='transform.local.parameters',
        defaultvalue=params,
        displayname='Command parameters',
        description='The parameters to pass to the transform command'
    )


def CmdParmTransformPropertySetting(params=''):
    return TransformPropertySetting(
        name='transform.local.parameters',
        value=params
    )


def CmdCwdTransformProperty(cwd=''):
    return TransformProperty(
        name='transform.local.working-directory',
        defaultvalue=cwd,
        displayname='Working directory',
        description='The working directory used when invoking the executable',
        samplevalue='/'
    )


def CmdCwdTransformPropertySetting(cwd=''):
    return TransformPropertySetting(
        name='transform.local.working-directory',
        value=cwd
    )


def CmdDbgTransformProperty(dbg=False):
    return TransformProperty(
        name='transform.local.debug',
        defaultvalue=str(dbg).lower(),
        displayname='Show debug info',
        description="When this is set, the transform's text output will be printed to the output window",
        samplevalue='false',
        type=PropertyType.Boolean
    )


def CmdDbgTransformPropertySetting(dbg=False):
    return TransformPropertySetting(
        name='transform.local.debug',
        value=str(dbg).lower(),
        type=PropertyType.Boolean
    )


class TransformSettings(MaltegoElement):

    enabled = fields_.Boolean(default=True)
    runwithall = fields_.Boolean(default=True)
    favorite = fields_.Boolean(default=False)
    accepted = fields_.Boolean(default=False, attrname='disclaimerAccepted')
    showhelp = fields_.Boolean(default=True, attrname='showHelp')
    properties = fields_.List(TransformPropertySetting, tagname='Properties')

    def __iadd__(self, other):
        if isinstance(other, TransformPropertySetting):
            self.properties.append(other)
        return self


class Protocol(MaltegoElement):

    version = fields_.String(default='2.0')


class AuthenticationType:
    """An enumeration class that defines the authentication type for a transform. This appears to apply only to Paterva
    transforms."""
    Anonymous = 'none'
    Mac = 'mac'
    License = 'license'


class Authentication(MaltegoElement):

    type = fields_.String(default=AuthenticationType.Anonymous)


class MaltegoServer(MaltegoElement):

    name = fields_.String(default='Local')
    enabled = fields_.Boolean(default=True)
    description = fields_.String(default='Local transforms hosted on this machine')
    url = fields_.String(default='http://localhost')
    lastsync = fields_.String(tagname='LastSync', default=time.strftime('%Y-%m-%d'))
    protocol = fields_.Model(Protocol)
    authentication = fields_.Model(Authentication)
    transforms = fields_.List(Transform, tagname='Transforms')

    def __iadd__(self, other):
        if isinstance(other, Transform):
            self.transforms.append(other)
        return self


class EntityCategory(MaltegoElement):

    name = fields_.String()


class attr(MaltegoElement):
    name = fields_.String()
    stringvalue = fields_.String(required=False)
    boolvalue = fields_.Boolean(required=False)


class fileobject(MaltegoElement):

    name = fields_.String()
    attrs = fields_.Dict(attr, key='name')

    def __iadd__(self, other):
        if isinstance(other, attr):
            self.attrs[other.name] = other
        return self


class attributes(MaltegoElement):

    version = fields_.String(default='1.0')
    fileobjects = fields_.Dict(fileobject, key='name')

    def __iadd__(self, other):
        if isinstance(other, fileobject):
            self.fileobjects[other.name] = other
        return self


class Properties(MaltegoElement):

    fields = fields_.Dict(TransformProperty, key='name', tagname='Fields')

    def __iadd__(self, other):
        if isinstance(other, TransformProperty):
            self.fields[other.name] = other
        return self


class MaltegoTransform(MaltegoElement):
    """This is the complete MaltegoTransform element definition that is present in Maltego profiles. It defines every
    aspect of a transform including it's input entity type, transform set, template, etc."""

    name = fields_.String()
    displayname = fields_.String(attrname='displayName', default='')
    abstract = fields_.String(default=False)
    template = fields_.Boolean(default=False)
    visibility = fields_.String(default=VisibilityType.Public)
    description = fields_.String(default='')
    helpurl = fields_.String(attrname='helpURL', default='')
    author = fields_.String(default='')
    owner = fields_.String(default='')
    locrel = fields_.String(attrname='locationRelevance', default='global')
    version = fields_.String(default='1.0')
    requireinfo = fields_.Boolean(default=False, attrname='requireDisplayInfo')
    adapter = fields_.String(tagname='TransformAdapter', default=TransformAdapter.Local)
    properties = fields_.Model(Properties)
    input = fields_.List(InputConstraint, tagname='InputConstraints', required=False)
    output = fields_.List(OutputEntity, tagname='OutputEntities', required=False)
    help = fields_.CDATA(tagname='Help', default='')
    disclaimer = fields_.CDATA(tagname='Disclaimer', default='')
    sets = fields_.List(Set, tagname='defaultSets')
    stealthlevel = fields_.Integer(tagname='StealthLevel', default=0)
    authenticator = fields_.String(tagname='Authenticator', required=False)

    def __iadd__(self, other):
        if isinstance(other, Set):
            self.sets.append(other)
        elif isinstance(other, TransformProperty):
            self.properties.fields_.append(other)
        elif isinstance(other, InputConstraint) or isinstance(other, InputEntity):
            self.input.append(other)
        elif isinstance(other, OutputEntity):
            self.output.append(other)
        return self


class Field(MaltegoElement):

    name = fields_.String()
    type = fields_.String()
    nullable = fields_.Boolean(default=True)
    hidden = fields_.Boolean(default=False)
    readonly = fields_.Boolean(default=False)
    description = fields_.String(required=False)
    displayname = fields_.String(attrname='displayName', required=False)
    defaultvalue = fields_.String(tagname='DefaultValue', required=False)
    samplevalue = fields_.String(tagname='SampleValue', default='')


class Groups(MaltegoElement):
    pass


class EntityProperties(MaltegoElement):

    class meta:
        tagname = 'Properties'

    value = fields_.String(required=False)
    groups = fields_.Model(Groups, required=False)
    fields = fields_.Dict(Field, key='name', tagname='Fields', required=False)


class RegexGroup(MaltegoElement):

    property = fields_.String(required=False)


class Converter(MaltegoElement):

    value = fields_.CDATA(default='', tagname='Value', required=False)
    regexgroups = fields_.Dict(RegexGroup, key='property', required=False)


class MaltegoEntity(MaltegoElement):

    id = fields_.String()
    displayname = fields_.String(attrname='displayName', required=False)
    plural = fields_.String(attrname='displayNamePlural', required=False)
    description = fields_.String(default='', required=False)
    category = fields_.String(required=False)
    smallicon = fields_.String(attrname='smallIconResource', required=False)
    largeicon = fields_.String(attrname='largeIconResource', required=False)
    allowedRoot = fields_.Boolean(default=True, required=False)
    conversion_order = fields_.Integer(attrname='conversionOrder', default=2147483647, required=False)
    visible = fields_.Boolean(default=True, required=False)
    largeicontag = fields_.String(tagname='Icon', required=False)
    smallicontag = fields_.String(tagname='SmallIcon', required=False)
    converter = fields_.Model(Converter, required=False)
    properties = fields_.Model(EntityProperties, required=False)
