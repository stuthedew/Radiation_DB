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
    values = payload
    arr = array.array('B', values)
    s = struct.Struct('<10s h L h') #Little endian 10 char, unsigned long, signed int16
    feed_id, dist, capTime, value = s.unpack_from(arr)
    feed_id = feed_id.rstrip(' \t\r\n\0')
    return feed_id, dist, capTime, value


def main():
    """Parses test packet"""
    pass

if __name__ == '__main__':
    main()
