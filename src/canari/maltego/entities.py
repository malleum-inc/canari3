from message import Entity, StringEntityField, IntegerEntityField, FloatEntityField, BooleanEntityField

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'Affiliation',
    'Bebo',
    'Facebook',
    'Flickr',
    'Linkedin',
    'MySpace',
    'Orkut',
    'Spock',
    'Twitter',
    'WikiEdit',
    'Zoominfo',
    'Alias',
    'AS',
    'Banner',
    'BuiltWithTechnology',
    'Device',
    'DNSName',
    'Document',
    'Domain',
    'EmailAddress',
    'FacebookObject',
    'File',
    'GPS',
    'Image',
    'IPv4Address',
    'Location',
    'MXRecord',
    'Netblock',
    'NominatimLocation',
    'NSRecord',
    'Person',
    'PhoneNumber',
    'Phrase',
    'Port',
    'Service',
    'Twit',
    'URL',
    'Vulnerability',
    'Webdir',
    'Website',
    'WebTitle'
]


class Unknown(Entity):
    pass


class GPS(Entity):
    gps = StringEntityField('properties.gps', displayname='GPS Co-ordinate', is_value=True)
    latitude = FloatEntityField('latitude', displayname='Latitude')
    longitude = FloatEntityField('longitude', displayname='Longitude')


class Device(Entity):
    device = StringEntityField('properties.device', displayname='Device')


class BuiltWithTechnology(Entity):
    builtwith = StringEntityField('properties.builtwithtechnology', displayname='BuiltWith Technology')


class Domain(Entity):
    fqdn = StringEntityField('fqdn', displayname='Domain Name', is_value=True)
    whois_info = StringEntityField('whois-info', displayname='WHOIS Info', alias='whois')


class DNSName(Entity):
    fqdn = StringEntityField('fqdn', displayname='DNS Name', is_value=True)


class MXRecord(DNSName):
    priority = IntegerEntityField('mxrecord.priority', displayname='Priority')


class NSRecord(DNSName):
    pass


class IPv4Address(Entity):
    _alias_ = 'IPAddress'
    ipv4address = StringEntityField('ipv4-address', displayname='IP Address', is_value=True)
    internal = BooleanEntityField('ipaddress.internal', displayname='Internal')


class Netblock(Entity):
    ipv4range = StringEntityField('ipv4-range', displayname='IP Range', is_value=True)


class AS(Entity):
    _alias_ = 'ASNumber'
    number = IntegerEntityField('as.number', displayname='AS Number', is_value=True)


class Website(Entity):
    fqdn = StringEntityField('fqdn', displayname='Website', is_value=True)
    ssl_enabled = BooleanEntityField('website.ssl-enabled', displayname='SSL Enabled')
    ports = IntegerEntityField('ports', displayname='Ports')


class URL(Entity):
    short_title = StringEntityField('short-title', displayname='Short title', is_value=True,
                                    alias='maltego.v2.value.property')
    url = StringEntityField('url', displayname='URL', alias='theurl')
    title = StringEntityField('title', displayname='Title', alias='fulltitle')


class Phrase(Entity):
    text = StringEntityField('text', displayname='Text', is_value=True)


class Document(Entity):
    url = StringEntityField('url', displayname='URL', alias='link', is_value=True)
    title = StringEntityField('title', displayname='Title', alias='maltego.v2.value.property')
    metadata = StringEntityField('document.metadata', displayname='Meta-Data', alias='metainfo')


class Person(Entity):
    fullname = StringEntityField('person.fullname', displayname='Full Name', is_value=True)
    lastname = StringEntityField('person.lastname', displayname='Surname', alias='lastname')
    firstnames = StringEntityField('person.firstnames', displayname='First Names', alias='firstname')


class EmailAddress(Entity):
    email = StringEntityField('email', displayname='Email Address', is_value=True)


class Twit(Entity):
    name = StringEntityField('twit.name', displayname='Twit', is_value=True)
    content = StringEntityField('content', displayname='Content')
    pubdate = StringEntityField('pubdate', displayname='Date published')
    img_link = StringEntityField('img_link', displayname='Image Link', alias='imglink')
    author = StringEntityField('author', displayname='Author')
    title = StringEntityField('title', displayname='Title')
    author_uri = StringEntityField('author_uri', displayname='Author URI')
    id = StringEntityField('id', displayname='Twit ID')


class Affiliation(Entity):
    _namespace_ = 'maltego.affiliation'
    person_name = StringEntityField('person.name', displayname='Name', is_value=True)
    uid = StringEntityField('affiliation.uid', displayname='UID', alias='uid')
    network = StringEntityField('affiliation.network', displayname='Network', alias='network')
    profile_url = StringEntityField('affiliation.profile-url', displayname='Profile URL', alias='profile_url')


class Bebo(Affiliation):
    _alias_ = 'AffiliationBebo'


class Facebook(Affiliation):
    _alias_ = 'AffiliationFacebook'


class Flickr(Affiliation):
    _alias_ = 'AffiliationFlickr'


class Linkedin(Affiliation):
    _alias_ = 'AffiliationLinkedin'


class MySpace(Affiliation):
    _alias_ = 'AffiliationMySpace'


class Orkut(Affiliation):
    _alias_ = 'AffiliationOrkut'


class Twitter(Affiliation):
    _alias_ = 'AffiliationTwitter'
    number = IntegerEntityField('twitter.number', displayname='Twitter Number')
    screenname = StringEntityField('twitter.screen-name', displayname='Screen Name')
    friendcount = IntegerEntityField('twitter.friendcount', displayname='Friend Count')
    fullname = StringEntityField('person.fullname', displayname='Real Name')


class Zoominfo(Affiliation):
    pass


class WikiEdit(Affiliation):
    pass


class Spock(Affiliation):
    _alias_ = 'AffiliationSpock'
    websites = StringEntityField('spock.websites', displayname='Listed Websites')


class FacebookObject(Entity):
    object = StringEntityField('properties.facebookobject', displayname='Facebook Object')


class Location(Entity):
    name = StringEntityField('location.name', displayname='Name', is_value=True)
    city = StringEntityField('city', displayname='City')
    countrycode = StringEntityField('countrycode', displayname='Country Code', alias='countrysc')
    area = StringEntityField('location.area', displayname='Area', alias='area')
    country = StringEntityField('country', displayname='Country')
    longitude = FloatEntityField('longitude', displayname='Longitude', alias='long')
    latitude = FloatEntityField('latitude', displayname='Latitude', alias='lat')
    streetaddress = StringEntityField('streetaddress', displayname='Street Address')
    areacode = StringEntityField('location.areacode', displayname='Area Code')


class NominatimLocation(Entity):
    nominatim = StringEntityField('properties.nominatimlocation', displayname='Nominatim Location', is_value=True)


class PhoneNumber(Entity):
    phonenumber = StringEntityField('phonenumber', displayname='Phone Number', is_value=True)
    areacode = StringEntityField('phonenumber.areacode', displayname='Area Code', alias='areacode')
    lastnumbers = StringEntityField('phonenumber.lastnumbers', displayname='Last Digits', alias='lastnumbers')
    citycode = StringEntityField('phonenumber.citycode', displayname='City Code', alias='citycode')
    countrycode = StringEntityField('phonenumber.countrycode', displayname='Country Code', alias='countrycode')


class Alias(Entity):
    alias = StringEntityField('properties.alias', displayname='Alias')


class File(Entity):
    source = StringEntityField('source', displayname='Source')
    description = StringEntityField('description', displayname='Description')


class Image(Entity):
    description = StringEntityField('properties.image', displayname='Description')
    url = StringEntityField('fullImage', displayname='URL')


class Banner(Entity):
    text = StringEntityField('banner.text', displayname='Banner', is_value=True)


class Port(Entity):
    number = StringEntityField('port.number', displayname='Ports', is_value=True)


class Service(Entity):
    name = StringEntityField('service.name', displayname='Description', is_value=True)
    banner = StringEntityField('banner.text', displayname='Service Banner')
    ports = StringEntityField('port.number', displayname='Ports')


class Vulnerability(Entity):
    _alias_ = 'Vuln'
    id = StringEntityField('vulnerability.id', displayname='ID', is_value=True)


class Webdir(Entity):
    name = StringEntityField('directory.name', displayname='Name', is_value=True)


class WebTitle(Entity):
    title = StringEntityField('title', displayname='Title', is_value=True)
