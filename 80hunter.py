# This program looks through files for strings of bytes that are >= 0x80h to
# spot possible charset issues.

import sys
import os

if len(sys.argv) != 2:
    sys.exit('Usage: %s "[file.ext]"' % sys.argv[0])

if not os.path.isfile(sys.argv[1]):
    sys.exit('Error: File %s not found.' % sys.argv[1])

in_utf = False
counter = 0
hex_string = ''
hex_start = 0

try:
    f = open(sys.argv[1], "rb")
    byte = f.read(1)
    while byte != "":
        char_code = ord(byte)
        if in_utf:
            if char_code >= 128:
                hex_string += " " + hex(char_code)
            else:
                in_utf = False
                print "%s : %s" % (hex_start, hex_string)
        else:
            if char_code >= 128:
                in_utf = True
                hex_start = hex(counter)
                hex_string = hex(char_code)
        counter += 1
        byte = f.read(1)
finally:
    f.close()
    if in_utf:
        print "%s : %s" % (hex_start, hex_string)
