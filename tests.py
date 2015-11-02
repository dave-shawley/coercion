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


class NormalizeCollectionTests(unittest.TestCase):

    def test_that_list_elements_are_transformed(self):
        now = datetime.datetime.utcnow()
        guid = uuid.uuid4()

        result = coercion.normalize_collection([
            b'\xce\xb1\xce\xb2\xce\xbe\xce\xb4\xce\xb5\xcf\x86\xce\xb3'
            b'\xce\xb7\xce\xb9\xcf\x82\xce\xba\xce\xbb\xce\xbc\xce\xbd'
            b'\xce\xbf\xcf\x80\xce\xb8\xcf\x81\xcf\x83\xcf\x84\xcf\x85'
            b'\xcf\x89\xcf\x87\xcf\x88\xce\xb6',

            u'\u043d\u0435\u043a\u043e\u0442\u043e\u0440\u044b\u0439 '
            u'\u0442\u0435\u043a\u0441\u0442 \u042e\u043d\u0438\u043a'
            u'\u043e\u0434',

            'simple native text string', 1, 2.0, True, False, None,
            now, guid])

        self.assertEqual(
            result[0],
            u'\u03b1\u03b2\u03be\u03b4\u03b5\u03c6\u03b3\u03b7\u03b9'
            u'\u03c2\u03ba\u03bb\u03bc\u03bd\u03bf\u03c0\u03b8\u03c1'
            u'\u03c3\u03c4\u03c5\u03c9\u03c7\u03c8\u03b6')

        self.assertEqual(
            result[1],
            u'\u043d\u0435\u043a\u043e\u0442\u043e\u0440\u044b\u0439 '
            u'\u0442\u0435\u043a\u0441\u0442 \u042e\u043d\u0438\u043a'
            u'\u043e\u0434')

        self.assertEqual(result[2], 'simple native text string')
        self.assertEqual(result[3], 1)
        self.assertEqual(result[4], 2.0)
        self.assertEqual(result[5], True)
        self.assertEqual(result[6], False)
        self.assertEqual(result[7], None)
        self.assertEqual(result[8], now.strftime('%Y-%m-%dT%H:%M:%S.%f'))
        self.assertEqual(result[9], str(guid))

    def test_that_nested_sequences_are_transformed(self):
        result = coercion.normalize_collection(
            [b'one', 2, [u'three', b'four', 5.0]])
        self.assertEqual(result, [u'one', 2, [u'three', u'four', 5.0]])

    def test_that_flat_dictionarys_are_transformed(self):
        result = coercion.normalize_collection({b'one': 1, 2: 'two',
                                                3: u'three'})
        self.assertEqual(result, {u'one': 1, 2: u'two', 3: u'three'})

    def test_that_tuple_are_converted_to_lists(self):
        result = coercion.normalize_collection([b'bytes', ('tuple', ['list'])])
        self.assertEqual(result, [u'bytes', [u'tuple', [u'list']]])

    def test_that_non_collection_root_raises_runtime_error(self):
        with self.assertRaises(RuntimeError):
            coercion.normalize_collection('a string')
