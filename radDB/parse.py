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

    feed_id = payload[:10]
    values = payload[10:]

    y2 = array.array('B', values)

    s2 = struct.Struct('<L h') #Little endian unsigned long, signed int16

    capTime, value = s2.unpack_from(y2)
    return feed_id, capTime, value


def main():
    """Parses test packet"""
    pass

if __name__ == '__main__':
    main()
