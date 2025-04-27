from config import *
from words import WORDS as wordset
import binascii

class Seed:
    def __init__(self):
        self.lstseed = []
        self.hexseed = ''
        self.n = len(wordset);
    
    def from_seed(self, seed:str):
        self.lstseed = seed.split(' ')
        if len(self.lstseed) == 25:
            self.hexseed = self.mn_decode(seed)
    
    def from_hexs(self, hexs:str):
        self.hexseed = hexs
        self.lstseed = self.mn_encode(hexs).split(' ')

    def show(self):
        print()
        print('Mnemonic Seed:        '," ".join(self.lstseed))
        print('Hexadecimal Seed:     ',self.hexseed)

    def mn_decode(self,str):
        out = ''
        wlist = str.split(' ')
        for i in range(0,len(wlist)-1,3):
            w1 = wordset.index(wlist[i])
            w2 = wordset.index(wlist[i+1])
            w3 = wordset.index(wlist[i+2])
            x = w1 + self.n * (((self.n - w1) + w2) % self.n) + self.n * self.n * (((self.n - w2) + w3) % self.n)
            out += (x).to_bytes(4, byteorder='little').hex()
        return out;

    def mn_encode(self, hex):
        out = []
        for i in range(len(hex) // 8):
            word = int(hex[8 * i : 8 * i + 8],16).to_bytes(4, byteorder='little').hex()
            x = int(word, 16)
            w1 = x % self.n
            w2 = (x // self.n + w1) % self.n
            w3 = (x // self.n // self.n + w2) % self.n
            out += [wordset[w1], wordset[w2], wordset[w3]]
        checksum = self.get_checksum(" ".join(out))
        out.append(checksum)
        return " ".join(out)

    def get_checksum(self, phrase):
        """Given a mnemonic word string, return a string of the computed checksum.

        :rtype: str
        """
        unique_prefix_length = 3
        phrase_split = phrase.split(" ")
        if len(phrase_split) < 12:
            raise ValueError("Invalid mnemonic phrase")
        if len(phrase_split) > 13:
            # Standard format
            phrase = phrase_split[:24]
        else:
            # MyMonero format
            phrase = phrase_split[:12]
        wstr = "".join(word[: unique_prefix_length] for word in phrase)
        wstr = bytearray(wstr.encode("utf-8"))
        z = ((binascii.crc32(wstr) & 0xFFFFFFFF) ^ 0xFFFFFFFF) >> 0
        z2 = ((z ^ 0xFFFFFFFF) >> 0) % len(phrase)
        return phrase_split[z2]


if __name__ == '__main__':
    print(__file__)
    print('Test Mnemonic Seed:   ',test_mnemonic_seed)
    print('Test Hexadecimal Seed:',test_hexadecimal_seed)
    s = Seed()
    s.from_seed(test_mnemonic_seed)
    s.show()
    s.from_hexs(test_hexadecimal_seed)
    s.show()
