:mod:`canari.maltego.entities` Maltego Entities
===============================================

.. module:: canari.maltego.entities
    :synopsis: Maltego Entity Classes
.. moduleauthor:: Nadeem Douba <ndouba@redcanari.com>
.. sectionauthor:: Nadeem Douba <ndouba@redcanari.com>

.. versionadded:: 3.0

----


``maltego.Alias``
^^^^^^^^^^^^^^^^^

.. class:: Alias(**kwargs)

        :keyword str alias: Alias (``properties.alias``)
    


-------------


``maltego.affiliation.Facebook`` (alias: ``AffiliationFacebook``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Facebook(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)



-------------


``maltego.NSRecord``
^^^^^^^^^^^^^^^^^^^^

.. class:: NSRecord(**kwargs)

        :keyword str fqdn: DNS Name (``fqdn``)
    


-------------


``maltego.FacebookObject``
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: FacebookObject(**kwargs)

        :keyword str object: Facebook Object (``properties.facebookobject``)
    


-------------


``maltego.affiliation.Affiliation``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Affiliation(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.GPS``
^^^^^^^^^^^^^^^

.. class:: GPS(**kwargs)

        :keyword float longitude: Longitude (``longitude``)
        :keyword float latitude: Latitude (``latitude``)
        :keyword str gps: GPS Co-ordinate (``properties.gps``)
    


-------------


``maltego.Domain``
^^^^^^^^^^^^^^^^^^

.. class:: Domain(**kwargs)

        :keyword str whois_info: WHOIS Info (``whois-info``)
        :keyword str fqdn: Domain Name (``fqdn``)
    


-------------


``maltego.Image``
^^^^^^^^^^^^^^^^^

.. class:: Image(**kwargs)

        :keyword str url: URL (``fullImage``)
        :keyword str description: Description (``properties.image``)
    


-------------


``maltego.WebTitle``
^^^^^^^^^^^^^^^^^^^^

.. class:: WebTitle(**kwargs)

        :keyword str title: Title (``title``)
    


-------------


``maltego.affiliation.Spock`` (alias: ``AffiliationSpock``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Spock(**kwargs)

        :keyword str websites: Listed Websites (``spock.websites``)
        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.URL``
^^^^^^^^^^^^^^^

.. class:: URL(**kwargs)

        :keyword str url: URL (``url``)
        :keyword str title: Title (``title``)
        :keyword str short_title: Short title (``short-title``)
    


-------------


``maltego.IPv4Address`` (alias: ``IPAddress``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: IPv4Address(**kwargs)

        :keyword str ipv4address: IP Address (``ipv4-address``)
        :keyword bool internal: Internal (``ipaddress.internal``)
    


-------------


``maltego.Website``
^^^^^^^^^^^^^^^^^^^

.. class:: Website(**kwargs)

        :keyword bool ssl_enabled: SSL Enabled (``website.ssl-enabled``)
        :keyword int ports: Ports (``ports``)
        :keyword str fqdn: Website (``fqdn``)
    


-------------


``maltego.affiliation.Zoominfo``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Zoominfo(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.EmailAddress``
^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: EmailAddress(**kwargs)

        :keyword str email: Email Address (``email``)
    


-------------


``maltego.Person``
^^^^^^^^^^^^^^^^^^

.. class:: Person(**kwargs)

        :keyword str lastname: Surname (``person.lastname``)
        :keyword str fullname: Full Name (``person.fullname``)
        :keyword str firstnames: First Names (``person.firstnames``)
    


-------------


``maltego.Device``
^^^^^^^^^^^^^^^^^^

.. class:: Device(**kwargs)

        :keyword str device: Device (``properties.device``)
    


-------------


``maltego.DNSName``
^^^^^^^^^^^^^^^^^^^

.. class:: DNSName(**kwargs)

        :keyword str fqdn: DNS Name (``fqdn``)
    


-------------


``maltego.BuiltWithTechnology``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: BuiltWithTechnology(**kwargs)

        :keyword str builtwith: BuiltWith Technology (``properties.builtwithtechnology``)
    


-------------


``maltego.Document``
^^^^^^^^^^^^^^^^^^^^

.. class:: Document(**kwargs)

        :keyword str url: URL (``url``)
        :keyword str title: Title (``title``)
        :keyword str metadata: Meta-Data (``document.metadata``)
    


-------------


``maltego.MXRecord``
^^^^^^^^^^^^^^^^^^^^

.. class:: MXRecord(**kwargs)

        :keyword int priority: Priority (``mxrecord.priority``)
        :keyword str fqdn: DNS Name (``fqdn``)
    


-------------


``maltego.Banner``
^^^^^^^^^^^^^^^^^^

.. class:: Banner(**kwargs)

        :keyword str text: Banner (``banner.text``)
    


-------------


``maltego.affiliation.MySpace`` (alias: ``AffiliationMySpace``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: MySpace(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.Phrase``
^^^^^^^^^^^^^^^^^^

.. class:: Phrase(**kwargs)

        :keyword str text: Text (``text``)
    


-------------


``maltego.Netblock``
^^^^^^^^^^^^^^^^^^^^

.. class:: Netblock(**kwargs)

        :keyword str ipv4range: IP Range (``ipv4-range``)
    


-------------


``maltego.NominatimLocation``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: NominatimLocation(**kwargs)

        :keyword str nominatim: Nominatim Location (``properties.nominatimlocation``)
    


-------------


``maltego.affiliation.Flickr`` (alias: ``AffiliationFlickr``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Flickr(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.PhoneNumber``
^^^^^^^^^^^^^^^^^^^^^^^

.. class:: PhoneNumber(**kwargs)

        :keyword str phonenumber: Phone Number (``phonenumber``)
        :keyword str lastnumbers: Last Digits (``phonenumber.lastnumbers``)
        :keyword str countrycode: Country Code (``phonenumber.countrycode``)
        :keyword str citycode: City Code (``phonenumber.citycode``)
        :keyword str areacode: Area Code (``phonenumber.areacode``)
    


-------------


``maltego.affiliation.Bebo`` (alias: ``AffiliationBebo``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Bebo(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.Service``
^^^^^^^^^^^^^^^^^^^

.. class:: Service(**kwargs)

        :keyword str ports: Ports (``port.number``)
        :keyword str name: Description (``service.name``)
        :keyword str banner: Service Banner (``banner.text``)
    


-------------


``maltego.File``
^^^^^^^^^^^^^^^^

.. class:: File(**kwargs)

        :keyword str source: Source (``source``)
        :keyword str description: Description (``description``)
    


-------------


``maltego.Port``
^^^^^^^^^^^^^^^^

.. class:: Port(**kwargs)

        :keyword str number: Ports (``port.number``)
    


-------------


``maltego.Location``
^^^^^^^^^^^^^^^^^^^^

.. class:: Location(**kwargs)

        :keyword str streetaddress: Street Address (``streetaddress``)
        :keyword str name: Name (``location.name``)
        :keyword float longitude: Longitude (``longitude``)
        :keyword float latitude: Latitude (``latitude``)
        :keyword str countrycode: Country Code (``countrycode``)
        :keyword str country: Country (``country``)
        :keyword str city: City (``city``)
        :keyword str areacode: Area Code (``location.areacode``)
        :keyword str area: Area (``location.area``)
    


-------------


``maltego.AS`` (alias: ``ASNumber``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: AS(**kwargs)

        :keyword int number: AS Number (``as.number``)
    


-------------


``maltego.Unknown``
^^^^^^^^^^^^^^^^^^^

.. class:: Unknown(**kwargs)

    


-------------


``maltego.affiliation.WikiEdit``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: WikiEdit(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.Twit``
^^^^^^^^^^^^^^^^

.. class:: Twit(**kwargs)

        :keyword str title: Title (``title``)
        :keyword str pubdate: Date published (``pubdate``)
        :keyword str name: Twit (``twit.name``)
        :keyword str img_link: Image Link (``img_link``)
        :keyword str id: Twit ID (``id``)
        :keyword str content: Content (``content``)
        :keyword str author_uri: Author URI (``author_uri``)
        :keyword str author: Author (``author``)
    


-------------


``maltego.Vulnerability`` (alias: ``Vuln``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Vulnerability(**kwargs)

        :keyword str id: ID (``vulnerability.id``)
    


-------------


``maltego.affiliation.Twitter`` (alias: ``AffiliationTwitter``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Twitter(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str screenname: Screen Name (``twitter.screen-name``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword int number: Twitter Number (``twitter.number``)
        :keyword str network: Network (``affiliation.network``)
        :keyword str fullname: Real Name (``person.fullname``)
        :keyword int friendcount: Friend Count (``twitter.friendcount``)
    


-------------


``maltego.affiliation.Orkut`` (alias: ``AffiliationOrkut``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Orkut(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.affiliation.Linkedin`` (alias: ``AffiliationLinkedin``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Linkedin(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.Webdir``
^^^^^^^^^^^^^^^^^^

.. class:: Webdir(**kwargs)

        :keyword str name: Name (``directory.name``)
    

