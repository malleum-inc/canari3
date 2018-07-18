:mod:`canari.maltego.entities` Maltego Entities
================================================

.. module:: canari.maltego.entities
    :synopsis: Maltego Entity Classes

.. moduleauthor:: Nadeem Douba <ndouba@redcanari.com>
.. sectionauthor:: Nadeem Douba <ndouba@redcanari.com>

.. versionadded:: 3.0

----



-------------


``maltego.TrackingCode`` (alias: ``maltego.UniqueIdentifier``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: TrackingCode(**kwargs)

        :keyword str unique_identifier: Uniqueidentifier (``properties.uniqueidentifier``)
        :keyword str identifier_type: Identifier Type (``identifierType``)
    


-------------


``maltego.NSRecord``
^^^^^^^^^^^^^^^^^^^^

.. class:: NSRecord(**kwargs)

        :keyword str fqdn: DNS Name (``fqdn``)
    


-------------


``maltego.affiliation.Bebo`` (alias: ``AffiliationBebo``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Bebo(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.NominatimLocation``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: NominatimLocation(**kwargs)

        :keyword str nominatim: Nominatim Location (``properties.nominatimlocation``)
    


-------------


``maltego.EmailAddress``
^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: EmailAddress(**kwargs)

        :keyword str email: Email Address (``email``)
    


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


``maltego.Unknown``
^^^^^^^^^^^^^^^^^^^

.. class:: Unknown(**kwargs)

    


-------------


``maltego.DNSName``
^^^^^^^^^^^^^^^^^^^

.. class:: DNSName(**kwargs)

        :keyword str fqdn: DNS Name (``fqdn``)
    


-------------


``maltego.Webdir``
^^^^^^^^^^^^^^^^^^

.. class:: Webdir(**kwargs)

        :keyword str name: Name (``directory.name``)
    


-------------


``maltego.Document``
^^^^^^^^^^^^^^^^^^^^

.. class:: Document(**kwargs)

        :keyword str url: URL (``url``)
        :keyword str title: Title (``title``)
        :keyword str metadata: Meta-Data (``document.metadata``)
    


-------------


``maltego.affiliation.Zoominfo``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Zoominfo(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.BuiltWithRelationship``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: BuiltWithRelationship(**kwargs)

        :keyword str matches: Matches (``matches``)
        :keyword str builtwith: BuiltWith Technology (``properties.builtwithrelationship``)
    


-------------


``maltego.Service``
^^^^^^^^^^^^^^^^^^^

.. class:: Service(**kwargs)

        :keyword str ports: Ports (``port.number``)
        :keyword str name: Description (``service.name``)
        :keyword str banner: Service Banner (``banner.text``)
    


-------------


``maltego.Organization``
^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Organization(**kwargs)

        :keyword str name: Name (``title``)
    


-------------


``maltego.URL``
^^^^^^^^^^^^^^^

.. class:: URL(**kwargs)

        :keyword str url: URL (``url``)
        :keyword str title: Title (``title``)
        :keyword str short_title: Short title (``short-title``)
    


-------------


``maltego.affiliation.Orkut`` (alias: ``AffiliationOrkut``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Orkut(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.Device``
^^^^^^^^^^^^^^^^^^

.. class:: Device(**kwargs)

        :keyword str device: Device (``properties.device``)
    


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


``maltego.Banner``
^^^^^^^^^^^^^^^^^^

.. class:: Banner(**kwargs)

        :keyword str text: Banner (``banner.text``)
    


-------------


``maltego.Hashtag``
^^^^^^^^^^^^^^^^^^^

.. class:: Hashtag(**kwargs)

        :keyword str hashtag: Hashtag (``twitter.hashtag``)
    


-------------


``maltego.AS`` (alias: ``ASNumber``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: AS(**kwargs)

        :keyword int number: AS Number (``as.number``)
    


-------------


``maltego.affiliation.Linkedin`` (alias: ``AffiliationLinkedin``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Linkedin(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.File``
^^^^^^^^^^^^^^^^

.. class:: File(**kwargs)

        :keyword str source: Source (``source``)
        :keyword str description: Description (``description``)
    


-------------


``maltego.CircularArea``
^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: CircularArea(**kwargs)

        :keyword int radius: Radius (m) (``radius``)
        :keyword float longitude: Longitude (``longitude``)
        :keyword float latitude: Latitude (``latitude``)
        :keyword str area_circular: Circular Area (``area.circular``)
    


-------------


``maltego.IPv4Address`` (alias: ``IPAddress``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: IPv4Address(**kwargs)

        :keyword str ipv4address: IP Address (``ipv4-address``)
        :keyword bool internal: Internal (``ipaddress.internal``)
    


-------------


``maltego.affiliation.Facebook`` (alias: ``AffiliationFacebook``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Facebook(**kwargs)

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


``maltego.Tweet``
^^^^^^^^^^^^^^^^^

.. class:: Tweet(**kwargs)

        :keyword str tweet_id: Tweet ID (``id``)
        :keyword str tweet: Tweet (``twit.name``)
        :keyword str title: Title (``title``)
        :keyword str image_link: Image Link (``imglink``)
        :keyword str date_published: Date published (``pubdate``)
        :keyword str content: Content (``content``)
        :keyword str author_uri: Author URI (``author_uri``)
        :keyword str author: Author (``author``)
    


-------------


``maltego.affiliation.Flickr`` (alias: ``AffiliationFlickr``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Flickr(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.FacebookObject``
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: FacebookObject(**kwargs)

        :keyword str object: Facebook Object (``properties.facebookobject``)
    


-------------


``maltego.WebTitle``
^^^^^^^^^^^^^^^^^^^^

.. class:: WebTitle(**kwargs)

        :keyword str title: Title (``title``)
    


-------------


``maltego.GPS``
^^^^^^^^^^^^^^^

.. class:: GPS(**kwargs)

        :keyword float longitude: Longitude (``longitude``)
        :keyword float latitude: Latitude (``latitude``)
        :keyword str gps: GPS Co-ordinate (``properties.gps``)
    


-------------


``maltego.MXRecord``
^^^^^^^^^^^^^^^^^^^^

.. class:: MXRecord(**kwargs)

        :keyword int priority: Priority (``mxrecord.priority``)
        :keyword str fqdn: DNS Name (``fqdn``)
    


-------------


``maltego.affiliation.Affiliation``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Affiliation(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.Person``
^^^^^^^^^^^^^^^^^^

.. class:: Person(**kwargs)

        :keyword str lastname: Surname (``person.lastname``)
        :keyword str fullname: Full Name (``person.fullname``)
        :keyword str firstnames: First Names (``person.firstnames``)
    


-------------


``maltego.affiliation.WikiEdit``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: WikiEdit(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.Domain``
^^^^^^^^^^^^^^^^^^

.. class:: Domain(**kwargs)

        :keyword str whois_info: WHOIS Info (``whois-info``)
        :keyword str fqdn: Domain Name (``fqdn``)
    


-------------


``maltego.Vulnerability`` (alias: ``Vuln``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Vulnerability(**kwargs)

        :keyword str id: ID (``vulnerability.id``)
    


-------------


``maltego.Alias``
^^^^^^^^^^^^^^^^^

.. class:: Alias(**kwargs)

        :keyword str alias: Alias (``properties.alias``)
    


-------------


``maltego.Sentiment``
^^^^^^^^^^^^^^^^^^^^^

.. class:: Sentiment(**kwargs)

        :keyword str sentiment: Sentiment (``properties.sentiment``)
    


-------------


``maltego.Phrase``
^^^^^^^^^^^^^^^^^^

.. class:: Phrase(**kwargs)

        :keyword str text: Text (``text``)
    


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


``maltego.BuiltWithTechnology``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: BuiltWithTechnology(**kwargs)

        :keyword str builtwith: BuiltWith Technology (``properties.builtwithtechnology``)
    


-------------


``maltego.Port``
^^^^^^^^^^^^^^^^

.. class:: Port(**kwargs)

        :keyword str number: Ports (``port.number``)
    


-------------


``maltego.TwitterUserList``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: TwitterUserList(**kwargs)

        :keyword str uri: URI (``twitter.list.uri``)
        :keyword str subscriber_count: Subscriber Count (``twitter.list.subscribers``)
        :keyword str slug: Slug (``twitter.list.slug``)
        :keyword str name: Name (``twitter.list.name``)
        :keyword str member_count: Member Count (``twitter.list.members``)
        :keyword str id_: ID (``twitter.list.id``)
        :keyword str full_name: Full Name (``twitter.list.fullname``)
        :keyword str description: Description (``twitter.list.description``)
    


-------------


``maltego.Company``
^^^^^^^^^^^^^^^^^^^

.. class:: Company(**kwargs)

        :keyword str name: Name (``title``)
    


-------------


``maltego.Website``
^^^^^^^^^^^^^^^^^^^

.. class:: Website(**kwargs)

        :keyword bool ssl_enabled: SSL Enabled (``website.ssl-enabled``)
        :keyword int ports: Ports (``ports``)
        :keyword str fqdn: Website (``fqdn``)
    


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


``maltego.affiliation.MySpace`` (alias: ``AffiliationMySpace``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: MySpace(**kwargs)

        :keyword str uid: UID (``affiliation.uid``)
        :keyword str profile_url: Profile URL (``affiliation.profile-url``)
        :keyword str person_name: Name (``person.name``)
        :keyword str network: Network (``affiliation.network``)
    


-------------


``maltego.Image``
^^^^^^^^^^^^^^^^^

.. class:: Image(**kwargs)

        :keyword str url: URL (``fullImage``)
        :keyword str description: Description (``properties.image``)
    


-------------


``maltego.Hash``
^^^^^^^^^^^^^^^^

.. class:: Hash(**kwargs)

        :keyword str owner: Owner (``owner``)
        :keyword str included_media_types: Included Media Types (``includeMediaType``)
        :keyword str hash: Hash (``properties.hash``)
        :keyword str excluded_media_types: Excluded Media Types (``excludeMediaType``)
        :keyword date before: Before (``before``)
        :keyword date after: After (``after``)
    


-------------


``maltego.Netblock``
^^^^^^^^^^^^^^^^^^^^

.. class:: Netblock(**kwargs)

        :keyword str ipv4range: IP Range (``ipv4-range``)
    

