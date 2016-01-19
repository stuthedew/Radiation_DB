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


def parseMsg(hexStr):
    """Parses C struct to Python list"""
    feed_id = binascii.unhexlify(hexStr[:20]) #get feed id
    values = binascii.unhexlify(hexStr[20:])
    y1 = array.array('h', feed_id)
    y2 = array.array('h', values)
    y2.byteswap()
    s1 = struct.Struct('>10s')
    s2 = struct.Struct('>LI')
    str1 = s1.unpack_from(y1)
    feed_id = str1[0]
    capTime, value = s2.unpack_from(y2)
    return feed_id, capTime, value


def main():
    """Parses test packet"""
    pass

if __name__ == '__main__':
    main()
