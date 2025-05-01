from ..config import *
import binascii

def mn_get_checksum_index(words, prefix_len=3):
    '''
function mn_get_checksum_index(words, prefix_len) {
    var trimmed_words = "";
    for (var i = 0; i < words.length; i++) {
        trimmed_words += words[i].slice(0, prefix_len);
    }
    var checksum = crc32.run(trimmed_words);
    var index = checksum % words.length;
    return index;
}
'''
    trimmed_words = ""
    for word in words:
        trimmed_words += word[:prefix_len]
    return binascii.crc32(str.encode(trimmed_words)) % len(words)

def words25(seed:str):
    seed_arr = seed.split(" ")
    if len(seed_arr)>25 or len(seed_arr)<24: return False
    if len(seed_arr)==24:
        seed_arr += [seed_arr[mn_get_checksum_index(seed_arr)]]
    return " ".join(seed_arr)

if __name__ == '__main__':
    print(__file__)
    print('Mnemonic Seed:',test_mnemonic_seed)
    print('25 words seed:',words25(" ".join(test_mnemonic_seed.split(" ")[:24])))
