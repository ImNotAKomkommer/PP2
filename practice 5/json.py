#json module
import json

json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
'["foo", {"bar": ["baz", null, 1.0, 2]}]'

print(json.dumps("\"foo\bar"))
"\"foo\bar"

print(json.dumps('\u1234'))
"\u1234"

print(json.dumps('\\'))
"\\"

print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))
{"a": 0, "b": 0, "c": 0}

from io import StringIO

io = StringIO()

json.dump(['streaming API'], io)

io.getvalue()
'["streaming API"]'
#
import json

json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))
'[1,2,3,{"4":5,"6":7}]'
#
import json

print(json.dumps({'6': 7, '4': 5}, sort_keys=True, indent=4))
{
    "4": 5,
    "6": 7
}
#
import json

def custom_json(obj):

    if isinstance(obj, complex):

        return {'__complex__': True, 'real': obj.real, 'imag': obj.imag}

    raise TypeError(f'Cannot serialize object of {type(obj)}')


json.dumps(1 + 2j, default=custom_json)
'{"__complex__": true, "real": 1.0, "imag": 2.0}'
#
import json

json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
['foo', {'bar': ['baz', None, 1.0, 2]}]

json.loads('"\\"foo\\bar"')
'"foo\x08ar'

from io import StringIO

io = StringIO('["streaming API"]')

json.load(io)
['streaming API']