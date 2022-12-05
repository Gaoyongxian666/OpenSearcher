import re

from . import reference
from .lib import exiv2api


class Image:
    """
    Open an image based on the file path. Read and write the metadata of the image.
    Please call the public methods of this class.
    """

    def __init__(self, filename, encoding='utf-8'):
        """ Open an image and load its metadata. """
        self.img = exiv2api.Image(filename.encode(encoding))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """ Free the memory for storing image data. """
        self.img.close_image()

        # Disable all methods and properties
        def closed_warning(*args, **kwargs):
            raise RuntimeError('The image has been closed, so it is not allowed to operate.')
        for attr in dir(self):
            if not attr.startswith('__'):
                if callable(getattr(self, attr)):
                    setattr(self, attr, closed_warning)
                else:
                    setattr(self, attr, None)

    def get_mime_type(self) -> str:
        """ Get the MIME type of the image, such as 'image/jpeg'. """
        return self.img.get_mime_type()

    def get_access_mode(self) -> dict:
        """ Get the access mode to various metadata. """
        access_modes = {0: None,
                        1: 'read',
                        2: 'write',
                        3: 'read+write'}
        dic = self.img.get_access_mode()
        dic = {k:access_modes.get(v) for k,v in dic.items()}
        return dic

    def read_exif(self, encoding='utf-8') -> dict:
        data = self._parse(self.img.read_exif(), encoding)

        # Decode some tags
        for tag in reference.EXIF_TAGS_ENCODED_IN_UCS2:
            value = data.get(tag)
            if value:
                data[tag] = self._decode_ucs2(value)

        return data

    def read_iptc(self, encoding='utf-8') -> dict:
        data = self._parse(self.img.read_iptc(), encoding)

        # For repeatable tags, even if they do not have multiple values, their values are converted to list type.
        for tag in reference.IPTC_TAGS_REPEATABLE:
            value = data.get(tag)
            if isinstance(value, str):
                data[tag] = [value]

        return data

    def read_xmp(self, encoding='utf-8') -> dict:
        return self._parse(self.img.read_xmp(), encoding)

    def read_raw_xmp(self, encoding='utf-8') -> str:
        return self.img.read_raw_xmp().decode(encoding)

    def read_comment(self, encoding='utf-8') -> str:
        return self.img.read_comment().decode(encoding)

    def read_icc(self) -> bytes:
        return self.img.read_icc()

    def read_thumbnail(self) -> bytes:
        return self.img.read_thumbnail()

    def modify_exif(self, data: dict, encoding='utf-8'):
        # Encode some tags
        for tag in reference.EXIF_TAGS_ENCODED_IN_UCS2:
            value = data.get(tag)
            if value:
                data[tag] = self._encode_ucs2(value)

        self.img.modify_exif(self._dumps(data), encoding)

    def modify_iptc(self, data: dict, encoding='utf-8'):
        self.img.modify_iptc(self._dumps(data), encoding)

    def modify_xmp(self, data: dict, encoding='utf-8'):
        self.img.modify_xmp(self._dumps(data), encoding)

    def modify_raw_xmp(self, data: str, encoding='utf-8'):
        self.img.modify_raw_xmp(data, encoding)

    def modify_comment(self, data: str, encoding='utf-8'):
        self.img.modify_comment(data, encoding)

    def modify_icc(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError('The ICC profile should be of bytes type.')
        return self.img.modify_icc(data, len(data))

    def modify_thumbnail(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError('The thumbnail should be of bytes type.')
        return self.img.modify_thumbnail(data, len(data))

    def _parse(self, table: list, encoding='utf-8') -> dict:
        """ Parse the metadata from a text table into a dict. """
        data = {}
        for line in table:
            tag, value, typeName = [field.decode(encoding) for field in line]
            if typeName in ['XmpBag', 'XmpSeq']:
                value = value.split(', ')
            elif typeName in ['LangAlt']:
                if 'lang=' in value:
                    fields = re.split(r', (lang="\S+") ', ', ' + value)[1:]
                    value  = {language: content for language, content in zip(fields[0::2], fields[1::2])}

            # Convert the values to a list of strings if the tag has multiple values
            pre_value = data.get(tag)
            if pre_value == None:
                data[tag] = value
            elif isinstance(pre_value, str):
                data[tag] = [pre_value, value]
            elif isinstance(pre_value, list):
                data[tag].append(value)

        return data

    def _dumps(self, data: dict) -> list:
        """ Convert the metadata from a dict into a text table. """
        table = []
        for tag, value in data.items():
            tag      = str(tag)
            if value == None:
                typeName = '_delete'
                value    = ''
            elif isinstance(value, (list, tuple)):
                typeName = 'array'
                value    = list(value)
            elif isinstance(value, dict):
                typeName = 'string'
                value    = ', '.join(['{} {}'.format(k,v) for k,v in value.items()])
            else:
                typeName = 'string'
                value    = str(value)
            line = [tag, value, typeName]
            table.append(line)
        return table

    def _decode_ucs2(self, text):
        """
        Convert text from UCS2 encoding to UTF8 encoding.
        For example:
        >>> img._decode_ucs2('116 0 101 0 115 0 116 0')
        'test'
        """
        hex_str = ''.join(['{:02x}'.format(int(i)) for i in text.split()])
        return bytes.fromhex(hex_str).decode('utf-16le')

    def _encode_ucs2(self, text):
        """
        Convert text from UTF8 encoding to UCS2 encoding.
        For example:
        >>> img._encode_ucs2('test')
        '116 0 101 0 115 0 116 0'
        """
        hex_str = text.encode('utf-16le').hex()
        int_list = [int(''.join(i), base=16) for i in zip(*[iter(hex_str)] * 2)]
        return ' '.join([str(i) for i in int_list])

    def clear_exif(self):
        self.img.clear_exif()

    def clear_iptc(self):
        self.img.clear_iptc()

    def clear_xmp(self):
        self.img.clear_xmp()

    def clear_comment(self):
        self.img.clear_comment()

    def clear_icc(self):
        self.img.clear_icc()

    def clear_thumbnail(self):
        self.img.clear_thumbnail()


class ImageData(Image):
    """
    Similar to class `Image`, but opens the image from bytes data.
    """
    def __init__(self, data: bytes):
        """ Open an image and load its metadata. """
        length = len(data)
        if length >= 2**31:
            raise ValueError('Only images smaller than 2GB can be opened. The size of your image is {} bytes.'.format(length))
        self.buffer = exiv2api.Buffer(data, length)
        self.img = exiv2api.Image(self.buffer)

    def get_bytes(self) -> bytes:
        """ Get the bytes data of the image. """
        return self.img.get_bytes()

    def close(self):
        """ Free the memory for storing image data. """
        self.buffer.destroy()
        super().close()


def registerNs(namespace: str, prefix: str):
    """ Register a XMP namespace with prefix. Sample:
    >>> pyexiv2.registerNs('a namespace for test', 'Ns1')
    >>> img.modify_xmp({'Xmp.Ns1.mytag1': 'Hello'})
    """
    return exiv2api.registerNs(namespace, prefix)

def enableBMFF(enable=True):
    """ Enable or disable reading BMFF images. Return True on success. """
    return exiv2api.enableBMFF(enable)

def set_log_level(level=2):
    """
    Set the level of handling logs. There are five levels of handling logs:
        0 : debug
        1 : info
        2 : warn
        3 : error
        4 : mute
    """
    if level in [0, 1, 2, 3, 4]:
        exiv2api.set_log_level(level)
    else:
        raise ValueError('Invalid log level.')


exiv2api.init()
set_log_level(2)
