from canari.maltego.message import (Entity, StringEntityField, IntegerEntityField,
                                    FloatEntityField, BooleanEntityField, DateEntityField, Unknown)

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2015, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@redcanari.com'
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
    'Alias',
    'BuiltWithTechnology',
    'BuiltWithRelationship',
    'Company',
    'Banner',
    'WikiEdit',
    'Zoominfo',
    'AS',
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
    'WebTitle',
    'TrackingCode',
    'CircularArea',
    'Hash',
    'Hashtag',
    'Tweet',
    'TwitterUserList',
    'Organization',
    'Sentiment',
    'Unknown'
]


class GPS(Entity):
    _category_ = 'Locations'
    gps = StringEntityField('properties.gps', display_name='GPS Co-ordinate', is_value=True)
    latitude = FloatEntityField('latitude', display_name='Latitude')
    longitude = FloatEntityField('longitude', display_name='Longitude')


class Device(Entity):
    _category_ = 'Devices'
    device = StringEntityField('properties.device', display_name='Device')


class BuiltWithTechnology(Entity):
    _category_ = 'Penetration Testing'
    builtwith = StringEntityField('properties.builtwithtechnology', display_name='BuiltWith Technology')


class BuiltWithRelationship(Entity):
    _category_ = 'Penetration Testing'
    builtwith = StringEntityField('properties.builtwithrelationship', display_name='BuiltWith Technology')
    matches = StringEntityField('matches', display_name='Matches')


class Domain(Entity):
    _category_ = 'Infrastructure'
    fqdn = StringEntityField('fqdn', display_name='Domain Name', is_value=True)
    whois_info = StringEntityField('whois-info', display_name='WHOIS Info', alias='whois')


class DNSName(Entity):
    _category_ = 'Infrastructure'
    fqdn = StringEntityField('fqdn', display_name='DNS Name', is_value=True)


class MXRecord(DNSName):
    priority = IntegerEntityField('mxrecord.priority', display_name='Priority')


class NSRecord(DNSName):
    pass


class IPv4Address(Entity):
    _category_ = 'Infrastructure'
    _alias_ = 'IPAddress'
    ipv4address = StringEntityField('ipv4-address', display_name='IP Address', is_value=True)
    internal = BooleanEntityField('ipaddress.internal', display_name='Internal')


class Netblock(Entity):
    _category_ = 'Infrastructure'
    ipv4range = StringEntityField('ipv4-range', display_name='IP Range', is_value=True)


class AS(Entity):
    _category_ = 'Infrastructure'
    _alias_ = 'ASNumber'
    number = IntegerEntityField('as.number', display_name='AS Number', is_value=True)


class Website(Entity):
    _category_ = 'Infrastructure'
    fqdn = StringEntityField('fqdn', display_name='Website', is_value=True)
    ssl_enabled = BooleanEntityField('website.ssl-enabled', display_name='SSL Enabled')
    ports = IntegerEntityField('ports', display_name='Ports')


class URL(Entity):
    _category_ = 'Infrastructure'
    short_title = StringEntityField('short-title', display_name='Short title', is_value=True,
                                    alias='maltego.v2.value.property')
    url = StringEntityField('url', display_name='URL', alias='theurl')
    title = StringEntityField('title', display_name='Title', alias='fulltitle')


class Phrase(Entity):
    _category_ = 'Personal'
    text = StringEntityField('text', display_name='Text', is_value=True)


class Document(Entity):
    _category_ = 'Personal'
    url = StringEntityField('url', display_name='URL', alias='link', is_value=True)
    title = StringEntityField('title', display_name='Title', alias='maltego.v2.value.property')
    metadata = StringEntityField('document.metadata', display_name='Meta-Data', alias='metainfo')


class Person(Entity):
    _category_ = 'Personal'
    fullname = StringEntityField('person.fullname', display_name='Full Name', is_value=True)
    lastname = StringEntityField('person.lastname', display_name='Surname', alias='lastname')
    firstnames = StringEntityField('person.firstnames', display_name='First Names', alias='firstname')


class EmailAddress(Entity):
    _category_ = 'Personal'
    email = StringEntityField('email', display_name='Email Address', is_value=True)


class Twit(Entity):
    _category_ = 'Social Network'
    name = StringEntityField('twit.name', display_name='Twit', is_value=True)
    content = StringEntityField('content', display_name='Content')
    pubdate = StringEntityField('pubdate', display_name='Date published')
    img_link = StringEntityField('img_link', display_name='Image Link', alias='imglink')
    author = StringEntityField('author', display_name='Author')
    title = StringEntityField('title', display_name='Title')
    author_uri = StringEntityField('author_uri', display_name='Author URI')
    id = StringEntityField('id', display_name='Twit ID')


class Affiliation(Entity):
    _category_ = 'Social Network'
    _namespace_ = 'maltego.affiliation'
    person_name = StringEntityField('person.name', display_name='Name', is_value=True)
    uid = StringEntityField('affiliation.uid', display_name='UID', alias='uid')
    network = StringEntityField('affiliation.network', display_name='Network', alias='network')
    profile_url = StringEntityField('affiliation.profile-url', display_name='Profile URL', alias='profile_url')


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
    number = IntegerEntityField('twitter.number', display_name='Twitter Number')
    screenname = StringEntityField('twitter.screen-name', display_name='Screen Name')
    friendcount = IntegerEntityField('twitter.friendcount', display_name='Friend Count')
    fullname = StringEntityField('person.fullname', display_name='Real Name')


class Zoominfo(Affiliation):
    pass


class WikiEdit(Affiliation):
    pass


class Spock(Affiliation):
    _alias_ = 'AffiliationSpock'
    websites = StringEntityField('spock.websites', display_name='Listed Websites')


class FacebookObject(Entity):
    _category_ = 'Social Network'
    object = StringEntityField('properties.facebookobject', display_name='Facebook Object')


class Location(Entity):
    _category_ = 'Locations'
    name = StringEntityField('location.name', display_name='Name', is_value=True)
    city = StringEntityField('city', display_name='City')
    countrycode = StringEntityField('countrycode', display_name='Country Code', alias='countrysc')
    area = StringEntityField('location.area', display_name='Area', alias='area')
    country = StringEntityField('country', display_name='Country')
    longitude = FloatEntityField('longitude', display_name='Longitude', alias='long')
    latitude = FloatEntityField('latitude', display_name='Latitude', alias='lat')
    streetaddress = StringEntityField('streetaddress', display_name='Street Address')
    areacode = StringEntityField('location.areacode', display_name='Area Code')


class NominatimLocation(Entity):
    _category_ = 'Locations'
    nominatim = StringEntityField('properties.nominatimlocation', display_name='Nominatim Location', is_value=True)


class PhoneNumber(Entity):
    _category_ = 'Personal'
    phonenumber = StringEntityField('phonenumber', display_name='Phone Number', is_value=True)
    areacode = StringEntityField('phonenumber.areacode', display_name='Area Code', alias='areacode')
    lastnumbers = StringEntityField('phonenumber.lastnumbers', display_name='Last Digits', alias='lastnumbers')
    citycode = StringEntityField('phonenumber.citycode', display_name='City Code', alias='citycode')
    countrycode = StringEntityField('phonenumber.countrycode', display_name='Country Code', alias='countrycode')


class Alias(Entity):
    _category_ = 'Personal'
    alias = StringEntityField('properties.alias', display_name='Alias')


class File(Entity):
    _category_ = 'Personal'
    source = StringEntityField('source', display_name='Source')
    description = StringEntityField('description', display_name='Description')


class Image(Entity):
    _category_ = 'Personal'
    description = StringEntityField('properties.image', display_name='Description')
    url = StringEntityField('fullImage', display_name='URL')


class Banner(Entity):
    _category_ = 'Infrastructure'
    text = StringEntityField('banner.text', display_name='Banner', is_value=True)


class Port(Entity):
    _category_ = 'Infrastructure'
    number = StringEntityField('port.number', display_name='Ports', is_value=True)


class Service(Entity):
    _category_ = 'Infrastructure'
    name = StringEntityField('service.name', display_name='Description', is_value=True)
    banner = StringEntityField('banner.text', display_name='Service Banner')
    ports = StringEntityField('port.number', display_name='Ports')


class Vulnerability(Entity):
    _category_ = 'Penetration Testing'
    _alias_ = 'Vuln'
    id = StringEntityField('vulnerability.id', display_name='ID', is_value=True)


class Webdir(Entity):
    _category_ = 'Infrastructure'
    name = StringEntityField('directory.name', display_name='Name', is_value=True)


class WebTitle(Entity):
    _category_ = 'Infrastructure'
    title = StringEntityField('title', display_name='Title', is_value=True)


class TrackingCode(Entity):
    _alias_ = 'maltego.UniqueIdentifier'
    _category_ = 'Infrastructure'
    unique_identifier = StringEntityField('properties.uniqueidentifier', display_name='Uniqueidentifier', is_value=True)
    identifier_type = StringEntityField('identifierType', display_name='Identifier Type')


class CircularArea(Entity):
    _category_ = 'Locations'
    area_circular = StringEntityField('area.circular', display_name='Circular Area', is_value=True)
    latitude = FloatEntityField('latitude', display_name='Latitude')
    longitude = FloatEntityField('longitude', display_name='Longitude')
    radius = IntegerEntityField('radius', display_name='Radius (m)')


class Hash(Entity):
    _category_ = 'Malware'
    hash = StringEntityField('properties.hash', display_name='Hash', is_value=True)
    type = StringEntityField('type', display_name='Hash Type')
    owner = StringEntityField('owner', display_name='Owner')
    before = DateEntityField('before', display_name='Before')
    after = DateEntityField('after', display_name='After')
    included_media_types = StringEntityField('includeMediaType', display_name='Included Media Types')
    excluded_media_types = StringEntityField('excludeMediaType', display_name='Excluded Media Types')


class Hashtag(Entity):
    _category_ = 'Social'
    hashtag = StringEntityField('twitter.hashtag', display_name='Hashtag', is_value=True)


class Company(Entity):
    _category_ = "Groups"
    name = StringEntityField('title', display_name='Name', is_value=True)


class Organization(Entity):
    _category_ = "Groups"
    name = StringEntityField('title', display_name='Name', is_value=True)


class Sentiment(Entity):
    _category_ = "Personal"
    sentiment = StringEntityField('properties.sentiment', display_name='Sentiment', is_value=True)


class TwitterUserList(Entity):
    _category_ = "Social Network"
    name = StringEntityField('twitter.list.name', display_name='Name', is_value=True)
    full_name = StringEntityField('twitter.list.fullname', display_name='Full Name')
    id_ = StringEntityField('twitter.list.id', display_name='ID')
    description = StringEntityField('twitter.list.description', display_name='Description')
    member_count = StringEntityField('twitter.list.members', display_name='Member Count')
    subscriber_count = StringEntityField('twitter.list.subscribers', display_name='Subscriber Count')
    slug = StringEntityField('twitter.list.slug', display_name='Slug')
    uri = StringEntityField('twitter.list.uri', display_name='URI')


class Tweet(Entity):
    _category = "Social Network"
    tweet = StringEntityField('twit.name', display_name='Tweet', is_value=True)
    tweet_id = StringEntityField('id', display_name='Tweet ID')
    author = StringEntityField('author', display_name='Author')
    author_uri = StringEntityField('author_uri', display_name='Author URI')
    content = StringEntityField('content', display_name='Content')
    image_link = StringEntityField('imglink', display_name='Image Link')
    date_published = StringEntityField('pubdate', display_name='Date published')
    title = StringEntityField('title', display_name='Title')
