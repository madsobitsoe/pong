# Helper functions for converting between floating point and integers
import struct
import random
# http://stackoverflow.com/questions/14431170/get-the-bits-of-a-float-in-python
def floatToBits(f):
    s = struct.pack('>f', f)
    return struct.unpack('>l', s)[0]

def bitsToFloat(b):
    s = struct.pack('>l', b)
    return struct.unpack('>f', s)[0]

def mutate(neuralNet):
    # For each weight, check to see if weight should mutate, and mutate if so
    for net in neuralNet.W1:
        for weight in net:
            print 'Value as float is: ' + str(weight)
            print 'Value as int is: ' + str(floatToBits(weight))
            print 'Value as bits is: ' + bin(floatToBits(weight))
    
    print str(floatToBits(neuralNet.W1[0][0]))

    binary = bin(floatToBits(neuralNet.W1[0][0]))
    print binary
    print str(type(binary))
    index = random.randint(2,len(binary))

    print 'Index is: ' + str(index)
    
    print 'The value is: ' + str(binary[index])
    
    if binary[index] == '1':
        newBinary = binary[:index] + '0' + binary[index+1:]
    else:
        newBinary = binary[:index] + '1' + binary[index+1:]

    print 'The changed value is: ' + str(newBinary[index])
        
    print newBinary

    newFloat = bitsToFloat(int(newBinary, 2))
    print newFloat
    
    


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
