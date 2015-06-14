# Helper functions for converting between floating point and integers
import struct

# http://stackoverflow.com/questions/14431170/get-the-bits-of-a-float-in-python
def floatToBits(f):
    s = struct.pack('>f', f)
    return struct.unpack('>l', s)[0]

def bitsToFloat(b):
    s = struct.pack('>l', b)
    return struct.unpack('>f', s)[0]


#def binary(num):
#   return ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', num))

# how to use this
# >>> h.bitsToFloat(int((bin(h.floatToBits(-1.111111111111))),2))
# convert the float to bits (signed int) with floatToBits
# convert the int to binary
# convert the binary to int
# convert the int to a float

# The weights will be stored as floats
# to mutate on them i will convert them to signed ints, then to binary
# then mutate them
# then convert them back to signed ints
# then to floats
