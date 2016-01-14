
Maltego Entities
===============================================================

.. moduleauthor:: xxx xxx <xxx@xxx.com>
.. sectionauthor:: xxx xxx <xxx@xxx.com>

.. versionadded:: 3.0



-------------




AS
--

* Class: ``AS``
* Inherits from: ``Entity``
* Class alias: ``ASNumber``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    AS Number,IntegerEntityField,``number``,``as.number``,Yes

-------------




Affiliation
-----------

* Class: ``Affiliation``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Name,StringEntityField,``person_name``,``person.name``,Yes
    UID,StringEntityField,``uid``,``affiliation.uid``,No
    Network,StringEntityField,``network``,``affiliation.network``,No
    Profile URL,StringEntityField,``profile_url``,``affiliation.profile-url``,No

-------------




Alias
-----

* Class: ``Alias``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Alias,StringEntityField,``alias``,``properties.alias``,No

-------------




Banner
------

* Class: ``Banner``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Banner,StringEntityField,``text``,``banner.text``,Yes

-------------




Bebo
----

* Class: ``Bebo``
* Inherits from: ``Affiliation``
* Class alias: ``AffiliationBebo``


-------------




BuiltWithTechnology
-------------------

* Class: ``BuiltWithTechnology``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    BuiltWith Technology,StringEntityField,``builtwith``,``properties.builtwithtechnology``,No

-------------




DNSName
-------

* Class: ``DNSName``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    DNS Name,StringEntityField,``fqdn``,``fqdn``,Yes

-------------




Device
------

* Class: ``Device``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Device,StringEntityField,``device``,``properties.device``,No

-------------




Document
--------

* Class: ``Document``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    URL,StringEntityField,``url``,``url``,Yes
    Title,StringEntityField,``title``,``title``,No
    Meta-Data,StringEntityField,``metadata``,``document.metadata``,No

-------------




Domain
------

* Class: ``Domain``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Domain Name,StringEntityField,``fqdn``,``fqdn``,Yes
    WHOIS Info,StringEntityField,``whois_info``,``whois-info``,No

-------------




EmailAddress
------------

* Class: ``EmailAddress``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Email Address,StringEntityField,``email``,``email``,Yes

-------------




Facebook
--------

* Class: ``Facebook``
* Inherits from: ``Affiliation``
* Class alias: ``AffiliationFacebook``


-------------




FacebookObject
--------------

* Class: ``FacebookObject``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Facebook Object,StringEntityField,``object``,``properties.facebookobject``,No

-------------




File
----

* Class: ``File``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Source,StringEntityField,``source``,``source``,No
    Description,StringEntityField,``description``,``description``,No

-------------




Flickr
------

* Class: ``Flickr``
* Inherits from: ``Affiliation``
* Class alias: ``AffiliationFlickr``


-------------




GPS
---

* Class: ``GPS``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    GPS Co-ordinate,StringEntityField,``gps``,``properties.gps``,Yes
    Latitude,FloatEntityField,``latitude``,``latitude``,No
    Longitude,FloatEntityField,``longitude``,``longitude``,No

-------------




IPv4Address
-----------

* Class: ``IPv4Address``
* Inherits from: ``Entity``
* Class alias: ``IPAddress``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    IP Address,StringEntityField,``ipv4address``,``ipv4-address``,Yes
    Internal,BooleanEntityField,``internal``,``ipaddress.internal``,No

-------------




Image
-----

* Class: ``Image``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Description,StringEntityField,``description``,``properties.image``,No
    URL,StringEntityField,``url``,``fullImage``,No

-------------




Linkedin
--------

* Class: ``Linkedin``
* Inherits from: ``Affiliation``
* Class alias: ``AffiliationLinkedin``


-------------




Location
--------

* Class: ``Location``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Name,StringEntityField,``name``,``location.name``,Yes
    City,StringEntityField,``city``,``city``,No
    Country Code,StringEntityField,``countrycode``,``countrycode``,No
    Area,StringEntityField,``area``,``location.area``,No
    Country,StringEntityField,``country``,``country``,No
    Longitude,FloatEntityField,``longitude``,``longitude``,No
    Latitude,FloatEntityField,``latitude``,``latitude``,No
    Street Address,StringEntityField,``streetaddress``,``streetaddress``,No
    Area Code,StringEntityField,``areacode``,``location.areacode``,No

-------------




MXRecord
--------

* Class: ``MXRecord``
* Inherits from: ``DNSName``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Priority,IntegerEntityField,``priority``,``mxrecord.priority``,No

-------------




MySpace
-------

* Class: ``MySpace``
* Inherits from: ``Affiliation``
* Class alias: ``AffiliationMySpace``


-------------




NSRecord
--------

* Class: ``NSRecord``
* Inherits from: ``DNSName``
* Class alias: ``-``


-------------




Netblock
--------

* Class: ``Netblock``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    IP Range,StringEntityField,``ipv4range``,``ipv4-range``,Yes

-------------




NominatimLocation
-----------------

* Class: ``NominatimLocation``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Nominatim Location,StringEntityField,``nominatim``,``properties.nominatimlocation``,Yes

-------------




Orkut
-----

* Class: ``Orkut``
* Inherits from: ``Affiliation``
* Class alias: ``AffiliationOrkut``


-------------




Person
------

* Class: ``Person``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Full Name,StringEntityField,``fullname``,``person.fullname``,Yes
    Surname,StringEntityField,``lastname``,``person.lastname``,No
    First Names,StringEntityField,``firstnames``,``person.firstnames``,No

-------------




PhoneNumber
-----------

* Class: ``PhoneNumber``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Phone Number,StringEntityField,``phonenumber``,``phonenumber``,Yes
    Area Code,StringEntityField,``areacode``,``phonenumber.areacode``,No
    Last Digits,StringEntityField,``lastnumbers``,``phonenumber.lastnumbers``,No
    City Code,StringEntityField,``citycode``,``phonenumber.citycode``,No
    Country Code,StringEntityField,``countrycode``,``phonenumber.countrycode``,No

-------------




Phrase
------

* Class: ``Phrase``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Text,StringEntityField,``text``,``text``,Yes

-------------




Port
----

* Class: ``Port``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Ports,StringEntityField,``number``,``port.number``,Yes

-------------




Service
-------

* Class: ``Service``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Description,StringEntityField,``name``,``service.name``,Yes
    Service Banner,StringEntityField,``banner``,``banner.text``,No
    Ports,StringEntityField,``ports``,``port.number``,No

-------------




Spock
-----

* Class: ``Spock``
* Inherits from: ``Affiliation``
* Class alias: ``AffiliationSpock``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Listed Websites,StringEntityField,``websites``,``spock.websites``,No

-------------




Twit
----

* Class: ``Twit``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Twit,StringEntityField,``name``,``twit.name``,Yes
    Content,StringEntityField,``content``,``content``,No
    Date published,StringEntityField,``pubdate``,``pubdate``,No
    Image Link,StringEntityField,``img_link``,``img_link``,No
    Author,StringEntityField,``author``,``author``,No
    Title,StringEntityField,``title``,``title``,No
    Author URI,StringEntityField,``author_uri``,``author_uri``,No
    Twit ID,StringEntityField,``id``,``id``,No

-------------




Twitter
-------

* Class: ``Twitter``
* Inherits from: ``Affiliation``
* Class alias: ``AffiliationTwitter``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Twitter Number,IntegerEntityField,``number``,``twitter.number``,No
    Screen Name,StringEntityField,``screenname``,``twitter.screen-name``,No
    Friend Count,IntegerEntityField,``friendcount``,``twitter.friendcount``,No
    Real Name,StringEntityField,``fullname``,``person.fullname``,No

-------------




URL
---

* Class: ``URL``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Short title,StringEntityField,``short_title``,``short-title``,Yes
    URL,StringEntityField,``url``,``url``,No
    Title,StringEntityField,``title``,``title``,No

-------------




Unknown
-------

* Class: ``Unknown``
* Inherits from: ``Entity``
* Class alias: ``-``


-------------




Vulnerability
-------------

* Class: ``Vulnerability``
* Inherits from: ``Entity``
* Class alias: ``Vuln``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    ID,StringEntityField,``id``,``vulnerability.id``,Yes

-------------




Webdir
------

* Class: ``Webdir``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Name,StringEntityField,``name``,``directory.name``,Yes

-------------




Website
-------

* Class: ``Website``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Website,StringEntityField,``fqdn``,``fqdn``,Yes
    SSL Enabled,BooleanEntityField,``ssl_enabled``,``website.ssl-enabled``,No
    Ports,IntegerEntityField,``ports``,``ports``,No

-------------




WikiEdit
--------

* Class: ``WikiEdit``
* Inherits from: ``Affiliation``
* Class alias: ``-``


-------------




Zoominfo
--------

* Class: ``Zoominfo``
* Inherits from: ``Affiliation``
* Class alias: ``-``
