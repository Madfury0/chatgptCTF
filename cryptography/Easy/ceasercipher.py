import sys

text = sys.argv[1]

def rot(text,s):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if (char.isupper()):
         result += chr((ord(char) + s-65) % 26 + 65)
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
    return result


print ("Plain Text : " + text)
print (" ")
for n in range(27):
    print ("Shift pattern : " + str(n))
    print ("Cipher: " + rot(text,n))
    print (" ")
