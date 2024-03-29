from math import sqrt, ceil

#globals
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
REGION = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,:;-?! \'()$%&"'

#helpers
def has_numbers(text):
    for c in text:
        if c.isdigit():
            return True
    return False

# === SUBSTITUTION CIPHERS === 
def encode_polybius(text):
    #encodes text with polybius square using the modern latin alphabet

    if has_numbers(text):
        raise ValueError("text should not have digit characters")

    text = text.upper()
    square = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    r = ""
    for c in text:
        if c in square:
            i = square.index(c)
            r += str(i//5 + 1) + str(i % 5 + 1)
        elif c == "J":
            r += "24"
        else:
            r += c
    return r

def decode_polybius(text):
    square = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    r = ""
    n = 0
    while n < len(text):
        if text[n].isnumeric():
            i, j = text[n: n+2]
            r += square[(int(i) - 1)*5 + int(j) - 1]
            n += 2
        else:
            r += text[n]
            n += 1
    if "I" in r:
        print("\'J \'may have been overwritten by \'I\', have a closer look human!\n" + r)
    return r

def encode_caesar(key, message):
    key = key % 26
    r = ""
    for c in message:
        if c.upper() in ALPHABET:
            i = (ALPHABET.index(c.upper()) + key) % 26
            if c.isupper():
                r += ALPHABET[i]
            else:
                r += ALPHABET[i].lower()
        else:
            r += c
    return r
    
def decode_caesar(key, message):
    return encode_caesar(-key, message)


def encode_ragbaby(text, key, enc = 1):
    #Similar to ceasar.  key is added to the start of the alphabet, and all non-unique letters are removed.  if "key" is our key, then our 26 char key will be:
    #"KEYABCDFGHIJLMNOPQRSTUVWXZ"
    #each letter is then replaced with a letter in that key, offset by its position in its own word
    
    #clean key
    key = list(key)
    _list = []
    for c in key:
        if c not in _list:
            _list += c
    key = "".join(_list).upper()
    
    #set alp
    alp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alp = "".join([c for c in alp if c not in key])
    alp = key + alp
    
    r = ""
    j = 1
    for c in text:
        if c.upper() in alp:
            i = (alp.index(c.upper()) + (j * enc)) % 26
            if c.isupper():
                r += alp[i]
            else:
                r += alp[i].lower()
            j += 1
        else:
            r += c
            j = 1

    return r

def decode_ragbaby(text, key):
    return encode_ragbaby(text, key, -1)

def encode_tongues(text):
    #Ceasar ciper but vowels are replaced with vowels, consonants are replaced with consonants.  Rotation is half the length of each set, so encode function is also decode.
    VOWELS = "AIYEOU"
    CONSONANTS = "BKXZNHDCWGPVJQTSRLMF"
    r = ""
    for c in text:
        if c.upper() in VOWELS + CONSONANTS:
            if c.upper() in VOWELS:
                alp = VOWELS
            else:
                alp = CONSONANTS
            i = (alp.index(c.upper()) + len(alp)//2) % len(alp)
            if c.isupper():
                r += alp[i]
            else:
                r += alp[i].lower()
        else:
            r += c
    return r


def encrypt_index_difference(text):
    #encrypts in three steps explained in comments
    REGION = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,:;-?! \'()$%&"'
    if not text:
        return text
    
    #validate input, throw error if char not in REGION
    if any([c not in REGION for c in text]):
        raise ValueError(f'char "{c}" not in REGION')
    
    #Step 1: Swap case of every 2nd char
    text = list(text)
    for i in range(1, len(text), 2):
        c = text[i]
        if c.upper() in REGION[:26]:
            text[i] = c.swapcase()
    text = "".join(text)
    
    #step 2: replace every char with index in REGION of difference of index in REGION of self and the index in REGION of left neighbor.  Ignore first char.  
    r = text[0]
    for i in range(1, len(text)):
        c1 = text[i - 1]
        c2 = text[i]
        r += REGION[REGION.index(c1) - REGION.index(c2)]
    
    #step 3: replace first char with its mirrored index in REGION
    r = REGION[-1 * REGION.index(r[0]) - 1] + r[1:]
    
    return r

def decrypt_index_difference(text):
    if not text:
        return text
    
    #validate input, throw error if char not in REGION
    if any([c not in REGION for c in text]):
        raise ValueError(f'char "{c}" not in REGION')
    
    text = REGION[-1 * REGION.index(text[0]) - 1] + text[1:]
    
    text = list(text)
    for i in range(1, len(text)):
        c1 = text[i - 1]
        c2 = text[i]
        text[i] = REGION[REGION.index(c1) - REGION.index(c2)]
    
    for i in range(1, len(text), 2):
        c = text[i]
        if c.upper() in REGION[:26]:
            text[i] = c.swapcase()
    
    text = "".join(text)
    
    return text
    
# === TRANSPOSITION CIPHERS ===

def column_transpose(string):
    # Transposes string by the square root of its length (will rjust string so its length is a perfect square as needed)
    side_l = ceil(sqrt(len(string)))
    string = string.ljust(side_l ** 2)
    r = ''
    for i in range(side_l):
        for j in range(side_l):
            r += (string[j * side_l + i])
    return r
    
def encode_IRC(n, string):
    #Shifts all nonspace charaacters right by n
    #Then for each word (delimited by space) shift to right by n
    #repeat n times
    #add n to start of string

    space_ins = []
    i = 0
    while string.find(" ", i + 1) != -1:
        i = string.find(" ", i + 1)
        space_ins.append(i)

    for _ in range(n):
        string = string.replace(" ", "")
        string = string[-n:] + string[:-n]
        string = list(string)
        for i in space_ins:
            string.insert(i, " ")
        string = "".join(string).split(" ")
        for i, word in enumerate(string):
            if len(word) != 0:
                sn = n % len(word)
                string[i] = word[-sn:] + word[:-sn]
        string = " ".join(string)

    return str(n) + " " + string


def decode_IRC(string):
    n = int(string[:string.index(" ")])
    string = string[string.index(" ") + 1:]

    i = 0
    space_ins = []
    while string.find(" ", i + 1) != -1:
        i = string.find(" ", i + 1)
        space_ins.append(i)

    for _ in range(n):
        string = string.split(" ")
        for i, word in enumerate(string):
            if len(word) != 0:
                sn = n % len(word)
                string[i] = word[sn:] + word[:sn]
        string = " ".join(string)

        string = string.replace(" ", "")
        string = string[n:] + string[:n]
        string = list(string)
        for i in space_ins:
            string.insert(i, " ")
        string = ''.join(string)

    return string

def encode_cut_deck(text):
    #returns string of every other char appended to every otherchar offset by 1
    return "".join([text[i] for i in range(0, len(text), 2)] + [text[i] for i in range(1, len(text), 2)])

def decode_cut_deck(text):
    mid = len(text)//2
    if len(text) % 2 == 1:
        mid += 1
        r = [text[:mid][i] + text[mid:][i] for i in range(mid - 1)]
        r.append(text[mid - 1])
    else:
        r = [text[:mid][i] + text[mid:][i] for i in range(mid)]
    return "".join(r)
