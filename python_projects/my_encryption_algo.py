import string

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', ' ']
size = len(chars)

def cycle(offset, x):
    shift = (chars.index(x) + offset) % size
    return chars[shift]


def encrypt(str, key):
    dir_rep = int(key[0])
    multiplier = int(key[1])
    mult_grth = int(key[2])
    gap = int(key[3])
    gap_grth = int(key[4])

    res = ""
    direction = 1

    for i in range(len(str)):
        res += cycle(multiplier*direction,str[i])
        if (i+1) % dir_rep == 0:
            direction *= -1
        if (i+1) % gap == 0:
            gap += gap_grth
            multiplier += mult_grth
    return res

def decrypt(str, key):
    dir_rep = int(key[0])
    multiplier = int(key[1])
    mult_grth = int(key[2])
    gap = int(key[3])
    gap_grth = int(key[4])

    res = ""
    direction = -1

    for i in range(len(str)):
        res += cycle(multiplier*direction,str[i])
        if (i+1) % dir_rep == 0:
            direction *= -1
        if (i+1) % gap == 0:
            gap += gap_grth
            multiplier += mult_grth
    return res

test = "hello this is a secret msg , you should leave right now!"
key = "12222"
print(encrypt(test,key))
print(decrypt("jcphu_B sil|G<q:K=w}A}x?S,BTD`U?H;R*6%R013S)YU$14Y*O&1<g",key)) #same chars never repeat. for eg) 'eee' gets transformed into 'f4:'
