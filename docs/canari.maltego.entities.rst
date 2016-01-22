
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

    Network,StringEntityField,``network``,``affiliation.network``,No
    Name,StringEntityField,``person_name``,``person.name``,Yes
    Profile URL,StringEntityField,``profile_url``,``affiliation.profile-url``,No
    UID,StringEntityField,``uid``,``affiliation.uid``,No

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

    Meta-Data,StringEntityField,``metadata``,``document.metadata``,No
    Title,StringEntityField,``title``,``title``,No
    URL,StringEntityField,``url``,``url``,Yes

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

    Description,StringEntityField,``description``,``description``,No
    Source,StringEntityField,``source``,``source``,No

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

    Internal,BooleanEntityField,``internal``,``ipaddress.internal``,No
    IP Address,StringEntityField,``ipv4address``,``ipv4-address``,Yes

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

    Area,StringEntityField,``area``,``location.area``,No
    Area Code,StringEntityField,``areacode``,``location.areacode``,No
    City,StringEntityField,``city``,``city``,No
    Country,StringEntityField,``country``,``country``,No
    Country Code,StringEntityField,``countrycode``,``countrycode``,No
    Latitude,FloatEntityField,``latitude``,``latitude``,No
    Longitude,FloatEntityField,``longitude``,``longitude``,No
    Name,StringEntityField,``name``,``location.name``,Yes
    Street Address,StringEntityField,``streetaddress``,``streetaddress``,No

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

    First Names,StringEntityField,``firstnames``,``person.firstnames``,No
    Full Name,StringEntityField,``fullname``,``person.fullname``,Yes
    Surname,StringEntityField,``lastname``,``person.lastname``,No

-------------




PhoneNumber
-----------

* Class: ``PhoneNumber``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Area Code,StringEntityField,``areacode``,``phonenumber.areacode``,No
    City Code,StringEntityField,``citycode``,``phonenumber.citycode``,No
    Country Code,StringEntityField,``countrycode``,``phonenumber.countrycode``,No
    Last Digits,StringEntityField,``lastnumbers``,``phonenumber.lastnumbers``,No
    Phone Number,StringEntityField,``phonenumber``,``phonenumber``,Yes

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

    Service Banner,StringEntityField,``banner``,``banner.text``,No
    Description,StringEntityField,``name``,``service.name``,Yes
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

    Author,StringEntityField,``author``,``author``,No
    Author URI,StringEntityField,``author_uri``,``author_uri``,No
    Content,StringEntityField,``content``,``content``,No
    Twit ID,StringEntityField,``id``,``id``,No
    Image Link,StringEntityField,``img_link``,``img_link``,No
    Twit,StringEntityField,``name``,``twit.name``,Yes
    Date published,StringEntityField,``pubdate``,``pubdate``,No
    Title,StringEntityField,``title``,``title``,No

-------------




Twitter
-------

* Class: ``Twitter``
* Inherits from: ``Affiliation``
* Class alias: ``AffiliationTwitter``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Friend Count,IntegerEntityField,``friendcount``,``twitter.friendcount``,No
    Real Name,StringEntityField,``fullname``,``person.fullname``,No
    Twitter Number,IntegerEntityField,``number``,``twitter.number``,No
    Screen Name,StringEntityField,``screenname``,``twitter.screen-name``,No

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
    Title,StringEntityField,``title``,``title``,No
    URL,StringEntityField,``url``,``url``,No

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




WebTitle
--------

* Class: ``WebTitle``
* Inherits from: ``Entity``
* Class alias: ``-``

**Parameters**

.. csv-table::
    :header: Display Name,Type,Canari Property,Maltego Property,Main Property

    Title,StringEntityField,``title``,``title``,Yes

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
    Ports,IntegerEntityField,``ports``,``ports``,No
    SSL Enabled,BooleanEntityField,``ssl_enabled``,``website.ssl-enabled``,No

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
