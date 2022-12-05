# These tags are used by Windows and encoded in UCS2.
# pyexiv2 will automatically convert encoding formats when reading and writing them.
EXIF_TAGS_ENCODED_IN_UCS2 = [
    'Exif.Image.XPTitle',
    'Exif.Image.XPComment',
    'Exif.Image.XPAuthor',
    'Exif.Image.XPKeywords',
    'Exif.Image.XPSubject',
]

# These tags can be written repeatedly, so there may be multiple values.
# pyexiv2 will convert their values to a list of strings.
IPTC_TAGS_REPEATABLE = [
    'Iptc.Envelope.Destination',
    'Iptc.Envelope.ProductId',
    'Iptc.Application2.ObjectAttribute',
    'Iptc.Application2.Subject',
    'Iptc.Application2.SuppCategory',
    'Iptc.Application2.Keywords',
    'Iptc.Application2.LocationCode',
    'Iptc.Application2.LocationName',
    'Iptc.Application2.ReferenceService',
    'Iptc.Application2.ReferenceDate',
    'Iptc.Application2.ReferenceNumber',
    'Iptc.Application2.Byline',
    'Iptc.Application2.BylineTitle',
    'Iptc.Application2.Contact',
    'Iptc.Application2.Writer',
]
