"""Parses incoming C struct payload to Python values"""
from __future__ import division

import struct
import binascii
import array


'''packet:
 Feed Name (char x 10)
 Capture Time (Unsigned long)
 Value (Int)
'''


def parseMsg(payload):
    """Parses C struct to Python list"""
    #feed_id = binascii.unhexlify(payload[:10]) #get feed id
    #values = binascii.unhexlify(payload[10:])
    feed_id = payload[:10]
    values = payload[10:]

    y2 = array.array('B', values)
    print(y2)

    #y2.byteswap()

    s2 = struct.Struct('<L h')

    capTime, value = s2.unpack_from(y2)
    return feed_id, capTime, value


def main():
    """Parses test packet"""
    pass

if __name__ == '__main__':
    main()
