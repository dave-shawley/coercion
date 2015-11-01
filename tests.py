import datetime
import sys
import unittest
import uuid

import coercion


class UTC(datetime.tzinfo):
    def tzname(self, dt):
        return 'UTC'

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def dst(self, dt):
        return datetime.timedelta(0)


class PrimitiveStringifyTests(unittest.TestCase):

    def test_that_bytes_is_encoded_as_utf8(self):
        self.assertEqual(coercion.stringify(b'Wei\xC3\x9Fbier'),
                         u'Wei\u00DFbier')

    def test_that_memoryview_is_treated_as_bytes(self):
        view = memoryview(b'Wei\xC3\x9Fbier')
        self.assertEqual(coercion.stringify(view), u'Wei\u00DFbier')

    def test_that_bytearray_is_treated_as_bytes(self):
        ary = bytearray(b'Wei\xC3\x9Fbier')
        self.assertEqual(coercion.stringify(ary), u'Wei\u00DFbier')

    @unittest.skipIf(sys.version_info >= (3, 0), 'buffer is Py2 only')
    def test_that_buffer_is_treated_as_bytes(self):
        buf = buffer(b'Wei\xC3\x9Fbier')
        self.assertEqual(coercion.stringify(buf), u'Wei\u00DFbier')

    def test_that_unicode_is_return_unchanged(self):
        self.assertEqual(coercion.stringify(u'Hi there'), u'Hi there')

    def test_that_uuid_is_stringified(self):
        val = uuid.uuid4()
        self.assertEqual(coercion.stringify(val),
                         coercion.stringify(str(val)))

    def test_that_tznaive_datetime_omits_timezone(self):
        now = datetime.datetime.now()
        self.assertEqual(coercion.stringify(now),
                         now.strftime('%Y-%m-%dT%H:%M:%S.%f'))

    def test_that_tzaware_datetime_includes_timezone(self):
        now = datetime.datetime.utcnow().replace(tzinfo=UTC())
        self.assertEqual(coercion.stringify(now),
                         now.strftime('%Y-%m-%dT%H:%M:%S.%f+0000'))

    def test_that_numbers_are_untouched(self):
        self.assertEqual(coercion.stringify(42), 42)
        self.assertEqual(coercion.stringify(22.0 / 7.0), 22.0 / 7.0)

    def test_that_bools_are_untouched(self):
        self.assertEqual(coercion.stringify(True), True)
        self.assertEqual(coercion.stringify(False), False)

    def test_that_none_is_untouched(self):
        self.assertEqual(coercion.stringify(None), None)

    def test_that_str_is_converted_to_unicode(self):
        self.assertEqual(coercion.stringify('one'), u'one')
