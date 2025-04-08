from config import test_mnemonic_seed, test_hexadecimal_seed
from words import WORDS as wordset

def mn_decode(str):
    '''
function mn_decode(str, wordset_name) {
    'use strict';
    wordset_name = wordset_name || mn_default_wordset;
    var wordset = mn_words[wordset_name];
    var out = '';
    var n = wordset.words.length;
    var wlist = str.split(' ');
    var checksum_word = '';
    //if (wlist.length < 12) throw "You've entered too few words, please try again";
    if ((wordset.prefix_len === 0 && (wlist.length % 3 !== 0)) ||
        (wordset.prefix_len > 0 && (wlist.length % 3 === 2))) throw "You've entered too few words, please try again";
    if (wordset.prefix_len > 0 && (wlist.length % 3 === 0)) throw "You seem to be missing the last word in your private key, please try again";
    if (wordset.prefix_len > 0) {
        // Pop checksum from mnemonic
        checksum_word = wlist.pop();
    }
    // Decode mnemonic
    for (var i = 0; i < wlist.length; i += 3) {
        var w1, w2, w3;
        if (wordset.prefix_len === 0) {
            w1 = wordset.words.indexOf(wlist[i]);
            w2 = wordset.words.indexOf(wlist[i + 1]);
            w3 = wordset.words.indexOf(wlist[i + 2]);
        } else {
            w1 = wordset.trunc_words.indexOf(wlist[i].slice(0, wordset.prefix_len));
            w2 = wordset.trunc_words.indexOf(wlist[i + 1].slice(0, wordset.prefix_len));
            w3 = wordset.trunc_words.indexOf(wlist[i + 2].slice(0, wordset.prefix_len));
        }
        if (w1 === -1 || w2 === -1 || w3 === -1) {
            throw "invalid word in mnemonic";
        }
        var x = w1 + n * (((n - w1) + w2) % n) + n * n * (((n - w2) + w3) % n);
        if (x % n != w1) throw 'Something went wrong when decoding your private key, please try again';
        out += mn_swap_endian_4byte(('0000000' + x.toString(16)).slice(-8));
    }
    // Verify checksum
    if (wordset.prefix_len > 0) {
        var index = mn_get_checksum_index(wlist, wordset.prefix_len);
        var expected_checksum_word = wlist[index];
        if (expected_checksum_word.slice(0, wordset.prefix_len) !== checksum_word.slice(0, wordset.prefix_len)) {
            throw "Your private key could not be verified, please try again";
        }
    }
    return out;
}
'''
    out = ''
    n = len(wordset);
    wlist = str.split(' ')
    for i in [0,3,6,9,12,15,18,21]:
        w1 = wordset.index(wlist[i])
        w2 = wordset.index(wlist[i+1])
        w3 = wordset.index(wlist[i+2])
        x = w1 + n * (((n - w1) + w2) % n) + n * n * (((n - w2) + w3) % n)
        out += mn_swap_endian_4byte(('0000000'+hex(x)[2:])[-8:])
    return out;

def mn_swap_endian_4byte(str):
    '''
function mn_swap_endian_4byte(str) {
    'use strict';
    if (str.length !== 8) throw 'Invalid input length: ' + str.length;
    return str.slice(6, 8) + str.slice(4, 6) + str.slice(2, 4) + str.slice(0, 2);
}
'''
    return str[6:8] + str[4:6] + str[2:4] + str[0:2]

if __name__ == '__main__':
    print(__file__)
    print('Mnemonic Seed:',test_mnemonic_seed)
    print('mn_decode:',mn_decode(test_mnemonic_seed))
    print('Hexadecimal Seed:',test_hexadecimal_seed)
